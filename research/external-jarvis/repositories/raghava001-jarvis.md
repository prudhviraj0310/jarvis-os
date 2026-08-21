# Research Inspection: Raghava001-web / Jarvis

- **Repository URL**: `https://github.com/Raghava001-web/Jarvis`
- **Primary License**: MIT License
- **Primary Languages**: Python 3.10+, HTML5 / Three.js / CSS3
- **Primary Frameworks**: PyQt5/PyQt6, Gemini Live API, MediaPipe, Three.js, WebSockets

---

## 1. System Architecture
`Raghava001-web/Jarvis` focuses heavily on the futuristic Iron Man tactical HUD user experience and real-time multimodal interaction:
* **Holographic 3D HUD (`jarvis/gui/integrated_hud.py`, `web_hud/`)**: Three.js 3D rotating globe, waveform visualizers, glowing reactor telemetry, and holographic window management.
* **Gemini Live Multimodal Engine (`jarvis/core/gemini_live_engine.py`)**: Full-duplex bidirectional audio streaming with sub-500ms voice response and dynamic interruption handling.
* **Perception & Emotion Detection (`jarvis/core/perception.py`, `multimodal_emotion.py`)**: MediaPipe face tracking, emotion estimation, and gesture command interpretation.
* **Intent & Decision Router (`jarvis/core/intent_handlers.py`, `decision_engine.py`)**: Fast local intent classification using cached embeddings (`intent_embeddings_v2.npz`).

---

## 2. Major Capabilities
1. **Full-Duplex Voice with Interruption**: Can be interrupted mid-sentence without crashing the audio stream.
2. **Iron Man 3D Tactical Interface**: Real-time 60 FPS Three.js canvas with particle effects and telemetry dials.
3. **Multimodal Emotion & Gesture Input**: Reads user facial expressions and hand gestures (pinch, swipe, open palm) for UI navigation.
4. **Local Intent Caching**: High-frequency intents bypass the LLM completely via cosine similarity over local vector embeddings.

---

## 3. Entry Points & Key Modules
* **Main Launcher**: `jarvis/main.py`, `jarvis/jarvis_ultimate.py`.
* **Voice Engine**: `jarvis/core/gemini_live_engine.py`.
* **GUI Engine**: `jarvis/gui/integrated_hud.py`, `web_hud_launcher.py`.
* **Perception**: `jarvis/core/perception.py`.

---

## 4. Dependencies
* `google-genai`, `mediapipe`, `opencv-python`, `pyaudio`, `websockets`, `three.js`

---

## 5. Security & Machine Sovereignty Analysis
* Primarily designed as an interactive desktop layer. Low emphasis on execution sandboxing or permission gating; all commands execute with user desktop privileges.

---

## 6. What Can Be Adapted to JARVIS OS
* **Full-Duplex Voice Interruption Pattern**: WebRTC / WebSocket audio streaming buffer design allowing instant cut-off when the user starts speaking.
* **3D Particle & Waveform HUD Aesthetics**: Can be rendered directly in Wayland layer surfaces or WebKit glassmorphic overlays.
* **Local Intent Vector Cache**: Fast sub-5ms intent routing for common system operations.

---

## 7. What is NOT Suitable
* Heavy MediaPipe/OpenCV dependencies in the core kernel — Perception must run as an optional isolated userland process.

---

## 8. License Compliance
* **MIT License**: Fully permissive for commercial use and modification with attribution.
