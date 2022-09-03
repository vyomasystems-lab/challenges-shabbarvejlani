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
    len_of_stimulus = 10000
    stimulus = []
    for ii in range(len_of_stimulus):
        stimulus.append(random.randint(0, 1)%2)
    #stimulus = ['1', '0', '1', '1','0']
    #print(stimulus)

    prev_list = []
    seq_seen = ""
    debug_seq = []
    for ii in range(len(stimulus)):
        await FallingEdge(dut.clk)
        if seq_seen == valid_seq:
            #print(dut.seq_seen.value)
            assert dut.seq_seen.value == 1, f"fsm output not 1 {seq_seen, debug_seq}"
        dut.inp_bit.value = int(stimulus[ii])
        #print(valid_seq[ii])
        prev_list.append(str(stimulus[ii]))
        if len(prev_list) > 4:
            prev_list = prev_list[-4:]
        seq_seen = "".join(prev_list)
        if ii >20 :
            debug_seq = stimulus[ii-20:ii+1]
        else:
            debug_seq = stimulus[:ii+1]

    
    cocotb.log.info('#### CTB: Develop your test here! ######')
