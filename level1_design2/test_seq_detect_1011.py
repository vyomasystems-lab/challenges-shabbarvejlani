# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    valid_seq = "1011"
    for ii in range(len(valid_seq)):
        await FallingEdge(dut.clk)
        dut.inp_bit.value = int(valid_seq[ii])
        #print(valid_seq[ii])
    await FallingEdge(dut.clk)
    print(dut.seq_seen.value)    
    cocotb.log.info('#### CTB: Develop your test here! ######')
