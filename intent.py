import re

COMMAND_PATTERNS = {

    

    "open_app": [
        r"open (.+)",
        r"launch (.+)",
        r"start (.+)"
    ],

    "close_app": [
        r"close (.+)",
        r"quit (.+)",
        r"exit (.+)"
    ],

    

    "volume_up": [
        r"volume up",
        r"increase volume",
        r"turn up volume"
    ],

    "volume_down": [
        r"volume down",
        r"decrease volume",
        r"turn down volume"
    ],

    "mute": [
        r"mute",
        r"mute volume"
    ],

    "unmute": [
        r"unmute",
        r"unmute volume"
    ],

    "lock_system": [
        r"lock system",
        r"lock screen"
    ],

    "sleep_system": [
        r"sleep system",
        r"put system to sleep"
    ],

    "restart_system": [
        r"restart system",
        r"restart computer"
    ],

    "shutdown_system": [
        r"shutdown system",
        r"shut down system",
        r"power off"
    ],


    "confirm_yes": [
        r"^yes$",
        r"^confirm$",
        r"^okay$"
    ],

    "confirm_no": [
        r"^no$",
        r"^cancel$",
        r"^stop$"
    ],

    

    "remember": [
        r"remember (.+)"
    ],

    "recall": [
        r"what is my (.+)",
        r"do you remember my (.+)"
    ],

    "list_notes": [
        r"what did i ask you to remember",
        r"list my notes"
    ]
}


def detect_intent(text: str) -> dict:
    """
    Detects whether user input is a command or normal conversation.

    Returns:
    - { type: "command", intent: "...", target: "..." }
    - { type: "conversation" }
    """
    text = text.lower().strip()

    for intent, patterns in COMMAND_PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                target = match.group(1) if match.groups() else None
                return {
                    "type": "command",
                    "intent": intent,
                    "target": target
                }

    return {
        "type": "conversation"
    }

