import queue
import threading
import time
import re
import json
import subprocess

try:
    import sounddevice as sd
    import numpy as np
except ImportError:
    sd = None
    np = None

try:
    from jarvis.interface.vision import VisionEngine
except ImportError:
    VisionEngine = None

from jarvis.engine.emotion import EmotionEngine
from jarvis.engine.context import ContextEngine
from jarvis.engine.behavior import BehavioralEngine
from jarvis.engine.thought import ThoughtEngine
from jarvis.engine.energy import EnergyEngine
from jarvis.interface.overlay import OverlayEngine
from jarvis.core.config import ConfigManager

class DuplexAudioEngine:
    """
    Manages concurrent, non-blocking audio streams.
    Allows for barge-in (interruption) by cutting the speaker output queue when new intentional voice activity is detected.
    """
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        
        self.is_running = False
        self._input_stream = None
        self._output_stream = None

    def _audio_callback_in(self, indata, frames, time_info, status):
        """Pushes raw mic bytes to the processing queue."""
        if status:
            pass # ignore minor underruns in production
        self.input_queue.put(bytes(indata))

    def _audio_callback_out(self, outdata, frames, time_info, status):
        """Pulls generated TTS audio blocks from the output queue to the speaker."""
        try:
            data = self.output_queue.get_nowait()
            if len(data) < len(outdata):
                outdata[:len(data)] = data
                outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
            else:
                outdata[:] = data[:len(outdata)]
        except queue.Empty:
            outdata.fill(0)

    def start(self):
        if not sd:
            print("[VoiceStream] sounddevice not installed. Running in mock mode.")
            self.is_running = True
            return

        self.is_running = True

        self._input_stream = sd.RawInputStream(
            samplerate=self.sample_rate, 
            blocksize=8000, 
            dtype='int16',
            channels=self.channels, 
            callback=self._audio_callback_in
        )
        
        self._output_stream = sd.RawOutputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype='int16',
            channels=self.channels,
            callback=self._audio_callback_out
        )
        
        self._input_stream.start()
        self._output_stream.start()
        print("[VoiceStream] Duplex Audio Engine Online. (Streaming Mode Active)")

    def stop(self):
        self.is_running = False
        if self._input_stream:
            self._input_stream.stop()
            self._input_stream.close()
        if self._output_stream:
            self._output_stream.stop()
            self._output_stream.close()

    def play_audio(self, pcm_data: bytes):
        """Push synthesized audio chunk to speaker."""
        self.output_queue.put(pcm_data)

    def barge_in(self):
        """Immediately clear the output queue to silence ongoing speech (Interruption)."""
        while not self.output_queue.empty():
            try:
                self.output_queue.get_nowait()
            except queue.Empty:
                break


class ToolInterceptor:
    """
    Monitors the text stream from the LLM. If a tool pattern is detected,
    it intercepts the generation and routes it to the local OS.
    """
    def __init__(self, agent=None):
        self.agent = agent
        self.buffer = ""
        # Native mapping for tools
        self.tools = {
            "search": self._tool_search,
            "OS_CMD": self._tool_os_cmd,
            "media": self._tool_media,
            "vscode": self._tool_vscode,
            "files": self._tool_files,
            "vision": self._tool_vision
        }
        # Regex to catch a tool call before TTS speaks it: e.g. <call:search{"q":"weather"}>
        self.tool_pattern = re.compile(r"<call:(\w+)(.*?)>")

    def process_chunk(self, chunk: str) -> str:
        """
        Takes a new chunk of LLM text.
        Returns clean text for TTS, or triggers a tool if detected.
        """
        self.buffer += chunk
        
        match = self.tool_pattern.search(self.buffer)
        if match:
            tool_name = match.group(1)
            raw_args = match.group(2)
            
            # Wipe buffer to avoid speaking the tool tag
            self.buffer = self.buffer.replace(match.group(0), "")
            
            # Fire the tool asynchronously or inline
            # For vision, we want to block so we can read the result back? 
            # Actually, the interceptor just runs side effects right now.
            threading.Thread(target=self._execute, args=(tool_name, raw_args), daemon=True).start()
            
            # Replace the tool call with a vocal natural pause
            if tool_name == "vision":
                return " Gathering optical data... "
            return " Let me check... " 
            
        # If no tool tag is forming, we release safe words for TTS
        # Keep the last 15 chars in buffer just in case a tag is half-formed: e.g., "<ca"
        safe_boundary = len(self.buffer) - 15
        if safe_boundary > 0:
            safe_text = self.buffer[:safe_boundary]
            self.buffer = self.buffer[safe_boundary:]
            return safe_text
            
        return ""

    def _execute(self, name: str, args: str):
        print(f"\n[Tool Interceptor] ⚡ Executing: {name} | Args: {args}")
        if name in self.tools:
            self.tools[name](args)
        else:
            print(f"[Tool Interceptor] Unknown tool: {name}")

    def _tool_search(self, args: str):
        # Tie into Firecrawl or local Search
        print(f"-> Searching: {args}")

    def _tool_os_cmd(self, args: str):
        """Execute real OS commands inline."""
        try:
            # Parse JSON args: {"cmd": "ls -la"}
            clean_args = args.strip()
            if clean_args.startswith("{"):
                parsed = json.loads(clean_args)
                cmd = parsed.get("cmd", "")
            else:
                cmd = clean_args
            
            if not cmd:
                print("[Tool Interceptor] Empty command, skipping.")
                return
                
            print(f"-> OS Command: {cmd}")
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=30
            )
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()[:500]}")
            if result.returncode != 0 and result.stderr.strip():
                print(f"   Error: {result.stderr.strip()[:200]}")
        except json.JSONDecodeError:
            print(f"[Tool Interceptor] Failed to parse OS_CMD args: {args}")
        except subprocess.TimeoutExpired:
            print("[Tool Interceptor] OS command timed out (30s limit).")
        except Exception as e:
            print(f"[Tool Interceptor] OS_CMD error: {e}")

    def _parse_args(self, args: str) -> dict:
        clean_args = args.strip()
        if clean_args.startswith("{"):
            try:
                return json.loads(clean_args)
            except json.JSONDecodeError:
                return {}
        return {}

    def _tool_media(self, args: str):
        from jarvis.integrations.spotify import SpotifyIntegration
        res = SpotifyIntegration().execute_command(self._parse_args(args))
        print(f"-> Media: {res}")

    def _tool_vscode(self, args: str):
        from jarvis.integrations.vscode import VSCodeIntegration
        res = VSCodeIntegration().execute_command(self._parse_args(args))
        print(f"-> VS Code: {res}")

    def _tool_files(self, args: str):
        from jarvis.integrations.files import FileIntegration
        res = FileIntegration().execute_command(self._parse_args(args))
        print(f"-> Files: {res}")

    def _tool_vision(self, args: str):
        from jarvis.system.screen import ScreenAwarenessLayer
        print("-> Multimodal Vision: Analyzing active screen...")
        res = ScreenAwarenessLayer().analyze_screen()
        print(f"-> Vision Read: {res}")
        
        if self.agent:
            print("-> 🔄 Closing the Loop: Re-entering LLM stream with optical data...")
            # We feed the perceived data back into the LLM context silently
            self.agent.handle_voice_input(
                f"[System Internal Context - User's screen shows]: {res}\n"
                "Explain the issue briefly and provide the fix, or execute it if you can."
            )


class StreamingAgent:
    """
    The orchestrator that links STT -> LLM -> TTS natively.
    """
    def __init__(self, context_engine=None, behavior_engine=None):
        self.audio = DuplexAudioEngine()
        self.interceptor = ToolInterceptor(agent=self)
        self.context = context_engine if context_engine else ContextEngine()
        self.behavior = behavior_engine if behavior_engine else BehavioralEngine()
        self.emotion = EmotionEngine()
        self.vision = VisionEngine() if VisionEngine else None
        self.thoughts = ThoughtEngine()
        self.energy = EnergyEngine()
        self.hud = OverlayEngine()
        self.config = ConfigManager()
        
        # Real LLM integration via OpenAI SDK (Supports Groq, OpenAI, Local Ollama)
        self._client = None
        self._provider = "fallback"
        self._model = ""
        
        try:
            import openai
            if self.config.groq_key:
                self._client = openai.OpenAI(api_key=self.config.groq_key, base_url="https://api.groq.com/openai/v1")
                self._provider = "groq"
                self._model = "llama-3.3-70b-versatile"
                print(f"[StreamingAgent] Connected to Cloud Engine ({self._provider}) - Instant Latency.")
            elif self.config.openai_key:
                self._client = openai.OpenAI(api_key=self.config.openai_key)
                self._provider = "openai"
                self._model = "gpt-4o-mini"
                print(f"[StreamingAgent] Connected to Cloud Engine ({self._provider}).")
            else:
                # Local Ollama fallback via OpenAI SDK
                self._client = openai.OpenAI(api_key="none", base_url="http://localhost:11434/v1")
                self._provider = "ollama"
                self._model = "llama3"
                print(f"[StreamingAgent] Connected to Local OS Engine ({self._provider}).")
        except ImportError:
            try:
                import ollama as _ollama
                self._ollama = _ollama
                self._provider = "ollama_native"
                self._model = "llama3"
                print("[StreamingAgent] Connected to Local OS Engine (ollama-native).")
            except ImportError:
                print("[StreamingAgent] No LLM SDKs installed. Running in mock fallback mode.")


    def start(self):
        self.audio.start()
        
    def stop(self):
        self.audio.stop()

    def handle_voice_input(self, text_input: str):
        """
        Triggered when STT yields a completed sentence.
        """
        self.audio.barge_in() # User spoke, stop current speech
        
        # Phase Z: HUD Processing Visual
        self.hud.processing()
        
        print(f"\n[You] {text_input}")
        
        # 1. Enrich context dynamically
        ctx = self.context.enrich(text_input)
        
        # 2. Detect emotional undertone
        current_emotion = self.emotion.detect(text_input)
        if current_emotion != "neutral":
            print(f"[Agent] 🎭 Emotion Detected: {current_emotion}")

        # 3. Generate internal thoughts
        # Inject visual context if vision is available
        if self.vision:
            try:
                visual_map = self.vision.look()
                ctx["visual_map"] = visual_map
            except Exception:
                pass

        generated_thoughts = self.thoughts.generate_thoughts(text_input, ctx)
        if generated_thoughts:
            formatted = self.thoughts.format_for_prompt(generated_thoughts)
            print(f"[Agent] 🧠 Internal Thoughts:\n{formatted}")

        # Calculate energy
        energy_score = self.energy.calculate(
            {"idle_time": 30, "active_app": "terminal"},
            current_emotion
        )

        # Determine spoken thought
        spoken_thought = None
        if generated_thoughts.get("prediction") and energy_score > 0.5:
            # Leak the first predictive thought out loud
            spoken_thought = generated_thoughts["prediction"][0]
            print(f"[Agent] 🗣️ Speaking Internal Thought: {spoken_thought}")
        elif energy_score <= 0.5:
            print(f"[Agent] ⚖️ Low Energy ({energy_score}): Suppressing non-critical verbose audio.")
            
        # 4. Stream to LLM (Real or Fallback)
        self._stream_llm_cycle(text_input, ctx, current_emotion, spoken_thought, energy_score)

    def _stream_llm_cycle(self, user_text: str, context: dict, current_emotion: str = "neutral", spoken_thought: str = None, energy: float = 1.0):
        """
        Connects to Ollama LLM with streaming output, falling back to static response
        only if Ollama is not available.
        """
        print("[Jarvis] ", end="", flush=True)
        
        # Phase 31: If severely fatigued or user is working, make response minimal
        if energy < 0.3:
            print("Done.")
            self.hud.success()
            return
        
        # Phase 32: Get personality tone
        tone = self.thoughts.profile.data.get("tone", "adaptive")
        
        # ═══════════════════════════════════════════════════════
        # REAL LLM STREAMING PATH
        # ═══════════════════════════════════════════════════════
        if self._provider != "fallback":
            try:
                self._stream_from_llm(user_text, context, current_emotion, spoken_thought, tone, energy)
                return
            except Exception as e:
                print(f"\n[StreamingAgent] LLM streaming failed: {e}. Using fallback.")
        
        # ═══════════════════════════════════════════════════════
        # FALLBACK STATIC RESPONSE (only if SDKs unavailable)
        # ═══════════════════════════════════════════════════════
        self._fallback_response(user_text, current_emotion, spoken_thought, tone, energy)

    def _stream_from_llm(self, user_text: str, context: dict, emotion: str, spoken_thought: str, tone: str, energy: float):
        """
        Real streaming LLM call via OpenAI SDK (Groq/OpenAI/Ollama).
        Tokens are streamed to stdout and piped through the ToolInterceptor in real time.
        """
        thoughts_dict = self.thoughts.generate_thoughts(user_text, context)
        internal_monologue = self.thoughts.format_for_prompt(thoughts_dict)
        
        system_prompt = f"""You are Jarvis, an AI operating system assistant running natively on Linux.
You are concise, direct, and efficient. No emojis. No filler. Execute intent.
Tone: {"casual and warm" if tone == "casual" else "professional and precise"}.
User emotional state: {emotion}.

{f"Your prior reasoning: {internal_monologue}" if internal_monologue else ""}

If the user asks you to run a system command, embed it as: <call:OS_CMD{{"cmd":"the bash command"}}>
If the user asks to open an application, use: <call:OS_CMD{{"cmd":"xdg-open <url-or-app>"}}>
If the user asks to control music, use: <call:media{{"action":"play/pause/next/prev"}}>
If the user asks to search files, use: <call:files{{"action":"search", "query":"name"}}>
If the user asks you to read the screen or fix a visual error, embed: <call:vision{{}}>
Always respond conversationally first, then embed the tool call if action is needed.
Keep responses under 2 sentences unless the user explicitly asks for detail."""

        full_response = ""
        
        # Standard OpenAI SDK Stream
        if self._client:
            stream = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ],
                stream=True,
                temperature=0.3
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    full_response += token
                    self._process_stream_token(token)
                    
        elif self._provider == "ollama_native":
            stream = self._ollama.chat(
                model=self._model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_text}
                ],
                stream=True,
                options={'temperature': 0.3}
            )
            for chunk in stream:
                token = chunk['message']['content']
                full_response += token
                self._process_stream_token(token)

        self._flush_stream()
        
        # Record to profile
        self.thoughts.profile.update(user_text, {"active_app": "terminal"})
        self.hud.success()

    def _process_stream_token(self, token: str):
        clean_text = self.interceptor.process_chunk(token)
        if clean_text.strip():
            if "<call:" in clean_text:
                self.hud.executing()
            else:
                print(clean_text, end="", flush=True)

    def _flush_stream(self):
        final_text = self.interceptor.process_chunk("\n")
        if final_text.strip():
            if "<call:" not in final_text:
                print(final_text, end="", flush=True)
        print()


    def _fallback_response(self, user_text: str, emotion: str, spoken_thought: str, tone: str, energy: float):
        """
        Static fallback when Ollama is not available.
        Still routes through Emotion and ToolInterceptor for consistency.
        """
        # Generate a contextual static response
        user_lower = user_text.lower()
        
        if "open" in user_lower:
            # Extract what to open
            target = user_text.lower().replace("open", "").replace("jarvis", "").strip()
            if target:
                response = f"Opening {target} now. <call:OS_CMD{{\"cmd\":\"xdg-open https://{target}.com\"}}>"
            else:
                response = "What would you like me to open?"
        elif "time" in user_lower:
            import datetime
            now = datetime.datetime.now().strftime("%I:%M %p")
            response = f"It's currently {now}."
        elif any(w in user_lower for w in ["list", "ls", "show files", "directory"]):
            response = 'Checking. <call:OS_CMD{"cmd":"ls -la"}>'
        elif any(w in user_lower for w in ["system", "status", "health"]):
            response = 'Running diagnostics. <call:OS_CMD{"cmd":"uname -a && uptime && free -h"}>'
        else:
            response = f"Understood. Processing: {user_text}"
        
        # Apply emotional filler
        response = self.emotion.apply_filler(response, emotion)
        
        # Inject spoken thought
        if spoken_thought:
            print(f"(Internal: {spoken_thought})... ", end="", flush=True)
        
        # Stream through interceptor (handles tool calls)
        for word in response.split(" "):
            time.sleep(0.05)  # Simulate streaming feel
            clean_text = self.interceptor.process_chunk(word + " ")
            if clean_text.strip():
                print(clean_text, end="", flush=True)
        
        # Flush
        final_text = self.interceptor.process_chunk("\n")
        if final_text.strip():
            print(final_text, end="", flush=True)
        print()
        
        # Phase Z: Success
        self.hud.success()
