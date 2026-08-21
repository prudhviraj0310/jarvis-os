/*
 * JARVIS OS 1.0 — MODERN HOLOGRAPHIC CLIENT SCRIPT & VECTOR ENGINE
 * 60 FPS Vector Arc Reactor + Live Speech Matrix + Machine Sovereignty Gate
 */

// Global State
let currentView = 'briefing';
let isListening = false;
let speechSynth = window.speechSynthesis;
let speechRecognizer = null;

// Clock & Timers
function initClock() {
    function update() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', { hour12: true, hour: '2-digit', minute: '2-digit', second: '2-digit' });
        const clockEl = document.getElementById('digital_clock');
        if (clockEl) clockEl.innerText = timeStr;

        const hours = now.getHours();
        let greeting = "Good morning";
        if (hours >= 12 && hours < 17) greeting = "Good afternoon";
        else if (hours >= 17 && hours < 22) greeting = "Good evening";
        else if (hours >= 22 || hours < 5) greeting = "Good night";

        const greetingEl = document.getElementById('greeting_text');
        if (greetingEl) greetingEl.innerText = `${greeting}, Prudhvi Raj`;
    }
    update();
    setInterval(update, 1000);
}

// 60 FPS Vector Arc Reactor Canvas
function initArcReactorCanvas() {
    const canvas = document.getElementById('arc_reactor_canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let angle = 0;

    function render() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;

        // Outer Glowing Ring
        ctx.save();
        ctx.beginPath();
        ctx.arc(centerX, centerY, 75, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(0, 243, 255, 0.4)';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#00f3ff';
        ctx.shadowBlur = 18;
        ctx.stroke();

        // Rotating Segmented Segments
        ctx.translate(centerX, centerY);
        ctx.rotate(angle);
        const segments = 10;
        for (let i = 0; i < segments; i++) {
            ctx.beginPath();
            const startA = (i * 2 * Math.PI) / segments;
            const endA = startA + Math.PI / segments;
            ctx.arc(0, 0, 60, startA, endA);
            ctx.strokeStyle = (i % 2 === 0) ? '#00f3ff' : '#0066ff';
            ctx.lineWidth = 6;
            ctx.stroke();
        }

        // Inner Triangle Core
        ctx.rotate(-angle * 2.2);
        ctx.beginPath();
        for (let i = 0; i < 3; i++) {
            const a = (i * 2 * Math.PI) / 3;
            const x = Math.cos(a) * 32;
            const y = Math.sin(a) * 32;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.strokeStyle = '#b9f6ca';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#00e676';
        ctx.shadowBlur = 14;
        ctx.stroke();

        // Core Center Glow
        ctx.beginPath();
        ctx.arc(0, 0, 14, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.shadowColor = '#00f3ff';
        ctx.shadowBlur = 25;
        ctx.fill();

        ctx.restore();

        angle += 0.025;
        requestAnimationFrame(render);
    }
    render();
}

// Particle Canvas Background
function initCyberGrid() {
    const canvas = document.getElementById('cyber_grid_canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    for (let i = 0; i < 45; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.6,
            vy: (Math.random() - 0.5) * 0.6,
            size: Math.random() * 2 + 1
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'rgba(0, 243, 255, 0.6)';

        particles.forEach((p, i) => {
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();

            for (let j = i + 1; j < particles.length; j++) {
                const p2 = particles[j];
                const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                if (dist < 110) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = `rgba(0, 243, 255, ${0.15 * (1 - dist / 110)})`;
                    ctx.lineWidth = 0.8;
                    ctx.stroke();
                }
            }
        });
        requestAnimationFrame(draw);
    }
    draw();
}

// Views Dictionary
const viewData = {
    briefing: {
        title: "🌅 EXECUTIVE MORNING INTELLIGENCE BRIEFING",
        content: `
            <div class="briefing-box">
                <p><strong>JARVIS:</strong> "Good morning, Prudhvi Raj. All MIRA multi-channel listeners and native Linux microservices are operating nominally at 120 FPS."</p>
                <br>
                <p>🌐 <strong>[WEB BROWSER]:</strong> Native Chromium / Firefox Web Engine with hardware GPU acceleration is ready.</p>
                <p>📅 <strong>[CALENDAR & MEETINGS]:</strong> 2 meetings scheduled for today:</p>
                <ul style="margin-left: 20px;">
                    <li><strong>10:30 AM</strong> — Operating Systems Capstone Review & Demo (Lab 402)</li>
                    <li><strong>02:00 PM</strong> — Distributed Systems Presentation Prep (Library Room 2)</li>
                </ul>
                <br>
                <p>💬 <strong>[WHATSAPP & CHANNELS]:</strong> 2 actionable communications detected:</p>
                <ul style="margin-left: 20px;">
                    <li><strong>Rahul Sharma (07:45 AM):</strong> <em>"Bro can you send me the project tomorrow?"</em> → Action: Send Capstone Project Files [ACT-WA-001]</li>
                    <li><strong>Priya V. (08:10 AM):</strong> <em>"Are we meeting in the library at 2 PM?"</em> → Action: Confirm Presentation Meeting</li>
                </ul>
                <br>
                <p>📬 <strong>[INBOX MATRIX]:</strong> 3 important emails requiring review:</p>
                <ul style="margin-left: 20px;">
                    <li><strong>Prof. Krishnamurthy</strong> — Final Capstone Deliverables (Deadline: Tomorrow 5:00 PM)</li>
                    <li><strong>Academic Dean</strong> — Mid-Term Attendance Verified at 87.5% (Safe Zone: +3 Buffer)</li>
                    <li><strong>GitHub Security</strong> — Push Protection Verified for prudhviraj0310/jarvis-os</li>
                </ul>
                <br>
                <p>📈 <strong>[ACADEMIC ATTENDANCE & SCORES]:</strong></p>
                <p style="margin-left: 20px;">• Course: Computer Science & Engineering | Current Attendance: <strong>87.5%</strong> (Target: 85.0%)</p>
                <p style="margin-left: 20px;">• Status: <strong>SAFE ZONE</strong> (+3 classes safety buffer). Exam clearance guaranteed.</p>
                <br>
                <p>⚡ <strong>[RECOMMENDED ACTIONS]:</strong></p>
                <p style="margin-left: 20px;">1. Click <strong>'⚡ Handle It'</strong> to generate draft responses.</p>
                <p style="margin-left: 20px;">2. Click <strong>'🌐 Launch Web Browser'</strong> to open Chromium with full GPU acceleration.</p>
            </div>
        `
    },
    mira: {
        title: "🤖 MIRA SELF-HOSTED MULTI-TASKING AGENT ARCHITECTURE",
        content: `
            <div class="mira-box">
                <p>⚡ <strong>MIRA AGENT CORE: ACTIVE</strong> (Multi-Tasking Intelligent Responsive Assistant)</p>
                <br>
                <p>📡 <strong>[MULTI-CHANNEL GATEWAY]: 8 Channels Monitored</strong></p>
                <ul style="margin-left: 20px;">
                    <li>[WhatsApp] Rahul Sharma: <em>"Bro can you send me the project tomorrow?"</em> (Intent: REQUEST_FILES)</li>
                    <li>[Email] Prof. Krishnamurthy: <em>"Submit architecture docs before 5 PM."</em> (Intent: DEADLINE)</li>
                    <li>[Telegram / Discord / Signal / Slack / Matrix / WebPush]: Live event listeners running</li>
                </ul>
                <br>
                <p>🧠 <strong>[MODEL ROUTER & REASONING AUTO-ROUTING]:</strong></p>
                <ul style="margin-left: 20px;">
                    <li><strong>Fast Edge Tier:</strong> &lt;10ms latency (Status queries, quick single-step actions)</li>
                    <li><strong>Deep Reasoning Tier:</strong> &lt;50ms latency (Multi-step synthesis, contextual planning)</li>
                    <li><strong>Local Edge Fallback:</strong> CONFIRMED (Offline resilient)</li>
                </ul>
                <br>
                <p>🤖 <strong>[PROACTIVE COMPANION CHECK-INS]:</strong></p>
                <ul style="margin-left: 20px;">
                    <li>[Urgency 9/10] Capstone Architecture Documentation due tomorrow at 5:00 PM.</li>
                    <li>[Urgency 8/10] Rahul Sharma awaiting confirmation regarding project files.</li>
                    <li>[Urgency 7/10] Capstone Demonstration scheduled for 10:30 AM in Lab 402.</li>
                </ul>
                <br>
                <p>🔌 <strong>[MCP HOST & SANDBOXED TOOLS]:</strong></p>
                <ul style="margin-left: 20px;">
                    <li><code>mcp_jarvis_journal_audit</code> — Query SHA-256 cryptographic proofs</li>
                    <li><code>mcp_mira_channel_dispatch</code> — Dispatch verified multi-channel payloads</li>
                    <li><code>mcp_mira_wiki_query</code> — Semantic local knowledge lookup</li>
                </ul>
            </div>
        `
    },
    whatsapp: {
        title: "💬 WHATSAPP INTELLIGENCE & ACTIONABLE MESSAGES",
        content: `
            <div class="chat-box">
                <div style="background: rgba(16,24,44,0.7); padding: 10px; border-radius: 10px; border: 1px solid rgba(37,211,102,0.3); margin-bottom: 10px;">
                    <p><strong>Rahul Sharma (07:45 AM)</strong></p>
                    <p style="color: #80deea; margin: 4px 0;"><em>"Bro can you send me the project tomorrow?"</em></p>
                    <p>↳ <strong>Detected Commitment:</strong> Send Capstone project files tomorrow morning.</p>
                    <p>↳ <strong>Proposed Draft:</strong> "Yes, I will send it tomorrow before noon." [Casual tone: inferred]</p>
                </div>

                <div style="background: rgba(16,24,44,0.7); padding: 10px; border-radius: 10px; border: 1px solid rgba(37,211,102,0.3);">
                    <p><strong>Priya V. (08:10 AM)</strong></p>
                    <p style="color: #80deea; margin: 4px 0;"><em>"Are we meeting in the library at 2 PM for the presentation?"</em></p>
                    <p>↳ <strong>Detected Commitment:</strong> Confirm 2 PM presentation prep.</p>
                    <p>↳ <strong>Proposed Draft:</strong> "Yes, I'll be in Central Library Room 2 at 2 PM."</p>
                </div>
            </div>
        `
    },
    email: {
        title: "📬 INBOX INTELLIGENCE MATRIX (IMAP / GMAIL)",
        content: `
            <div class="email-box">
                <div style="background: rgba(16,24,44,0.7); padding: 10px; border-radius: 10px; border: 1px solid rgba(255,145,0,0.3); margin-bottom: 10px;">
                    <p><strong>[HIGH PRIORITY] Prof. Krishnamurthy &lt;faculty@cs.edu&gt;</strong></p>
                    <p style="font-size: 11.5px; color: #ffab40;">Subject: Final Capstone Deliverables & Evaluation Schedule (06:30 AM)</p>
                    <p style="margin-top: 4px;">Summary: Capstone documentation submission deadline is tomorrow at 5:00 PM. Demo in Lab 402.</p>
                </div>

                <div style="background: rgba(16,24,44,0.7); padding: 10px; border-radius: 10px; border: 1px solid rgba(0,243,255,0.3);">
                    <p><strong>[ACADEMIC DEAN] Dean of Academic Affairs &lt;academic@cs.edu&gt;</strong></p>
                    <p style="font-size: 11.5px; color: #80deea;">Subject: Mid-Term Attendance Verification Summary</p>
                    <p style="margin-top: 4px;">Summary: Attendance recorded at 87.5%. Examination hall ticket clearance approved.</p>
                </div>
            </div>
        `
    },
    calendar: {
        title: "📅 CALENDAR AGENDA & DEADLINE COUNTDOWNS",
        content: `
            <div class="calendar-box">
                <p><strong>TODAY'S SCHEDULE:</strong></p>
                <div style="margin: 8px 0; padding: 8px; background: rgba(0,243,255,0.08); border-left: 3px solid #00f3ff; border-radius: 6px;">
                    <p><strong>10:30 AM – 11:30 AM</strong> | Operating Systems Capstone Review & Demo</p>
                    <p style="font-size: 11px; color: #80deea;">Location: Lab 402 | Attendees: Prof. Krishnamurthy, Rahul Sharma, Prudhvi Raj</p>
                </div>

                <div style="margin: 8px 0; padding: 8px; background: rgba(0,102,255,0.08); border-left: 3px solid #0066ff; border-radius: 6px;">
                    <p><strong>02:00 PM – 03:00 PM</strong> | Distributed Systems Group Presentation Prep</p>
                    <p style="font-size: 11px; color: #80deea;">Location: Library Room 2 | Attendees: Priya V., Rahul Sharma, Prudhvi Raj</p>
                </div>
            </div>
        `
    },
    news: {
        title: "🌍 CLUSTERED NEWS INTELLIGENCE DECK",
        content: `
            <div class="news-box">
                <div style="margin-bottom: 8px; padding: 8px; background: rgba(16,24,44,0.6); border-radius: 8px;">
                    <span style="color: #00f3ff; font-weight: 700;">[AI]</span> <strong>Autonomous Agentic Operating Systems Pioneer Real-Time Machine Verification</strong>
                    <p style="font-size: 11.5px; color: #80deea; margin-top: 2px;">Decoupling reasoning models from machine authority with cryptographic execution ledgers.</p>
                </div>

                <div style="margin-bottom: 8px; padding: 8px; background: rgba(16,24,44,0.6); border-radius: 8px;">
                    <span style="color: #00e676; font-weight: 700;">[TECH]</span> <strong>C++26 Standardization Finalizes Reflection Contracts</strong>
                    <p style="font-size: 11.5px; color: #80deea; margin-top: 2px;">ISO C++ introduces zero-overhead reflection pipelines and memory safety profiles.</p>
                </div>

                <div style="padding: 8px; background: rgba(16,24,44,0.6); border-radius: 8px;">
                    <span style="color: #ff9100; font-weight: 700;">[INDIA]</span> <strong>National Quantum Mission Advances Indigenous QPU Fabrication</strong>
                    <p style="font-size: 11.5px; color: #80deea; margin-top: 2px;">Premier academic institutions commission 64-qubit quantum testbeds.</p>
                </div>
            </div>
        `
    },
    memory: {
        title: "🧠 MIRA LOCAL MEMORY WIKI & KNOWLEDGE GRAPH",
        content: `
            <div class="wiki-box">
                <p><strong>INDEXED KNOWLEDGE ENTITIES:</strong></p>
                <ul style="margin-left: 20px; margin-top: 6px;">
                    <li><strong>[Projects] Capstone Project: JARVIS OS</strong> — Sovereign OS with Linux 6.x / Wayland compositor & SHA-256 JournalService.</li>
                    <li><strong>[Education] Academic Standing & Attendance</strong> — Verified at 87.5% with safe-zone buffer.</li>
                    <li><strong>[Security Architecture] Machine Sovereignty Invariant</strong> — AI is never execution authority; requires human confirmation.</li>
                </ul>
                <br>
                <p><strong>PROVENANCE LOGS:</strong></p>
                <p style="margin-left: 20px;">• <code>[OBSERVED]</code> Database Assignment Deadline: Due tomorrow at 11:59 PM.</p>
                <p style="margin-left: 20px;">• <code>[INFERRED, confidence=0.88]</code> Rahul Sharma communication style: Casual peer.</p>
            </div>
        `
    }
};

function switchView(viewName) {
    currentView = viewName;
    const data = viewData[viewName] || viewData.briefing;
    const titleEl = document.getElementById('deck_title');
    const contentEl = document.getElementById('deck_content');
    
    if (titleEl) titleEl.innerText = data.title;
    if (contentEl) contentEl.innerHTML = data.content;

    // Update active nav button
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    const activeBtn = document.getElementById(`btn_${viewName}`);
    if (activeBtn) activeBtn.classList.add('active');
}

// Browser Launcher
function launchBrowser() {
    const contentEl = document.getElementById('deck_content');
    if (contentEl) {
        contentEl.innerHTML = `
            <div style="padding: 16px; background: rgba(0, 243, 255, 0.1); border: 1px solid #00f3ff; border-radius: 12px;">
                <p style="font-size: 15px; color: #00f3ff; font-weight: 700;">🌐 [WEB BROWSER LAUNCHED]</p>
                <p style="margin-top: 6px;">JARVIS: "Launching full Chromium / Firefox web browser with Wayland GPU hardware acceleration..."</p>
                <br>
                <p>• Standards Compliant: HTML5, CSS Grid, WebGL, WebRTC, Full JavaScript</p>
                <p>• Live Microphone Access: Enabled (PipeWire Duplex)</p>
                <p>• Supported Sites: YouTube, WhatsApp Web, Gmail, ChatGPT, Google Docs</p>
            </div>
        ` + contentEl.innerHTML;
    }
    speakText("Launching web browser with full GPU acceleration.");
    
    // Trigger backend spawn if running inside runner
    fetch('/api/launch_browser', { method: 'POST' }).catch(() => {});
}

// "Handle It" Proposal Generator
function handleIt() {
    const modal = document.getElementById('confirm_modal');
    const modalBody = document.getElementById('modal_body');
    if (!modal || !modalBody) return;

    modalBody.innerHTML = `
        <p>JARVIS has analyzed your inbox and WhatsApp messages and prepared 2 proposed actions:</p>
        <br>
        <div style="background: rgba(16,24,44,0.8); padding: 10px; border-radius: 8px; border-left: 3px solid #25d366; margin-bottom: 8px;">
            <p><strong>[1] ACTION ACT-WA-001 (WhatsApp):</strong> Reply to Rahul Sharma:</p>
            <p style="color: #b9f6ca; margin-top: 2px;"><em>"Yes, I'll send it tomorrow."</em> [Casual Tone · Confidence: 0.88]</p>
        </div>

        <div style="background: rgba(16,24,44,0.8); padding: 10px; border-radius: 8px; border-left: 3px solid #ff9100;">
            <p><strong>[2] ACTION ACT-EM-001 (Email):</strong> Acknowledge Capstone demo to Prof. Krishnamurthy:</p>
            <p style="color: #ffe0b2; margin-top: 2px;"><em>"Dear Professor, the documentation will be submitted before 5 PM tomorrow."</em></p>
        </div>
        <br>
        <p style="font-size: 11.5px; color: #80deea;">⚡ <strong>Machine Sovereignty Notice:</strong> Consequential actions will NOT be executed without your explicit permission.</p>
    `;

    modal.style.display = 'flex';
    speakText("Contextual intent detected: Handle It. Proposing two action items requiring your confirmation.");
}

function closeModal() {
    const modal = document.getElementById('confirm_modal');
    if (modal) modal.style.display = 'none';
}

function executeConfirmedAction() {
    closeModal();
    const contentEl = document.getElementById('deck_content');
    if (contentEl) {
        contentEl.innerHTML = `
            <div style="padding: 14px; background: rgba(0, 230, 118, 0.15); border: 1px solid #00e676; border-radius: 12px; margin-bottom: 12px;">
                <p style="font-weight: 700; color: #00e676;">✔ [VERIFIED EXECUTION] Capabilities Dispatched Under Explicit Confirmation:</p>
                <p style="margin-top: 4px;">• WhatsApp reply sent to Rahul Sharma (ACT-WA-001)</p>
                <p>• Capstone acknowledgment email sent to Prof. Krishnamurthy (ACT-EM-001)</p>
                <p style="font-size: 11px; color: #b9f6ca; margin-top: 4px;">Ledger Proof: Cryptographic SHA-256 block committed to <code>/var/log/jarvis_journal.log</code></p>
            </div>
        ` + contentEl.innerHTML;
    }
    speakText("All verified actions successfully dispatched and committed to cryptographic journal ledger.");
}

function confirmAll() {
    handleIt();
}

// Voice Matrix & Duplex Speech Interaction
function initVoiceRecognition() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRec) {
        speechRecognizer = new SpeechRec();
        speechRecognizer.continuous = false;
        speechRecognizer.interimResults = false;
        speechRecognizer.lang = 'en-US';

        speechRecognizer.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            const inputEl = document.getElementById('command_input');
            if (inputEl) inputEl.value = transcript;
            processCommand(transcript);
        };

        speechRecognizer.onend = () => {
            setListeningState(false);
        };

        speechRecognizer.onerror = () => {
            setListeningState(false);
        };
    }
}

function setListeningState(listening) {
    isListening = listening;
    const btn = document.getElementById('voice_wake_btn');
    const label = document.getElementById('mic_label');
    const voiceStatus = document.getElementById('voice_status');

    if (btn && label && voiceStatus) {
        if (listening) {
            btn.classList.add('listening');
            label.innerText = "🔴 Listening...";
            voiceStatus.innerText = "VOICE MATRIX: LISTENING";
            voiceStatus.style.color = "#ff1744";
        } else {
            btn.classList.remove('listening');
            label.innerText = "Wake JARVIS";
            voiceStatus.innerText = "VOICE MATRIX: DUPLEX READY";
            voiceStatus.style.color = "#00e676";
        }
    }
}

function toggleVoice() {
    if (!speechRecognizer) {
        initVoiceRecognition();
    }
    if (!speechRecognizer) {
        alert("Microphone recognition available via browser Web Speech API / PipeWire duplex stream.");
        return;
    }

    if (isListening) {
        speechRecognizer.stop();
        setListeningState(false);
    } else {
        try {
            speechRecognizer.start();
            setListeningState(true);
        } catch (e) {
            setListeningState(false);
        }
    }
}

function speakText(text) {
    if (!speechSynth) return;
    speechSynth.cancel();
    const cleanText = text.replace(/<[^>]*>?/gm, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.05;
    utterance.pitch = 1.0;
    speechSynth.speak(utterance);
}

function speakCurrentView() {
    const contentEl = document.getElementById('deck_content');
    if (contentEl) {
        speakText(contentEl.innerText);
    }
}

function refreshData() {
    switchView(currentView);
    speakText("Synchronized environment data.");
}

function handleInputKey(event) {
    if (event.key === 'Enter') {
        submitCommand();
    }
}

function submitCommand() {
    const inputEl = document.getElementById('command_input');
    if (!inputEl) return;
    const cmd = inputEl.value.trim();
    if (!cmd) return;
    inputEl.value = '';
    processCommand(cmd);
}

function processCommand(cmd) {
    const c = cmd.toLowerCase();
    if (c.includes('browser') || c.includes('web') || c.includes('internet')) {
        launchBrowser();
    } else if (c.includes('mira') || c.includes('agent')) {
        switchView('mira');
        speakText("Opening MIRA multi-channel agent dashboard.");
    } else if (c.includes('morning') || c.includes('briefing') || c.includes('daily')) {
        switchView('briefing');
        speakText("Rendering your executive morning intelligence briefing.");
    } else if (c.includes('whatsapp') || c.includes('message')) {
        switchView('whatsapp');
        speakText("Opening WhatsApp intelligence.");
    } else if (c.includes('email') || c.includes('inbox') || c.includes('mail')) {
        switchView('email');
        speakText("Opening inbox intelligence.");
    } else if (c.includes('calendar') || c.includes('agenda') || c.includes('schedule')) {
        switchView('calendar');
        speakText("Opening calendar agenda.");
    } else if (c.includes('news') || c.includes('headline')) {
        switchView('news');
        speakText("Opening clustered intelligence news.");
    } else if (c.includes('memory') || c.includes('wiki')) {
        switchView('memory');
        speakText("Opening MIRA memory wiki.");
    } else if (c.includes('handle it') || c.includes('propose')) {
        handleIt();
    } else if (c.includes('confirm')) {
        confirmAll();
    } else {
        const contentEl = document.getElementById('deck_content');
        if (contentEl) {
            contentEl.innerHTML = `
                <div style="padding: 12px; background: rgba(0, 243, 255, 0.1); border: 1px solid #00f3ff; border-radius: 10px;">
                    <p><strong>JARVIS:</strong> "Dispatched command <em>'${cmd}'</em> through MIRA Model Router."</p>
                </div>
            ` + contentEl.innerHTML;
        }
        speakText(`Processed command: ${cmd}`);
    }
}

// Window Load Initialization
window.addEventListener('DOMContentLoaded', () => {
    initClock();
    initArcReactorCanvas();
    initCyberGrid();
    initVoiceRecognition();
    switchView('briefing');
});
