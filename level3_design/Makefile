# See LICENSE.vyoma for details

TOPLEVEL_LANG ?= verilog
PWD=$(shell pwd)
VERILOG_SOURCES = $(PWD)/sudoku/trunk/rtl/piece.v  $(PWD)/sudoku/trunk/rtl/sudoku.v  $(PWD)/sudoku/trunk/rtl/minPiece.v  $(PWD)/sudoku/trunk/rtl/sudoku_search.v # provide your design path

TOPLEVEL := sudoku_search # design file
MODULE   := test_sudoku_search # test file

include $(shell cocotb-config --makefiles)/Makefile.sim

clean_all: clean
	rm -rf *.xml sim_build __pycache__ 
