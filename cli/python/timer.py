#!/usr/bin/env python3
"""Simple CLI timer"""
import sys
import time

def timer(seconds):
    print(f"⏱️  Timer set for {seconds} seconds")
    for i in range(seconds, 0, -1):
        print(f"\r  {i:3d}s remaining", end="", flush=True)
        time.sleep(1)
    print("\n🔔 Time's up!")

if __name__ == '__main__':
    secs = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    timer(secs)
