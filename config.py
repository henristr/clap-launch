"""
Configuration file for clap detector
Modify the settings below to customize behavior
"""

# ============ ACTION SETTINGS ============
# List of commands to run when clap is detected
# Each command can be:
#   - A shell command: 'notepad', 'calc', 'start https://google.com'
#   - Python script: 'python script.py'
#   - Home Assistant: 'home-assistant' (requires HA settings below)
#
# Multiple commands run in order with delay between them
COMMANDS = [
    # "home-assistant",  # First: toggle Home Assistant switch
    # "start /max https://"
]

# Delay between commands (in seconds)
COMMAND_DELAY = 0.5

# ============ HOME ASSISTANT SETTINGS ============
# (Used when 'home-assistant' is in COMMANDS list)

# List of Home Assistant actions (one per command if multiple)
# If only one action, it applies to all 'home-assistant' commands
HA_ACTIONS = [
    {
        "enabled": True,
        "url": "",
        "token": "",
        "action": "toggle_light",  # 'toggle_switch', 'toggle_light', 'activate_scene', 'call_service'
        "entity_id": "light.licht",
        "service": "light.toggle",  # For 'call_service' action
    },
    # Add more Home Assistant actions here for multiple HA commands
    # {
    #     'enabled': False,
    #     'url': 'http://homeassistant.local:8123',
    #     'token': 'your_token',
    #     'action': 'toggle_light',
    #     'entity_id': 'light.bedroom',
    # }
]

# ============ DETECTION SETTINGS ============
# Number of claps needed to trigger action (1, 2, or 3)
CLAPS_TO_TRIGGER = 2

# Sensitivity: How loud a sound needs to be to register (0.01 to 1.0)
# Lower = more sensitive (detects quieter claps)
# Higher = less sensitive (requires louder claps)
CLAP_THRESHOLD = 0.008

# Time window in seconds to detect multiple claps
# If you want double-clap, this is how long to listen for the second clap
CLAP_TIME_WINDOW = 1

# Audio settings
SAMPLE_RATE = 44100  # Hz - audio samples per second
CHUNK_SIZE = 1024  # samples per audio chunk
AUDIO_DEVICE_INDEX = 1  # None = default microphone, or specify device index

# Enable debug output
DEBUG = True
