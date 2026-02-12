#!/usr/bin/env bash
set -euo pipefail

CONTAINER="test-setup"
IMAGE="images:ubuntu/24.04"

if ! command -v incus &>/dev/null; then
    echo "Error: incus not found. Install incus first."
    exit 1
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
