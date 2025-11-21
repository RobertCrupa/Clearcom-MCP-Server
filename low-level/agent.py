import os

from google import genai
from google.genai import types as genai_types
from .client import MCPClient
from dotenv import load_dotenv

load_dotenv()

LLM_API_KEY = os.environ["GOOGLE_API_KEY"]
client = genai.Client(api_key=LLM_API_KEY)


mcp_client = MCPClient(
    name="clearcom",
    command="uvx",
    server_args=[
        "fastmcp",
        "run",
        "src/main.py:mcp",
    ],
)


def resolve_schema_refs(schema: dict) -> dict:
    """Resolve $ref references in a JSON schema and remove unsupported properties."""
    if not isinstance(schema, dict):
        return schema
    
    # Make a copy to avoid modifying original
    resolved_schema = {}
    
    # Extract $defs if present
    defs = schema.get('$defs', {})
    
    # Copy properties, excluding $defs and resolving $refs
    for key, value in schema.items():
        if key == '$defs':
            continue  # Skip $defs as Google GenAI doesn't support it
        elif isinstance(value, dict):
            if '$ref' in value:
                # Resolve reference
                ref_path = value['$ref']
                if ref_path.startswith('#/$defs/'):
                    ref_key = ref_path.replace('#/$defs/', '')
                    if ref_key in defs:
                        resolved_value = resolve_schema_refs(defs[ref_key])
                        # If the resolved value is just a type definition, use it directly
                        resolved_schema[key] = resolved_value
                    else:
                        # If we can't resolve the reference, use a string type as fallback
                        resolved_schema[key] = {"type": "string"}
                else:
                    resolved_schema[key] = value
            else:
                # Recursively resolve nested objects
                resolved_schema[key] = resolve_schema_refs(value)
        elif isinstance(value, list):
            # Recursively resolve items in lists
            resolved_schema[key] = [resolve_schema_refs(item) if isinstance(item, dict) else item for item in value]
        else:
            resolved_schema[key] = value
    
    return resolved_schema


def convert_mcp_tools_to_gemini(mcp_tools):
    """Convert MCP tool format to Gemini function calling format."""
    gemini_tools = []
    
    for tool in mcp_tools:
        # Clean up the input schema by resolving refs and removing unsupported properties
        cleaned_schema = resolve_schema_refs(tool["input_schema"])
        
        # Create a FunctionDeclaration for each MCP tool
        function_declaration = genai_types.FunctionDeclaration(
            name=tool["name"],
            description=tool["description"],
            parameters_json_schema=cleaned_schema
        )
        
        # Create a Tool with the function declaration
        gemini_tool = genai_types.Tool(function_declarations=[function_declaration])
        gemini_tools.append(gemini_tool)
    
    return gemini_tools


async def agent_chat(conversation: list[str]) -> list[str]:
    response = []

    try:
        await mcp_client.connect()
        mcp_tools = await mcp_client.get_available_tools()
        available_tools = convert_mcp_tools_to_gemini(mcp_tools)
        print(
            f"Available tools: {", ".join([tool['name'] for tool in mcp_tools])}"
        )

        # Tool use loop - continue until we get a final text response
        while True:
            # Get LLM response
            current_response = await client.aio.models.generate_content(
                contents=conversation,
                model="gemini-2.5-pro",
                config=genai_types.GenerateContentConfig(
                    temperature=0,
                    tools=available_tools,
                    automatic_function_calling=genai_types.AutomaticFunctionCallingConfig(
                        disable=True
                    )
                )
            )

            # Check if we need to use tools by looking at function_calls
            if current_response.function_calls:
                # Add the model's function call response to history
                response.append(current_response.text or "[Function calls made]")
                
                # Execute all tools and collect results
                for function_call in current_response.function_calls:
                    if function_call.name:
                        print(f"Using tool: {function_call.name}")
                        tool_result = await mcp_client.use_tool(
                            tool_name=function_call.name, 
                            arguments=dict(function_call.args) if function_call.args else {}
                        )
                        
                        # Create function response and add to history
                        function_response = genai_types.Part.from_function_response(
                            name=function_call.name,
                            response={"result": "\n".join(tool_result)}
                        )
                        response.append(function_response)

                continue

            else:
                # No tools needed, extract final text response
                if current_response.text:
                    print(f"Assistant: {current_response.text}")
                    # Add assistant response to history for next turn
                    response.append(current_response.text)
                else:
                    print("Assistant: [No text response available]")
                    response.append("[No response]")

                break
    finally:
        await mcp_client.disconnect()

    return response
