"""
TimeTrap – Smart PC Lock System for macOS
Author: Anupom Kumar Ghosh
Copyright © 2025 Anupom Kumar Ghosh

⚠️ LICENSE NOTICE:
This source code is provided for educational viewing only.
Unauthorized use, modification, redistribution, or execution
of this software without the author's consent is prohibited.

Time Trap - Smart PC Lock System for macOS (V1 with Settings GUI)
A facial recognition security system that locks your Mac when you're away
or when an unauthorized user is detected.


"""

import cv2
import face_recognition
import numpy as np
import time
import subprocess
import os
import pickle
import json
from datetime import datetime
import sys
import tkinter as tk
from tkinter import ttk, messagebox

class TimeTrapSettings:
    """Settings manager with GUI"""
    
    def __init__(self):
        self.settings_file = "timetrap_settings.json"
        self.default_settings = {
            "lock_delay": 30,
            "check_interval": 0.1,
            "tolerance": 0.6,
            "sound_enabled": True,
            "log_enabled": True,
            "auto_start": False
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file or create defaults"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except:
                return self.default_settings.copy()
        return self.default_settings.copy()
    
    def save_settings(self):
        """Save settings to file"""
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def show_settings_window(self, callback=None):
        """Display settings GUI window"""
        window = tk.Tk()
        window.title("Time Trap Settings")
        window.geometry("600x520")
        window.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('aqua')  # Native Mac look
        
        # Main container
        main_frame = ttk.Frame(window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="⚙️ Time Trap Settings", 
                               font=("SF Pro Display", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Settings sections
        row = 1
        
        # Lock Delay Setting
        ttk.Label(main_frame, text="Lock Delay (seconds):", 
                 font=("SF Pro Text", 12)).grid(row=row, column=0, sticky=tk.W, pady=10)
        
        lock_delay_var = tk.IntVar(value=self.settings["lock_delay"])
        lock_delay_frame = ttk.Frame(main_frame)
        lock_delay_frame.grid(row=row, column=1, sticky=tk.W, pady=10)
        
        lock_delay_slider = ttk.Scale(lock_delay_frame, from_=10, to=300, 
                                      orient=tk.HORIZONTAL, length=200,
                                      variable=lock_delay_var)
        lock_delay_slider.pack(side=tk.LEFT)
        
        lock_delay_label = ttk.Label(lock_delay_frame, text=f"{lock_delay_var.get()}s",
                                     font=("SF Mono", 11))
        lock_delay_label.pack(side=tk.LEFT, padx=10)
        
        def update_lock_delay_label(*args):
            lock_delay_label.config(text=f"{lock_delay_var.get()}s")
        
        lock_delay_var.trace('w', update_lock_delay_label)
        
        row += 1
        
        # Check Interval Setting
        ttk.Label(main_frame, text="Check Interval (seconds):", 
                 font=("SF Pro Text", 12)).grid(row=row, column=0, sticky=tk.W, pady=10)
        
        check_interval_var = tk.IntVar(value=self.settings["check_interval"])
        check_interval_frame = ttk.Frame(main_frame)
        check_interval_frame.grid(row=row, column=1, sticky=tk.W, pady=10)
        
        check_interval_slider = ttk.Scale(check_interval_frame, from_=1, to=10, 
                                          orient=tk.HORIZONTAL, length=200,
                                          variable=check_interval_var)
        check_interval_slider.pack(side=tk.LEFT)
        
        check_interval_label = ttk.Label(check_interval_frame, text=f"{check_interval_var.get()}s",
                                        font=("SF Mono", 11))
        check_interval_label.pack(side=tk.LEFT, padx=10)
        
        def update_check_interval_label(*args):
            check_interval_label.config(text=f"{check_interval_var.get()}s")
        
        check_interval_var.trace('w', update_check_interval_label)
        
        row += 1
        
        # Tolerance Setting (Face Recognition Tolerance)
        ttk.Label(main_frame, text="Face Match Tolerance:", 
                 font=("SF Pro Text", 12)).grid(row=row, column=0, sticky=tk.W, pady=10)
        
        tolerance_var = tk.DoubleVar(value=self.settings["tolerance"])
        tolerance_frame = ttk.Frame(main_frame)
        tolerance_frame.grid(row=row, column=1, sticky=tk.W, pady=10)
        
        tolerance_slider = ttk.Scale(tolerance_frame, from_=0.3, to=0.9, 
                                     orient=tk.HORIZONTAL, length=200,
                                     variable=tolerance_var)
        tolerance_slider.pack(side=tk.LEFT)
        
        tolerance_label = ttk.Label(tolerance_frame, text=f"{tolerance_var.get():.2f}",
                                   font=("SF Mono", 11))
        tolerance_label.pack(side=tk.LEFT, padx=10)
        
        def update_tolerance_label(*args):
            tolerance_label.config(text=f"{tolerance_var.get():.2f}")
        
        tolerance_var.trace('w', update_tolerance_label)
        
        ttk.Label(main_frame, text="(Lower = Stricter)", 
                 font=("SF Pro Text", 9), foreground="gray").grid(row=row+1, column=1, sticky=tk.W)
        
        row += 2
        
        # Toggle Settings
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, 
                                                              columnspan=2, sticky=(tk.W, tk.E), 
                                                              pady=15)
        row += 1
        
        # Sound Enabled
        sound_var = tk.BooleanVar(value=self.settings["sound_enabled"])
        sound_check = ttk.Checkbutton(main_frame, text="🔊 Enable Sound Alerts", 
                                      variable=sound_var)
        sound_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Logging Enabled
        log_var = tk.BooleanVar(value=self.settings["log_enabled"])
        log_check = ttk.Checkbutton(main_frame, text="📊 Enable Activity Logging", 
                                    variable=log_var)
        log_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Auto Start
        auto_start_var = tk.BooleanVar(value=self.settings["auto_start"])
        auto_start_check = ttk.Checkbutton(main_frame, text="🚀 Start Monitoring Automatically", 
                                           variable=auto_start_var)
        auto_start_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, 
                                                              columnspan=2, sticky=(tk.W, tk.E), 
                                                              pady=15)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        def save_and_close():
            # Update settings
            self.settings["lock_delay"] = lock_delay_var.get()
            self.settings["check_interval"] = check_interval_var.get()
            self.settings["tolerance"] = round(tolerance_var.get(), 2)
            self.settings["sound_enabled"] = sound_var.get()
            self.settings["log_enabled"] = log_var.get()
            self.settings["auto_start"] = auto_start_var.get()
            
            # Save to file
            self.save_settings()
            
            messagebox.showinfo("Settings Saved", 
                              "Your settings have been saved successfully!\n\n" +
                              "Restart Time Trap for changes to take effect.")
            
            if callback:
                callback(self.settings)
            
            window.destroy()
        
        def reset_defaults():
            if messagebox.askyesno("Reset Settings", 
                                  "Are you sure you want to reset all settings to defaults?"):
                self.settings = self.default_settings.copy()
                self.save_settings()
                messagebox.showinfo("Settings Reset", "Settings have been reset to defaults.")
                window.destroy()
                self.show_settings_window(callback)
        
        save_button = ttk.Button(button_frame, text="💾 Save Settings", 
                                command=save_and_close, width=20)
        save_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = ttk.Button(button_frame, text="🔄 Reset to Defaults", 
                                 command=reset_defaults, width=20)
        reset_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="❌ Cancel", 
                                  command=window.destroy, width=15)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Info text at bottom
        row += 1
        info_text = "💡 Tip: Lower tolerance = more strict face matching\n" + \
                   "Higher check interval = less battery usage"
        info_label = ttk.Label(main_frame, text=info_text, 
                              font=("SF Pro Text", 9), foreground="gray",
                              justify=tk.CENTER)
        info_label.grid(row=row, column=0, columnspan=2, pady=10)
        
        window.mainloop()


class TimeTrap:
    def __init__(self, settings_manager):
        """
        Initialize Time Trap security system with settings
        """
        self.settings = settings_manager
        config = self.settings.settings
        
        self.lock_delay = config["lock_delay"]
        self.check_interval = config["check_interval"]
        self.tolerance = config["tolerance"]
        self.sound_enabled = config["sound_enabled"]
        self.log_enabled = config["log_enabled"]
        
        self.authorized_face_encoding = None
        self.user_absent_since = None
        self.camera = None
        self.running = False
        self.encoding_file = "authorized_user.pkl"
        self.log_file = "timetrap_activity.log"
    
    def log_event(self, message):
        """Log events to file if logging is enabled"""
        if self.log_enabled:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(self.log_file, 'a') as f:
                f.write(f"[{timestamp}] {message}\n")
    
    def play_sound(self, sound_type='alert'):
        """Play system sound if sounds are enabled"""
        if self.sound_enabled:
            try:
                if sound_type == 'alert':
                    subprocess.run(['afplay', '/System/Library/Sounds/Sosumi.aiff'])
                elif sound_type == 'lock':
                    subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'])
            except:
                pass
        
    def lock_mac(self):
        """Lock the macOS system"""
        try:
            subprocess.run([
                "osascript", "-e",
                'tell application "System Events" to keystroke "q" using {control down, command down}'
            ])
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔒 System locked!")
            self.log_event("System locked")
            self.play_sound('lock')
        except Exception as e:
            print(f"Error locking system: {e}")
            self.log_event(f"Error locking system: {e}")
    
    def setup_authorized_user(self):
        """Capture and save the authorized user's face"""
        print("\n" + "="*60)
        print("TIME TRAP - AUTHORIZED USER SETUP")
        print("="*60)
        print("\n📸 Starting camera for face registration...")
        print("Please position your face clearly in front of the camera.")
        print("Press SPACE when ready to capture your face.")
        print("Press ESC to cancel.\n")
        
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("❌ Error: Could not access camera!")
            return False
        
        captured = False
        while True:
            ret, frame = self.camera.read()
            if not ret:
                print("❌ Failed to grab frame")
                break
            
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Find faces in current frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            
            # Draw rectangle around detected faces
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, "Face Detected", (left, top - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Display instructions
            cv2.putText(frame, "Press SPACE to capture", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press ESC to cancel", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow("Time Trap - Setup", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                print("\n❌ Setup cancelled")
                break
            elif key == 32 and len(face_locations) > 0:  # SPACE
                print("\n📷 Capturing face...")
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                if len(face_encodings) > 0:
                    self.authorized_face_encoding = face_encodings[0]
                    # Save encoding to file
                    with open(self.encoding_file, 'wb') as f:
                        pickle.dump(self.authorized_face_encoding, f)
                    print("✅ Face captured and saved successfully!")
                    self.log_event("Authorized user registered")
                    captured = True
                    time.sleep(1)
                    break
                else:
                    print("❌ Could not encode face. Please try again.")
            elif key == 32 and len(face_locations) == 0:
                print("⚠️  No face detected. Please position yourself properly.")
        
        self.camera.release()
        cv2.destroyAllWindows()
        return captured
    
    def load_authorized_user(self):
        """Load the authorized user's face encoding from file"""
        if os.path.exists(self.encoding_file):
            with open(self.encoding_file, 'rb') as f:
                self.authorized_face_encoding = pickle.load(f)
            print("✅ Authorized user profile loaded")
            return True
        return False
    
    def check_for_face(self):
        """
        Check camera for faces and determine if authorized user is present
        
        Returns:
            'authorized' - Authorized user detected
            'unauthorized' - Unknown person detected
            'absent' - No person detected
        """
        ret, frame = self.camera.read()
        if not ret:
            return 'absent'
        
        # Convert to RGB for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if len(face_locations) == 0:
            return 'absent'
        
        # Get face encodings
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for face_encoding in face_encodings:
            # Compare with authorized user using configured tolerance
            matches = face_recognition.compare_faces(
                [self.authorized_face_encoding], face_encoding, tolerance=self.tolerance
            )
            
            if matches[0]:
                return 'authorized'
        
        return 'unauthorized'
    
    def run(self):
        """Main monitoring loop"""
        print("\n" + "="*60)
        print("TIME TRAP - ACTIVE MONITORING")
        print("="*60)
        print(f"⚙️  Lock delay: {self.lock_delay} seconds")
        print(f"⚙️  Check interval: {self.check_interval} seconds")
        print(f"⚙️  Face match tolerance: {self.tolerance}")
        print(f"⚙️  Sound alerts: {'Enabled' if self.sound_enabled else 'Disabled'}")
        print(f"⚙️  Activity logging: {'Enabled' if self.log_enabled else 'Disabled'}")
        print("🟢 Monitoring started. Press Ctrl+C to stop.\n")
        
        self.log_event("Monitoring started")
        
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("❌ Error: Could not access camera!")
            return
        
        self.running = True
        self.user_absent_since = None
        
        try:
            while self.running:
                status = self.check_for_face()
                current_time = datetime.now().strftime('%H:%M:%S')
                
                if status == 'authorized':
                    if self.user_absent_since is not None:
                        print(f"[{current_time}] ✅ Authorized user returned")
                        self.log_event("Authorized user returned")
                    self.user_absent_since = None
                    
                elif status == 'absent':
                    if self.user_absent_since is None:
                        self.user_absent_since = time.time()
                        print(f"[{current_time}] ⚠️  User absent - lock countdown started")
                        self.log_event("User absent - countdown started")
                        self.play_sound('alert')
                    else:
                        elapsed = time.time() - self.user_absent_since
                        remaining = self.lock_delay - elapsed
                        if remaining > 0:
                            print(f"[{current_time}] ⏳ Locking in {int(remaining)} seconds...")
                        else:
                            print(f"[{current_time}] 🔒 Lock delay exceeded - locking system")
                            self.lock_mac()
                            self.user_absent_since = None
                
                elif status == 'unauthorized':
                    print(f"[{current_time}] 🚨 UNAUTHORIZED USER DETECTED - LOCKING IMMEDIATELY")
                    self.log_event("UNAUTHORIZED USER DETECTED - System locked")
                    self.play_sound('alert')
                    self.lock_mac()
                    self.user_absent_since = None
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🛑 Monitoring stopped by user")
            self.log_event("Monitoring stopped by user")
        finally:
            self.camera.release()
            print("👋 Time Trap shutdown complete")
    
    def start(self):
        """Initialize and start Time Trap"""
        print("\n" + "="*60)
        print("  _____ ___ __  __ _____   _____ ____      _    ____  ")
        print(" |_   _|_ _|  \\/  | ____| |_   _|  _ \\    / \\  |  _ \\ ")
        print("   | |  | || |\\/| |  _|     | | | |_) |  / _ \\ | |_) |")
        print("   | |  | || |  | | |___    | | |  _ <  / ___ \\|  __/ ")
        print("   |_| |___|_|  |_|_____|   |_| |_| \\_\\/_/   \\_\\_|    ")

        print("    ")
        print("                                          MADE BY REDEYES(ANUPOM)")
        print("="*60)
        print("Smart PC Lock System with Face Recognition")
        print("="*60 + "\n")
        
        # Check if authorized user exists
        if not self.load_authorized_user():
            print("⚠️  No authorized user found. Starting setup...\n")
            if not self.setup_authorized_user():
                print("\n❌ Setup failed. Exiting.")
                return
        
        print("\n✅ System ready!")
        
        # Check if auto-start is enabled
        if self.settings.settings.get("auto_start", False):
            print("🚀 Auto-start enabled. Starting monitoring in 3 seconds...")
            time.sleep(3)
        else:
            input("Press ENTER to start monitoring...")
        
        self.run()


def main():

    """Main entry point"""
    print("="*60)
    print("TIME TRAP - STARTUP")
    print("="*60)
    
    # Load settings
    settings_manager = TimeTrapSettings()
    
    print("\n1. Start Monitoring")
    print("2. Re-register Face")
    print("3. View Activity Log")
    print("4. Exit")
    
    choice = input("\nSelect option (1-5): ").strip()
    
   
    if choice == "2":
        # Force re-registration
        time_trap = TimeTrap(settings_manager)
        time_trap.setup_authorized_user()
        return
    elif choice == "3":
        # View activity log
        if os.path.exists("timetrap_activity.log"):
            print("\n" + "="*60)
            print("ACTIVITY LOG")
            print("="*60 + "\n")
            with open("timetrap_activity.log", 'r') as f:
                print(f.read())
            print("\n" + "="*60)
            input("\nPress ENTER to continue...")
        else:
            print("\n⚠️  No activity log found. Enable logging in settings.")
            time.sleep(2)
        return
    elif choice == "4":
        print("👋 Goodbye!")
        return
    
    # Start monitoring
    time_trap = TimeTrap(settings_manager)
    time_trap.start()


if __name__ == "__main__":
    main()