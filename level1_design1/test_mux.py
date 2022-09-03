# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""  
    cocotb.log.info('##### CTB: Develop your test here ########')
    
    for jj in range(32):
        dut.sel.value = jj    
        for ii in range(31):
            if ii != jj:
                getattr(dut, "inp%0d"%(ii)).value = 0
            else:
                getattr(dut, "inp%0d"%(ii)).value = 1
        await Timer(2, units='ns')
        if (jj == 31):
            assert dut.out.value == 0, f"Mux output is incorrect for sel{jj}"
        else:
            assert dut.out.value == 1, f"Mux output is incorrect for sel{jj}"    
                                   
    
