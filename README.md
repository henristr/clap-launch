# Clap Detection System

A simple Python system that detects hand claps and triggers actions.

## Files

- **config.py** - Configuration settings (what to run, sensitivity, etc.)
- **clap_detector.py** - Main detection script
- **requirements.txt** - Python dependencies

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** PyAudio may require extra setup on Windows:
- Download and install the PyAudio wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Or use: `pip install pipwin` then `pipwin install pyaudio`

### 2. Configure Settings

Edit `config.py` to set:
- **COMMAND_TO_RUN** - What to execute (app, command, URL, script)
- **CLAPS_TO_TRIGGER** - Number of claps needed (1, 2, or 3)
- **CLAP_THRESHOLD** - Sensitivity (lower = more sensitive)
- **DEBUG** - Enable verbose output

### 3. Run the Script

```bash
python clap_detector.py
```

The detector will start listening on your default microphone. Press Ctrl+C to stop.

## Configuration Examples

### Single Command - Open Notepad
```python
COMMANDS = ['notepad']
```

### Single Command - Toggle Home Assistant Switch
```python
COMMANDS = ['home-assistant']

HA_ACTIONS = [
    {
        'enabled': True,
        'url': 'http://homeassistant.local:8123',
        'token': 'your_token_here',
        'action': 'toggle_switch',
        'entity_id': 'switch.living_room',
    }
]
```

### Multiple Commands - Home Assistant + Open App
```python
COMMANDS = [
    'home-assistant',    # Toggle switch first
    'notepad',          # Then open notepad
]
COMMAND_DELAY = 0.5  # 0.5 second delay between commands
```

### Multiple Home Assistant Actions
```python
COMMANDS = ['home-assistant', 'home-assistant']

HA_ACTIONS = [
    {
        'enabled': True,
        'url': 'http://homeassistant.local:8123',
        'token': 'your_token',
        'action': 'toggle_light',
        'entity_id': 'light.bedroom',
    },
    {
        'enabled': True,
        'url': 'http://homeassistant.local:8123',
        'token': 'your_token',
        'action': 'toggle_switch',
        'entity_id': 'switch.fan',
    }
]
```

### Complex Chain - Activate Scene + Play Music + Send Notification
```python
COMMANDS = [
    'home-assistant',           # Activate movie scene
    'start https://music.com',  # Open music service
]

HA_ACTIONS = [
    {
        'enabled': True,
        'url': 'http://homeassistant.local:8123',
        'token': 'your_token',
        'action': 'activate_scene',
        'entity_id': 'scene.movie_time',
    }
]
```

## Troubleshooting

### Device/Microphone Issues

**List all audio devices:**
```bash
python clap_detector.py --list-devices
```
Shows detailed info about each device (name, channels, sample rate, index)

**Interactive device selector:**
```bash
python clap_detector.py --select-device
```
Walks you through selecting a device and shows the code to add to config.py

**Manually set device:**
Edit `config.py` and set:
```python
AUDIO_DEVICE_INDEX = 2  # Use device index 2
```

### "Error opening audio stream"
1. Run `python clap_detector.py --list-devices` to see available devices
2. If no devices show up, your microphone may not be recognized
3. Try `--select-device` for interactive selection
4. Or update `AUDIO_DEVICE_INDEX` in config.py

### Claps Not Detecting
- Lower `CLAP_THRESHOLD` to make it more sensitive
- Clap louder
- Check `DEBUG = True` to see when sounds are detected on the dB meter

### Home Assistant Connection Issues
- **"Could not connect to Home Assistant"** - Check:
  - HA_URL is correct (try finding your Home Assistant IP/hostname)
  - Home Assistant is running and accessible
  - Firewall isn't blocking access
- **"401 Unauthorized"** - Token issue:
  - Go to Settings > Devices & Services > Create Token
  - Copy the entire token and paste in HA_TOKEN
  - Make sure there are no extra spaces in the token
- **Still not working?** - Test connection manually:
  ```bash
  curl -X GET http://homeassistant.local:8123/api/ -H "Authorization: Bearer YOUR_TOKEN"
  ```

## How It Works

1. Captures audio from your microphone continuously
2. Analyzes energy levels (RMS) of each audio chunk
3. When energy exceeds threshold, counts it as a clap
4. After detecting the configured number of claps within the time window, executes the command
5. Resets counter and waits for next clap sequence

## Beautiful Terminal UI

The Clap Detector features a stunning terminal interface with:

- **ASCII Art Headers** - Eye-catching title and status displays
- **Color-Coded Output** - Visual feedback with bright colors and emojis
- **Real-Time Audio Meter** - Live dB level visualization with color gradients
- **Structured Boxes** - Information organized in elegant bordered sections
- **Status Indicators** - Clear visual markers for claps, errors, and successes
- **Command Execution Display** - Watch as your commands execute in real-time

### Example UI Features:

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ╔═══════════════════════════════════════════════════════════════════╗   ║
║   ║                        🎙️  CLAP DETECTOR 🎙️                       ║   ║
║   ║                  Hand Clap Recognition System                     ║   ║
║   ╚═══════════════════════════════════════════════════════════════════╝   ║
```

**Features:**
- Real-time dB meter with threshold indicator
- Animated clap detection counter
- Color-coded device list
- Beautiful error messages with suggestions
- Command execution tracking
- Celebration display on successful clap trigger

## Tips

- **Sensitivity:** Start with CLAP_THRESHOLD = 0.02, adjust up or down
- **Multiple Actions:** Run multiple clap detectors with different configs in separate terminals
- **Environment:** Works best in quiet environments; loud noise may cause false triggers
- **Time Window:** Increase CLAP_TIME_WINDOW if you clap slowly, decrease if you clap quickly
- **Home Assistant:** Find entity IDs in Developer Tools > States in Home Assistant UI
