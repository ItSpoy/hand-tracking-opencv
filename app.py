"""Backward-compatible entry point for the hand-tracking application."""
from hand_tracker import main

if __name__ == "__main__":
    raise SystemExit(main())
