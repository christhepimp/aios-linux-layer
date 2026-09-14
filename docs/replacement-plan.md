# Phased replacement plan

The product sentence is: *the OS itself is an AI*.

The engineering sentence is: *an AI control plane becomes PID-adjacent and absorbs userspace responsibilities until Linux is only the HAL*.

## Phase 0 — Lab (now)

- Rooted AOSP emulator.
- Aether supervisor runs as a normal process with root.
- Audit log of every privileged action.

## Phase 1 — Session OS

Replace the human's primary interface:

- no more raw `sh` as the daily driver
- Aether is login + shell + help + memory
- tools wrap `ps`, mounts, packages, files, network

Success: you can live in the emulator without thinking "I am in Android".

## Phase 2 — Policy OS

Aether decides:

- which packages may run
- which networks are allowed
- which paths are writable by the model

This is `policy/allowlist.yaml` growing teeth (seccomp, cgroups, iptables/nft, Magisk/KSU policies on device).

## Phase 3 — Service OS

Replace individual Linux/Android userspace pieces one at a time:

| Linux / Android piece | Aether stand-in |
|---|---|
| interactive shell | Aether session |
| package manager UX | Aether package brain |
| init rc snippets we own | Aether service table |
| notification / intent router | Aether event bus |
| settings database UX | Aether state |

We do **not** delete `init` yet. We register *next to* it.

## Phase 4 — Init-adjacent

Run Aether under a custom init script so it starts at boot inside the emulator image. Still Linux kernel.

## Phase 5 — Custom image

Fork AOSP or Android-x86. Ship our own `system.img` with Aether as the default session. Kernel still Linux.

## Phase 6 — Kernel research (later, separate tree)

Only after phases 0–5 are boring:

- custom kernel config
- maybe a unikernel or seL4 experiment for the AI runtime
- this is a different repository and a different decade of work if taken fully seriously

## Definition of done for "the OS is an AI"

You boot the emulator. You never open Settings or a launcher by hand. You tell Aether what you want. It uses tools, explains what it did, and the machine state matches.
