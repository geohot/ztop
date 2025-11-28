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
sudo ./ztop.py
```

Gets battery watts every second by reading regs right from the EC. (30 sec with ACPI)

Reads the MSR for CPU package watts.

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

## CPU (RyzenAdj)

This seems to be the tool to adjust the CPU power.

`sudo ./ryzenadj --info` shows all the knobs.

```
|        Name         |   Value   |     Parameter      |
|---------------------|-----------|--------------------|
| STAPM LIMIT         |    60.000 | stapm-limit        |
| STAPM VALUE         |     4.272 |                    |
| PPT LIMIT FAST      |    60.000 | fast-limit         |
| PPT VALUE FAST      |     6.396 |                    |
| PPT LIMIT SLOW      |    20.000 | slow-limit         |
| PPT VALUE SLOW      |     4.240 |                    |
| StapmTimeConst      |       nan | stapm-time         |
| SlowPPTTimeConst    |       nan | slow-time          |
| PPT LIMIT APU       |    70.000 | apu-slow-limit     |
| PPT VALUE APU       |     0.000 |                    |
| TDC LIMIT VDD       |       nan | vrm-current        |
| TDC VALUE VDD       |       nan |                    |
| TDC LIMIT SOC       |       nan | vrmsoc-current     |
| TDC VALUE SOC       |       nan |                    |
| EDC LIMIT VDD       |       nan | vrmmax-current     |
| EDC VALUE VDD       |       nan |                    |
| EDC LIMIT SOC       |       nan | vrmsocmax-current  |
| EDC VALUE SOC       |       nan |                    |
| THM LIMIT CORE      |   100.000 | tctl-temp          |
| THM VALUE CORE      |    38.754 |                    |
| STT LIMIT APU       |   100.000 | apu-skin-temp      |
| STT VALUE APU       |    38.754 |                    |
| STT LIMIT dGPU      |   100.000 | dgpu-skin-temp     |
| STT VALUE dGPU      |    38.785 |                    |
| CCLK Boost SETPOINT |       nan | power-saving /     |
| CCLK BUSY VALUE     |       nan | max-performance    |
```

Lowest I have seen is 3.59W
