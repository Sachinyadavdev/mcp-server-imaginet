import asyncio
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_llama_mcp_client():
    # This specifies how to launch your existing MCP server within your local folder
    server_params = StdioServerParameters(
        command="python",
        # Use python to run your local mcp_server package
        args=["-m", "mcp_server.server"] 
    )
    
    print(f"Connecting to MCP server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection with the MCP server
            await session.initialize()
            print("Connected to MCP Server!")
            
            # Retrieve available tools from your MCP server
            tools_list = await session.list_tools()
            
            # Format the MCP tool schemas into the format Ollama expects
            ollama_tools = []
            for tool in tools_list.tools:
                ollama_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.inputSchema
                    }
                })

            print(f"Loaded {len(ollama_tools)} tools from your MCP server.")
            print("Start chatting with LLaMA 3.2! (type 'quit' to exit)\n")

            messages = []
            
            # Continuous Loop!
            while True:
                user_query = input("\nYou: ")
                if user_query.lower() in ['quit', 'exit']:
                    print("Closing proxy...")
                    break
                    
                messages.append({'role': 'user', 'content': user_query})
                
                # Call Ollama using the local llama3.2 API
                response = ollama.chat(
                    model='llama3.2',
                    messages=messages,
                    tools=ollama_tools
                )
                
                # Append the assistant's intermediate message
                messages.append(response.message)
                
                # Check if LLM decided to use a tool to get more context
                if response.message.tool_calls:
                    print("\n--- LLaMA Tool Execution Triggered ---")
                    for tool_call in response.message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = tool_call.function.arguments
                        
                        print(f"Executing Tool: {tool_name}")
                        print(f"With Arguments: {tool_args}")
                        
                        try:
                            # Send the execution request straight to your MCP server
                            result = await session.call_tool(tool_name, arguments=tool_args)
                            
                            # Extract the text content from the MCP generic response
                            result_text = "\n".join([c.text for c in result.content if c.type == 'text'])
                            print(f"Tool Result (from MCP server):\n{result_text[:500]}... [truncated]\n")
                            
                            # Provide the result back contextually to the LLM for it to give a final answer
                            messages.append({
                                'role': 'tool',
                                'name': tool_name,
                                'content': result_text
                            })
                            
                            final_response = ollama.chat(
                                model='llama3.2',
                                messages=messages
                            )
                            # Append the final response to conversation history
                            messages.append(final_response.message)
                            
                            print("LLaMA:", final_response.message.content)

                        except Exception as e:
                            print(f"\nError executing tool: {e}")
                else:
                    # Expected if LLaMA chose to skip using a tool
                    print("LLaMA:", response.message.content)

if __name__ == "__main__":
    try:
        # Start the async interactive terminal
        asyncio.run(run_llama_mcp_client())
    except KeyboardInterrupt:
        print("\nExiting...")
