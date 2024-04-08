import os
import subprocess
import time
from multiprocessing import Process

def run_phase1():
    print("Running Phase 1...")
    subprocess.run(["python", "phase1.py"])

def run_phase2():
    print("Running Phase 2...")
    subprocess.run(["python", "phase2.py"])

if __name__ == "__main__":
    # Start Phase 1 as a child process
    phase1_process = Process(target=run_phase1)
    phase1_process.start()
    print(f"Phase 1 Process ID: {phase1_process.pid}")

    # Start Phase 2 as a child process
    phase2_process = Process(target=run_phase2)
    phase2_process.start()
    print(f"Phase 2 Process ID: {phase2_process.pid}")

    try:
        while phase1_process.is_alive() or phase2_process.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping child processes...")
        phase1_process.terminate()
        phase2_process.terminate()
        phase1_process.join()
        phase2_process.join()

    print("Main process exiting.")
