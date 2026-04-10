import sys
import argparse
from jarvis.core.runtime import JarvisRuntime

def main():
    parser = argparse.ArgumentParser(description="Jarvis OS Foundation Runtime")
    parser.add_argument("--mode", choices=["interactive", "daemon"], default="interactive", help="Start mode for the runtime")
    args = parser.parse_args()

    print(f"Jarvis System Initializing... (Mode: {args.mode})")
    
    runtime = JarvisRuntime(mode=args.mode)
    
    try:
        runtime.start()
    except KeyboardInterrupt:
        print("\nJarvis System Offline.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[CRITICAL ERROR] Runtime Terminated: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
