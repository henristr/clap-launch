"""
Beautiful terminal UI for Clap Detector
Provides ASCII art and formatted output
"""

import os
import sys
import time
from datetime import datetime

class TerminalUI:
    """Handles all terminal UI and formatting"""
    
    # ANSI color codes
    COLORS = {
        'RESET': '\033[0m',
        'BOLD': '\033[1m',
        'DIM': '\033[2m',
        'ITALIC': '\033[3m',
        'UNDERLINE': '\033[4m',
        
        # Foreground colors
        'BLACK': '\033[30m',
        'RED': '\033[31m',
        'GREEN': '\033[32m',
        'YELLOW': '\033[33m',
        'BLUE': '\033[34m',
        'MAGENTA': '\033[35m',
        'CYAN': '\033[36m',
        'WHITE': '\033[37m',
        
        # Bright foreground colors
        'BRIGHT_RED': '\033[91m',
        'BRIGHT_GREEN': '\033[92m',
        'BRIGHT_YELLOW': '\033[93m',
        'BRIGHT_BLUE': '\033[94m',
        'BRIGHT_MAGENTA': '\033[95m',
        'BRIGHT_CYAN': '\033[96m',
        'BRIGHT_WHITE': '\033[97m',
    }
    
    def __init__(self, width=80):
        self.width = width
        # Enable UTF-8 output on Windows
        if sys.platform == 'win32':
            import io
            import os
            os.environ['PYTHONIOENCODING'] = 'utf-8'
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        
        self.disable_colors = os.getenv('NO_COLOR')
        
    def colorize(self, text, color):
        """Apply color to text"""
        if self.disable_colors:
            return text
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['RESET']}"
    
    def header(self, title):
        """Display main header with ASCII art"""
        art = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ╔═══════════════════════════════════════════════════════════════════╗   ║
║   ║                        🎙️  CLAP DETECTOR 🎙️                       ║   ║
║   ║                  Hand Clap Recognition System                     ║   ║
║   ╚═══════════════════════════════════════════════════════════════════╝   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
        """
        print(self.colorize(art, 'BRIGHT_CYAN'))
    
    def section_header(self, title):
        """Display section header"""
        padding = self.width - len(title) - 4
        left_pad = padding // 2
        right_pad = padding - left_pad
        line = f"┌{'─' * left_pad} {title} {'─' * right_pad}┐"
        print(self.colorize(line, 'BRIGHT_CYAN'))
    
    def section_footer(self):
        """Display section footer"""
        print(self.colorize(f"└{'─' * (self.width - 2)}┘", 'BRIGHT_CYAN'))
    
    def info_box(self, title, content_lines):
        """Display an information box"""
        self.section_header(title)
        for line in content_lines:
            print(f"│ {line:<{self.width - 4}} │")
        self.section_footer()
    
    def status_line(self, label, value, color='BRIGHT_WHITE'):
        """Display a status line"""
        colored_label = self.colorize(label, 'BRIGHT_CYAN')
        colored_value = self.colorize(value, color)
        print(f"  ├─ {colored_label}: {colored_value}")
    
    def success(self, message):
        """Display success message"""
        emoji = self.colorize("✓", 'BRIGHT_GREEN')
        msg = self.colorize(message, 'BRIGHT_GREEN')
        print(f"\n  {emoji} {msg}")
    
    def error(self, message):
        """Display error message"""
        emoji = self.colorize("✗", 'BRIGHT_RED')
        msg = self.colorize(message, 'BRIGHT_RED')
        print(f"\n  {emoji} {msg}")
    
    def warning(self, message):
        """Display warning message"""
        emoji = self.colorize("⚠", 'BRIGHT_YELLOW')
        msg = self.colorize(message, 'BRIGHT_YELLOW')
        print(f"\n  {emoji} {msg}")
    
    def info(self, message):
        """Display info message"""
        emoji = self.colorize("ℹ", 'BRIGHT_BLUE')
        msg = self.colorize(message, 'BRIGHT_BLUE')
        print(f"\n  {emoji} {msg}")
    
    def draw_db_meter(self, db, rms, threshold):
        """Draw a visual dB meter with threshold indicator"""
        # Normalize db to 0-100 scale (-60 to 0 dB)
        meter_value = max(0, min(100, (db + 60) / 0.6))
        filled = int(meter_value / 5)
        empty = 20 - filled
        
        # Color coding based on level
        if db > -5:  # Likely a clap
            color = 'BRIGHT_RED'
            status = "CLAP!  "
            meter_char = "█"
        elif db > -20:
            color = 'BRIGHT_YELLOW'
            status = "LOUD  "
            meter_char = "▓"
        elif db > -40:
            color = 'BRIGHT_GREEN'
            status = "MED   "
            meter_char = "▒"
        else:
            color = 'BRIGHT_WHITE'
            status = "QUIET "
            meter_char = "░"
        
        bar = self.colorize(meter_char * filled, color) + self.colorize("░" * empty, 'DIM')
        
        # Threshold indicator
        threshold_pos = max(0, min(20, int((threshold + 60) / 3)))
        threshold_marker = ""
        if threshold_pos > 0 and threshold_pos < 20:
            threshold_marker = f" {self.colorize('│', 'BRIGHT_BLUE')} threshold"
        
        meter_line = f"  ║ [{bar}] {db:6.1f}dB {status} RMS:{rms:.4f}{threshold_marker} ║"
        return meter_line
    
    def listening_display(self, claps_detected, claps_needed, time_window):
        """Display listening state"""
        clap_str = self.colorize(f"{claps_detected}/{claps_needed}", 'BRIGHT_YELLOW')
        print(f"\n  ├─ Status: Listening for claps ({clap_str})")
        print(f"  ├─ Time Window: {self.colorize(f'{time_window}s', 'BRIGHT_WHITE')}")
        print(f"  └─ Waiting for next clap...")
    
    def clap_detected(self, clap_count, total_needed):
        """Display clap detection message"""
        emoji = self.colorize("👏", 'BRIGHT_GREEN')
        count = self.colorize(f"{clap_count}/{total_needed}", 'BRIGHT_YELLOW')
        msg = f"\n  {emoji} Clap detected! ({count})"
        print(msg)
    
    def execution_box(self, commands, ha_actions):
        """Display command execution box"""
        self.section_header("EXECUTING COMMANDS")
        
        cmd_index = 0
        ha_index = 0
        
        for i, cmd in enumerate(commands, 1):
            if cmd == 'home-assistant':
                if ha_index < len(ha_actions):
                    ha_config = ha_actions[ha_index]
                    entity = self.colorize(ha_config.get('entity_id', 'unknown'), 'BRIGHT_CYAN')
                    action = self.colorize(ha_config.get('action', 'unknown'), 'BRIGHT_YELLOW')
                    print(f"│ {i}. {action} → {entity} {' ' * (self.width - 60)} │")
                    ha_index += 1
            else:
                cmd_display = self.colorize(cmd[:self.width - 20], 'BRIGHT_WHITE')
                print(f"│ {i}. {cmd_display} {' ' * (self.width - len(cmd) - 10)} │")
        
        self.section_footer()
    
    def command_executing(self, index, command):
        """Display command execution in progress"""
        emoji = self.colorize("▶", 'BRIGHT_BLUE')
        cmd = self.colorize(command[:50], 'BRIGHT_YELLOW')
        print(f"  {emoji} [{index}] Executing: {cmd}")
    
    def command_success(self, index, command):
        """Display command executed successfully"""
        emoji = self.colorize("✓", 'BRIGHT_GREEN')
        cmd = self.colorize(command[:50], 'BRIGHT_WHITE')
        print(f"  {emoji} [{index}] Complete: {cmd}")
    
    def command_failed(self, index, error):
        """Display command execution failure"""
        emoji = self.colorize("✗", 'BRIGHT_RED')
        err = self.colorize(str(error)[:50], 'BRIGHT_RED')
        print(f"  {emoji} [{index}] Failed: {err}")
    
    def divider(self, char="═"):
        """Print a divider line"""
        print(self.colorize(f"╔{'═' * (self.width - 4)}╗", 'BRIGHT_CYAN'))
    
    def startup_info(self, claps_needed, time_window, device_name, command_count):
        """Display startup information"""
        print()
        self.section_header("SYSTEM CONFIGURATION")
        
        lines = [
            f"Microphone:        {self.colorize(device_name, 'BRIGHT_GREEN')}",
            f"Claps Required:    {self.colorize(str(claps_needed), 'BRIGHT_YELLOW')}",
            f"Detection Window:  {self.colorize(f'{time_window}s', 'BRIGHT_YELLOW')}",
            f"Commands Ready:    {self.colorize(str(command_count), 'BRIGHT_YELLOW')}",
            f"Status:            {self.colorize('ACTIVE', 'BRIGHT_GREEN')}",
        ]
        
        for line in lines:
            print(f"│ {line:<{self.width - 4}} │")
        
        self.section_footer()
    
    def listening_state(self):
        """Display listening state header"""
        print()
        self.section_header("LISTENING FOR CLAPS")
        print(f"│ {'Monitoring audio input...':<{self.width - 4}} │")
        self.section_footer()
        print()
    
    def meter_header(self):
        """Display meter section header"""
        print(self.colorize("  ╔" + "═" * 74 + "╗", 'BRIGHT_CYAN'))
        print(self.colorize("  ║ " + "Audio Level Monitor".center(72) + " ║", 'BRIGHT_CYAN'))
        print(self.colorize("  ╠" + "═" * 74 + "╣", 'BRIGHT_CYAN'))
    
    def meter_footer(self):
        """Display meter section footer"""
        print(self.colorize("  ╚" + "═" * 74 + "╝", 'BRIGHT_CYAN'))
    
    def controls(self):
        """Display control instructions"""
        print()
        self.section_header("CONTROLS")
        lines = [
            "Press Ctrl+C to stop the detector",
        ]
        for line in lines:
            print(f"│ {line:<{self.width - 4}} │")
        self.section_footer()
    
    def goodbye(self):
        """Display goodbye message"""
        print()
        goodbye_art = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                      👋 Clap Detector Stopped                              ║
║                      Thank you for using CLAP-LAUNCH!                      ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
        """
        print(self.colorize(goodbye_art, 'BRIGHT_CYAN'))
    
    def error_box(self, title, error_msg, suggestions=None):
        """Display error box with suggestions"""
        print()
        self.section_header(f"ERROR: {title}")
        
        # Split error message into lines
        error_lines = error_msg.split('\n')
        for line in error_lines:
            if line.strip():
                print(f"│ {self.colorize(line, 'BRIGHT_RED'):<{self.width - 4}} │")
        
        if suggestions:
            print(f"│ {'─' * (self.width - 4)} │")
            print(f"│ {self.colorize('Suggestions:', 'BRIGHT_YELLOW'):<{self.width - 4}} │")
            for suggestion in suggestions:
                print(f"│ • {suggestion:<{self.width - 6}} │")
        
        self.section_footer()
    
    def clap_celebration(self):
        """Display celebration animation for clap trigger"""
        celebration = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                   🎉 🎉 🎉 CLAP DETECTED! 🎉 🎉 🎉                         ║
║                                                                            ║
║                         Executing Commands...                              ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
        """
        print(self.colorize(celebration, 'BRIGHT_GREEN'))
    
    def progress_bar(self, current, total, width=40):
        """Draw a progress bar"""
        filled = int(width * current / total)
        bar = "█" * filled + "░" * (width - filled)
        percent = 100 * current / total
        return f"[{self.colorize(bar, 'BRIGHT_GREEN')}] {percent:.0f}%"


# Singleton instance
_ui = None

def get_ui():
    """Get or create UI instance"""
    global _ui
    if _ui is None:
        _ui = TerminalUI()
    return _ui
