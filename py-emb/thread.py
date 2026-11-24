import time
import threading
import multiprocessing

# CPU-heavy task
def task(n):
    count = 0
    for i in range(10_000_000):
        count += i
    print(f"Task {n} done")

# -------------------------
# MULTITHREADING VERSION
# -------------------------
def run_threads():
    print("\n[Multithreading Start]")
    start = time.time()

    threads = []
    for i in range(4):
        t = threading.Thread(target=task, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"[Multithreading Time] {time.time() - start:.2f} sec")

# -------------------------
# MULTIPROCESSING VERSION
# -------------------------
def run_processes():
    print("\n[Multiprocessing Start]")
    start = time.time()

    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=task, args=(i,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print(f"[Multiprocessing Time] {time.time() - start:.2f} sec")

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    run_threads()
    run_processes()