# ztop

Power monitoring for HP ZBook Strix Halo.

One of the key features of MacBook's is good power management. It's the main thing that makes Linux on a laptop hard to use.

## The Laptop

HP ZBook Ultra G1a: MAX PRO 390, 64GB RAM, OLED display, 74.5 Wh battery

The CPU/GPU in this laptop is great, the first one I have used that's close to MacBook tier.

## Lid closed

With amd-s2idle, I got lid closed idle power down to 0.14W-0.20W.

I needed to disable the IOMMU in kernel args and disable the webcam in BIOS.

That's 15 days of lid closed power, that's good enough.

## Lid open

CPU draws min 4W, whole laptop min 7W

Parts
* Screen -- Only like 1 watt on a dark mode screen
* Keyboard backlight -- 2 stupid watts, leave it off

Looking into other things.
* Is there any way to get the CPU below 4?
* What are the other 3 watts in the laptop I can't remove?

## Usage

```bash
sudo modprobe ec_sys
sudo ./ztop.py
```

We found a fast way to get battery W (every second) by reading regs right from the EC.
We read the MSR for CPU package W

```

                  ▁
           ▃      █
▁ ▁ ▁▁▅▁▂▁▁█▁▁▁ ▄▂█▃▁ ▂▃    ▁
█████████████████████▂████▇███
██████████████████████████████
██████████████████████████████
pkg (W):    4.09



                  ▁
                  █
            ▄     █▆
▆           █     ██
█▁   ▃ █▁▄█ █ ▂ ▃▇██▂ ▂▃   ▃
██▂▅▄█▆████▇█▇█▃████████▆███▄▃
██████████████████████████████
██████████████████████████████
██████████████████████████████
██████████████████████████████
██████████████████████████████
██████████████████████████████
bat (W):    7.38
```