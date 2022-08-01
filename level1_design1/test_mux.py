# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""  
    for sel in range(2):
        dut.sel.value = sel
        if (sel == 0):
            dut.inp0.value = random.randint(0,3)
            await Timer(2, units='ns')
            assert dut.out.value == dut.inp0.value, f"Mux output is incorrect {dut.out.value != dut.inp0.value}"
        if (sel == 1):
            dut.inp1.value = random.randint(0,3)
            await Timer(2, units='ns')
            assert dut.out.value == dut.inp1.value, f"Mux output is incorrect {dut.out.value != dut.inp1.value}"   
        if (sel == 2):
            dut.inp2.value = random.randint(0,3)
            await Timer(2, units='ns')
            assert dut.out.value == dut.inp2.value, f"Mux output is incorrect {dut.out.value != dut.inp2.value}"
        if (sel == 3):
            dut.inp3.value = random.randint(0,3)
            await Timer(2, units='ns')
            assert dut.out.value == dut.inp3.value, f"Mux output is incorrect {dut.out.value != dut.inp3.value}"                            
        if (sel == 4):
            dut.inp4.value = random.randint(0,3)
            await Timer(2, units='ns')
            assert dut.out.value == dut.inp4.value, f"Mux output is incorrect {dut.out.value != dut.inp4.value}"            
        if (sel == 5):
            dut.inp5.value = random.randint(0,3)
            await Timer(2, units='ns')
            assert dut.out.value == dut.inp5.value, f"Mux output is incorrect {dut.out.value != dut.inp5.value}"                        
        if (sel == 6):
            dut.inp6.value = random.randint(0,3)
            await Timer(2, units='ns')
            assert dut.out.value == dut.inp6.value, f"Mux output is incorrect {dut.out.value != dut.inp6.value}"                        
    cocotb.log.info('##### CTB: Develop your test here ########')
