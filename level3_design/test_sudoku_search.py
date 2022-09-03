# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path
import math

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

def read_sudoku_data():
  fh = open("./sudoku/trunk/verif/puzzles/puzzle_0.hex", 'r')	
  data = fh.readlines()
  data_bin = []
  for ii in range(81):
    val = data[ii].strip()
    bin_val = bin(int(val, 16))[2:].zfill(9)
    data_bin.append(bin_val)
  data_bin = "".join(data_bin)
  print(len(data_bin))
  #print(data_bin)
  fh.close()
  return data_bin

def print_dut_out(dut):
  sudoku_out = []
  for ii in range(9):  
    for jj in range(9):
      digit = []
      for kk in range(9):
        digit.append(str(dut.outGrid[81*ii + 9*jj + kk].value))
      digit_one_hot = int("".join(digit), 2)
      digit_dec = int(math.log(digit_one_hot, 2.0)) + 1
      #print(digit_dec)
      sudoku_out.append(digit_dec)
  for ii in range(81):
    print(sudoku_out[ii], end=' ')
    if ((ii + 1) % 9 == 0) and (ii != 0):
       print("")
  print("")

@cocotb.test()
async def test_basic(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.rst.value = 1
    await FallingEdge(dut.clk)  
    dut.rst.value = 0
    await FallingEdge(dut.clk)
    data_in = read_sudoku_data()
    for ii in range(729):
    	dut.inGrid[ii].value = int(data_in[ii])	

    await FallingEdge(dut.clk)
    dut.start.value = 1
    #print(hex(dut.inGrid.value))
    await RisingEdge(dut.done)
    await FallingEdge(dut.clk)
    print(dut.error.value)
    print_dut_out(dut)
    cocotb.log.info('#### CTB: Develop your test here! ######')
