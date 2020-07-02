#=========================================================================
# slt
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 4
    csrr x2, mngr2proc < 5
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slt x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
def gen_dest_dep_test():
  return [
    gen_rr_dest_dep_test( 5, "slt", 2, 1, 0 ),
    gen_rr_dest_dep_test( 4, "slt", 2, 2, 0 ),
    gen_rr_dest_dep_test( 3, "slt", 3, 1, 0 ),
    gen_rr_dest_dep_test( 2, "slt", 4, 1, 0 ),
    gen_rr_dest_dep_test( 1, "slt", 5, 1, 0 ),
    gen_rr_dest_dep_test( 0, "slt", 6, 1, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "slt",  15, 10,  0 ),
    gen_rr_src0_dep_test( 4, "slt",  30, 10,  0 ),
    gen_rr_src0_dep_test( 3, "slt",  45, 10, 0 ),
    gen_rr_src0_dep_test( 2, "slt",  57, 10, 0 ),
    gen_rr_src0_dep_test( 1, "slt",  78, 10, 0 ),
    gen_rr_src0_dep_test( 0, "slt", 142, 10, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "slt", 1, 13, 1 ),
    gen_rr_src1_dep_test( 4, "slt", 1, 14, 1 ),
    gen_rr_src1_dep_test( 3, "slt", 1, 15, 1 ),
    gen_rr_src1_dep_test( 2, "slt", 1, 16, 1 ),
    gen_rr_src1_dep_test( 1, "slt", 1, 17, 1 ),
    gen_rr_src1_dep_test( 0, "slt", 1, 18, 1 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "slt", 12, 12, 0 ),
    gen_rr_srcs_dep_test( 4, "slt", 13, 13, 0 ),
    gen_rr_srcs_dep_test( 3, "slt", 14, 14, 0 ),
    gen_rr_srcs_dep_test( 2, "slt", 15, -5, 0 ),
    gen_rr_srcs_dep_test( 1, "slt", 16, -6, 0 ),
    gen_rr_srcs_dep_test( 0, "slt", 17, -7, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "slt", 0, 1, 1 ),
    gen_rr_src1_eq_dest_test( "slt", 26, -1, 0 ),
    gen_rr_src0_eq_src1_test( "slt", -27, 0 ),
    gen_rr_srcs_eq_dest_test( "slt", -280, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "slt", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rr_value_test( "slt", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rr_value_test( "slt", 0x00000007, 0x00000003, 0x00000000 ),

    gen_rr_value_test( "slt", 0x00000000, 0xffff8000, 0x00000000 ),  
    gen_rr_value_test( "slt", 0x80000000, 0x00000000, 0x00000001 ),  
    gen_rr_value_test( "slt", 0x80000000, 0xffff8000, 0x00000001 ),  # -2147483648 vs (-32768)

    gen_rr_value_test( "slt", 0x00000000, 0x00007fff, 0x00000001 ),  # 0 vs 32767 = - 32767
    gen_rr_value_test( "slt", 0x7fffffff, 0x00000000, 0x00000000 ),
    gen_rr_value_test( "slt", 0x7fffffff, 0x00007fff, 0x00000000 ),

    gen_rr_value_test( "slt", 0x80000000, 0x00007fff, 0x00000001 ),   # -2147483648 vs 32767 = -2147516414
    gen_rr_value_test( "slt", 0x7fffffff, 0xffff8000, 0x00000000 ),   

    gen_rr_value_test( "slt", 0x00000000, 0xffffffff, 0x00000000 ),
    gen_rr_value_test( "slt", 0xffffffff, 0x00000001, 0x00000001 ),
    gen_rr_value_test( "slt", 0xffffffff, 0xffffffff, 0x00000000 ),
    gen_rr_value_test( "slt", 0xffffffff, 0x00000000, 0x00000001 ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():  # random test
  asm_code = []
  for i in xrange(100):
    src0  = Bits( 32, random.randint(0,0xffffffff) )
    src1  = Bits( 32, random.randint(0,0xffffffff) )
    #dest = src + sext(imm,32)
    if (src0.int() < src1.int()):
      dest = Bits(32, 0x00000000000000000000000000000001)
    elif (src0.int() >= src1.int()):
      dest = Bits(32, 0x00000000000000000000000000000000)
    asm_code.append( gen_rr_value_test( "slt", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
