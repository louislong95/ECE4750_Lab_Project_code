#=========================================================================
# ProcBaseRTL_alu_test.py
#=========================================================================

import pytest
import random

from pymtl   import *
from harness import *
from lab2_proc.ProcBaseRTL import ProcBaseRTL

#-------------------------------------------------------------------------
# addi
#-------------------------------------------------------------------------

import inst_addi

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_addi.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_addi.gen_dest_dep_test  ),
  asm_test( inst_addi.gen_src_dep_test   ),
  asm_test( inst_addi.gen_src_eq_dest_test ) ,
  asm_test( inst_addi.gen_value_test     ),
  asm_test( inst_addi.gen_random_test              ),
  
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_addi( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_addi_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_addi.gen_random_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_addi_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_addi.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_addi_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_addi.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_addi_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_addi.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=10 )

def test_addi_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_addi.gen_random_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=10 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# andi
#-------------------------------------------------------------------------

import inst_andi

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_andi.gen_basic_test     ) ,
  asm_test( inst_andi.gen_dest_dep_test  ) ,
  asm_test( inst_andi.gen_src_dep_test   ) ,
  asm_test( inst_andi.gen_src_eq_dest_test ) ,
  asm_test( inst_andi.gen_value_test     ) ,
  asm_test( inst_andi.gen_random_test    ) ,
])
def test_andi( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_andi_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_andi.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# ori
#-------------------------------------------------------------------------

import inst_ori

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_ori.gen_basic_test     ) ,
  asm_test( inst_ori.gen_dest_dep_test  ) ,
  asm_test( inst_ori.gen_src_dep_test   ) ,
  asm_test( inst_ori.gen_src_eq_dest_test ) ,
  asm_test( inst_ori.gen_value_test     ) ,
  asm_test( inst_ori.gen_random_test    ) ,
])
def test_ori( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_ori_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_ori.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# xori
#-------------------------------------------------------------------------

import inst_xori

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_xori.gen_basic_test     ) ,
  asm_test( inst_xori.gen_dest_dep_test  ) ,
  asm_test( inst_xori.gen_src_dep_test   ) ,
  asm_test( inst_xori.gen_src_eq_dest_test ) ,
  asm_test( inst_xori.gen_value_test     ) ,
  asm_test( inst_xori.gen_random_test    ) ,
])
def test_xori( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_xori_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_xori.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# slti
#-------------------------------------------------------------------------

import inst_sltis

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_sltis.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.

  asm_test( inst_sltis.gen_dest_dep_test  ) ,
  asm_test( inst_sltis.gen_src_dep_test   ) ,
  asm_test( inst_sltis.gen_src_eq_dest_test ) ,
  asm_test( inst_sltis.gen_value_test     ),
  asm_test( inst_sltis.gen_random_test    ) ,

  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_sltis( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_sltis_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_sltis.gen_random_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_sltis_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_sltis.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_sltis_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_sltis.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_sltis_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_sltis.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=10 )

def test_sltis_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_sltis.gen_random_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=10 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# sltiu
#-------------------------------------------------------------------------

import inst_sltiu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_sltiu.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_sltiu.gen_dest_dep_test  ) ,
  asm_test( inst_sltiu.gen_src_dep_test   ) ,
  asm_test( inst_sltiu.gen_src_eq_dest_test ) ,
  asm_test( inst_sltiu.gen_value_test     ),
  asm_test( inst_sltiu.gen_random_test    ) ,
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_sltiu( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_sltiu_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_sltiu.gen_random_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_sltiu_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_sltiu.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_sltiu_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_sltiu.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_sltiu_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_sltiu.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=10 )

def test_sltiu_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_sltiu.gen_random_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=10 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# srai
#-------------------------------------------------------------------------

import inst_srai

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_srai.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_srai.gen_dest_dep_test  ) ,
  asm_test( inst_srai.gen_src_dep_test   ),
  asm_test( inst_srai.gen_src_eq_dest_test   ),
  asm_test( inst_srai.gen_value_test   ),
  asm_test( inst_srai.gen_random_test    ) ,
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_srai( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_srai_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_srai.gen_random_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_srai_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_srai.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_srai_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_srai.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_srai_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_srai.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=10 )

def test_srai_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_srai.gen_random_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=10 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# srli
#-------------------------------------------------------------------------

import inst_srli

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_srli.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_srli.gen_dest_dep_test  ) ,
  asm_test( inst_srli.gen_src_dep_test   ),
  asm_test( inst_srli.gen_src_eq_dest_test   ),
  asm_test( inst_srli.gen_value_test   ),
  asm_test( inst_srli.gen_random_test    ) ,
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_srli( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_srli_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_srli.gen_random_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_srli_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_srli.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_srli_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_srli.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_srli_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_srli.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=10 )

def test_srli_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_srli.gen_random_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=10 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# slli
#-------------------------------------------------------------------------

import inst_slli

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_slli.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_slli.gen_dest_dep_test  ) ,
  asm_test( inst_slli.gen_src_dep_test   ),
  asm_test( inst_slli.gen_src_eq_dest_test   ),
  asm_test( inst_slli.gen_value_test   ),
  asm_test( inst_slli.gen_random_test    ) ,
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_slli( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_slli_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_slli.gen_random_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )
 
def test_slli_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_slli.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_slli_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_slli.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_slli_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_slli.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=10 )

def test_slli_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_slli.gen_random_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=10 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# lui
#-------------------------------------------------------------------------

import inst_lui

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_lui.gen_basic_test    ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_lui.gen_dest_dep_test  ) ,
  asm_test( inst_lui.gen_value_test   ),
  asm_test( inst_lui.gen_random_test    ) ,
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_lui( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_lui_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_lui.gen_random_test, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_lui_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_lui.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_lui_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_lui.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_lui_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_lui.gen_random_test, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=10 )

def test_lui_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_lui.gen_random_test, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=10 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# auipc
#-------------------------------------------------------------------------

import inst_auipc

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_auipc.gen_basic_test    ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  asm_test( inst_auipc.gen_no_nop_after ),
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_auipc( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
def test_auipc_rand_delays_1( dump_vcd ):
  run_test( ProcBaseRTL, inst_auipc.gen_no_nop_after, dump_vcd,
            src_delay=0, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_auipc_rand_delays_2( dump_vcd ):
  run_test( ProcBaseRTL, inst_auipc.gen_no_nop_after, dump_vcd,
            src_delay=5, sink_delay=0, mem_stall_prob=0.5, mem_latency=3 )

def test_auipc_rand_delays_3( dump_vcd ):
  run_test( ProcBaseRTL, inst_auipc.gen_no_nop_after, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

def test_auipc_rand_delays_4( dump_vcd ):
  run_test( ProcBaseRTL, inst_auipc.gen_no_nop_after, dump_vcd,
            src_delay=5, sink_delay=5, mem_stall_prob=0.5, mem_latency=10 )

def test_auipc_rand_delays_5( dump_vcd ):
  run_test( ProcBaseRTL, inst_auipc.gen_no_nop_after, dump_vcd,
            src_delay=10, sink_delay=10, mem_stall_prob=0.8, mem_latency=10 )
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
