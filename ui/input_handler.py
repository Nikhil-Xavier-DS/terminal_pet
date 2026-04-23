import threading
from engine.commands import handle_command

class InputHandler:
    def __init__(self, state):
        self.state = state
        self.last_user_action = None
        self.running = True

    def start(self):
        thread = threading.Thread(target=self.listen, daemon=True)
        thread.start()

    def listen(self):
        while self.running:
            cmd = input("> ").strip().lower()

            self.state, message = handle_command(cmd, self.state)

            if message:
                print(f"\n🧑 You: {message}")

                # store simple action type for memory
                self.last_user_action = cmd

    def get_last_action(self):
        action = self.last_user_action
        self.last_user_action = None
        return action