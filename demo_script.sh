#!/bin/bash
# 🎬 Jarvis OS — Viral Demo Script
# ══════════════════════════════════════
# This file doesn't execute code, it is the choreography for the screen recording.
# Follow these exact steps to record the viral GitHub / Twitter video.

echo "🎬 JARVIS OS — DEMO CHOREOGRAPHY 🎬"
echo ""

cat << 'EOF'
[SCENE 1: The Boot]
1. Start with the computer entirely powered off.
2. Press power.
3. Camera shows the dark screen. The GRUB bootloader appears:
   -> Custom JARVIS OS dark theme with cyan arc reactor logo.
4. Hit Enter to boot.
5. The cinematic GTK4 boot animation takes over:
   -> Concentric rings spin up.
   -> 20 lines of diagnostic text scroll quickly (Emotion Engine... ONLINE).
   -> Fades into the desktop.
6. Desktop appears (Hyprland + Waybar).
   -> Voice announces: "All systems online. Ready for your commands, sir."

[SCENE 2: Continuous Conversation & Ecosystem]
1. User: "Jarvis."
   -> Arc reactor HUD overlay pulses cyan (Listening Mode).
2. User: "Open Firefox and go to YouTube."
   -> Jarvis parses Intent -> Generates `<call:OS_CMD{"cmd":"xdg-open https://youtube.com"}>`
   -> Piper TTS speaks instantly (ultra-human voice): "Opening YouTube right away."
   -> Firefox opens.
   -> HUD stays open in Listening Mode (Active Session).
3. User: "Search for some lofi beats."
   -> Jarvis: "Searching for lofi beats."
   -> Executes bash/ydotool to type into search bar.
4. User: "Play the first video."
   -> Jarvis executes click. Music starts playing.

[SCENE 3: Multimodal Vision (The Magic Trick)]
1. Open a terminal. Write a python script with a deliberate syntax error (e.g. missing colon).
2. Run it. It throws a traceback.
3. User: "Jarvis, fix that error."
   -> Jarvis parses intent. Issues `<call:vision{}>`
   -> ScreenAwarenessLayer captures screen -> base64 -> Ollama (llava model).
   -> Jarvis: "Gathering optical data... Ah, you missed a colon on line 14. Fixing it now."
   -> Jarvis executes `<call:OS_CMD{"cmd":"sed -i 's/def foo()/def foo():/' test.py"}>`
4. User: "Run it again."
   -> Jarvis: "Executing." It runs successfully.
5. User: "Good job, go back to sleep."
   -> Jarvis: "Always a pleasure, sir."
   -> Active session closes.

EOF

echo "To record:"
echo "1. Use OBS Studio or a high quality phone camera over-the-shoulder."
echo "2. Ensure lighting shows the transparent glassmorphism UI clearly."
echo "3. Post to r/unixporn, Twitter/X, and Product Hunt."
