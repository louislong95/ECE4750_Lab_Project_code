#=========================================================================
# mul
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
    mul x3, x1, x2
    mul x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 20
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
    gen_rr_dest_dep_test( 5, "mul", 0x00000001, 0x0000000f, 0x0000000f ),
    gen_rr_dest_dep_test( 4, "mul", 0x00000002, 0x0000000f, 0x0000001E ),
    gen_rr_dest_dep_test( 3, "mul", 0x00000004, 0x0000000f, 0x0000003C ),
    gen_rr_dest_dep_test( 2, "mul", 0x00000008, 0x0000000f, 0x00000078 ),
    gen_rr_dest_dep_test( 1, "mul", 0x0000000f, 0x0000000f, 0x000000E1 ),
    gen_rr_dest_dep_test( 0, "mul", 0x000000ff, 0x0000000f, 0x00000EF1 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "mul", 0x00000010, 0x0000000a, 0x000000A0 ),
    gen_rr_src0_dep_test( 4, "mul", 0x00000022, 0x0000000a, 0x00000154 ),
    gen_rr_src0_dep_test( 3, "mul", 0x00000044, 0x0000000a, 0x000002A8 ),
    gen_rr_src0_dep_test( 2, "mul", 0x00000088, 0x0000000a, 0x00000550 ),
    gen_rr_src0_dep_test( 1, "mul", 0x000000ff, 0x0000000a, 0x000009F6 ),
    gen_rr_src0_dep_test( 0, "mul", 0x00000fff, 0x0000000a, 0x00009FF6 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "mul", 0x0000000f, 0x00000001, 0x0000000f ),
    gen_rr_src1_dep_test( 4, "mul", 0x0000000f, 0x00000002, 0x0000001E ),
    gen_rr_src1_dep_test( 3, "mul", 0x0000000f, 0x00000004, 0x0000003C ),
    gen_rr_src1_dep_test( 2, "mul", 0x0000000f, 0x00000008, 0x00000078 ),
    gen_rr_src1_dep_test( 1, "mul", 0x0000000f, 0x0000000f, 0x000000E1 ),
    gen_rr_src1_dep_test( 0, "mul", 0x0000000f, 0x000000ff, 0x00000EF1 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "mul", 0x000f0f00, 0x0000ff00, 0xFFF10000 ),
    gen_rr_srcs_dep_test( 4, "mul", 0x00f0f000, 0x000ff000, 0xF1000000 ),
    gen_rr_srcs_dep_test( 3, "mul", 0x0f0f0000, 0x00ff0000, 0x00000000 ),
    gen_rr_srcs_dep_test( 2, "mul", 0x00000ABC, 0x000000d0, 0x0008B8C0 ),
    gen_rr_srcs_dep_test( 1, "mul", 0x0000000f, 0x00f00000, 0x0E100000 ),
    gen_rr_srcs_dep_test( 0, "mul", 0x000000f0, 0x000C0000, 0x0B400000 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "mul", 0x00000f0f, 0x000000ff, 0x000EFFF1 ),
    gen_rr_src1_eq_dest_test( "mul", 0x0000abcd, 0x0000000f, 0x000A1103 ),
    gen_rr_src0_eq_src1_test( "mul", 0x000f0f00, 0xC2E10000 ),
    gen_rr_srcs_eq_dest_test( "mul", 0x00000ece, 0x00DB2DC4 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rr_value_test( "mul", 0x000dfc00, 0x0000e5d3, 0x8DF2B400 ),
    gen_rr_value_test( "mul", 0x00100d91, 0x00001765, 0x778D6135 ),
    gen_rr_value_test( "mul", 0x00000234, 0x00000fca, 0x0022C908 ),
    gen_rr_value_test( "mul", 0xabcdeeee, 0x00000463, 0xA85F1E0A ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0xffffffff) )
    res  = src0 * src1
    dest = Bits( 32, res, trunc=1 )
    asm_code.append( gen_rr_value_test( "mul", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
