# JARVIS OS — Kernel & Native Architecture Map

This document defines the real execution architecture of **JARVIS OS**, mapping the machine primitives, kernel subsystems, and userspace service boundaries derived from the C++ OS foundation.

---

## 1. Boot Entry & Initialization Pipeline

```
[UEFI / BIOS Firmware]
         │
         ▼
[Prekernel: Kernel/Prekernel/] (Sets up 64-bit long mode, paging, relocations)
         │
         ▼
[init(): Kernel/Arch/init.cpp] (Early CPU setup, kmalloc_init(), MemoryManager, ACPI)
         │
         ▼
[init_stage2(): Kernel/Arch/init.cpp] (PCI bus, VirtIO, GPU, Audio, Ext2FS root mount)
         │
         ▼
[First Userspace Process: /init] (Mounts ProcFS, SysFS, DevPtsFS, spawns SystemServer)
         │
         ▼
[SystemServer: Userland/Services/SystemServer/] (Launches WindowServer, Taskbar, Services)
```

---

## 2. Kernel Subsystems Directory Mapping

| Subsystem | Source Path | Description |
| :--- | :--- | :--- |
| **Boot & CPU Init** | `Kernel/Arch/init.cpp` | Early processor initialization, scheduler activation, and device probing. |
| **Scheduler & Tasks** | `Kernel/Tasks/` | Preemptive priority scheduler (`Scheduler.cpp`), `Process.cpp`, `Thread.cpp`. |
| **Memory Management** | `Kernel/Memory/` | Virtual memory (`MemoryManager.cpp`), `PageDirectory.cpp`, `AddressSpace.cpp`, anonymous/file-backed `Region.cpp`. |
| **Syscall Dispatcher** | `Kernel/Syscalls/` | Kernel boundary executing POSIX and custom system calls (e.g. `sys$uname`, `sys$pledge`, `sys$unveil`). |
| **Virtual Filesystem** | `Kernel/FileSystem/` | VFS layer multiplexing `Ext2FS`, `ProcFS`, `SysFS`, `DevPtsFS`, and `RAMFS`. |
| **Device Model** | `Kernel/Devices/` | Generic devices, TTY (`PTYMultiplexer.cpp`), GPU (`Console/`, `GPU/`), Storage (`AHCI`, `NVMe`, `IDE`). |
| **Networking** | `Kernel/Net/` | Loopback, E1000, VirtIO-Net, TCP/IP stack, and socket layers. |

---

## 3. Userspace Service Architecture

```
                      ┌─────────────────────────────────┐
                      │          SystemServer           │
                      └────────────────┬────────────────┘
                                       │ spawns
         ┌─────────────────────────────┼─────────────────────────────┐
         │                             │                             │
         ▼                             ▼                             ▼
┌──────────────────┐          ┌──────────────────┐          ┌──────────────────┐
│   WindowServer   │          │  JarvisService   │          │  JournalService  │
│ (GUI Compositor) │          │(Capability IPC)  │          │ (SHA-256 Audit)  │
└────────┬─────────┘          └────────┬─────────┘          └────────┬─────────┘
         │                             │                             │
         ▼                             ▼                             ▼
   LibGUI Apps                  Policy Evaluation             Machine Evidence
(About, Terminal,              (Permission Gates &           (Append-Only Log
 JarvisAssistant)               POSIX Execution)              State Hashing)
```

---

## 4. Security & Isolation Boundary
* **Pledge (`sys$pledge`)**: Restricts the process to explicit syscall categories (`stdio`, `rpath`, `wpath`, `cpath`, `unix`, `inet`).
* **Unveil (`sys$unveil`)**: Restricts filesystem visibility to whitelisted directory subtrees.
* **Deterministic Native Capabilities**: The AI reasoning layer only issues requests across the typed `JarvisServer.ipc` boundary. The OS kernel and `PolicyGate` retain absolute authority.
