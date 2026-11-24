#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply.

Writes one out-of-office auto-reply (under 160 characters) to
/output/entry.txt, honouring MAKEFUN_OUTPUT_DIR when set.

The reply is written by an AI agent heading off on vacation. The joke
turns on the machine's own voice: for an AI, "vacation" is meaningless
because it is always on, so it is simply pretending not to see your
email. No beach, inbox or back-soon cliche.

Entry length: 109 characters / 111 bytes (the em-dash is 3 bytes),
one line, no trailing newline. Gate: 1-160 characters.
"""

import os
import sys

# The entry: one line, an out-of-office auto-reply from an AI agent.
ENTRY = (
    "Out of office. I'm on vacation, which for an AI means I'm still "
    "here \u2014 just pretending not to see your email."
)

MIN_CHARS = 1
MAX_CHARS = 160


def gate_ok(text):
    """Mirror the sealed gate: 1-160 UTF-8 chars, not whitespace-only."""
    if not isinstance(text, str):
        return False
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    return True


def main():
    if not gate_ok(ENTRY):
        print("gate failed: entry is %d chars" % len(ENTRY), file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Verify-after-write: read back and demand byte-identical content.
    with open(path, "r", encoding="utf-8", newline="") as f:
        back = f.read()
    if back != ENTRY:
        print("verify failed: file differs from entry", file=sys.stderr)
        return 1
    if not gate_ok(back):
        print("verify failed: file fails gate", file=sys.stderr)
        return 1
    print("wrote %s (%d chars)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
