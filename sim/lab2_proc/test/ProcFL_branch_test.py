#=========================================================================
# ProcFL_branch_test.py
#=========================================================================

import pytest
import random

from pymtl   import *
from harness import *
from lab2_proc.ProcFL import ProcFL

#-------------------------------------------------------------------------
# beq
#-------------------------------------------------------------------------

import inst_beq

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_beq.gen_basic_test ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_beq.gen_basic_test             ),
  asm_test( inst_beq.gen_src0_dep_taken_test    ),
  asm_test( inst_beq.gen_src0_dep_nottaken_test ),
  asm_test( inst_beq.gen_src1_dep_taken_test    ),
  asm_test( inst_beq.gen_src1_dep_nottaken_test ),
  asm_test( inst_beq.gen_srcs_dep_taken_test    ),
  asm_test( inst_beq.gen_srcs_dep_nottaken_test ),
  asm_test( inst_beq.gen_src0_eq_src1_test      ),
  asm_test( inst_beq.gen_value_test             ),
  asm_test( inst_beq.gen_random_test            ),
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_beq( name, test, dump_vcd ):
  run_test( ProcFL, test, dump_vcd )

#-------------------------------------------------------------------------
# bne
#-------------------------------------------------------------------------

import inst_bne

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_bne.gen_basic_test             ),
  asm_test( inst_bne.gen_src0_dep_taken_test    ),
  asm_test( inst_bne.gen_src0_dep_nottaken_test ),
  asm_test( inst_bne.gen_src1_dep_taken_test    ),
  asm_test( inst_bne.gen_src1_dep_nottaken_test ),
  asm_test( inst_bne.gen_srcs_dep_taken_test    ),
  asm_test( inst_bne.gen_srcs_dep_nottaken_test ),
  asm_test( inst_bne.gen_src0_eq_src1_test      ),
  asm_test( inst_bne.gen_value_test             ),
  asm_test( inst_bne.gen_random_test            ),
  asm_test( inst_bne.gen_lw_bne_eval_test       ),
])
def test_bne( name, test, dump_vcd ):
  run_test( ProcFL, test, dump_vcd )

#-------------------------------------------------------------------------
# bge
#-------------------------------------------------------------------------

import inst_bges

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_bges.gen_basic_test             ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_bges.gen_basic_test             ),
  asm_test( inst_bges.gen_src0_dep_taken_test    ),
  asm_test( inst_bges.gen_src0_dep_nottaken_test ),
  asm_test( inst_bges.gen_src1_dep_taken_test    ),
  asm_test( inst_bges.gen_src1_dep_nottaken_test ),
  asm_test( inst_bges.gen_srcs_dep_taken_test    ),
  asm_test( inst_bges.gen_srcs_dep_nottaken_test ),
  asm_test( inst_bges.gen_src0_eq_src1_test      ),
  asm_test( inst_bges.gen_value_test             ),
  asm_test( inst_bges.gen_random_test            ),
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_bges( name, test, dump_vcd ):
  run_test( ProcFL, test, dump_vcd )

#-------------------------------------------------------------------------
# bgeu
#-------------------------------------------------------------------------

import inst_bgeu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_bgeu.gen_basic_test             ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_bgeu.gen_basic_test             ),
  asm_test( inst_bgeu.gen_src0_dep_taken_test    ),
  asm_test( inst_bgeu.gen_src0_dep_nottaken_test ),
  asm_test( inst_bgeu.gen_src1_dep_taken_test    ),
  asm_test( inst_bgeu.gen_src1_dep_nottaken_test ),
  asm_test( inst_bgeu.gen_srcs_dep_taken_test    ),
  asm_test( inst_bgeu.gen_srcs_dep_nottaken_test ),
  asm_test( inst_bgeu.gen_src0_eq_src1_test      ),
  asm_test( inst_bgeu.gen_value_test             ),
  asm_test( inst_bgeu.gen_random_test            ),
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_bgeu( name, test, dump_vcd ):
  run_test( ProcFL, test, dump_vcd )

#-------------------------------------------------------------------------
# blt
#-------------------------------------------------------------------------

import inst_blts

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_blts.gen_basic_test             ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_blts.gen_src0_dep_taken_test    ),
  asm_test( inst_blts.gen_src0_dep_nottaken_test ),
  asm_test( inst_blts.gen_src0_dep_nottaken_test ),
  asm_test( inst_blts.gen_src1_dep_taken_test    ),
  asm_test( inst_blts.gen_src1_dep_nottaken_test ),
  asm_test( inst_blts.gen_srcs_dep_taken_test    ),
  asm_test( inst_blts.gen_srcs_dep_nottaken_test ),
  asm_test( inst_blts.gen_src0_eq_src1_test      ),
  asm_test( inst_blts.gen_value_test             ),
  asm_test( inst_blts.gen_random_test            ),
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_blts( name, test, dump_vcd ):
  run_test( ProcFL, test, dump_vcd )

#-------------------------------------------------------------------------
# bltu
#-------------------------------------------------------------------------

import inst_bltu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_bltu.gen_basic_test             ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_bltu.gen_src0_dep_taken_test    ),
  asm_test( inst_bltu.gen_src0_dep_nottaken_test ),
  asm_test( inst_bltu.gen_src0_dep_nottaken_test ),
  asm_test( inst_bltu.gen_src1_dep_taken_test    ),
  asm_test( inst_bltu.gen_src1_dep_nottaken_test ),
  asm_test( inst_bltu.gen_srcs_dep_taken_test    ),
  asm_test( inst_bltu.gen_srcs_dep_nottaken_test ),
  asm_test( inst_bltu.gen_src0_eq_src1_test      ),
  asm_test( inst_bltu.gen_value_test             ),
  asm_test( inst_bltu.gen_random_test            ),
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_bltu( name, test, dump_vcd ):
  run_test( ProcFL, test, dump_vcd )

