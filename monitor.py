import threading
import queue
import random
import time
from collections import deque

# Shared queue between sensor thread and monitor thread
data_queue = queue.Queue()

# Shared stop event to cleanly shut down both threads
stop_event = threading.Event()

# Shared stats (protected by a lock for safe cross-thread access)
stats_lock = threading.Lock()
total_values = 0
total_sum = 0.0
threshold_warnings = 0


def encode(value):
    high = value >> 8
    low = value & 0xFF
    return high, low


def decode(high, low):
    return (high << 8) | low


def sensor_thread():
    """Thread 1 - Generates a random sensor value every 100ms, encodes it, puts in queue."""
    while not stop_event.is_set():
        value = random.randint(0, 4095)
        high, low = encode(value)
        data_queue.put((high, low))
        time.sleep(0.1)


def monitor_thread():
    """Thread 2 - Reads encoded values from queue, decodes, tracks running avg, warns on threshold."""
    global total_values, total_sum, threshold_warnings
    window = deque(maxlen=10)  # Automatically drops oldest when full

    while not stop_event.is_set():
        try:
            high, low = data_queue.get(timeout=0.2)
        except queue.Empty:
            continue

        value = decode(high, low)

        with stats_lock:
            total_values += 1
            total_sum += value

        window.append(value)

        if len(window) == 10:
            running_avg = sum(window) / len(window)
            if running_avg > 3000:
                with stats_lock:
                    threshold_warnings += 1
                print(f"WARNING: Running avg = {running_avg:.1f} - too high!")
            elif running_avg < 500:
                with stats_lock:
                    threshold_warnings += 1
                print(f"WARNING: Running avg = {running_avg:.1f} - too low!")


if __name__ == "__main__":
    print("Starting real-time sensor monitor for 20 seconds...\n")

    t_sensor = threading.Thread(target=sensor_thread, daemon=True)
    t_monitor = threading.Thread(target=monitor_thread, daemon=True)

    t_sensor.start()
    t_monitor.start()

    # Run for 20 seconds, then signal both threads to stop
    time.sleep(20)
    stop_event.set()

    t_sensor.join(timeout=2)
    t_monitor.join(timeout=2)

    with stats_lock:
        overall_avg = total_sum / total_values if total_values > 0 else 0
        print(f"\nTotal values received: {total_values}")
        print(f"Overall average: {overall_avg:.1f}")
        print(f"Threshold warnings: {threshold_warnings}")
