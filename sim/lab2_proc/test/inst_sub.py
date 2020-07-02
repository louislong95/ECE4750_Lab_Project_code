#=========================================================================
# sub
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 5
    csrr x2, mngr2proc < 4
    nop
    nop
    sub x3, x1, x2
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
    gen_rr_dest_dep_test( 5, "sub", 2, 1, 1 ),
    gen_rr_dest_dep_test( 4, "sub", 2, 2, 0 ),
    gen_rr_dest_dep_test( 3, "sub", 3, 1, 2 ),
    gen_rr_dest_dep_test( 2, "sub", 4, 1, 3 ),
    gen_rr_dest_dep_test( 1, "sub", 5, 1, 4 ),
    gen_rr_dest_dep_test( 0, "sub", 6, 1, 5 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sub",  15, 10,  5 ),
    gen_rr_src0_dep_test( 4, "sub",  30, 10,  20 ),
    gen_rr_src0_dep_test( 3, "sub",  45, 10, 35 ),
    gen_rr_src0_dep_test( 2, "sub",  57, 10, 47 ),
    gen_rr_src0_dep_test( 1, "sub",  78, 10, 68 ),
    gen_rr_src0_dep_test( 0, "sub", 142, 10, 132 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "sub", 1, 13, -12 ),
    gen_rr_src1_dep_test( 4, "sub", 1, 14, -13 ),
    gen_rr_src1_dep_test( 3, "sub", 1, 15, -14 ),
    gen_rr_src1_dep_test( 2, "sub", 1, 16, -15 ),
    gen_rr_src1_dep_test( 1, "sub", 1, 17, -16 ),
    gen_rr_src1_dep_test( 0, "sub", 1, 18, -17 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sub", 12, 12, 0 ),
    gen_rr_srcs_dep_test( 4, "sub", 13, 13, 0 ),
    gen_rr_srcs_dep_test( 3, "sub", 14, 14, 0 ),
    gen_rr_srcs_dep_test( 2, "sub", 15, -5, 20 ),
    gen_rr_srcs_dep_test( 1, "sub", 16, -6, 22 ),
    gen_rr_srcs_dep_test( 0, "sub", 17, -7, 24 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sub", 0, 1, -1 ),
    gen_rr_src1_eq_dest_test( "sub", 26, -1, 27 ),
    gen_rr_src0_eq_src1_test( "sub", 27, 0 ),
    gen_rr_srcs_eq_dest_test( "sub", 28, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "sub", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rr_value_test( "sub", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rr_value_test( "sub", 0x00000007, 0x00000003, 0x00000004 ),

    gen_rr_value_test( "sub", 0x00000000, 0xffff8000, 0x00008000 ),  # 0 - (-32768) = 32768
    gen_rr_value_test( "sub", 0x80000000, 0x00000000, 0x80000000 ),  
    gen_rr_value_test( "sub", 0x80000000, 0xffff8000, 0x80008000 ),  # -2147483648 - (-32768)= -2147450880

    gen_rr_value_test( "sub", 0x00000000, 0x00007fff, 0xffff8001 ),  # 0 - 32767 = - 32767
    gen_rr_value_test( "sub", 0x7fffffff, 0x00000000, 0x7fffffff ),
    gen_rr_value_test( "sub", 0x7fffffff, 0x00007fff, 0x7FFF8000 ),

    gen_rr_value_test( "sub", 0x80000000, 0x00007fff, 0x7fff8001 ),   # -2147483648 - 32767 = -2147516414
    gen_rr_value_test( "sub", 0x7fffffff, 0xffff8000, 0x80007fff ),   

    gen_rr_value_test( "sub", 0x00000000, 0xffffffff, 0x00000001 ),
    gen_rr_value_test( "sub", 0xffffffff, 0x00000001, 0xfffffffe ),
    gen_rr_value_test( "sub", 0xffffffff, 0xffffffff, 0x00000000 ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0xffffffff) )
    dest = src0 - src1
    asm_code.append( gen_rr_value_test( "sub", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
