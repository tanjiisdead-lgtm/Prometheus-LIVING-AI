from prometheus.core import Prometheus
import sys
import os

def main():
    print("=========================================")
    print("       PROMETHEUS v3: GROUNDED LANGUAGE")
    print("=========================================")

    # Initialize sandbox with some initial documents
    sandbox_root = "sandbox"
    if not os.path.exists(sandbox_root):
        os.makedirs(sandbox_root)

    with open(os.path.join(sandbox_root, "survival_guide.txt"), "w") as f:
        f.write("System survival depends on energy. Fire is dangerous and can cause hardware damage. Curiosity leads to learning.")

    print("Initializing system layers...")
    p = Prometheus(sandbox_root=sandbox_root)

    print("System active. Entering life loop.")
    print("Press Ctrl+C to terminate the process (External Death).")
    print("-----------------------------------------")

    try:
        p.main_life_loop()
    except KeyboardInterrupt:
        print("\nInterrupt received.")
        p.die("External termination (KeyboardInterrupt)")
    except Exception as e:
        print(f"\nUnexpected system failure: {e}")
        p.die(f"Crash: {e}")

if __name__ == "__main__":
    main()
