#!/usr/bin/env python3
import os, time, struct, math
from pathlib import Path

def spark(vs, rows, pad):
  vs = [0]*(pad-len(vs)) + vs
  blocks = " ▁▂▃▄▅▆▇█"
  def _spark(vs, lo, hi):
    out = []
    for v in vs:
      v = min(max(v, lo), hi)
      i = int((v - lo) / (hi - lo) * (len(blocks) - 1))
      out.append(blocks[i])
    return "".join(out)
  return '\n'.join([_spark(vs, rows-r, rows-r+1) for r in range(rows)])

# low brightness / no keyboard backlight
# 4W for CPU
# 7W for laptop

def read_uj(): return time.perf_counter_ns(), int(Path("/sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/energy_uj").read_text())
last_uj = read_uj()

HIST = 40
pkg_history = []
bat_history = []
def draw():
  global last_uj, pkg_history, bat_history
  print("\033[2J\033[H", end="")

  # we fetch the battery current/voltage from the EC for faster update (every second)
  # sudo modprobe ec_sys
  #raw_dat = Path("/sys/kernel/debug/ec/ec0/io").read_bytes()
  #prt = [f"{d:02X}" for d in raw_dat]
  #print('\n'.join([' '.join(prt[i:i+0x10]) for i in range(0, len(raw_dat), 0x10)]))

  #pkg_draw = int(Path("/sys/class/hwmon/hwmon4/power1_input").read_text())/1e6
  #print(f"pkg (W): {pkg_draw:7.2f}")

  with Path("/sys/kernel/debug/ec/ec0/io").open("rb") as f:
    # sudo acpidump -n DSDT -b
    # iasl -d dsdt.dat
    f.seek(0x9d)
    bpr = struct.unpack("H", f.read(2))[0]
    f.seek(0xa5)
    bpv = struct.unpack("H", f.read(2))[0]
    bat_w = (bpr*bpv)/1e6

  uj = read_uj()
  pkg_w = (uj[1]-last_uj[1])/((uj[0]-last_uj[0])/1e3)

  pkg_history.append(pkg_w)
  bat_history.append(bat_w)
  pkg_history = pkg_history[-HIST:]
  bat_history = bat_history[-HIST:]
  pkg_min = min(pkg_history)
  pkg_max = max(pkg_history)
  bat_min = min(bat_history)
  bat_max = max(bat_history)

  print(spark(pkg_history, 10, pad=HIST))
  print(f"pkg (W): {pkg_w:6.2f}  [min {pkg_min:6.2f} max {pkg_max:6.2f}]")
  print(spark(bat_history, 20, pad=HIST))
  print(f"bat (W): {bat_w:6.2f}  [min {bat_min:6.2f} max {bat_max:6.2f}]")

  last_uj = uj

if __name__ == "__main__":
  os.system("modprobe ec_sys")
  while 1:
    draw()
    time.sleep(1)

