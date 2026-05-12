import random

def encode(value):
    """
    Splits a 12-bit integer (0-4095) into two bytes.
    high byte = upper 4 bits (value >> 8)
    low byte  = lower 8 bits (value & 0xFF)
    """
    high = value >> 8
    low = value & 0xFF
    return high, low

def decode(high, low):
    """
    Reconstructs the original integer from two bytes.
    value = (high << 8) | low
    """
    value = (high << 8) | low
    return value

if __name__ == "__main__":
    print("Testing encode → decode with 10 random values:\n")
    for _ in range(10):
        original = random.randint(0, 4095)
        high, low = encode(original)
        decoded = decode(high, low)
        match = "✓" if decoded == original else "✗"
        print(f"Original: {original:<5} →  High: {high:<3}, Low: {low:<3}  →  Decoded: {decoded:<5} {match}")
        assert decoded == original, f"Mismatch! {original} != {decoded}"

    print("\nAll 10 values passed assertion check.")
