# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

from model_mkbitmanip import *

from collections import defaultdict

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

def generate_valid_instr(instr_enc_map, instr):
    enc_list = instr_enc_map[instr]
    dec_list = []
    for value in enc_list:                
        if value == "rs1" or value == "rs2" or value == "rd" or value == "rs3":
            dec_value = bin(random.randint(0,31))[2:].zfill(5)
        elif value == "imm":
            dec_value = bin(random.randint(0,127))[2:].zfill(7)
        elif value == "imm6":
            dec_value = bin(random.randint(0,63))[2:].zfill(6)
        else:    
            dec_value = value
        dec_list.append(dec_value)
    instr = "".join(dec_list)
    #print(instr)
    return instr

# Sample Test
@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # input transaction


    instr_enc= defaultdict()
    instr_enc['AND']     = ["0000000", "rs2", "rs1", "111", "rd", "0110011"]
    instr_enc['OR']      = ["0000000", "rs2", "rs1", "110", "rd", "0110011"]
    instr_enc['XOR']     = ["0000000", "rs2", "rs1", "100", "rd", "0110011"]
    instr_enc['ANDN']    = ["0100000", "rs2", "rs1", "111", "rd", "0110011"]
    instr_enc['ORN']     = ["0100000", "rs2", "rs1", "110", "rd", "0110011"]
    instr_enc['XNOR']    = ["0100000", "rs2", "rs1", "100", "rd", "0110011"]
    
    instr_enc['SLL']     = ["0000000", "rs2", "rs1", "001", "rd", "0110011"]
    instr_enc['SRL']     = ["0000000", "rs2", "rs1", "101", "rd", "0110011"]
    instr_enc['SRA']     = ["0100000", "rs2", "rs1", "101", "rd", "0110011"]
    instr_enc['SLO']     = ["0010000", "rs2", "rs1", "001", "rd", "0110011"]
    instr_enc['SRO']     = ["0010000", "rs2", "rs1", "101", "rd", "0110011"]
    instr_enc['ROL']     = ["0110000", "rs2", "rs1", "001", "rd", "0110011"]
    instr_enc['ROR']     = ["0110000", "rs2", "rs1", "101", "rd", "0110011"]
    
    instr_enc['SBCLR']   = ["0100100", "rs2", "rs1", "001", "rd", "0110011"]
    instr_enc['SBSET']   = ["0010100", "rs2", "rs1", "001", "rd", "0110011"]
    instr_enc['SBINV']   = ["0110100", "rs2", "rs1", "001", "rd", "0110011"]
    instr_enc['SBEXT']   = ["0100100", "rs2", "rs1", "101", "rd", "0110011"]
    instr_enc['GORC']    = ["0010100", "rs2", "rs1", "101", "rd", "0110011"]
    instr_enc['GREV']    = ["0110100", "rs2", "rs1", "101", "rd", "0110011"]

    instr_enc['SLLI']    = ["00000",   "imm", "rs1", "001", "rd", "0010011"]
    instr_enc['SRLI']    = ["00000",   "imm", "rs1", "101", "rd", "0010011"]
    instr_enc['SRAI']    = ["01000",   "imm", "rs1", "101", "rd", "0010011"]
    instr_enc['SLOI']    = ["00100",   "imm", "rs1", "001", "rd", "0010011"]
    instr_enc['SROI']    = ["00100",   "imm", "rs1", "101", "rd", "0010011"]
    instr_enc['RORI']    = ["01100",   "imm", "rs1", "101", "rd", "0010011"]

    instr_enc['SBCLRI']  = ["01001",   "imm", "rs1", "001", "rd", "0010011"]
    instr_enc['SBSETI']  = ["00101",   "imm", "rs1", "001", "rd", "0010011"]
    instr_enc['SBINVI']  = ["01101",   "imm", "rs1", "001", "rd", "0010011"]
    instr_enc['SBEXTI']  = ["01001",   "imm", "rs1", "101", "rd", "0010011"]
    instr_enc['GORCI']   = ["00101",   "imm", "rs1", "101", "rd", "0010011"]
    instr_enc['GREVI']   = ["01101",   "imm", "rs1", "101", "rd", "0010011"]

    instr_enc['CMIX']    = ["rs3", "11", "rs2", "rs1", "001", "rd", "0110011"]
    instr_enc['CMOV']    = ["rs3", "11", "rs2", "rs1", "101", "rd", "0110011"]
    instr_enc['FSL']     = ["rs3", "10", "rs2", "rs1", "101", "rd", "0110011"]
    instr_enc['FSR']     = ["rs3", "10", "rs2", "rs1", "101", "rd", "0110011"]
    instr_enc['FSRI']    = ["rs3", "1", "imm6", "rs1", "101", "rd", "0110011"]

    instr_not_modelled_list = ['AND', 'OR', 'XOR', 'SLL', 'SRL', 'SRA', 'SLLI', 'SRLI', 'SRAI']    
    #instr_w_issues = ['ANDN']
    instr_w_issues = []
    instr_not_modelled_list = instr_not_modelled_list + instr_w_issues
    all_instr = list(instr_enc.keys())
    instr_set = []
    for ii  in all_instr:
        if ii not in instr_not_modelled_list:
            instr_set.append(ii)
    
    for ii in range(10000):  
        mav_putvalue_src1 = random.randint(0,31)
        mav_putvalue_src2 = random.randint(0,31)
        mav_putvalue_src3 = random.randint(0,31)
        instr_num = random.randint(0, len(instr_set)-1)
        bin_instr = generate_valid_instr(instr_enc, instr_set[instr_num])
        print(len(bin_instr), instr_set[instr_num])
        mav_putvalue_instr = int(bin_instr,2)
        print(hex(mav_putvalue_instr))

        # expected output from the model
        expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

        # driving the input transaction
        dut.mav_putvalue_src1.value = mav_putvalue_src1
        dut.mav_putvalue_src2.value = mav_putvalue_src2
        dut.mav_putvalue_src3.value = mav_putvalue_src3
        dut.EN_mav_putvalue.value = 1
        dut.mav_putvalue_instr.value = mav_putvalue_instr
    
        yield Timer(1) 

        # obtaining the output
        dut_output = dut.mav_putvalue.value

        cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        assert dut_output == expected_mav_putvalue, error_message
