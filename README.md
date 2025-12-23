# 🔒 Time Trap

**Smart PC Lock System with Facial Recognition for macOS**

Time Trap is an intelligent security application that automatically locks your Mac when you step away and instantly locks when it detects an unauthorized user. Built with Python and powered by facial recognition technology.

---

## ✨ Features

### 🎯 Core Security
- **Auto-Lock on Absence** - Automatically locks your Mac after you leave (customizable delay)
- **Unauthorized User Detection** - Instantly locks when an unknown person is detected
- **Facial Recognition** - Uses advanced face recognition to identify authorized users
- **Customizable Sensitivity** - Adjust face matching tolerance to your preference

### 🎨 User Interface
- **Beautiful Settings GUI** - Easy-to-use graphical settings interface
- **Real-time Monitoring** - Live console feedback with timestamps
- **Interactive Setup** - Visual face registration with camera preview

### 📊 Additional Features
- **Activity Logging** - Track all security events with timestamps
- **Sound Alerts** - Audio notifications for important events
- **Auto-start Option** - Begin monitoring automatically on launch
- **Multiple Profiles** - Easy face re-registration

---

## 🖥️ System Requirements

- **Operating System:** macOS 11.0 (Big Sur) or later
- **Python:** 3.8 or higher
- **Camera:** Built-in or external webcam
- **RAM:** 2GB minimum (4GB recommended)

---

## 📦 Installation

### Step 1: Install Dependencies

```bash
# Install required Python packages
pip3 install opencv-python
pip3 install face-recognition
pip3 install numpy
```

**Note:** If `face_recognition` installation fails, you may need to install cmake first:

```bash
brew install cmake
pip3 install face-recognition
```

### Step 2: Download Time Trap

```bash
# Clone or download the repository
git clone https://github.com/yourusername/time-trap.git
cd time-trap
```

### Step 3: Run Time Trap

```bash
python3 main.py
```

---

## 🚀 Quick Start Guide

### First Time Setup

1. **Launch Time Trap**
   ```bash
   python3 main.py
   ```

2. **Select Option 2** - Open Settings (optional but recommended)
   - Adjust lock delay, check interval, and sensitivity
   - Enable sound alerts and activity logging
   - Save your preferences

3. **Register Your Face**
   - If no authorized user is registered, setup will start automatically
   - Position your face clearly in front of the camera
   - Press **SPACE** when ready to capture
   - Your face will be captured and saved securely

4. **Start Monitoring**
   - Select **Option 1** from the menu
   - Time Trap will now monitor for your presence
   - Walk away to test the absence detection!

---

## ⚙️ Configuration

### Settings Menu Options

#### 🔧 Lock Delay (10-300 seconds)
- **Default:** 60 seconds
- **Description:** Time to wait before locking when you're absent
- **Recommendation:** 
  - 30-60s for high security
  - 90-180s for convenience

#### ⏱️ Check Interval (1-10 seconds)
- **Default:** 2 seconds
- **Description:** How often Time Trap checks for your face
- **Recommendation:**
  - 1-2s for quick response
  - 3-5s for balanced performance
  - 5-10s for battery saving

#### 🎯 Face Match Tolerance (0.3-0.9)
- **Default:** 0.6
- **Description:** How strict face matching is
- **Recommendation:**
  - 0.3-0.5: Very strict (fewer false matches, may fail in varied lighting)
  - 0.5-0.7: Balanced (recommended for most users)
  - 0.7-0.9: Lenient (works in varied conditions, slightly less secure)

#### 🔊 Sound Alerts
- Enable/disable audio notifications
- Alert when you leave
- Sound when system locks

#### 📊 Activity Logging
- Logs all events to `timetrap_activity.log`
- Includes timestamps and event details
- Perfect for security auditing

#### 🚀 Auto-start
- Skip the "Press ENTER" prompt
- Begin monitoring immediately on launch

---

## 📋 Menu Options

### Main Menu

```
1. Start Monitoring     - Begin facial recognition monitoring
2. Open Settings        - Adjust Time Trap configuration
3. Re-register Face     - Capture your face again
4. View Activity Log    - See all logged security events
5. Exit                 - Close Time Trap
```

---

## 🔐 Security Features

### How It Works

1. **Authorized User Detection**
   - Continuously monitors camera for faces
   - Compares detected faces with registered authorized user
   - Allows access only to authorized users

2. **Absence Detection**
   - Starts countdown when no face is detected
   - Locks system after configured delay
   - Resets countdown if you return

3. **Unauthorized User Protection**
   - Instantly locks if unknown person detected
   - No countdown - immediate protection
   - Logs security event for review

### What Gets Logged

With logging enabled, Time Trap records:
- Monitoring start/stop times
- User absence events
- System lock events
- Authorized user returns
- **Unauthorized access attempts** ⚠️

---

## 📁 Files Created

Time Trap creates these files in its directory:

| File | Purpose |
|------|---------|
| `timetrap_settings.json` | Your configuration settings |
| `authorized_user.pkl` | Encrypted face data (DO NOT DELETE) |
| `timetrap_activity.log` | Security event history |

---

## 🛡️ Privacy & Security

### Your Data is Safe

- ✅ **All face data stored locally** - Never uploaded to cloud
- ✅ **No internet connection required** - Works completely offline
- ✅ **Encrypted face templates** - Face data is encoded, not raw images
- ✅ **No tracking or telemetry** - Your privacy is respected

### Limitations

⚠️ **Important Security Notes:**

- Time Trap can be fooled by a high-quality photo or video of your face
- Not recommended as sole security measure for highly sensitive systems
- Works best in good lighting conditions
- Requires Mac to be powered on and unlocked for initial face capture

---

## 🐛 Troubleshooting

### Camera Not Working

```bash
# Check camera permissions
# System Preferences > Security & Privacy > Camera
# Ensure Terminal or Python has camera access
```

### Face Not Detected

- **Ensure good lighting** - Face the camera directly with adequate light
- **Adjust tolerance** - Increase tolerance in settings (0.7-0.8)
- **Re-register face** - Use Option 3 to capture face again

### Installation Errors

```bash
# If face_recognition fails to install
brew install cmake
pip3 install dlib
pip3 install face-recognition

# If opencv fails
pip3 install --upgrade pip
pip3 install opencv-python
```

### System Won't Lock

```bash
# Test lock command manually
osascript -e 'tell application "System Events" to keystroke "q" using {control down, command down}'

# If this doesn't work, check System Preferences > Security & Privacy
```

---

## 🎯 Use Cases

### Perfect For:

- 🏢 **Office Workers** - Automatically lock when stepping away from desk
- 👨‍💻 **Developers** - Security without interrupting workflow
- 🏠 **Home Users** - Prevent family members from accessing your Mac
- 🎓 **Students** - Secure your laptop in libraries or shared spaces
- 💼 **Remote Workers** - Extra security for home office

---

## 🔄 Updates & Roadmap

### Coming Soon

- [ ] Eye blink detection (anti-spoofing)
- [ ] Multiple authorized users
- [ ] Screenshot intruders
- [ ] Email notifications
- [ ] Menu bar app
- [ ] Bluetooth proximity lock
- [ ] Dark mode support

---

## 📖 FAQ

**Q: Does Time Trap work when my Mac is asleep?**  
A: No, Time Trap only works when your Mac is awake and unlocked. It locks the screen when you leave, preventing unauthorized access.

**Q: Can someone fool Time Trap with my photo?**  
A: Currently yes. Basic facial recognition can be fooled by photos. We're working on eye blink detection to prevent this.

**Q: Does Time Trap use internet?**  
A: No, Time Trap works completely offline. All processing happens locally on your Mac.

**Q: Will Time Trap slow down my Mac?**  
A: Time Trap has minimal impact. Adjust the check interval to 5+ seconds for even lower CPU usage.

**Q: Can I use Time Trap on multiple Macs?**  
A: Yes, but you'll need to register your face on each Mac separately.

**Q: What happens if I delete `authorized_user.pkl`?**  
A: You'll need to re-register your face. Time Trap will prompt you automatically.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve documentation

---

## 📄 License

MIT License - Feel free to use, modify, and distribute Time Trap.

---

## 👨‍💻 Author

Created by **Anupam Ghosh**

---

## 🙏 Acknowledgments

- **OpenCV** - Computer vision library
- **face_recognition** - Facial recognition powered by dlib
- **MediaPipe** - Alternative face detection (future versions)

---

## 📞 Support

Having issues? Check out:

1. **Troubleshooting section** above
2. **Activity log** - View Option 4 to see what's happening
3. **Settings** - Try adjusting tolerance and check interval

---

## ⚡ Quick Commands

```bash
# Install dependencies
pip3 install opencv-python face-recognition numpy

# Run Time Trap
python3 main.py

# View activity log
cat timetrap_activity.log

# Reset settings (delete settings file)
rm timetrap_settings.json
```

---

## 🎉 Thank You!

Thank you for using Time Trap! Stay secure! 🔒

**Star this repository if you find it useful!** ⭐

---

*Time Trap - Your intelligent security companion for macOS*
