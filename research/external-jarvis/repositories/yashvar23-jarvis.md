# Research Inspection: yashvar23 / jarvis

- **Repository URL**: `https://github.com/yashvar23/jarvis`
- **Primary License**: Jarvis Source Available License 2.0 (RSALv2 based) — `LICENSE_REVIEW_REQUIRED`
- **Primary Languages**: TypeScript / Bun / Node.js, Go (Sidecar agent), Rust
- **Primary Frameworks**: Bun, React / Electron (UI), Go `robotgo` / native desktop APIs

---

## 1. System Architecture
`yashvar23/jarvis` implements an advanced distributed assistant architecture:
* **Always-On Central Brain (`src/daemon/`)**: Bun-powered master daemon managing goals, roles, active workflows, and long-term memory.
* **Native Sidecar Subsystem (`sidecar/`)**: Native Go agent running on client machines (`desktop_linux.go`, `desktop_darwin.go`, `desktop_windows.go`) that executes local OS actions and observes the desktop.
* **Authority & Approval Matrix (`src/authority/`)**: Explicit permission system categorizing actions into Read-Only, Safe, and Consequential (requiring user approval).
* **Desktop Awareness (`src/awareness/`)**: Screen capture, active window monitoring, and OCR pipeline.
* **Emergency Kill Switch & Audit (`src/authority/audit.ts`)**: Real-time action audit trail with pause/kill capability.

---

## 2. Major Capabilities
1. **Sidecar Client-Server Model**: The central LLM brain can orchestrate multiple physical/virtual machines through lightweight Go sidecars.
2. **Desktop Awareness & OCR**: Continuously tracks which application is focused, parses visible text, and detects user context switches.
3. **Multi-Agent Role Pursuit (`src/roles/`, `src/goals/`)**: Decomposes long-term goals into background task threads.
4. **Approval & Audit Trail**: Real-time permission gate intercepting dangerous OS actions.

---

## 3. Entry Points & Key Modules
* **Daemon**: `bin/jarvis`, `src/daemon/index.ts`.
* **Go Sidecar**: `sidecar/main.go`, `sidecar/client.go`, `sidecar/desktop_linux.go`.
* **Authority Engine**: `src/authority/authority.ts`, `src/authority/policy.ts`.
* **UI**: `ui/` (Electron / Web ambient assistant).

---

## 4. Dependencies
* `bun`, `typescript`, `electron`, `react`
* Go: `github.com/go-vgo/robotgo`, `github.com/kbinani/screenshot`, `golang.org/x/sys`

---

## 5. Security & Machine Sovereignty Analysis
* **Strong Alignment with JARVIS OS**: Yashvar's `src/authority/` matches our core principle: "The model proposes; the authority engine decides."
* **Audit Trail**: Every sidecar command invocation generates a signed record.

---

## 6. What Can Be Adapted to JARVIS OS
* **Sidecar Architecture**: A lightweight native C++/Go sidecar communicating with our microkernel/Wayland compositor via Unix domain sockets.
* **Screen Observation & Active Window Awareness**: Tracking active window titles and desktop state to inform the context engine.

---

## 7. What is NOT Suitable
* Monolithic Bun runtime inside the kernel — Sidecar must be native C++/Rust.

---

## 8. License Compliance & Warning
* **`LICENSE_REVIEW_REQUIRED`**: Uses a proprietary source-available license (RSALv2). **DO NOT copy source code directly.** Only extract and reimplement architectural ideas independently.
