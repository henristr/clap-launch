# Terminal UI Features

The Clap Detector now includes a beautiful, professional terminal interface with ASCII art decorations and colored output.

## 🎨 Visual Features

### Header Display
A stunning ASCII art header that displays when the program starts:
```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ╔═══════════════════════════════════════════════════════════════════╗   ║
║   ║                        🎙️  CLAP DETECTOR 🎙️                       ║   ║
║   ║                  Hand Clap Recognition System                     ║   ║
║   ╚═══════════════════════════════════════════════════════════════════╝   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

### System Configuration Display
Shows startup information in an elegant box:
- Microphone device name
- Number of claps required
- Detection time window
- Number of commands configured
- Current status (ACTIVE)

### Real-Time Audio Meter
Live visualization of audio levels with color coding:
- **QUIET (Green)**: Below -40dB
- **MED (Yellow)**: Between -40dB and -20dB  
- **LOUD (Orange)**: Between -20dB and -5dB
- **CLAP! (Red)**: Above -5dB

The meter displays:
- Animated bar with blocks (█, ▓, ▒, ░)
- Current dB level
- RMS (Root Mean Square) energy
- Threshold indicator

Example:
```
║ [███████████████████░]   -2.0dB CLAP!   RMS:0.1200 │ threshold ║
```

### Status Messages

#### Success (Green ✓)
```
  ✓ Command executed successfully
```

#### Warning (Yellow ⚠)
```
  ⚠ Device not found, using default
```

#### Error (Red ✗)
```
  ✗ Error reading audio stream
```

#### Info (Blue ℹ)
```
  ℹ Listening for claps...
```

### Clap Detection Display
Visual feedback when claps are detected:
```
  👏 Clap detected! (1/2)
```

### Command Execution Display
Beautiful box showing commands being executed:
```
╔───────────────────────────── EXECUTING COMMANDS ───────────────────────────┐
│ 1. toggle_light → light.licht                                              │
└──────────────────────────────────────────────────────────────────────────────┘
  ▶ [1] Executing: toggle_light on light.licht
  ✓ [1] Complete: toggle_light on light.licht
```

### Error Boxes
Helpful error messages with suggestions:
```
╔──────────────────────── ERROR: INVALID AUDIO DEVICE ──────────────────────┐
│ Error: Device not found                                                    │
│ ─────────────────────────────────────────────────────────────────────────── │
│ Suggestions:                                                               │
│ • python clap_detector.py --list-devices                                  │
│ • python clap_detector.py --select-device                                 │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Device List
Color-coded device selection:
```
┌─────────────────────── AVAILABLE AUDIO INPUT DEVICES ────────────────────────┐
│ [0] Microsoft Soundmapper - Input                                           │
│     Channels: 2                                                             │
│     Sample Rate: 44100 Hz                                                   │
│                                                                             │
│ [1] Headset (Realtek(R) Audio) ← DEFAULT                                  │
│     Channels: 2                                                             │
│     Sample Rate: 44100 Hz                                                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 🎯 Color Scheme

The UI uses a professional color scheme:
- **Cyan**: Borders and headers
- **Green**: Success messages and good status
- **Yellow**: Warnings and waiting states
- **Red**: Errors and alert states
- **Blue**: Information and additional details
- **White**: Normal text and values

## 📦 Implementation

The UI is implemented in `ui.py` using:
- ANSI color codes for terminal coloring
- Unicode box-drawing characters (╔═╗╚╝║├┤┬┴┼┌─┐└┘│├┤)
- Emoji for visual appeal
- Structured formatting with margins and padding

## 🔧 Usage

The UI is automatically integrated into the clap detector. Simply run:
```bash
python clap_detector.py
```

All output will use the new beautiful interface!

## 💡 Features

- ✅ Cross-platform color support (with fallback)
- ✅ Structured information boxes
- ✅ Real-time visualization
- ✅ Clear visual hierarchy
- ✅ Professional appearance
- ✅ Emoji support
- ✅ Customizable width (defaults to 80 characters)
