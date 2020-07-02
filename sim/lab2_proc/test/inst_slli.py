#=========================================================================
# slli
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
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slli x3, x1, 0x03
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
    gen_rimm_dest_dep_test(5, "slli", 0xF0000000, 1,  0xE0000000  ),
    gen_rimm_dest_dep_test(4, "slli", 0x00000001, 1,  0x00000002 ),
    gen_rimm_dest_dep_test(3, "slli", 0x00000010, 1,  0x00000020  ),
    gen_rimm_dest_dep_test(2, "slli", 0x00000200, 1,  0x00000400  ),
    gen_rimm_dest_dep_test(1, "slli", 0x0F000000, 1,  0x1E000000  ),
    gen_rimm_dest_dep_test(0, "slli", 0x00F00000, 1,  0x01E00000  ),
  ]
  
def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test(5, "slli", 0x0000F000, 2, 0x0003c000),
    gen_rimm_src_dep_test(4, "slli", 0x0ABCDEFF, 2, 0x2AF37BFC),
    gen_rimm_src_dep_test(3, "slli", 0x00AACCDD, 2, 0x02AB3374),
    gen_rimm_src_dep_test(2, "slli", 0xFF000000, 3, 0xF8000000),
    gen_rimm_src_dep_test(1, "slli", 0xA0B0C0D0, 3, 0x05860680),
    gen_rimm_src_dep_test(0, "slli", 0xFFFFFFFF, 3, 0xFFFFFFF8),
  ]
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test("slli", 0x00000000, 2, 0x00000000),
    gen_rimm_src_eq_dest_test("slli", 0x00ECEECE, 5, 0x1d9dd9c0),
    gen_rimm_src_eq_dest_test("slli", 0xF0000000, 6, 0x00000000),
    gen_rimm_src_eq_dest_test("slli", 0x0000000F, 7, 0x00000780),
    gen_rimm_src_eq_dest_test("slli", 0x000000F0, 8, 0x0000f000),
    gen_rimm_src_eq_dest_test("slli", 0x00000F00, 9, 0x001e0000),
  ]

def gen_value_test():
  return [
    gen_rimm_value_test("slli", 0xECEECECE, 16, 0xcece0000),
    gen_rimm_value_test("slli", 0xCECECECE, 16, 0xcece0000),
    gen_rimm_value_test("slli", 0xEEEEEEEE, 11, 0x77777000),
    gen_rimm_value_test("slli", 0x00000000, 16, 0x00000000),
    gen_rimm_value_test("slli", 0xFFFF0000, 16, 0x00000000),
    gen_rimm_value_test("slli", 0xAAAAAAAA, 8 , 0xaaaaaa00),
    gen_rimm_value_test("slli", 0x996ab63d, 0 , 0x996AB63D),
  ]
  
def gen_random_test():  # random test
  asm_code = []
  for i in xrange(100):
    src  = Bits( 32, random.randint(0,0xffffffff) )
    imm  = Bits( 4, random.randint(0,0xf) )
    dest = src << imm
    dest = Bits(32, dest)
    asm_code.append( gen_rimm_value_test( "slli", src.uint(), imm.uint(), dest.uint() ) )
  return asm_code
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
