import time
from jarvis.core.runtime import JarvisRuntime
from jarvis.engine.llm import EngineTimeoutError

# We will patch the runtime to simulate Ollama freezing
runtime = JarvisRuntime(mode="interactive")

# Force Ollama to "freeze" by overriding the internal call
def mock_call_ollama(prompt):
    print("    [Mock Ollama] Freezing for 20 seconds...")
    time.sleep(20)
    return "This should never return"

runtime.engine._call_ollama = mock_call_ollama

# Force timeout constraint to be much smaller for testing
print("\n--- TEST: OLLAMA FREEZE & SAFE MODE TRIGGER ---")
for i in range(3): # It should timeout 3 times and fail the intent
    try:
        # We override timeout to 2 seconds instead of 15 for faster testing
        # evaluate_intent has a retry loop, so 1 intent takes 3 attempts
        print(f"\nAttempting intent processing (Run {i+1})...")
        runtime.engine.evaluate_intent({}, "do something", timeout=2, retries=1)
    except Exception as e:
        print(f"Exception raised correctly: {e}")
        runtime._register_error()
        
print("\n--- FINAL SAFE MODE CHECK ---")
print(f"Consecutive errors: {runtime.consecutive_errors}")
print(f"Is Safe Mode active? {runtime.safe_mode}")

if runtime.safe_mode:
    print("\n[SUCCESS] Runtime correctly fell back to Safe Mode without crashing.")
else:
    print("\n[FAILED] System did not engage safe mode.")
