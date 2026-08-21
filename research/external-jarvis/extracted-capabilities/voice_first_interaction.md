# Capability Blueprint: Voice-First Full-Duplex Interaction

- **Inspired by**: `Raghava001/Jarvis` (Gemini Live Full-Duplex), `ambartsumov/jarvis-agent` (Vosk Offline STT)

---

## 1. Dual-Mode Voice Pipeline
1. **Offline Mode (Zero-Cloud / Latency <50ms)**:
   * Engine: Local Vosk / Whisper.cpp small model running directly on CPU.
   * Recognizes system wake words (`"Hey Jarvis"`, `"Jarvis"`) and core control commands (`"Open Browser"`, `"MIRA"`, `"Handle It"`, `"Confirm"`).
2. **Cloud Full-Duplex Streaming Mode (Conversational AI)**:
   * Engine: Bidirectional WebRTC / WebSocket audio streaming (Gemini Live / ElevenLabs / OpenAI Realtime).
   * Live Voice Interruption: Instantly stops speaker playback when the user starts speaking.
