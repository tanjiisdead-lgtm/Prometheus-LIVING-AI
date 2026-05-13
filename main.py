from prometheus.core import Prometheus
import sys

def main():
    print("=========================================")
    print("       PROMETHEUS v2: COMPUTATIONAL LIFE")
    print("=========================================")
    print("Initializing system layers...")

    p = Prometheus()

    print("System active. Entering life loop.")
    print("Press Ctrl+C to terminate the process (External Death).")
    print("-----------------------------------------")

    try:
        # Run for a limited number of steps if in a non-interactive environment
        # or run indefinitely. For demo, we can just call main_life_loop.
        p.main_life_loop()
    except KeyboardInterrupt:
        print("\nInterrupt received.")
        p.die("External termination (KeyboardInterrupt)")
    except Exception as e:
        print(f"\nUnexpected system failure: {e}")
        p.die(f"Crash: {e}")

if __name__ == "__main__":
    main()
