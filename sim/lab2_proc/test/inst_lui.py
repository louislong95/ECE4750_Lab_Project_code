#=========================================================================
# lui
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    lui x1, 0x0001
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x1 > 0x00001000
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
    gen_imm_dest_dep_test(5, "lui", 0x00000, 0x00000000  ),
    gen_imm_dest_dep_test(4, "lui", 0x00001, 0x00001000 ),
    gen_imm_dest_dep_test(3, "lui", 0x00010, 0x00010000  ),
    gen_imm_dest_dep_test(2, "lui", 0x00200, 0x00200000  ),
    gen_imm_dest_dep_test(1, "lui", 0x0F000, 0x0F000000  ),
    gen_imm_dest_dep_test(0, "lui", 0x000F0, 0x000F0000  ),
  ]
  
def gen_value_test():
  return [
    gen_imm_value_test("lui", 0x0F000, 0x0F000000),
    gen_imm_value_test("lui", 0x0ABCD, 0x0ABCD000),
    gen_imm_value_test("lui", 0xAACCD, 0xAACCD000),
    gen_imm_value_test("lui", 0xFF000, 0xFF000000),
    gen_imm_value_test("lui", 0x12345, 0x12345000),
    gen_imm_value_test("lui", 0xFFFFF, 0xFFFFF000),
  ]

def gen_random_test():  # random test
  asm_code = []
  for i in xrange(100):
    imm  = Bits( 20, random.randint(0,0xfffff) )
    imm_32 = Bits( 32, imm )
    twl  = Bits( 4, 12)
    dest = Bits(32, imm_32 << twl)
    #dest = imm_32 << twl
    asm_code.append( gen_imm_value_test( "lui", imm.uint(), dest.uint() ) )
  return asm_code
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
