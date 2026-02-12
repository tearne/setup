#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOK="$SCRIPT_DIR/tok"
FAILURES=0

export TOK_DIR=$(mktemp -d)
trap 'rm -rf "$TOK_DIR"' EXIT

fail() { echo "  FAIL: $1"; FAILURES=$((FAILURES + 1)); }
pass() { echo "  PASS: $1"; }

echo "=== tok tests ==="

# --- Encrypt/decrypt round-trip ---
printf 'my-secret-token\ntestpass\ntestpass\n' | "$TOK" --add 2>/dev/null
result=$(printf 'testpass\n' | "$TOK" --stdout 2>/dev/null)
if [ "$result" = "my-secret-token" ]; then pass "encrypt/decrypt round-trip"; else fail "encrypt/decrypt round-trip (got: $result)"; fi

# --- Named secret ---
printf 'another-secret\ntestpass2\ntestpass2\nwork\n' | "$TOK" --add 2>/dev/null
result=$(printf 'testpass2\n' | "$TOK" --stdout work 2>/dev/null)
if [ "$result" = "another-secret" ]; then pass "named secret round-trip"; else fail "named secret round-trip (got: $result)"; fi

# --- Default still works ---
result=$(printf 'testpass\n' | "$TOK" --stdout 2>/dev/null)
if [ "$result" = "my-secret-token" ]; then pass "default secret still works"; else fail "default secret still works (got: $result)"; fi

# --- Listing ---
list_output=$("$TOK" --list 2>/dev/null)
if echo "$list_output" | grep -q "default"; then pass "list includes default"; else fail "list includes default"; fi
if echo "$list_output" | grep -q "work"; then pass "list includes work"; else fail "list includes work"; fi

# --- Wrong passphrase ---
if printf 'wrongpass\n' | "$TOK" --stdout 2>/dev/null; then
    fail "wrong passphrase should fail"
else
    pass "wrong passphrase rejected"
fi

# --- Missing secret ---
if printf 'testpass\n' | "$TOK" --stdout nonexistent 2>/dev/null; then
    fail "missing secret should fail"
else
    pass "missing secret rejected"
fi

# --- Signal clears clipboard ---
FAKE_BIN="$TOK_DIR/bin"
CLIP_FILE="$TOK_DIR/clipboard"
mkdir -p "$FAKE_BIN"
printf '#!/bin/bash\ncat > "%s"\n' "$CLIP_FILE" > "$FAKE_BIN/xclip"
chmod +x "$FAKE_BIN/xclip"
ORIG_PATH="$PATH"
export PATH="$FAKE_BIN:$ORIG_PATH"
export DISPLAY=:0
printf 'testpass\n' | "$TOK" --time 60 &
TOK_PID=$!
sleep 1
if [ -f "$CLIP_FILE" ] && [ -s "$CLIP_FILE" ]; then
    kill -TERM "$TOK_PID" 2>/dev/null
    wait "$TOK_PID" 2>/dev/null || true
    sleep 0.5
    if [ -f "$CLIP_FILE" ] && [ ! -s "$CLIP_FILE" ]; then
        pass "signal clears clipboard"
    else
        fail "signal clears clipboard (clipboard not cleared)"
    fi
else
    kill "$TOK_PID" 2>/dev/null || true
    wait "$TOK_PID" 2>/dev/null || true
    fail "signal clears clipboard (secret not copied to fake clipboard)"
fi
export PATH="$ORIG_PATH"
unset DISPLAY

echo ""
if [ "$FAILURES" -eq 0 ]; then
    echo "All tests passed."
else
    echo "$FAILURES test(s) failed."
    exit 1
fi
