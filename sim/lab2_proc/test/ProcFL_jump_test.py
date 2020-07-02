#=========================================================================
# ProcFL_test.py
#=========================================================================

import pytest
import random

from pymtl   import *
from harness import *
from lab2_proc.ProcFL import ProcFL

#-------------------------------------------------------------------------
# jal
#-------------------------------------------------------------------------

import inst_jals

@pytest.mark.parametrize( "name,test", [
  #asm_test( inst_jals.gen_basic_test        ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  #asm_test( inst_jals.gen_no_nop_test       ) ,
  #asm_test( inst_jals.gen_stall_before_test ) ,
  asm_test( inst_jals.gen_jal_eval_test     ) ,
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_jals( name, test, dump_vcd ):
  run_test( ProcFL, test, dump_vcd )

#-------------------------------------------------------------------------
# jalr
#-------------------------------------------------------------------------

import inst_jalr

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_jalr.gen_basic_test    ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_jalr.gen_no_nop_test   ) ,
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_jalr( name, test, dump_vcd ):
  run_test( ProcFL, test, dump_vcd )
