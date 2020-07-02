#=========================================================================
# srli
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
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    srli x3, x1, 0x03
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
    gen_rimm_dest_dep_test(5, "srli", 0xF0000000, 1,  0x78000000  ),
    gen_rimm_dest_dep_test(4, "srli", 0x00000001, 1,  0x00000000 ),
    gen_rimm_dest_dep_test(3, "srli", 0x00000010, 1,  0x00000008  ),
    gen_rimm_dest_dep_test(2, "srli", 0x00000200, 1,  0x00000100  ),
    gen_rimm_dest_dep_test(1, "srli", 0x0F000000, 1,  0x07800000  ),
    gen_rimm_dest_dep_test(0, "srli", 0x00F00000, 1,  0x00780000  ),
  ]
  
def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test(5, "srli", 0x0000F000, 2, 0x00003c00),
    gen_rimm_src_dep_test(4, "srli", 0x0ABCDEFF, 2, 0x02AF37BF),
    gen_rimm_src_dep_test(3, "srli", 0x00AACCDD, 2, 0x002AB337),
    gen_rimm_src_dep_test(2, "srli", 0xFF000000, 3, 0x1FE00000),
    gen_rimm_src_dep_test(1, "srli", 0xA0B0C0D0, 3, 0x1416181A),
    gen_rimm_src_dep_test(0, "srli", 0xFFFFFFFF, 3, 0x1FFFFFFF),
  ]
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test("srli", 0x00000000, 2, 0x00000000),
    gen_rimm_src_eq_dest_test("srli", 0x00ECEECE, 5, 0x00076776),
    gen_rimm_src_eq_dest_test("srli", 0xF0000000, 6, 0x03C00000),
    gen_rimm_src_eq_dest_test("srli", 0xF0000000, 7, 0x01E00000),
    gen_rimm_src_eq_dest_test("srli", 0xF0000000, 8, 0x00F00000),
    gen_rimm_src_eq_dest_test("srli", 0xF0000000, 9, 0x00780000),
  ]

def gen_value_test():
  return [
    gen_rimm_value_test("srli", 0xECEECECE, 16, 0x0000ECEE),
    gen_rimm_value_test("srli", 0xCECECECE, 16, 0x0000CECE),
    gen_rimm_value_test("srli", 0xEEEEEEEE, 11, 0x001DDDDD),
    gen_rimm_value_test("srli", 0x00000000, 16, 0x00000000),
    gen_rimm_value_test("srli", 0xFFFF0000, 16, 0x0000FFFF),
    gen_rimm_value_test("srli", 0xAAAAAAAA, 8 , 0x00AAAAAA),
    gen_rimm_value_test("srli", 0x996ab63d, 0 , 0x996AB63D),
  ]
  
def gen_random_test():  # random test
  asm_code = []
  for i in xrange(100):
    src  = Bits( 32, random.randint(0,0xffffffff) )
    imm  = Bits( 4, random.randint(0,0xf) )
    dest = src >> imm
    dest = Bits(32, dest)
    asm_code.append( gen_rimm_value_test( "srli", src.uint(), imm.uint(), dest.uint() ) )
  return asm_code
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
