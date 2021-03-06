#=========================================================================
# sra
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 0x00008000
    csrr x2, mngr2proc < 0x00000003
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sra x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x00001000
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
    gen_rr_dest_dep_test( 5, "sra", 0x00000001, 1, 0x00000000 ),
    gen_rr_dest_dep_test( 4, "sra", 0x00000010, 1, 0x00000008 ),
    gen_rr_dest_dep_test( 3, "sra", 0x00000100, 1, 0x00000080 ),
    gen_rr_dest_dep_test( 2, "sra", 0x00001000, 1, 0x00000800 ),
    gen_rr_dest_dep_test( 1, "sra", 0x00010000, 1, 0x00008000 ),
    gen_rr_dest_dep_test( 0, "sra", 0x00100000, 1, 0x00080000 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sra",  0x00000001, 2,  0x00000000 ),
    gen_rr_src0_dep_test( 4, "sra",  0x00000010, 2,  0x00000004 ),
    gen_rr_src0_dep_test( 3, "sra",  0x00000100, 2,  0x00000040 ),
    gen_rr_src0_dep_test( 2, "sra",  0x00001000, 2,  0x00000400 ),
    gen_rr_src0_dep_test( 1, "sra",  0x00010000, 2,  0x00004000 ),
    gen_rr_src0_dep_test( 0, "sra",  0x00100000, 2,  0x00040000 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "sra", 0x0000000A, 3, 0x00000001 ),
    gen_rr_src1_dep_test( 4, "sra", 0x000000A0, 3, 0x00000014 ),
    gen_rr_src1_dep_test( 3, "sra", 0x00000A00, 3, 0x00000140 ),
    gen_rr_src1_dep_test( 2, "sra", 0x0000A000, 3, 0x00001400 ),
    gen_rr_src1_dep_test( 1, "sra", 0x000A0000, 3, 0x00014000 ),
    gen_rr_src1_dep_test( 0, "sra", 0x00A00000, 3, 0x00140000 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sra", 0xF0000000, 4, 0xFF000000 ),
    gen_rr_srcs_dep_test( 4, "sra", 0x0F000000, 4, 0x00F00000 ),
    gen_rr_srcs_dep_test( 3, "sra", 0x00F00000, 4, 0x000F0000 ),
    gen_rr_srcs_dep_test( 2, "sra", 0x000F0000, 4, 0x0000F000 ),
    gen_rr_srcs_dep_test( 1, "sra", 0x0000F000, 4, 0x00000F00 ),
    gen_rr_srcs_dep_test( 0, "sra", 0x00000F00, 4, 0x000000F0 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sra", 0xA0000000, 5, 0xFD000000 ),
    gen_rr_src1_eq_dest_test( "sra", 0x0A000000, 5, 0x00500000 ),
    gen_rr_src0_eq_src1_test( "sra", 28,  0),
    gen_rr_srcs_eq_dest_test( "sra", 4, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "sra", 0x00000000, 5,  0x00000000 ),
    gen_rr_value_test( "sra", 0x00000001, 10, 0x00000000 ),
    gen_rr_value_test( "sra", 0x00000007, 1,  0x00000003 ),

    gen_rr_value_test( "sra", 0x00000a00, 1, 0x00000500 ),  
    gen_rr_value_test( "sra", 0x80000000, 4, 0xF8000000 ),  
    gen_rr_value_test( "sra", 0x80000000, 6, 0xFE000000 ),  

    gen_rr_value_test( "sra", 0xECEECECE, 16, 0xFFFFECEE),
    gen_rr_value_test( "sra", 0xCECECECE, 16, 0xFFFFCECE),
    gen_rr_value_test( "sra", 0xEEEEEEEE, 11, 0xFFFDDDDD),
    gen_rr_value_test( "sra", 0x00000000, 16, 0x00000000),
    gen_rr_value_test( "sra", 0xFFFF0000, 16, 0xFFFFFFFF),
    gen_rr_value_test( "sra", 0xAAAAAAAA, 8 , 0xFFAAAAAA),
    gen_rr_value_test( "sra", 0x996ab63d, 0 , 0x996AB63D),
    gen_rr_value_test( "sra", 0x996ab63d, 31 , 0xFFFFFFFF),
    gen_rr_value_test( "sra", 0x996ab63d, 32 , 0x996ab63d),

  ]

def gen_random_test():  # random test
  asm_code = []
  for i in xrange(100):
    src0  = Bits( 32, random.randint(0,0xffffffff) )
    src1  = Bits( 32, random.randint(0,0xffffffff) )
    src1_low_five = src1[0:5]
    dest = src0.int() >> src1_low_five.uint()
    dest = Bits(32, dest)
    asm_code.append( gen_rr_value_test( "sra", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
