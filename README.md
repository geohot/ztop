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

For package watts, we read from the CPU's SMU.

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


## Experiments

I connected over SSH on USB network.

```
# kills WiFi
sudo rfkill block wifi
# kills hyprland
sudo systemctl stop display-manager
# turns off display
echo 1 | sudo tee /sys/class/graphics/fb0/blank
```

And now we are down to 2.7W on the APU and 3.7W on the laptop

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

Lowest I have seen is 3.25W by ryzenadj + disabling cores


## GPU

```
# sudo cat /sys/kernel/debug/dri/1/amdgpu_pm_info
GFX Clocks and Power:
        400 MHz (MCLK)
        600 MHz (SCLK)
        0 MHz (PSTATE_SCLK)
        0 MHz (PSTATE_MCLK)
        0 mV (VDDGFX)
        0 mV (VDDNB)
        4.11 W (average SoC including CPU)
        4.11 W (current SoC including CPU)

GPU Temperature: 39 C
GPU Load: 1 %
VCN Load: 0 %

SMC Feature Mask: 0x5eb5f3f2cbfffffd
VCN: Powered down

Clock Gating Flags Mask: 0x3bc38130d
        Graphics Fine Grain Clock Gating: On
        Graphics Medium Grain Clock Gating: On
        Graphics Medium Grain memory Light Sleep: Off
        Graphics Coarse Grain Clock Gating: On
        Graphics Coarse Grain memory Light Sleep: On
        Graphics Coarse Grain Tree Shader Clock Gating: Off
        Graphics Coarse Grain Tree Shader Light Sleep: Off
        Graphics Command Processor Light Sleep: Off
        Graphics Run List Controller Light Sleep: Off
        Graphics 3D Coarse Grain Clock Gating: On
        Graphics 3D Coarse Grain memory Light Sleep: On
        Memory Controller Light Sleep: On
        Memory Controller Medium Grain Clock Gating: On
        System Direct Memory Access Light Sleep: Off
        System Direct Memory Access Medium Grain Clock Gating: Off
        Bus Interface Medium Grain Clock Gating: On
        Bus Interface Light Sleep: On
        Unified Video Decoder Medium Grain Clock Gating: Off
        Video Compression Engine Medium Grain Clock Gating: Off
        Host Data Path Light Sleep: Off
        Host Data Path Medium Grain Clock Gating: Off
        Digital Right Management Medium Grain Clock Gating: Off
        Digital Right Management Light Sleep: Off
        Rom Medium Grain Clock Gating: Off
        Data Fabric Medium Grain Clock Gating: Off
        VCN Medium Grain Clock Gating: Off
        Host Data Path Deep Sleep: Off
        Host Data Path Shutdown: On
        Interrupt Handler Clock Gating: On
        JPEG Medium Grain Clock Gating: Off
        Repeater Fine Grain Clock Gating: On
        Perfmon Clock Gating: On
        Address Translation Hub Medium Grain Clock Gating: On
        Address Translation Hub Light Sleep: On
```
