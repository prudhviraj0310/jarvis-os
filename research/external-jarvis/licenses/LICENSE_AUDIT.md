# JARVIS OS — Open-Source License Compliance Audit

This audit evaluates the legal and licensing terms of all surveyed repositories before any architectural ideas or components are adapted.

---

## 📋 Comprehensive Audit Table

| Repository | Primary License | Copyright Holder | Commercial Use Permitted? | Attribution Required? | Source Disclosure Required? | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`dev-core-busy/jarvis`** | Apache 2.0 | dev-core-busy Contributors | Yes | Yes (NOTICE file) | No (Permissive) | ✅ **APPROVED (Attribution Needed)** |
| **`kar-ganap/jarvis`** | MIT License | Kartik Ganapathi (2026) | Yes | Yes (Copyright notice) | No (Permissive) | ✅ **APPROVED** |
| **`yashvar23/jarvis`** | RSALv2-based Source Available | Yash Varshney (2026) | **RESTRICTED** | Yes | Yes | ⚠️ **`LICENSE_REVIEW_REQUIRED` (Do not copy code; study architecture only)** |
| **`Raghava001-web/Jarvis`**| MIT License | JARVIS AI Assistant (2026) | Yes | Yes (Copyright notice) | No (Permissive) | ✅ **APPROVED** |
| **`LakshyaBadjatya/Friday`**| MIT License | Lakshya Badjatya (2026) | Yes | Yes (Copyright notice) | No (Permissive) | ✅ **APPROVED** |
| **`ambartsumov/jarvis-agent`**| MIT License | Jarvis Agent Contributors (2026) | Yes | Yes (Copyright notice) | No (Permissive) | ✅ **APPROVED** |

---

## 🔒 Policy on Code Reuse
1. **Permissive Repositories (MIT / Apache 2.0)**: Architectural concepts, protocol wrappers, and schema structures can be adapted into our native C++ / Wayland stack with proper attribution in `Documentation/THIRD_PARTY_NOTICES.md`.
2. **Restricted Repositories (`yashvar23/jarvis` - RSALv2)**: **Strictly forbidden** from copying any raw code or files. We only study the architectural patterns (e.g. sidecar IPC model, authority matrix) and create our own clean-room native implementations from scratch.
