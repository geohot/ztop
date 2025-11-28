#!/usr/bin/env python3
import os, time, struct
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

HIST = 40
pkg_history = []
bat_history = []
def draw(f_ec, f_pm):
  global pkg_history, bat_history
  print("\033[2J\033[H", end="")

  # we fetch the battery current/voltage from the EC for faster update (every second)
  # sudo modprobe ec_sys
  #raw_dat = Path("/sys/kernel/debug/ec/ec0/io").read_bytes()
  #prt = [f"{d:02X}" for d in raw_dat]
  #print('\n'.join([' '.join(prt[i:i+0x10]) for i in range(0, len(raw_dat), 0x10)]))

  # sudo acpidump -n DSDT -b
  # iasl -d dsdt.dat
  f_ec.seek(0x9d)
  bpr = struct.unpack("H", f_ec.read(2))[0]
  f_ec.seek(0xa5)
  bpv = struct.unpack("H", f_ec.read(2))[0]
  bat_w = (bpr*bpv)/1e6

  # 0xc is the "fast value" in RyzenAdj
  f_pm.seek(0xc)
  pkg_w = struct.unpack("f", f_pm.read(4))[0]

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

if __name__ == "__main__":
  # this was in my kernel
  os.system("modprobe ec_sys")
  # ryzen smu, https://github.com/amkillam/ryzen_smu/tree/main
  os.system("modprobe ryzen_smu")
  f_ec = Path("/sys/kernel/debug/ec/ec0/io").open("rb", buffering=0)
  f_pm = Path("/sys/kernel/ryzen_smu_drv/pm_table").open("rb", buffering=0)
  while 1:
    draw(f_ec, f_pm)
    time.sleep(1)

