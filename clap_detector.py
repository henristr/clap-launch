"""
Clap Detection Script with Beautiful Terminal UI
Detects hand claps and triggers configured actions
"""

import sounddevice as sd
import numpy as np
import subprocess
import sys
import time
import requests
from collections import deque
from config import (
    COMMANDS,
    COMMAND_DELAY,
    CLAPS_TO_TRIGGER,
    CLAP_THRESHOLD,
    CLAP_TIME_WINDOW,
    SAMPLE_RATE,
    CHUNK_SIZE,
    AUDIO_DEVICE_INDEX,
    DEBUG,
    HA_ACTIONS
)
from ui import get_ui


class ClapDetector:
    def __init__(self):
        self.clap_times = deque()
        self.is_running = False
        self.last_clap_time = 0
        self.clap_cooldown = 0.15  # Minimum time between claps
        self.ui = get_ui()
        
    def list_microphones(self):
        """Print available audio devices with details"""
        print()
        self.ui.section_header("AVAILABLE AUDIO INPUT DEVICES")
        devices = sd.query_devices()
        mic_count = 0
        
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                default_marker = " ← DEFAULT" if i == sd.default.device[0] else ""
                sample_rate = int(device['default_samplerate'])
                device_name = self.ui.colorize(device['name'], 'BRIGHT_CYAN')
                print(f"│ [{i}] {device_name}{default_marker:<40} │")
                print(f"│     Channels: {device['max_input_channels']:<50} │")
                print(f"│     Sample Rate: {sample_rate} Hz{' ' * 42} │")
                print(f"│ {' ' * 74} │")
                mic_count += 1
        
        if mic_count == 0:
            self.ui.error("No input devices found!")
        else:
            print(f"│ Total: {mic_count} input device(s){' ' * 54} │")
        
        self.ui.section_footer()
        print()
        self.ui.info("To use a specific device, set AUDIO_DEVICE_INDEX in config.py")
        print()

    def select_microphone_interactive(self):
        """Interactive device selection"""
        print()
        self.ui.section_header("SELECT AUDIO INPUT DEVICE")
        devices = sd.query_devices()
        input_devices = []
        
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                input_devices.append(i)
                default_marker = " ← DEFAULT" if i == sd.default.device[0] else ""
                device_name = self.ui.colorize(device['name'], 'BRIGHT_CYAN')
                print(f"│ [{len(input_devices)}] {device_name}{default_marker:<44} │")
        
        if not input_devices:
            self.ui.error("No input devices found!")
            return None
        
        print(f"│ [0] Use default device{' ' * 52} │")
        self.ui.section_footer()
        
        try:
            choice = input("\n  Enter device number (or press Enter for default): ").strip()
            if not choice or choice == "0":
                device_idx = sd.default.device[0]
                device_name = sd.query_devices(device_idx)['name']
                self.ui.success(f"Using default device: {device_name}")
                return device_idx
            
            choice_num = int(choice) - 1
            if 0 <= choice_num < len(input_devices):
                device_idx = input_devices[choice_num]
                device_name = sd.query_devices(device_idx)['name']
                self.ui.success(f"Using device: {device_name}")
                return device_idx
            else:
                self.ui.error("Invalid selection!")
                return None
        except (ValueError, KeyboardInterrupt):
            self.ui.warning("Using default device...")
            return None

    def calculate_db(self, audio_chunk):
        """Calculate dB level from audio chunk"""
        audio_normalized = np.abs(audio_chunk.flatten())
        rms_energy = np.sqrt(np.mean(audio_normalized ** 2))
        
        # Convert to dB (with floor at -80 dB to avoid log(0))
        if rms_energy > 0:
            db = 20 * np.log10(rms_energy)
        else:
            db = -80
        
        return db, rms_energy

    def draw_db_meter(self, db, rms):
        """Draw a visual dB meter"""
        return self.ui.draw_db_meter(db, rms, CLAP_THRESHOLD)

    def detect_clap(self, audio_chunk):
        """
        Detect if audio chunk contains a clap using multiple heuristics
        """
        db, rms = self.calculate_db(audio_chunk)
        
        # Print meter
        meter = self.draw_db_meter(db, rms)
        print(f"\r{meter}", end="", flush=True)
        
        # Check if above threshold and enough time has passed since last clap
        current_time = time.time()
        if rms > CLAP_THRESHOLD and (current_time - self.last_clap_time) > self.clap_cooldown:
            # Additional check: look for frequency content typical of claps (1-3 kHz)
            if len(audio_chunk) > 1:
                fft = np.fft.fft(audio_chunk.flatten())
                freqs = np.fft.fftfreq(len(fft), 1/SAMPLE_RATE)
                
                # Look at magnitude in clap frequency range (1-3 kHz)
                clap_range = np.abs(fft[(freqs > 1000) & (freqs < 3000)])
                if len(clap_range) > 0 and np.max(clap_range) > np.max(np.abs(fft)) * 0.3:
                    self.last_clap_time = current_time
                    return True
        
        return False

    def execute_command(self):
        """Execute all configured commands"""
        try:
            self.ui.clap_celebration()
            
            self.ui.execution_box(COMMANDS, HA_ACTIONS)
            
            ha_command_index = 0
            
            for i, cmd in enumerate(COMMANDS, 1):
                if cmd == 'home-assistant':
                    if ha_command_index < len(HA_ACTIONS):
                        ha_config = HA_ACTIONS[ha_command_index]
                        if ha_config['enabled']:
                            action = ha_config['action']
                            entity = ha_config['entity_id']
                            self.ui.command_executing(i, f"{action} on {entity}")
                            self.call_home_assistant(ha_config)
                            self.ui.command_success(i, f"{action} on {entity}")
                        ha_command_index += 1
                else:
                    self.ui.command_executing(i, cmd)
                    subprocess.Popen(cmd, shell=True)
                    self.ui.command_success(i, cmd)
                
                # Delay between commands
                if i < len(COMMANDS):
                    time.sleep(COMMAND_DELAY)
            
            return True
        except Exception as e:
            self.ui.command_failed(1, str(e))
            return False

    def call_home_assistant(self, ha_config):
        """Call Home Assistant API with given config"""
        try:
            headers = {
                'Authorization': f'Bearer {ha_config["token"]}',
                'Content-Type': 'application/json'
            }
            
            url = None
            payload = {}
            
            if ha_config['action'] == 'toggle_switch':
                url = f"{ha_config['url']}/api/services/switch/toggle"
                payload = {'entity_id': ha_config['entity_id']}
                
            elif ha_config['action'] == 'toggle_light':
                url = f"{ha_config['url']}/api/services/light/toggle"
                payload = {'entity_id': ha_config['entity_id']}
                
            elif ha_config['action'] == 'activate_scene':
                url = f"{ha_config['url']}/api/services/scene/turn_on"
                payload = {'entity_id': ha_config['entity_id']}
                
            elif ha_config['action'] == 'call_service':
                service_domain, service_name = ha_config['service'].split('.')
                url = f"{ha_config['url']}/api/services/{service_domain}/{service_name}"
                payload = {'entity_id': ha_config['entity_id']}
            
            if url is None:
                self.ui.error(f"Unknown action: {ha_config['action']}")
                return False
            
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            
            if response.status_code in [200, 201]:
                return True
            else:
                self.ui.error(f"Home Assistant error: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.ui.error(f"Could not connect to Home Assistant at {ha_config['url']}")
            return False
        except Exception as e:
            self.ui.error(f"Error calling Home Assistant: {e}")
            return False

    def process_clap(self):
        """Handle clap detection logic"""
        current_time = time.time()
        
        # Remove claps outside the time window
        while self.clap_times and (current_time - self.clap_times[0]) > CLAP_TIME_WINDOW:
            self.clap_times.popleft()
        
        # Add current clap
        self.clap_times.append(current_time)
        
        clap_count = len(self.clap_times)
        
        if clap_count < CLAPS_TO_TRIGGER:
            self.ui.clap_detected(clap_count, CLAPS_TO_TRIGGER)
        
        # Check if we have enough claps
        if clap_count >= CLAPS_TO_TRIGGER:
            self.execute_command()
            self.clap_times.clear()

    def run(self):
        """Main detection loop"""
        self.is_running = True
        
        try:
            # Display header
            self.ui.header("CLAP DETECTOR")
            
            # Validate device index
            device_index = AUDIO_DEVICE_INDEX
            if device_index is not None:
                try:
                    device_info = sd.query_devices(device_index)
                    if device_info['max_input_channels'] == 0:
                        self.ui.warning(f"Device {device_index} has no input channels!")
                        device_index = None
                except Exception as e:
                    self.ui.warning(f"Device {device_index} not found: {e}")
                    device_index = None
            
            # Get device name
            device_used = sd.query_devices(device_index)['name'] if device_index is not None else sd.query_devices(sd.default.device[0])['name']
            
            # Display startup info
            self.ui.startup_info(CLAPS_TO_TRIGGER, CLAP_TIME_WINDOW, device_used, len(COMMANDS))
            
            self.ui.listening_state()
            self.ui.meter_header()
            
            with sd.InputStream(
                device=device_index,
                samplerate=SAMPLE_RATE,
                channels=1,
                blocksize=CHUNK_SIZE,
                latency='low'
            ) as stream:
                while self.is_running:
                    try:
                        audio_chunk, _ = stream.read(CHUNK_SIZE)
                        
                        if self.detect_clap(audio_chunk):
                            self.process_clap()
                            
                    except KeyboardInterrupt:
                        break
                    except Exception as e:
                        self.ui.error(f"Error reading audio: {e}")
            
            self.ui.meter_footer()
            
        except ValueError as e:
            self.ui.error_box(
                "INVALID AUDIO DEVICE",
                f"Error: {e}",
                [
                    "python clap_detector.py --list-devices",
                    "python clap_detector.py --select-device",
                    "Or manually set AUDIO_DEVICE_INDEX in config.py"
                ]
            )
            self.list_microphones()
            
        except Exception as e:
            self.ui.error_box(
                "AUDIO SYSTEM ERROR",
                f"Error: {e}",
                [
                    "Check microphone is connected",
                    "Run: python clap_detector.py --list-devices",
                    "Run: python clap_detector.py --select-device",
                ]
            )
            
        finally:
            self.ui.meter_footer()
            self.ui.goodbye()

    def stop(self):
        """Stop the detector"""
        self.is_running = False


if __name__ == '__main__':
    detector = ClapDetector()
    
    if '--list-devices' in sys.argv:
        detector.list_microphones()
        sys.exit(0)
    
    if '--select-device' in sys.argv:
        device_idx = detector.select_microphone_interactive()
        if device_idx is not None:
            detector.ui.success(f"Add this to config.py:")
            print(f"  AUDIO_DEVICE_INDEX = {device_idx}")
        sys.exit(0)
    
    # Start detector
    try:
        detector.run()
    except KeyboardInterrupt:
        print("\n\nStopping...")
        detector.stop()
