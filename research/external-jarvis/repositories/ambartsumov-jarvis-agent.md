# Research Inspection: ambartsumov / jarvis-agent

- **Repository URL**: `https://github.com/ambartsumov/jarvis-agent`
- **Primary License**: MIT License
- **Primary Languages**: Python 3.11+, JavaScript
- **Primary Frameworks**: Telethon (Telegram MTProto), OpenClaw, OpenManus, Vosk (Offline STT), MCP (Model Context Protocol)

---

## 1. System Architecture
`ambartsumov/jarvis-agent` specializes in bridging multiple independent open-source agent ecosystems (OpenClaw, OpenManus) into a unified personal agent:
* **Multi-Agent Bridge (`openclaw-plugin/`, `pds_ultimate/`)**: Dispatches complex web browsing and OS tasks to OpenClaw and OpenManus workers.
* **Offline Voice Engine (`vosk/`)**: Zero-network-latency, zero-cloud offline speech-to-text using local Vosk small-en models.
* **Security Guardrails & PII Filter (`pds_ultimate/guardrails.py`, `pii_filter.py`)**: Sanitizes prompt injection attacks and masks sensitive personal data (passwords, credit cards, phone numbers) before sending prompts to external LLMs.
* **Communication Bridges**: Telethon MTProto Telegram daemon and Baileys WhatsApp integration.

---

## 2. Major Capabilities
1. **Offline Voice STT (Vosk)**: Allows voice commands to work 100% offline without sending audio to Google/OpenAI.
2. **PII Masking & Prompt Injection Defense**: Real-time regex and embedding filters that scrub personal identifiers from model contexts.
3. **OpenClaw Desktop & Browser Automation**: Deep browser and desktop control plugin.
4. **MCP Tool Bus**: Interoperates with external tools via standard JSON-RPC Model Context Protocol.

---

## 3. Entry Points & Key Modules
* **Agent Entry**: `start_agent.sh`, `pds_ultimate/main.py`.
* **Vosk Voice Server**: `vosk/voice_server.py`.
* **OpenClaw Plugin**: `openclaw-plugin/index.js`.
* **Security & Guardrails**: `pds_ultimate/guardrails.py`.

---

## 4. Dependencies
* `telethon`, `vosk`, `sounddevice`, `numpy`, `fastapi`, `pydantic`, `mcp-client`

---

## 5. Security & Machine Sovereignty Analysis
* **High Privacy Posture**: Strong emphasis on offline-first voice and PII scrubbing.

---

## 6. What Can Be Adapted to JARVIS OS
* **Vosk Offline STT Pipeline**: Extremely fast, lightweight local voice recognition running as a native C/Python microservice on PipeWire/ALSA.
* **PII & Prompt Injection Defense Filter**: Pre-dispatch sanitizer running before any capability prompt leaves the local device.

---

## 7. What is NOT Suitable
* Telethon session files stored unencrypted on disk — Must be stored in our cryptographic vault.

---

## 8. License Compliance
* **MIT License**: Fully permissive for commercial use and modification with attribution.
