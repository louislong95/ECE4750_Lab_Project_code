#=========================================================================
# ProcBaseRTL_test.py
#=========================================================================

import pytest
import random

from pymtl   import *
from harness import *
from lab2_proc.ProcBaseRTL import ProcBaseRTL

#-------------------------------------------------------------------------
# jal
#-------------------------------------------------------------------------

import inst_jals

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_jals.gen_basic_test        ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_jals.gen_no_nop_test       ) ,
  asm_test( inst_jals.gen_stall_before_test ) ,
  asm_test( inst_jals.gen_jal_eval_test     ) ,
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])

def test_jals( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_jals_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_jals.gen_jal_eval_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_jals_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_jals.gen_jal_eval_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_jals_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_jals.gen_jal_eval_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_jals_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_jals.gen_jal_eval_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=10 )

def test_jals_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_jals.gen_jal_eval_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=10 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# jalr
#-------------------------------------------------------------------------

import inst_jalr

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_jalr.gen_basic_test    ) ,
  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_jalr.gen_no_nop_test   ) ,
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_jalr( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_jalr_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_jalr.gen_no_nop_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_jalr_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_jalr.gen_no_nop_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_jalr_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_jalr.gen_no_nop_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_jalr_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_jalr.gen_no_nop_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=10 )

def test_jalr_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_jalr.gen_no_nop_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=10 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
 