# UDL-Vedanshi-25167-Python
Internship Assessment Task for Upside Down Labs

A two-part Python assignment exploring bitwise encoding for embedded systems and real-time multithreaded monitoring.

---

## Objective

Most systems (Bluetooth devices, Arduino sensors, serial communication) store and transmit data in bytes. A single byte holds values from 0 to 255 — so a sensor reading like 2850 must be split into two bytes before transmission and reassembled on the other end. This project implements that split-and-reconstruct logic and builds a live multithreaded monitor around it.

---

## Repository Structure

```
├── Encode_decode.py   # Part 1 — encode/decode functions + 10-value test loop
├── monitor.py         # Part 2 — two-thread real-time sensor simulation
├── analysis.md        # Written answers to 5 conceptual questions
└── README.md          # This file
```

---

## Part 1 — Split and Reconstruct (`Encode_decode.py`)

### How it works

| Function | Logic | Purpose |
|---|---|---|
| `encode(value)` | `high = value >> 8` / `low = value & 0xFF` | Splits a 12-bit int into two bytes |
| `decode(high, low)` | `value = (high << 8) \| low` | Reconstructs the original integer |

### Run

```bash
python3 Encode_decode.py
```

### Sample Output

```
Testing encode → decode with 10 random values:

Original: 2850  →  High: 11 , Low: 34   →  Decoded: 2850  ✓
Original: 733   →  High: 2  , Low: 221  →  Decoded: 733   ✓
...
All 10 values passed assertion check.
```

---

## Part 2 — Real-Time Monitor (`monitor.py`)

### Architecture

```
Thread 1 (Sensor)               queue.Queue              Thread 2 (Monitor)
─────────────────                                        ──────────────────
Every 100ms:                  ──────────────►            Decode (high, low)
  generate random int (0–4095)                           Maintain deque(maxlen=10)
  encode → (high, low)                                   Compute running average
  put into queue                                         Warn if avg > 3000 or < 500
```

### Key design choices

- **`queue.Queue`** — thread-safe producer-consumer handoff; no manual locking needed for data transfer
- **`collections.deque(maxlen=10)`** — automatically drops the oldest value when full, giving a sliding window average
- **`threading.Event`** — used to signal both threads to stop cleanly after 20 seconds
- **`threading.Lock`** — protects shared stats (total count, sum, warning count) from race conditions

### Run

```bash
python3 monitor.py
```

### Sample Output

```
Starting real-time sensor monitor for 20 seconds...

WARNING: Running avg = 3142.0 - too high!
WARNING: Running avg = 423.5 - too low!

Total values received: 200
Overall average: 2041.3
Threshold warnings: 14
```

---

## Concepts Covered

- Bitwise operators: `>>`, `<<`, `&`, `|`
- Byte-level data encoding/decoding
- Python `threading` module — `Thread`, `Event`, `Lock`
- Inter-thread communication with `queue.Queue`
- Sliding window statistics with `collections.deque`

---

## Requirements

- Python 3.7+
- No external libraries — uses only the standard library (`random`, `threading`, `queue`, `collections`, `time`)
