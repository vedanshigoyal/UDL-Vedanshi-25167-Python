Q1. Why can't 2850 fit in one byte? What is the maximum value a single byte can hold, and why?

A byte has 8 bits, and each bit can only be 0 or 1. That means there are 2^8 = 256 possible combinations, so a single byte can store values from 0 to 255.
Since 2850 is much bigger than 255, it can't fit inside one byte. That's why we split it into two parts (high byte and low byte) before sending or storing it.

---

Q2. For value = 2850, show step-by-step what value >> 8 and value & 0xFF give you.

2850 in binary looks like this:
0000 1011 0010 0010

value >> 8

This shifts the bits 8 places to the right, which leaves us with only the upper part:

0000 1011 0010 0010
→ 0000 0000 0000 1011

That becomes 11.

So:
high = 11

value & 0xFF

0xFF means:

1111 1111

Using & keeps only the last 8 bits:

0000 1011 0010 0010
0000 0000 1111 1111
-------------------

0000 0000 0010 0010

That gives 34.

So:
low = 34

Final result:
encode(2850) → (11, 34)

---

Q3. Explain what (high << 8) | low does during decoding. How do they reverse what encode() did?

During encoding, the original number was split into two parts:

* the upper bits (high)
* the lower bits (low)

While decoding:

* high << 8 shifts the high byte back to its original position
* | low adds the lower bits back in

For example:

11 << 8 = 2816
2816 | 34 = 2850

So decoding basically combines the two bytes back together to rebuild the original value.

---

Q4. What is the difference between a running average of the last 10 values and the total average of all values so far? Why does it matter for live data?

A running average only considers the most recent values (in this case, the last 10 readings). As new values come in, older ones are removed automatically.
A total average uses every value from the beginning of the program.

For live sensor data, a running average is more useful because it reacts quickly to sudden changes. If the sensor suddenly starts giving very high or very low readings, the running average will show that almost immediately. A total average changes much more slowly because older values still affect it.

So the running average gives a better picture of what is happening right now.

---

Q5. Why use queue.Queue between threads instead of a plain Python list?

queue.Queue is made specifically for communication between threads. It safely handles one thread adding data while another thread reads it.

With a normal Python list, both threads could try to access the list at the same time, which can lead to unexpected bugs or missed data.

queue.Queue also has useful features like waiting until data is available, which makes the program cleaner and more reliable for producer-consumer type tasks like this one.
