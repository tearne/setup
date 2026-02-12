#!/usr/bin/env bash
set -euo pipefail

CONTAINER="test-setup"
IMAGE="images:ubuntu/24.04"

if ! command -v incus &>/dev/null; then
    echo "Error: incus not found. Install incus first."
    exit 1
fi

# Detect if we're inside a container and verify nesting is possible
in_container=false
if [ -f /dev/.incus-agent ]; then
    in_container=true
elif systemd-detect-virt --container --quiet 2>/dev/null; then
    in_container=true
elif [ -f /.dockerenv ]; then
    in_container=true
fi

if [ "$in_container" = true ]; then
    nesting_ok=true

    # Check basic user namespace support (security.nesting)
    if ! unshare --user --pid --fork --mount-proc true 2>/dev/null; then
        echo "Error: User namespace creation failed."
        echo "  -> Set 'security.nesting=true' on the outer container."
        nesting_ok=false
    fi

    # Check BPF support (needed for cgroup2 device filtering in nested containers)
    bpf_check=$(cat /proc/sys/kernel/unprivileged_bpf_disabled 2>/dev/null || echo "unknown")
    if [ "$bpf_check" != "0" ]; then
        # BPF is restricted — test if we can actually load a trivial BPF program
        # via a nested incus dry-run isn't feasible, so check the known sysctl
        # and warn. The real test is whether incusd can call bpf(BPF_PROG_LOAD).
        if ! bpftool prog list &>/dev/null 2>&1; then
            echo "Error: BPF program loading is restricted."
            echo "  -> Set 'security.syscalls.intercept.bpf=true' on the outer container."
            echo "  -> Set 'security.syscalls.intercept.bpf.devices=true' on the outer container."
            nesting_ok=false
        fi
    fi

    if [ "$nesting_ok" = false ]; then
        echo ""
        echo "Required outer container settings (run from host):"
        echo "  incus config set <container> security.nesting=true"
        echo "  incus config set <container> security.syscalls.intercept.bpf=true"
        echo "  incus config set <container> security.syscalls.intercept.bpf.devices=true"
        echo "  incus restart <container>"
        echo ""
        echo "See TESTING.md for details."
        exit 1
    fi
    echo "NOTE: Running inside a container, nesting checks passed."
fi

# Clean up any existing container
if incus info "$CONTAINER" &>/dev/null; then
    echo "Deleting existing container '$CONTAINER'..."
    incus delete "$CONTAINER" --force
fi

echo "Launching $IMAGE as '$CONTAINER'..."
incus launch "$IMAGE" "$CONTAINER"

echo "Waiting for networking..."
sleep 5

echo "Pushing setup files into container..."
incus exec "$CONTAINER" -- mkdir -p /root/setup
incus file push "/root/setup/setup.sh" "$CONTAINER/root/setup/"
incus file push "/root/setup/setup.py" "$CONTAINER/root/setup/"
incus file push -r "/root/setup/resources" "$CONTAINER/root/setup/"

echo "Running setup inside container..."
echo "============================================================"
incus exec "$CONTAINER" -- bash /root/setup/setup.sh
echo "============================================================"

echo ""
echo "Container '$CONTAINER' is still running."
echo "  Shell in:  incus exec $CONTAINER -- bash"
echo "  Delete:    incus delete $CONTAINER --force"
