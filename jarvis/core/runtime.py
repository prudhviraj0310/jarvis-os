import time
import json
import threading

from jarvis.engine.llm import OllamaEngine, EngineTimeoutError, EngineValidationError
from jarvis.engine.context import ContextEngine
from jarvis.engine.behavior import BehavioralEngine
from jarvis.system.kernel import get_system_state
from jarvis.system.execution import ExecutionPolicy, RiskLevel, execute_command
from jarvis.system.input_control import InputControlLayer
from jarvis.system.screen import ScreenAwarenessLayer
from jarvis.interface.voice import VoiceEngine, Priority
from jarvis.interface.overlay import OverlayEngine
from jarvis.interface.listener import WakeWordEngine
from jarvis.engine.tool_router import ToolRouter
from jarvis.plugins.tool_manager import ToolManager
from jarvis.engine.guidance import GuidanceEngine
from jarvis.engine.planner import CrewAIPlanner
from jarvis.engine.habits import HabitEngine

class JarvisRuntime:
    def __init__(self, mode="interactive"):
        self.mode = mode
        self.engine = OllamaEngine()
        self.context_layer = ContextEngine() # Phase 5: Memory Interceptor
        self.behavior_layer = BehavioralEngine() # Phase 6: Prediction Interceptor
        self.screen_layer = ScreenAwarenessLayer() # Phase 4 Vision Hooks
        self.input_layer = InputControlLayer()
        self.voice = VoiceEngine() # Phase 8: Voice Output
        self.overlay = OverlayEngine() # Phase 8: Visual HUD
        self.listener = WakeWordEngine(self._wake_trigger) # Phase 9: Sentient Presence
        
        # Tool Orchestration (Phase 10 & 11)
        self.tool_router = ToolRouter()
        self.tool_manager = ToolManager()
        self.guidance_layer = GuidanceEngine()
        self.planner = CrewAIPlanner()
        self.habit_layer = HabitEngine() # Phase 12 Habit Integration
        
        self.running = False
        self.is_executing = False # Interrupt Safety Lock
        
        # Proactive Presence Trackers
        self.last_interaction_time = time.time()
        self.last_proactive_time = 0.0
        self.pending_proactive_habit = []
        
        # V2: Proactive Intelligence Loop
        self.autonomous_thread = threading.Thread(target=self._run_autonomous_loop, daemon=True)
        
        # Resilience Layer
        self.safe_mode = False
        self.consecutive_errors = 0
        self.MAX_ERRORS = 3

    def start(self):
        self.running = True
        print(f"[Jarvis Runtime] Started in {self.mode} mode.")
        
        # Start Autonomous Loop
        self.autonomous_thread.start()
        
        # Inject API keys/configs globally
        self.guidance_layer.inject_environment()
        
        if self.mode == "daemon":
            self.listener.start()
        
        # Boot Feedback
        self.voice.play_cue("listening")
        self.voice.speak("Online.", priority=Priority.CRITICAL)
        self.overlay.show_status("Boot Sequence", "System Online.", "normal")
        
        while self.running:
            try:
                if self.mode == "interactive":
                    user_intent = input("\n[Jarvis] Ready > ").strip()
                    if not user_intent:
                        continue
                    if user_intent.lower() in ["exit", "quit", "stop"]:
                        self.stop()
                        break
                    
                    self._process_intent(user_intent)
                else:
                    # Daemon mode loop stub
                    time.sleep(1)
            except Exception as e:
                # Catch ALL top-level errors to prevent loop crash
                print(f"[Jarvis ERROR] Unhandled framework exception: {e}")
                self._register_error()

    def _run_autonomous_loop(self):
        """
        V2 Autonomous Prediction Engine.
        Runs constantly in the background, checking OS state.
        If a prediction hits the 90% AUTO_EXEC threshold, Jarvis executes it before the user asks.
        """
        while True:
            try:
                time.sleep(60) # Poll every 60 seconds
                if not self.running or self.is_executing:
                    continue
                    
                now = time.time()
                
                # Phase 11 & 12: Idle Habit Proactive Triggers
                # If idle > 2 minutes and hasn't spoken proactively in an hour (cooldown)
                if now - self.last_interaction_time > 120 and now - self.last_proactive_time > 3600:
                    workflows = self.context_layer.mempalace.get_all_workflows()
                    habit_sequence, habit_confidence = self.habit_layer.check_habits(workflows)
                    
                    if habit_confidence >= self.habit_layer.HABIT_CONFIDENCE_THRESHOLD:
                        self.last_proactive_time = now
                        self.pending_proactive_habit = habit_sequence
                        self.voice.play_cue("listening")
                        print(f"\n[Jarvis Proactive] Context-aware habit detected (Confidence: {habit_confidence}).")
                        print(f"                   Sequence: {json.dumps(habit_sequence)[:60]}...")
                        self.voice.speak("Should I start your routine?", priority=Priority.ASSIST)
                        self.overlay.show_status("Habit Detected", "Autonomy standing by.", "normal")
                        continue 
                    
                # We generate a passive pseudo-intent based on OS state. In real prod, this is tied to triggers.
                # For Phase 11, we pass an empty "system_tick" intent to evaluate the time/date states.
                workflows = self.context_layer.mempalace.get_all_workflows()
                behavior_eval = self.behavior_layer.predict_next_action("system_tick", workflows)
                
                if behavior_eval.get("should_auto_exec", False):
                    print(f"\n[Jarvis Autonomous] High probability workflow detected (>90%). Executing proactively.")
                    self.voice.speak("Proactive execution initiated.", priority=Priority.ASSIST)
                    self.overlay.show_status("Autonomous Engine", "Predictive sequence initiated.", "normal")
                    self._process_intent("system_tick") # Push it through the pipeline
            except Exception:
                pass # Fail silently in background to avoid disrupting UX
                
    def _wake_trigger(self, intent: str):
        """Asynchronous callback fired by WakeWordEngine"""
        
        # 3. INTERRUPT SAFETY: Drop wake requests if system is actively executing
        if self.is_executing:
            print(f"[Jarvis Wake] Dropped interrupt '{intent}' - pipeline is active.")
            return

        # 2. LISTENING STATE FEEDBACK
        print(f"\n[Jarvis Wake Triggered] Command: '{intent}'")
        self.voice.play_cue("listening")
        self.overlay.show_status("Active Listening", f"I heard: {intent}", "normal")
        
        if intent.lower() == "System Wake":
            self.voice.speak("Ready.", priority=Priority.ASSIST)
            return
            
        # Push into reasoning loop
        self._process_intent(intent)

    def stop(self):
        self.running = False
        self.listener.stop()
        print("[Jarvis Runtime] Shutting down.")
        self.voice.speak("Offline.", priority=Priority.CRITICAL)
        self.overlay.show_status("System Offline", "Shutting down.", "normal")

    def _register_error(self):
        self.consecutive_errors += 1
        if self.consecutive_errors >= self.MAX_ERRORS and not self.safe_mode:
            self.safe_mode = True
            print(f"\n[CRITICAL WARNING] Consecutive error limit reached ({self.consecutive_errors}).")
            print("[CRITICAL WARNING] Jarvis Engine entering SAFE MODE. Auto-execution is suspended.")
            self.voice.play_cue("error")
            self.voice.speak("Safe mode active.", priority=Priority.CRITICAL)
            self.overlay.show_status("Safe Mode Activated", "Consecutive errors breached limit.", "critical")

    def _clear_errors(self):
        if self.safe_mode:
            print("\n[Jarvis] System stable. SAFE MODE deactivated.")
            self.voice.speak("Restored.", priority=Priority.ASSIST)
            self.overlay.show_status("System Stable", "Safe mode deactivated.", "normal")
        self.consecutive_errors = 0
        self.safe_mode = False

    def _verify_visual_context(self, expected_process: str) -> bool:
        if not expected_process:
            return True # Nothing to verify
            
        print(f"[Jarvis] Active perception polling: Looking for '{expected_process}' window...")
        
        for _ in range(10):
            if self.screen_layer.verify_context(expected_process):
                print(f"         Context visually confirmed: '{expected_process}' dominates focus.")
                return True
            time.sleep(0.5)
            
        return False

    def _process_intent(self, user_intent: str):
        self.is_executing = True
        self.last_interaction_time = time.time()
        try:
            self._process_intent_core(user_intent)
        finally:
            self.is_executing = False

    def _process_intent_core(self, user_intent: str):
        # 0. HABIT CONFIRMATION HOOK
        if self.pending_proactive_habit and (user_intent.lower() in ["y", "yes", "sure", "do it"]):
            pipeline = self.pending_proactive_habit
            self.pending_proactive_habit = []
            print("[Jarvis] Auto-chaining proactive habit sequence.")
            self.voice.speak("Proceeding.", priority=Priority.ASSIST)
            self._route_pipeline(pipeline, "habit_auto_trigger")
            return
        elif self.pending_proactive_habit:
            self.pending_proactive_habit = [] # Drop it if they say anything else
            
        # 1. UNIVERSAL COMMAND HOOK
        if user_intent.lower().startswith("help with "):
            target_tool = user_intent.lower().replace("help with ", "").strip()
            self.guidance_layer.provide_help(target_tool, self.voice)
            return

        if self.pending_proactive_habit is None:
            pass # Handle edge case but we already cleared it if we reached here
        elif "y" in user_intent.lower() and not self.pending_proactive_habit:
            pass # continue normal parsing

        # 1. Phase 6 Prediction Engine Interceptor 
        try:
            workflows = self.context_layer.mempalace.get_all_workflows()
            behavior_eval = self.behavior_layer.predict_next_action(user_intent, workflows)
            
            if behavior_eval["should_suggest"]:
                self.voice.play_cue("listening")
                self.voice.speak("Pattern found. Execute?", priority=Priority.ASSIST)
                self.overlay.show_status("Prediction Active", "Awaiting confirmation.", "normal")
                
                print(f"[Jarvis Behavior] High probability pattern detected (Confidence: {behavior_eval['confidence']})")
                print(f"                  Predicted Sequence Summary: {json.dumps(behavior_eval['prediction'])[:100]}...")
                confirm = input(f"                  Would you like to auto-chain this sequence? [y/N]: ").strip().lower()
                if confirm == 'y':
                    print("[Jarvis] Auto-chaining predicted workflow bypassing LLM generation.")
                    self.voice.speak("Proceeding.", priority=Priority.ASSIST)
                    # Fast-path Execution (Skipping LLM parsing entirely)
                    self._route_pipeline(behavior_eval["prediction"], user_intent)
                    return
        except Exception as e:
            print(f"[Jarvis Behavior] Warning: Behavioral prediction skewed: {e}")

        # 2. ORCHESTRATOR ROUTING (Phase 10 & Phase 12 CrewAI Extension)
        # If the intent requires planning, CrewAI builds a DAG. Else, static heuristic router is used securely.
        if self.planner.should_plan(user_intent):
            pipeline = self.planner.build_pipeline(user_intent)
        else:
            pipeline = self.tool_router.route(user_intent)
        
        # 3. ONBOARDING INTERCEPT (Phase 11: Guidance Engine)
        if not self.guidance_layer.validate_and_onboard(pipeline, self.voice):
            return
        
        external_agents_handled = False
        
        for agent_node in pipeline:
            tool = agent_node["tool"]
            task = agent_node["task"]
            
            if tool != "system":
                external_agents_handled = True
                print(f"\n[Jarvis Orchestrator] Delegating task to {tool}: '{task}'")
                
                if not self.tool_manager.is_installed(tool):
                    print(f"[Jarvis Orchestrator] Module '{tool}' is not installed.")
                    self.voice.speak("Tool not installed.")
                    self.overlay.show_status("Missing Tool", f"Install {tool} to proceed.", "critical")
                    print(f"                      Falling back to Local System OS Execution...\n")
                    external_agents_handled = False # Fall back completely
                    break
                else:
                    self.voice.speak(f"Delegating to {tool}.", priority=Priority.ASSIST)
                    if tool == "claude_code":
                        success = self.tool_manager.execute_claude_code(task, self.overlay.show_status)
                    elif tool == "openclaw":
                        success = self.tool_manager.execute_openclaw(task, self.overlay.show_status)
                    elif tool == "aider":
                        success = self.tool_manager.execute_aider(task, self.overlay.show_status)
                    elif tool == "n8n":
                        success = self.tool_manager.execute_n8n(task, self.overlay.show_status)
                        
                    if not success:
                        print(f"[Jarvis Orchestrator] Agent {tool} reported failure. Pipeline halted.")
                        break

        # If a specialized DAG pipeline entirely handled the intent, we terminate the loop successfully.
        if external_agents_handled:
            return

        # 2. Gather System Context (Fallback to Native OS Execution)
        try:
            os_context = get_system_state()
        except Exception as e:
            print(f"[Jarvis] Failed to retrieve system state: {e}")
            self._register_error()
            return
            
        # 3. Extract Phase 5 Semantic / Historical Context
        enriched_intent = self.context_layer.enrich(user_intent)
        
        # 3. Feed into AI Engine
        print("[Jarvis] Reasoning...")
        try:
            decision = self.engine.evaluate_intent(os_context, enriched_intent)
            self._clear_errors() # Clear errors on successful reasoning
        except EngineTimeoutError as e:
            print(f"[Jarvis ERROR] Engine Timeout: {e}")
            self._register_error()
            return
        except EngineValidationError as e:
            print(f"[Jarvis ERROR] Engine Validation Failure: {e}")
            self._register_error()
            return
        except Exception as e:
            print(f"[Jarvis ERROR] Unknown Engine Failure: {e}")
            self._register_error()
            return
        
        # 4. Process Validated Action Sequence (Atomicity)
        confidence = decision.get("confidence", 0.0)
        action_sequence = decision.get("action_sequence", [])
        response_msg = decision.get("response", "No response generated.")
        
        print(f"[Jarvis] Output: {response_msg}")
        
        if not action_sequence:
            self.voice.speak("Completed.", priority=Priority.ROUTINE)
            self.overlay.show_status("Response", response_msg, "normal")
            return
            
        if confidence < 0.7:
            print(f"[Jarvis] Confidence threshold failed at {confidence}. Aborting.")
            self.voice.play_cue("error")
            self.voice.speak("Aborted. Low confidence.", priority=Priority.ASSIST)
            self.overlay.show_status("Aborted", "Decision confidence too low.", "normal")
            return

        # 5. Enforce Safe Mode Boundary
        if self.safe_mode:
            print("[Jarvis SAFE MODE] Auto-execution globally suspended.")
            self.voice.speak("Safe mode override required.")
            confirm = input(f"Manual override! Execute {len(action_sequence)} actions? [y/N]: ").strip().lower()
            if confirm != 'y':
                print("[Jarvis] Sequence aborted.")
                return

        # Let user know what we are doing visually
        self.overlay.show_status("Executing", "Running instruction sequence...", "normal")
        self.voice.speak("Executing.", priority=Priority.ROUTINE)

        # 6. Route Action Pipeline Sequentially
        self._route_pipeline(action_sequence, user_intent)
        
    def _route_pipeline(self, action_sequence: list, trigger_intent: str):
        success_flag = True
        for idx, item in enumerate(action_sequence):
            action_type = item.get("type")
            
            print(f"         [Pipeline {idx+1}/{len(action_sequence)}] Executing {action_type} action...")
            
            if action_type == "system":
                success = self._handle_system_action(item)
                if not success:
                    print(f"         [Pipeline ERROR] System action failed/rejected. Aborting remainder of sequence.")
                    success_flag = False
                    break
            elif action_type == "input":
                success = self._handle_input_action(item)
                if not success:
                    print(f"         [Pipeline ERROR] Input action blocked. Aborting remainder of sequence.")
                    success_flag = False
                    break
        
        # 7. Commit successful workflow sequence back to L1/L3 memory
        if success_flag and action_sequence:
            self.voice.play_cue("success")
            self.voice.speak("Done.", priority=Priority.ROUTINE)
            self.context_layer.record_success(trigger_intent, action_sequence)


    def _handle_system_action(self, item: dict) -> bool:
        action = item.get("payload", "")
        expected = item.get("expected_process", "")
        
        risk = ExecutionPolicy.evaluate(action)
        
        if risk == RiskLevel.CRITICAL:
            print(f"[Jarvis] Action '{action}' blocked. Evaluated as CRITICAL risk.")
            self.voice.play_cue("error")
            self.voice.speak("Critical override required.", priority=Priority.CRITICAL)
            self.overlay.show_status("Warning", f"Critical command blocked: {action}", "critical")
            confirm = input(f"CRITICAL OVERRIDE! Execute {action}? [y/N]: ").strip().lower()
            if confirm != 'y':
                return False
        elif risk == RiskLevel.MODERATE:
            print(f"[Jarvis] WARNING: Action '{action}' evaluated as MODERATE risk.")
            confirm = input(f"Execute {action}? [y/N]: ").strip().lower()
            if confirm != 'y':
                return False
                
        print(f"[Jarvis] Executing System Command: {action}")
        result = execute_command(action)
        if result["status"] == "success":
            print(f"[Jarvis] Success. stdout:\n{result['stdout']}")
        else:
            print(f"[Jarvis] Command Failed (Code {result.get('code', -1)}). stderr:\n{result['stderr']}")
            return False
            
        # Core Phase 4 Perception Loop Block
        if expected:
            # We don't ask the OS if the process is running. We ask the Screen if the window is alive.
            if not self._verify_visual_context(expected):
                print(f"[Jarvis SAFETY TRIGGER] Expected '{expected}' to take compositor focus, but it did not spawn visually. Blocking remainder of Pipeline.")
                self.voice.speak("Wayland context verification failed.")
                self.overlay.show_status("Error", "Context verification failed.", "critical")
                self._register_error()
                return False # Clean abort
        else:
            time.sleep(1)
            
        return True

    def _handle_input_action(self, item: dict) -> bool:
        print(f"[Jarvis] Actuating Physical Input: {item}")
        
        try:
            result = self.input_layer.execute_input_action(item)
            if result.get("status") == "error":
                print(f"[Jarvis ERROR] Physical Actuation Blocked: {result.get('error')}")
                self._register_error()
                return False
            else:
                print(f"[Jarvis] Actuation complete.")
                time.sleep(0.5)
                return True
        except Exception as e:
            print(f"[Jarvis ERROR] Input Layer System Crash: {e}")
            self._register_error()
            return False
