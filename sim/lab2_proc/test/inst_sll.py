#=========================================================================
# sll
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 0x80008000
    csrr x2, mngr2proc < 0x00000003
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sll x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x00040000
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
    gen_rr_dest_dep_test( 5, "sll", 0x00000001, 1, 0x00000002 ),
    gen_rr_dest_dep_test( 4, "sll", 0x00000010, 1, 0x00000020 ),
    gen_rr_dest_dep_test( 3, "sll", 0x00000100, 1, 0x00000200 ),
    gen_rr_dest_dep_test( 2, "sll", 0x00001000, 1, 0x00002000 ),
    gen_rr_dest_dep_test( 1, "sll", 0x00010000, 1, 0x00020000 ),
    gen_rr_dest_dep_test( 0, "sll", 0x00100000, 1, 0x00200000 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sll",  0x00000001, 2,  0x00000004 ),
    gen_rr_src0_dep_test( 4, "sll",  0x00000010, 2,  0x00000040 ),
    gen_rr_src0_dep_test( 3, "sll",  0x00000100, 2,  0x00000400 ),
    gen_rr_src0_dep_test( 2, "sll",  0x00001000, 2,  0x00004000 ),
    gen_rr_src0_dep_test( 1, "sll",  0x00010000, 2,  0x00040000 ),
    gen_rr_src0_dep_test( 0, "sll",  0x00100000, 2,  0x00400000 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "sll", 0x0000000A, 3, 0x00000050 ),
    gen_rr_src1_dep_test( 4, "sll", 0x000000A0, 3, 0x00000500 ),
    gen_rr_src1_dep_test( 3, "sll", 0x00000A00, 3, 0x00005000 ),
    gen_rr_src1_dep_test( 2, "sll", 0x0000A000, 3, 0x00050000 ),
    gen_rr_src1_dep_test( 1, "sll", 0x000A0000, 3, 0x00500000 ),
    gen_rr_src1_dep_test( 0, "sll", 0x00A00000, 3, 0x05000000 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sll", 0xF0000000, 4, 0x00000000 ),
    gen_rr_srcs_dep_test( 4, "sll", 0x0F000000, 4, 0xF0000000 ),
    gen_rr_srcs_dep_test( 3, "sll", 0x00F00000, 4, 0x0F000000 ),
    gen_rr_srcs_dep_test( 2, "sll", 0x000F0000, 4, 0x00F00000 ),
    gen_rr_srcs_dep_test( 1, "sll", 0x0000F000, 4, 0x000F0000 ),
    gen_rr_srcs_dep_test( 0, "sll", 0x00000F00, 4, 0x0000F000 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sll", 0xA0000000, 5, 0x00000000 ),
    gen_rr_src1_eq_dest_test( "sll", 0x0A000000, 5, 0x40000000 ),
    gen_rr_src0_eq_src1_test( "sll", 28,  0xC0000000),
    gen_rr_srcs_eq_dest_test( "sll", 4,   0x00000040 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "sll", 0x00000000, 5,  0x00000000 ),
    gen_rr_value_test( "sll", 0x00000001, 10, 0x00000400 ),
    gen_rr_value_test( "sll", 0x00000007, 1,  0x0000000E ),

    gen_rr_value_test( "sll", 0x00000a00, 1, 0x00001400 ),  
    gen_rr_value_test( "sll", 0x80000000, 4, 0x00000000 ),  
    gen_rr_value_test( "sll", 0x00800000, 6, 0x20000000 ),  

    gen_rr_value_test( "sll", 0xECEECECE, 16, 0xcece0000),
    gen_rr_value_test( "sll", 0xCECECECE, 16, 0xCECE0000),
    gen_rr_value_test( "sll", 0xEEEEEEEE, 11, 0x77777000),
    gen_rr_value_test( "sll", 0x00000000, 16, 0x00000000),
    gen_rr_value_test( "sll", 0xFFFF0000, 16, 0x00000000),
    gen_rr_value_test( "sll", 0xAAAAAAAA, 8 , 0xaaaaaa00),
    gen_rr_value_test( "sll", 0x996ab63d, 31 , 0x80000000),
    gen_rr_value_test( "sll", 0x996ab63d, 32 , 0x996ab63d),

  ]

def gen_random_test():  # random test
  asm_code = []
  for i in xrange(100):
    src0  = Bits( 32, random.randint(0,0xffffffff) )
    src1  = Bits( 32, random.randint(0,0xffffffff) )
    src1_low_five = src1[0:5]
    dest = src0 << src1_low_five
    dest = Bits(32, dest)
    asm_code.append( gen_rr_value_test( "sll", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
