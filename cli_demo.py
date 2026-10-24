"""
cli_demo.py
===========
A minimal terminal-based AI demo.
Perfect for seeing how AI interactions work in raw Python!

Run this script:
    python cli_demo.py
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import ai_engine

def main():
    print("==================================================")
    print("Welcome to the Minimal Python AI Terminal Demo!")
    print("==================================================")
    print("Type your message below (or type 'exit' to quit).\n")

    history = []
    persona = "You are an encouraging and knowledgeable AI mentor."

    while True:
        try:
            user_text = input("\nYou: ").strip()
            if not user_text:
                continue
            if user_text.lower() in ["exit", "quit", "q"]:
                print("Goodbye! Happy coding!")
                break

            # Append user message
            history.append({"role": "user", "content": user_text})

            print("\nAI: ", end="", flush=True)
            # Call our engine
            reply = ai_engine.chat_with_ai(
                history=history,
                system_instruction=persona,
                api_key=None  # Leave None for automatic demo mode or pass your key
            )
            print(reply)

            # Append model reply to history
            history.append({"role": "assistant", "content": reply})

        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
