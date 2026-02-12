# Testing: Incus Nested Container Harness

`test.sh` launches an Ubuntu 24.04 incus container and runs `setup.sh` inside it.
This requires nested container support.

## Prerequisites

### Running on bare metal / VM

No special configuration — just have `incus` installed and initialised (`incus admin init`).

### Running inside an incus container (nested)

The **outer** container must have these settings applied **from the host**:

```bash
incus config set <outer-container> security.nesting=true
incus config set <outer-container> security.syscalls.intercept.bpf=true
incus config set <outer-container> security.syscalls.intercept.bpf.devices=true
incus restart <outer-container>
```

Without these, inner container launches fail with:
- `bpf_program_load_kernel: Operation not permitted` (cgroup2 device filtering blocked)
- `newuidmap: write to uid_map failed: Operation not permitted` (UID mapping blocked)

The `test.sh` script detects that it's inside a container and checks basic nesting
support (via `unshare`), but the `unshare` check can pass while BPF is still blocked,
so the above settings are still required.

### Kernel notes

On kernels with `apparmor_restrict_unprivileged_userns=1` (Ubuntu 24.04+), the
BPF interception settings on the outer container are essential — AppArmor will
block the BPF syscall even with `security.nesting=true` alone.
