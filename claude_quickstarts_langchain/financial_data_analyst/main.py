import os
import sys
import base64
import json
# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_core.messages import HumanMessage
from graph import app

def main():
    print("Financial Data Analyst (Type 'quit' to exit)")
    print("--------------------------------------------")

    chat_history = []

    while True:
        try:
            user_input = input("\nUser (enter text or file path): ")
        except EOFError:
            break

        if user_input.lower() in ["quit", "exit"]:
            break

        content = []

        # Check if input is a file path
        if os.path.isfile(user_input):
            try:
                # If image
                if user_input.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    with open(user_input, "rb") as f:
                        file_data = f.read()
                    b64_data = base64.b64encode(file_data).decode('utf-8')
                    media_type = "image/jpeg"
                    if user_input.lower().endswith('.png'): media_type = "image/png"
                    if user_input.lower().endswith('.webp'): media_type = "image/webp"

                    content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": b64_data
                        }
                    })
                    print(f"[Attached image: {user_input}]")
                    text_input = input("  Question about this file: ")
                    content.append({"type": "text", "text": text_input})
                else:
                    # Treat as text
                    with open(user_input, "r", encoding="utf-8") as f:
                        text_content = f.read()
                    content.append({"type": "text", "text": f"File content of {user_input}:\n{text_content}"})
                    print(f"[Attached file: {user_input}]")
                    text_input = input("  Question about this file: ")
                    content.append({"type": "text", "text": text_input})
            except Exception as e:
                print(f"Error reading file: {e}")
                continue
        else:
            content = user_input

        chat_history.append(HumanMessage(content=content))

        inputs = {"messages": chat_history}

        print("\nAnalyst is thinking...")
        try:
            result = app.invoke(inputs)

            # Extract new messages to print info
            new_messages = result["messages"][len(chat_history):]
            chat_history = result["messages"] # Update history

            for msg in new_messages:
                if msg.type == "ai":
                    if msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            if tool_call["name"] == "generate_graph_data":
                                print(f"\n[Generated Chart Data]:")
                                print(json.dumps(tool_call["args"], indent=2))
                    if msg.content:
                        print(f"\nAgent: {msg.content}")
                elif msg.type == "tool":
                    print(f"[Tool Output]: (hidden)")

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
