# Aether OS (aios-linux-layer)

Research project: an **AI-native operating layer** that runs on top of Linux inside a **rooted Android emulator** (or any Linux host), then gradually takes over userspace jobs that a traditional OS would do.

> Honest scope: we are **not** replacing the Linux kernel in one shot. Android *is* Linux. A real kernel rewrite is a multi-year systems project. This repo starts where it is actually possible: **root + userspace supervisor + AI policy engine**, then we peel services off Linux one by one.

Repo: https://github.com/christhepimp/aios-linux-layer

## Goal

Build an OS *personality* and *control plane*:

- The user talks to an AI that *is* the shell, scheduler advisor, package brain, and policy engine.
- Linux (kernel + init) stays underneath as the hardware abstraction.
- Over time we replace userspace daemons (init scripts, package manager, window/session manager, network policy, storage policy) with Aether-owned services.
- The AI is not a chat app on the OS. The AI *is* the OS interface.

## Recommended rooted Android environments (2026)

Best-first for *this* project:

| Environment | Root | Linux access | Why use it |
|---|---|---|---|
| **Android Studio Emulator** (AOSP / Google APIs image, not Play Store image) | Yes — `adb root` works on AOSP AVDs | Full `adb shell` as root | Official, scriptable, free, best for development |
| **Genymotion Desktop / SaaS** | Yes on supported images (can root dynamically) | Root shell + sensors + APIs | Fast, used for QA and security work |
| **Android-x86 / Bliss OS** in VirtualBox/QEMU | Can be rooted | Closest to a real x86 Android-on-PC | Good if you want a full disk you can mutate |
| **Waydroid** (on Linux host) | Possible with extra work | Shares the *host* Linux kernel | Fast, but you are not isolating a guest kernel |
| Gaming emulators (BlueStacks, LDPlayer, Nox) | Often have a root toggle | Messy, closed, anti-cheat noise | Avoid as the primary lab |

Practical lab path we document in `docs/emulator-lab.md`:

1. Install Android Studio.
2. Create an **AOSP** or **Google APIs** virtual device (not Google Play).
3. `adb root` then `adb shell` — you are already `#`.
4. Push the Aether supervisor and talk to it as the session.

On a *physical* rooted phone the same supervisor can run via Magisk/KernelSU + Termux, but the emulator is the safer lab.

## What we will NOT do in v0

- Rewrite `kernel/` from Android Open Source Project and flash it as a custom boot.img on day one.
- Claim this is a drop-in Linux replacement.
- Ship a binary that jailbreaks random devices.

Those are later, explicit milestones with signed images and a real kernel tree.

## Architecture (v0)

```
+------------------------------------------------------+
|  Aether Session  (AI OS face)                        |
|  natural language + tools + policy                   |
+---------------------------+--------------------------+
|  Aether Supervisor        |  Skill plugins           |
|  pid 1-adjacent userspace |  files, net, packages    |
+---------------------------+--------------------------+
|  Linux kernel (Android or host)                      |
|  drivers, cgroups, namespaces, seccomp               |
+------------------------------------------------------+
```

v0 code lives in `supervisor/` — a Python process that:

- owns a root shell when available
- exposes an AI command loop
- can inspect `/proc`, packages, mounts, network
- records every privileged action in an audit log
- never runs unsigned shell from the model without a confirm policy

## Repo map

```
docs/emulator-lab.md     how to stand up a rooted AVD
docs/replacement-plan.md phased takeover of userspace
supervisor/aether.py     AI OS loop (offline stub + tool runtime)
supervisor/tools.py      privileged tools with audit
policy/allowlist.yaml    what the AI may touch
```

## Quick start (Linux / macOS host)

```bash
cd supervisor
python3 aether.py
```

Inside a rooted emulator after `adb root`:

```bash
adb push supervisor /data/local/tmp/aether
adb shell
cd /data/local/tmp/aether
python3 aether.py   # or install python first
```

## License

MIT. Research software. Do not run the supervisor as a daily driver yet.
