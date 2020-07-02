#=========================================================================
# ProcBaseRTL_branch_test.py
#=========================================================================

import pytest
import random

from pymtl   import *
from harness import *
from lab2_proc.ProcBaseRTL import ProcBaseRTL

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
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_beq_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_beq.gen_random_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_beq_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_beq.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_beq_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_beq.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_beq_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_beq.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=5 )

def test_beq_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_beq.gen_random_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=3 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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
  run_test( ProcBaseRTL, test, dump_vcd )

def test_bne_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_bne.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3)

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
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_bges_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_bges.gen_random_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_bges_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_bges.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_bges_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_bges.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_bges_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_bges.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=5 )

def test_bges_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_bges.gen_random_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=3 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_bgeu_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_bgeu.gen_random_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_bgeu_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_bgeu.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_bgeu_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_bgeu.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_bgeu_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_bgeu.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=5 )

def test_bgeu_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_bgeu.gen_random_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=3 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_blts_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_blts.gen_random_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_blts_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_blts.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_blts_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_blts.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_blts_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_blts.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=5 )
 
def test_blts_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_blts.gen_random_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=3 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_bltu_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_bltu.gen_random_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_bltu_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_bltu.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_bltu_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_bltu.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_bltu_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_bltu.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=5 )

def test_bltu_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_bltu.gen_random_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=3 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
