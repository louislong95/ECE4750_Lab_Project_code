#=========================================================================
# addi
#=========================================================================

import random

from pymtl                import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """

    csrr x1, mngr2proc, < 5
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    addi x3, x1, 0x0004
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 9
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
def gen_dest_dep_test():     # test the nop between addi and csrw, the nop between csrr and addi is always 8
  return [
    gen_rimm_dest_dep_test( 5, "addi", 1, 1, 2 ),
    gen_rimm_dest_dep_test( 4, "addi", 2, 1, 3 ),
    gen_rimm_dest_dep_test( 3, "addi", 3, 1, 4 ),
    gen_rimm_dest_dep_test( 2, "addi", 4, 1, 5 ),
    gen_rimm_dest_dep_test( 1, "addi", 5, 1, 6 ),
    gen_rimm_dest_dep_test( 0, "addi", 6, 1, 7 ),
  ]
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' '''''''''
def gen_src_dep_test():      # test the nop between csrr and addi, the nop between addi and csrw is always 0
  return [
    gen_rimm_src_dep_test( 5, "addi", 10, 10, 20 ),
    gen_rimm_src_dep_test( 4, "addi", 10, 11, 21 ),
    gen_rimm_src_dep_test( 3, "addi", 10, 12, 22 ),
    gen_rimm_src_dep_test( 2, "addi", 10, 13, 23 ),
    gen_rimm_src_dep_test( 1, "addi", 10, 14, 24 ),
    gen_rimm_src_dep_test( 0, "addi", 10, 15, 25 ),
  ]
  
def gen_src_eq_dest_test():  # the nop between csrr and addi, addi and csrw are always 0
  return [
    gen_rimm_src_eq_dest_test( "addi", 23, 45, 68 ),
    gen_rimm_src_eq_dest_test( "addi", 25, 46, 71 ),
    gen_rimm_src_eq_dest_test( "addi", 27, 47, 74 ),
    gen_rimm_src_eq_dest_test( "addi", 30, 49, 79 ),
    gen_rimm_src_eq_dest_test( "addi", 34, 52, 86 ),
  ]

def gen_value_test():
  return [
    gen_rimm_value_test( "addi", 0x00000000, 0x000, 0x00000000 ),
    gen_rimm_value_test( "addi", 0x00000001, 0x001, 0x00000002 ),
    gen_rimm_value_test( "addi", 0x00000003, 0x007, 0x0000000a ),

    gen_rimm_value_test( "addi", 0x00000000, 0x800, 0xfffff800 ),
    gen_rimm_value_test( "addi", 0x80000000, 0x000, 0x80000000 ),
    gen_rimm_value_test( "addi", 0x80000000, 0xfff, 0x7fffffff ),

    gen_rimm_value_test( "addi", 0x00000000, 0x7ff, 0x000007ff ),
    gen_rimm_value_test( "addi", 0x7fffffff, 0x000, 0x7fffffff ),
    gen_rimm_value_test( "addi", 0x7fffffff, 0x7ff, 0x800007fe),

    gen_rimm_value_test( "addi", 0x80000000, 0x7ff, 0x800007ff ),
    gen_rimm_value_test( "addi", 0x7fffffff, 0xfff, 0x7ffffffe ),

    gen_rimm_value_test( "addi", 0x00000000, 0xfff, 0xffffffff ),
    gen_rimm_value_test( "addi", 0xffffffff, 0x001, 0x00000000 ),
    gen_rimm_value_test( "addi", 0xffffffff, 0xfff, 0xfffffffe ),
  ]

def gen_random_test():  # random test
  asm_code = []
  for i in xrange(100):
    src  = Bits( 32, random.randint(0,0xffffffff) )
    imm  = Bits( 12, random.randint(0,0xfff) )
    dest = src + sext(imm,32)
    asm_code.append( gen_rimm_value_test( "addi", src.uint(), imm.uint(), dest.uint() ) )
  return asm_code
  
def gen_addi_eval_test():
  return """

    csrr x6, mngr2proc, < 0
    nop
    nop
    nop
    addi x10, x0, 0x000
    addi x11, x6, 0x001
    addi x12, x6, 0xfff
    addi x13, x0, 0x000
    addi x14, x0, 0xfff
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    jal x0, label_test
    addi x3, x0, 0x001
    
   label_test:
    add x20, x10, x12
    addi x3, x0, 0x010
    nop
    nop 
    
    csrw proc2mngr, x3 > 0x010
    csrw proc2mngr, x20 > 0xffffffff
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

