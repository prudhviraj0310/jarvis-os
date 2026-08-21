# Capability Blueprint: Email & Inbox Intelligence

- **Inspired by**: `dev-core-busy/jarvis` (IMAP Mail Runner), `kar-ganap/jarvis` (Gmail API Tools), `Friday` (Specialist Mail Agent)

---

## 1. Core Architecture
Decoupled polling and real-time push synchronization using standard IMAP/IDLE or Gmail OAuth API.

```
IMAP / Gmail API (OAuth2 / App Password in Encrypted Vault)
       ↓
Background Mail Runner (Periodic / IDLE Push)
       ↓
Header & Body Extractor (HTML to Clean Markdown)
       ↓
Inbox Priority Classifier:
   ├── Actionable Deliverables (Professors, Dean, Capstone Reviews)
   ├── Calendar Event Invites (Auto-extracted to Agenda)
   └── Newsletters & Automated Bulletins (Summarized in Daily Digest)
       ↓
Context Engine & Daily Briefing Injector
```

---

## 2. Response Drafting & Safety Gate
* For actionable emails (e.g. from faculty), the system drafts formal, respectful responses aligned with academic standards and registers them as `ConfirmRequired` actions in the `PolicyGate`.
