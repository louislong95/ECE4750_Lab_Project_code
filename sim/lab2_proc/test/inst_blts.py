#=========================================================================
# blt
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """

    # Use x3 to track the control flow pattern
    addi  x3, x0, 0

    csrr  x1, mngr2proc < 2
    csrr  x2, mngr2proc < 1

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    # This branch should be taken
    blt   x2, x1, label_a
    addi  x3, x3, 0b01

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

  label_a:
    addi  x3, x3, 0b10

    # Only the second bit should be set if branch was taken
    csrw proc2mngr, x3 > 0b10

  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
def gen_src0_dep_taken_test():
  return [
    gen_br2_src0_dep_test( 5, "blt", 1, 2, True ),
    gen_br2_src0_dep_test( 4, "blt", 2, 3, True ),
    gen_br2_src0_dep_test( 3, "blt", 3, 4, True ),
    gen_br2_src0_dep_test( 2, "blt", 4, 5, True ),
    gen_br2_src0_dep_test( 1, "blt", 5, 6, True ),
    gen_br2_src0_dep_test( 0, "blt", 6, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_dep_nottaken_test():
  return [
    gen_br2_src0_dep_test( 5, "blt", 1, 1, False ),
    gen_br2_src0_dep_test( 4, "blt", 2, 2, False ),
    gen_br2_src0_dep_test( 3, "blt", 3, 2, False ),
    gen_br2_src0_dep_test( 2, "blt", 4, 3, False ),
    gen_br2_src0_dep_test( 1, "blt", 5, 4, False ),
    gen_br2_src0_dep_test( 0, "blt", 6, 5, False ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------

def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "blt", 7, 10, True ),
    gen_br2_src1_dep_test( 4, "blt", 7, 11, True ),
    gen_br2_src1_dep_test( 3, "blt", 7, 12, True ),
    gen_br2_src1_dep_test( 2, "blt", 7, 13, True ),
    gen_br2_src1_dep_test( 1, "blt", 7, 15, True ),
    gen_br2_src1_dep_test( 0, "blt", 7, 70, True ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "blt", 100, 11, False ),
    gen_br2_src1_dep_test( 4, "blt", 120, 22, False ),
    gen_br2_src1_dep_test( 3, "blt", 130, 33, False ),
    gen_br2_src1_dep_test( 2, "blt", 140, 44, False ),
    gen_br2_src1_dep_test( 1, "blt", 150, 55, False ),
    gen_br2_src1_dep_test( 0, "blt", 160, 66, False ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "blt", 11, 222, True ),
    gen_br2_srcs_dep_test( 4, "blt", 22, 333, True ),
    gen_br2_srcs_dep_test( 3, "blt", 33, 444, True ),
    gen_br2_srcs_dep_test( 2, "blt", 45, 555, True ),
    gen_br2_srcs_dep_test( 1, "blt", 56, 666, True ),
    gen_br2_srcs_dep_test( 0, "blt", 69, 777, True ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_nottaken_test():
  return [
    gen_br2_srcs_dep_test( 5, "blt", 100, 10, False ),
    gen_br2_srcs_dep_test( 4, "blt", 200, 22, False ),
    gen_br2_srcs_dep_test( 3, "blt", 300, 34, False ),
    gen_br2_srcs_dep_test( 2, "blt", 400, 41, False ),
    gen_br2_srcs_dep_test( 1, "blt", 500, 57, False ),
    gen_br2_srcs_dep_test( 0, "blt", 600, 69, False ),
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "blt", 1,   False ),
    gen_br2_src0_eq_src1_test( "blt", 50,  False ),
    gen_br2_src0_eq_src1_test( "blt", 700, False ),
    gen_br2_src0_eq_src1_test( "blt", 999, False ),
    gen_br2_src0_eq_src1_test( "blt", 814, False ),
    gen_br2_src0_eq_src1_test( "blt", 331, False ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_br2_value_test( "blt", 0xfffffff7, 0xfffffff7, False ),
    gen_br2_value_test( "blt", 0x7fffffff, 0x7fffffff, False ),
    gen_br2_value_test( "blt", 0xfffffff7, 0x7fffffff, True  ),
    gen_br2_value_test( "blt", 0x7fffffff, 0xfffffff7, False  ),
    gen_br2_value_test( "blt", 0xffffffff, 0xfffffffe, False  ),
    gen_br2_value_test( "blt", 0xfffffffd, 0xffffffff, True  ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    taken = random.choice([True, False])
    src1  = Bits( 32, random.randint(0,0xffffffff) )
    if taken:
      # Branch taken, operands are unequal
      if src1 == 0xf0000000:
        src1 = src1 + 0x00000001
        src0 = src1 - 0x00000001
      else:
        src0 = src1 - 0x00000001
    else:
      # Branch not taken, operands are equal
      if src1 == 0x7fffffff:
        src0 = src1
      else:
        src0 = src1 + 0x00000001
    asm_code.append( gen_br2_value_test( "blt", src0.uint(), src1.uint(), taken ) )
  return asm_code
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
