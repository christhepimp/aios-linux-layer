# Rooted Android emulator lab

## Why an emulator first

You asked to find a rooted Android emulator, get inside the Linux userspace, and start replacing Linux with an AI OS.

The emulator is the right first machine because:

- AOSP virtual devices already run `adbd` as root (`adb root`).
- You can snapshot, wipe, and break things.
- You are not bricking a phone while we experiment with init and mounts.

## Option A — Android Studio AVD (recommended)

1. Install [Android Studio](https://developer.android.com/studio).
2. Device Manager → Create Device → any phone profile.
3. System image: pick **AOSP** or **Google APIs**. Do **not** pick **Google Play** if you want easy root. Play images lock `adbd`.
4. Start the AVD.
5. From the host:

```bash
adb devices
adb root
adb shell
# prompt should be '#' not '$'
id
uname -a
cat /proc/version
```

You are now inside Android's Linux. The kernel is still Linux. Userspace is Bionic + toybox/toolbox + init (rc files under `/system/etc/init` and `/vendor/etc/init`).

### What you can actually change from here

Writable with root on a typical AVD:

- `/data`
- sometimes `/system` if remounted: `adb remount` or `mount -o rw,remount /system`
- `/data/local/tmp` always

Not writable without a custom image:

- the kernel itself (`/proc/version` is the running kernel)
- boot partitions unless you build an AOSP `boot.img`

## Option B — Genymotion

Genymotion can root supported images dynamically. Good if you want a faster GUI device and sensor injection. Use it the same way: `adb root` + push the supervisor.

## Option C — Android-x86 in QEMU/VirtualBox

Closer to a PC you can dual-boot. Heavier. Useful later when we want our own bootloader path.

## Option D — avoid as primary lab

BlueStacks / LDPlayer / Nox: root toggles exist in some builds, but they are closed, detection-heavy, and a poor place to grow a custom OS.

## After you have a root shell

Push this repo's supervisor and treat it as the session:

```bash
adb push supervisor /data/local/tmp/aether
adb shell "cd /data/local/tmp/aether && python3 aether.py"
```

If the image has no Python, install a static Python or use Termux inside the emulator.

## How this relates to "replacing Linux"

Phases are in `replacement-plan.md`. Short version:

1. Own the *session* (what the user talks to).
2. Own *policy* (what processes may start).
3. Own *userspace services* (network, packages, storage).
4. Only then consider a custom kernel / init replacement.
