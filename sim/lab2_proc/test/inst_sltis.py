#=========================================================================
# slti
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
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slti x3, x1, 6
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
    gen_rimm_dest_dep_test(5, "slti", 5, 10,  1  ),
    gen_rimm_dest_dep_test(4, "slti", 45, 100, 1 ),
    gen_rimm_dest_dep_test(3, "slti", 5, 2,   0  ),
    gen_rimm_dest_dep_test(2, "slti", 20, 7,  0  ),
    gen_rimm_dest_dep_test(1, "slti", 50, 0,  0  ),
    gen_rimm_dest_dep_test(0, "slti", 13, 14, 1  ),
  ]
  
def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test(5, "slti", 2, 3, 1),
    gen_rimm_src_dep_test(4, "slti", 2, 1, 0),
    gen_rimm_src_dep_test(3, "slti", 8, 7, 0),
    gen_rimm_src_dep_test(2, "slti", 100, 0, 0),
    gen_rimm_src_dep_test(1, "slti", 0, 103, 1),
    gen_rimm_src_dep_test(0, "slti", 200, 300, 1),
  ]
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test("slti", 0x00000000, 0x001, 1),
    gen_rimm_src_eq_dest_test("slti", 0x00000000, 0x000, 0),
    gen_rimm_src_eq_dest_test("slti", 0x00000000, 0xF00, 0),
    gen_rimm_src_eq_dest_test("slti", 0xF0000000, 0x000, 1),
    gen_rimm_src_eq_dest_test("slti", 0x80000000, 0x001, 1),
    gen_rimm_src_eq_dest_test("slti", 0x00000000, 0x800, 0),
  ]

def gen_value_test():
  return [
    gen_rimm_value_test("slti", 0x00000000, 0x7ff, 1),
    gen_rimm_value_test("slti", 0x0000F000, 0x7ff, 0),
    gen_rimm_value_test("slti", 0x7fffffff, 0x8ff, 0),
    gen_rimm_value_test("slti", 0x80000000, 0xfff, 1),
    gen_rimm_value_test("slti", 0x80000000, 0x800, 1),
    gen_rimm_value_test("slti", 0x00000000, 0x000, 0),
    gen_rimm_value_test("slti", 0x996ab63d, 0x6d1, 1),
  ]

def gen_random_test():  # random test
  asm_code = []
  for i in xrange(100):
    src  = Bits( 32, random.randint(0,0xffffffff) )
    imm  = Bits( 12, random.randint(0,0xfff) )
    #dest = src + sext(imm,32)
    if (src.int() < sext(imm, 32).int()):
      dest = Bits(32, 0x00000000000000000000000000000001)
    elif (src.int() >= sext(imm, 32).int()):
      dest = Bits(32, 0x00000000000000000000000000000000)
    asm_code.append( gen_rimm_value_test( "slti", src.uint(), imm.uint(), dest.uint() ) )
  return asm_code
