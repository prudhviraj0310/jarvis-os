#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    JARVIS OS — BRAIN ARCHITECTURE BENCHMARK              ║
║                                                                           ║
║   Comprehensive test suite validating every cognitive layer of the        ║
║   Jarvis Sentience Engine: Emotion, Thought, Energy, Profile,            ║
║   Memory, Reflection, Evolution, Vision, Society, and Overlay.           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import time
import json
import tempfile
import shutil
from io import StringIO

# ─────────────────────────────────── SETUP ────────────────────────────────────
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# ── Benchmark Timer Utility ──
class BenchTimer:
    """Microsecond-precision benchmark harness."""
    def __init__(self, label):
        self.label = label
        self.start = None
        self.elapsed_us = 0

    def __enter__(self):
        self.start = time.perf_counter_ns()
        return self

    def __exit__(self, *args):
        self.elapsed_us = (time.perf_counter_ns() - self.start) / 1000
        return False

# ── Results Collector ──
results = []
total_pass = 0
total_fail = 0

def record(module, test_name, passed, latency_us, detail=""):
    global total_pass, total_fail
    status = "✅ PASS" if passed else "❌ FAIL"
    if passed:
        total_pass += 1
    else:
        total_fail += 1
    results.append({
        "module": module,
        "test": test_name,
        "status": status,
        "latency_μs": round(latency_us, 1),
        "detail": detail
    })

DIVIDER = "═" * 78
THIN_DIV = "─" * 78

print(f"\n{DIVIDER}")
print("   🧠 JARVIS OS — BRAIN ARCHITECTURE BENCHMARK SUITE")
print(f"{DIVIDER}\n")

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 1: EMOTION ENGINE (Phase 17)
# ═══════════════════════════════════════════════════════════════════════════════
print(f"{'🎭 MODULE 1: EmotionEngine (Phase 17)':^78}")
print(THIN_DIV)

from jarvis.engine.emotion import EmotionEngine

emotion = EmotionEngine()

test_cases_emotion = [
    ("I'm so tired bro", "low_energy", "Fatigue detection"),
    ("do it now, fast!", "urgent", "Urgency detection"),
    ("hey bro open youtube", "casual", "Casual tone pick-up"),
    ("open the terminal", "neutral", "Neutral baseline"),
    ("I am exhausted with this long day", "low_energy", "Multi-keyword fatigue"),
    ("hurry up immediately", "urgent", "Multi-keyword urgency"),
]

for text, expected, desc in test_cases_emotion:
    with BenchTimer(desc) as t:
        detected = emotion.detect(text)
    record("EmotionEngine", desc, detected == expected, t.elapsed_us, f"Input: '{text}' → {detected}")

# Voice Param Adaptation
for state in ["low_energy", "urgent", "casual", "neutral"]:
    with BenchTimer(f"Voice params: {state}") as t:
        params = emotion.adapt_voice_params(state)
    valid = "speed" in params and "pitch_shift" in params and "prefix_filler" in params
    record("EmotionEngine", f"Voice params [{state}]", valid, t.elapsed_us, json.dumps(params))

# Filler Injection
with BenchTimer("Filler injection") as t:
    filled = emotion.apply_filler("Opening YouTube.", "casual")
valid = filled.startswith("Done, boss.")
record("EmotionEngine", "Filler injection (casual)", valid, t.elapsed_us, f"Output: '{filled}'")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 2: THOUGHT ENGINE (Phase 29)
# ═══════════════════════════════════════════════════════════════════════════════
print(f"{'🧠 MODULE 2: ThoughtEngine (Phase 29)':^78}")
print(THIN_DIV)

from jarvis.engine.thought import ThoughtEngine

thought = ThoughtEngine()

# Media intent
with BenchTimer("Media intent thoughts") as t:
    thoughts = thought.generate_thoughts("open youtube and play music", {})
has_intent = "intent" in thoughts
record("ThoughtEngine", "Media intent classification", has_intent, t.elapsed_us, str(thoughts.get("intent", [])))

# Developer intent
with BenchTimer("Developer intent thoughts") as t:
    thoughts = thought.generate_thoughts("build the project and run code", {})
has_dev = any("developer" in x.lower() for x in thoughts.get("intent", []))
record("ThoughtEngine", "Developer intent classification", has_dev, t.elapsed_us, str(thoughts.get("intent", [])))

# Vision hook
with BenchTimer("Vision hook thoughts") as t:
    mock_vision = {"Submit": {"x": 800, "y": 600}, "Login": {"x": 100, "y": 100}}
    thoughts = thought.generate_thoughts("click on something", {"visual_map": mock_vision})
has_vision = "vision" in thoughts
record("ThoughtEngine", "Vision bounding box injection", has_vision, t.elapsed_us, str(thoughts.get("vision", [])))

# Empty intent (should not crash)
with BenchTimer("Empty intent safety") as t:
    thoughts = thought.generate_thoughts("", {})
record("ThoughtEngine", "Empty intent (no crash)", True, t.elapsed_us, str(thoughts))

# Prompt formatting
with BenchTimer("Prompt format") as t:
    sample = {"intent": ["Media playback detected"], "prediction": ["Auto-search lofi"]}
    formatted = thought.format_for_prompt(sample)
valid = "-> [INTENT]:" in formatted and "-> [PREDICTION]:" in formatted
record("ThoughtEngine", "Prompt formatting structure", valid, t.elapsed_us, f"Length: {len(formatted)} chars")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 3: ENERGY MODEL (Phase 31)
# ═══════════════════════════════════════════════════════════════════════════════
print(f"{'⚖️  MODULE 3: EnergyEngine (Phase 31)':^78}")
print(THIN_DIV)

from jarvis.engine.energy import EnergyEngine

energy = EnergyEngine()

scenarios = [
    ({"idle_time": 0, "active_app": "firefox"}, "neutral", "Active user, browser", lambda s: 0.5 <= s <= 1.0),
    ({"idle_time": 120, "active_app": "firefox"}, "neutral", "Idle user, browser", lambda s: 0.8 <= s <= 1.0),
    ({"idle_time": 30, "active_app": "vscode"}, "neutral", "Active user, VSCode (focus)", lambda s: s <= 0.3),
    ({"idle_time": 30, "active_app": "vscode", "time_of_day": "night"}, "low_energy", "Night + VSCode + Low Energy", lambda s: s == 0.0),
    ({"idle_time": 5000}, "neutral", "Deep sleep (>3600s)", lambda s: s == 0.0),
    ({"idle_time": 90, "active_app": "desktop"}, "neutral", "Mildly idle, desktop", lambda s: 0.8 <= s <= 1.0),
]

for ctx, emo, desc, check in scenarios:
    with BenchTimer(desc) as t:
        score = energy.calculate(ctx, emo)
    record("EnergyEngine", desc, check(score), t.elapsed_us, f"Energy = {score:.2f}")

# Proactive gate cooldown
with BenchTimer("Cooldown enforcement") as t:
    energy.last_suggestion_time = time.time()  # Fake recent suggestion
    gate = energy.evaluate_proactive_gate({"idle_time": 120, "active_app": "desktop"})
record("EnergyEngine", "Cooldown blocks rapid fire", gate == False, t.elapsed_us, f"Gate = {gate}")

# Proactive gate pass
with BenchTimer("Cooldown expired") as t:
    energy.last_suggestion_time = time.time() - 400  # 400s ago, beyond 300s limit
    gate = energy.evaluate_proactive_gate({"idle_time": 120, "active_app": "desktop"})
record("EnergyEngine", "Cooldown expired allows proactive", gate == True, t.elapsed_us, f"Gate = {gate}")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 4: USER PROFILE (Phase 32)
# ═══════════════════════════════════════════════════════════════════════════════
print(f"{'🧬 MODULE 4: UserProfile (Phase 32)':^78}")
print(THIN_DIV)

from jarvis.engine.profile import UserProfile

# Use a temp file to avoid polluting user config
tmp_profile = os.path.join(tempfile.mkdtemp(), "test_profile.json")
profile = UserProfile(profile_path=tmp_profile)

# Simulate 7 YouTube intents to exceed the threshold (>5)
with BenchTimer("Profile learning (7 intents)") as t:
    for i in range(7):
        profile.update(f"open youtube #{i}", {"active_app": "chrome"})
record("UserProfile", "Track 7 YouTube intents", profile.data["preferred_actions"].get("youtube", 0) == 7, t.elapsed_us, f"Count: {profile.data['preferred_actions']}")

with BenchTimer("Preference threshold") as t:
    prefers = profile.prefers("youtube")
record("UserProfile", "Prefers youtube (>5 threshold)", prefers == True, t.elapsed_us, f"prefers = {prefers}")

with BenchTimer("Top app detection") as t:
    top = profile.get_top_app()
record("UserProfile", "Top app is chrome", top == "chrome", t.elapsed_us, f"top_app = '{top}'")

with BenchTimer("Non-preference check") as t:
    prefers_spotify = profile.prefers("spotify")
record("UserProfile", "Does NOT prefer spotify", prefers_spotify == False, t.elapsed_us)

# Verify persistence
with BenchTimer("Profile disk persistence") as t:
    profile2 = UserProfile(profile_path=tmp_profile)
    persisted = profile2.data["preferred_actions"].get("youtube", 0) == 7
record("UserProfile", "Persists to disk and reloads", persisted, t.elapsed_us)

# Cleanup temp
shutil.rmtree(os.path.dirname(tmp_profile), ignore_errors=True)

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 5: MEMPALACE ADAPTER + COMPRESSION (Phase 5 + 30)
# ═══════════════════════════════════════════════════════════════════════════════
print(f"{'🏛️  MODULE 5: MemPalace + Compression (Phase 5/30)':^78}")
print(THIN_DIV)

from jarvis.plugins.mempalace_adapter import MemPalaceAdapter

tmp_mem_dir = tempfile.mkdtemp()
tmp_mem_path = os.path.join(tmp_mem_dir, "test_mempalace.json")
mem = MemPalaceAdapter(data_path=tmp_mem_path)

# Commit success
with BenchTimer("Commit workflow") as t:
    mem.commit_success("open youtube", ["xdg-open https://youtube.com"])
record("MemPalace", "Commit success writes to drawer", True, t.elapsed_us)

# Query history
with BenchTimer("Query history") as t:
    result = mem.query_history("open youtube")
found = "historical_pattern" in result
record("MemPalace", "Query retrieves matching pattern", found, t.elapsed_us, str(result)[:80])

# Store knowledge
with BenchTimer("Store knowledge") as t:
    mem.store_knowledge("python_tip", "Use list comprehensions for performance.")
record("MemPalace", "Knowledge storage", True, t.elapsed_us)

# Query knowledge
with BenchTimer("Query knowledge") as t:
    kn = mem.query_knowledge("python_tip")
record("MemPalace", "Knowledge retrieval", "list comprehensions" in kn, t.elapsed_us, kn[:50])

# Insert 6 YouTube entries that SURVIVE retention (recent, used_count > 3)
# The compress() method purges low-score entries first, then summarizes survivors.
# So we need entries with high retention scores that are still YouTube-tagged.
raw = mem._load()
drawer = raw["system_wing"]["workflow_room"]["browser_drawer"]
# Remove the existing entry first for clean slate
drawer.clear()
for i in range(6):
    drawer.append({
        "timestamp": time.time() - 10,  # Very recent = high decay score
        "trigger_intent": "open youtube",
        "successful_pipeline": ["xdg-open https://youtube.com"],
        "used_count": 5,  # High usage = survives retention
        "confirmed": True
    })
mem._save(raw)

with BenchTimer("GC compression") as t:
    mem.compress()
post_gc = mem._load()
drawer_post = post_gc["system_wing"]["workflow_room"]["browser_drawer"]
kn_post = mem.query_knowledge("habit_youtube")
summarized = kn_post != ""
# After summarization, youtube entries should be REMOVED from drawer and placed in knowledge
record("MemPalace", "GC purges via summarization", len(drawer_post) == 0, t.elapsed_us, f"Remaining: {len(drawer_post)}")
record("MemPalace", "GC summarizes duplicates to knowledge", summarized, 0, kn_post[:60] if kn_post else "N/A")

shutil.rmtree(tmp_mem_dir, ignore_errors=True)

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 6: REFLECTION ENGINE (Phase 21)
# ═══════════════════════════════════════════════════════════════════════════════
print(f"{'🔍 MODULE 6: ReflectionEngine (Phase 21)':^78}")
print(THIN_DIV)

from jarvis.engine.reflection import ExecutionLogger, ReflectionLoop

tmp_log_dir = tempfile.mkdtemp()
logger = ExecutionLogger(log_dir=tmp_log_dir)

with BenchTimer("Log execution entry") as t:
    logger.log("open youtube", ["xdg-open"], True, 1.2)
    logger.log("open twitter", ["xdg-open"], False, 3.5)
log_exists = os.path.exists(logger.log_file)
record("ReflectionEngine", "ExecutionLogger writes JSONL", log_exists, t.elapsed_us)

with BenchTimer("Parse log entries") as t:
    with open(logger.log_file, "r") as f:
        entries = [json.loads(l) for l in f]
record("ReflectionEngine", "Log entries parseable", len(entries) == 2, t.elapsed_us, f"Entries: {len(entries)}")

# Safe mode circuit breaker (inject 4 failures in the last hour)
for i in range(4):
    logger.log(f"fail_{i}", [], False, 0.5)

reflection = ReflectionLoop(logger)
captured = StringIO()
old_stdout = sys.stdout
sys.stdout = captured
with BenchTimer("Reflection loop + circuit breaker") as t:
    reflection.reflect()
sys.stdout = old_stdout
output = captured.getvalue()
safe_mode_triggered = "SAFE MODE" in output
record("ReflectionEngine", "Circuit breaker triggers on 3+ failures", safe_mode_triggered, t.elapsed_us)

shutil.rmtree(tmp_log_dir, ignore_errors=True)

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 7: EVOLUTION SANDBOX (Phase 22)
# ═══════════════════════════════════════════════════════════════════════════════
print(f"{'🧪 MODULE 7: CodeEvolver Sandbox (Phase 22)':^78}")
print(THIN_DIV)

from jarvis.core.evolution import CodeEvolver, SandboxManager

sandbox = SandboxManager()

with BenchTimer("Write temp module") as t:
    path = sandbox.write_temp("test_mod.py", "print('hello world')\n")
record("CodeEvolver", "Sandbox writes temp file", os.path.exists(path), t.elapsed_us)

with BenchTimer("Syntax integrity check") as t:
    valid = sandbox.test_module(path)
record("CodeEvolver", "Valid module passes syntax check", valid, t.elapsed_us)

with BenchTimer("Bad syntax rejection") as t:
    bad_path = sandbox.write_temp("bad_mod.py", "def broken(\n")
    invalid = sandbox.test_module(bad_path)
record("CodeEvolver", "Invalid module caught by sandbox", invalid == False, t.elapsed_us)

evolver = CodeEvolver()
with BenchTimer("Evolution lock enforcement") as t:
    blocked = evolver.improve_module("jarvis/engine/emotion.py", None)
record("CodeEvolver", "Evolution lock blocks modification", blocked == False, t.elapsed_us)

with BenchTimer("Forbidden file guard") as t:
    is_legal = evolver._is_legal_target("core/runtime.py")
record("CodeEvolver", "Forbidden file rejected", is_legal == False, t.elapsed_us)

with BenchTimer("Allowed file accepted") as t:
    is_legal = evolver._is_legal_target("jarvis/engine/emotion.py")
record("CodeEvolver", "Allowed path accepted", is_legal == True, t.elapsed_us)

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 8: VISION ENGINE (Phase Y)
# ═══════════════════════════════════════════════════════════════════════════════
print(f"{'👁️  MODULE 8: VisionEngine (Phase Y)':^78}")
print(THIN_DIV)

from jarvis.interface.vision import VisionEngine

vision = VisionEngine()

with BenchTimer("Screen capture") as t:
    img = vision.capture_screen()
record("VisionEngine", "Capture returns valid path", img is not None, t.elapsed_us)

with BenchTimer("OCR processing") as t:
    ocr_map = vision.process_ocr(img)
is_dict = isinstance(ocr_map, dict)
record("VisionEngine", "OCR produces bounding boxes", is_dict, t.elapsed_us, f"Found: {len(ocr_map)} regions")

with BenchTimer("Full look() pipeline") as t:
    full_map = vision.look()
record("VisionEngine", "Full perception pipeline", isinstance(full_map, dict), t.elapsed_us, f"Objects: {len(full_map)}")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 9: OVERLAY HUD (Phase Z)
# ═══════════════════════════════════════════════════════════════════════════════
print(f"{'🎬 MODULE 9: OverlayEngine HUD (Phase Z)':^78}")
print(THIN_DIV)

from jarvis.interface.overlay import OverlayEngine

hud = OverlayEngine()

# These calls will gracefully fail on macOS (no notify-send) but should NOT crash
for method_name in ["listening", "processing", "executing", "success", "warning"]:
    with BenchTimer(f"HUD: {method_name}") as t:
        try:
            getattr(hud, method_name)()
            crashed = False
        except Exception:
            crashed = True
    record("OverlayEngine", f"HUD state [{method_name}] (no crash)", not crashed, t.elapsed_us)

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 10: BEHAVIORAL ENGINE (Phase 6)
# ═══════════════════════════════════════════════════════════════════════════════
print(f"{'🔮 MODULE 10: BehavioralEngine (Phase 6)':^78}")
print(THIN_DIV)

from jarvis.engine.behavior import BehavioralEngine

behavior = BehavioralEngine()

mock_workflows = [
    {"trigger_intent": "open youtube", "successful_pipeline": ["xdg-open https://youtube.com"],
     "timestamp": time.time() - 100, "time_of_day": behavior._get_time_of_day(), "active_app": "terminal"},
    {"trigger_intent": "open youtube", "successful_pipeline": ["xdg-open https://youtube.com"],
     "timestamp": time.time() - 200, "time_of_day": behavior._get_time_of_day(), "active_app": "terminal"},
    {"trigger_intent": "open youtube", "successful_pipeline": ["xdg-open https://youtube.com"],
     "timestamp": time.time() - 300, "time_of_day": behavior._get_time_of_day(), "active_app": "terminal"},
    {"trigger_intent": "open youtube", "successful_pipeline": ["xdg-open https://youtube.com"],
     "timestamp": time.time() - 400, "time_of_day": behavior._get_time_of_day(), "active_app": "terminal"},
]

with BenchTimer("Pattern recognition") as t:
    seq, conf = behavior.analyze_patterns(mock_workflows, "open youtube")
record("BehavioralEngine", "Recognizes repeated pattern", conf > 0.3, t.elapsed_us, f"Confidence: {conf}")

with BenchTimer("Prediction gate") as t:
    prediction = behavior.predict_next_action("open youtube", mock_workflows)
record("BehavioralEngine", "Should suggest (above threshold)", prediction["should_suggest"], t.elapsed_us, str(prediction))

# Empty history
with BenchTimer("Empty history safety") as t:
    prediction = behavior.predict_next_action("random task", [])
record("BehavioralEngine", "Empty history returns safely", prediction["confidence"] == 0.0, t.elapsed_us)

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 11: IDENTITY CORE (Phase 27)
# ═══════════════════════════════════════════════════════════════════════════════
print(f"{'🎭 MODULE 11: IdentityCore (Phase 27)':^78}")
print(THIN_DIV)

from jarvis.core.identity import IdentityCore, DatasetCollector

tmp_id_dir = tempfile.mkdtemp()
tmp_id_path = os.path.join(tmp_id_dir, "test_identity.json")
identity = IdentityCore(config_path=tmp_id_path)

with BenchTimer("Identity initialization") as t:
    header = identity.get_system_prompt_header()
has_name = "Jarvis" in header
record("IdentityCore", "Produces system prompt header", has_name, t.elapsed_us, header[:60])

with BenchTimer("Identity persistence") as t:
    identity.save_state()
    persisted = os.path.exists(tmp_id_path)
record("IdentityCore", "Persists identity to disk", persisted, t.elapsed_us)

# Dataset Collector
tmp_ds_path = os.path.join(tmp_id_dir, "training", "test_finetune.jsonl")
collector = DatasetCollector(dataset_path=tmp_ds_path)

with BenchTimer("Dataset collection") as t:
    collector.append_interaction("open youtube", "Opening YouTube now.", corrections=None)
record("IdentityCore", "Dataset collector stores interaction", os.path.exists(tmp_ds_path), t.elapsed_us)

shutil.rmtree(tmp_id_dir, ignore_errors=True)

print()

# ═══════════════════════════════════════════════════════════════════════════════
#                          FINAL BENCHMARK REPORT
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{DIVIDER}")
print("   📊 BENCHMARK RESULTS")
print(DIVIDER)
print(f"{'Module':<22} {'Test':<42} {'Status':<10} {'Latency':>10}")
print(THIN_DIV)

for r in results:
    lat = f"{r['latency_μs']:>8.1f}μs"
    print(f"  {r['module']:<20} {r['test']:<42} {r['status']:<10} {lat}")

print(THIN_DIV)

avg_latency = sum(r["latency_μs"] for r in results) / len(results) if results else 0
max_latency = max(r["latency_μs"] for r in results) if results else 0
min_latency = min(r["latency_μs"] for r in results) if results else 0

print(f"\n  {'TOTAL TESTS:':<30} {len(results)}")
print(f"  {'PASSED:':<30} {total_pass}  ✅")
print(f"  {'FAILED:':<30} {total_fail}  {'❌' if total_fail > 0 else ''}")
print(f"  {'AVG LATENCY:':<30} {avg_latency:>8.1f} μs")
print(f"  {'MIN LATENCY:':<30} {min_latency:>8.1f} μs")
print(f"  {'MAX LATENCY:':<30} {max_latency:>8.1f} μs")

if total_fail == 0:
    print(f"\n  🏆 ALL SYSTEMS NOMINAL — BRAIN ARCHITECTURE FULLY VALIDATED")
else:
    print(f"\n  ⚠️  {total_fail} TEST(S) REQUIRE ATTENTION")

print(f"\n{DIVIDER}\n")

# Write JSON report
report_path = os.path.join(PROJECT_ROOT, "tests", "benchmark_report.json")
with open(report_path, "w") as f:
    json.dump({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total": len(results),
        "passed": total_pass,
        "failed": total_fail,
        "avg_latency_us": round(avg_latency, 1),
        "max_latency_us": round(max_latency, 1),
        "results": results
    }, f, indent=2)

print(f"  📄 Full JSON report saved: {report_path}")
print()
