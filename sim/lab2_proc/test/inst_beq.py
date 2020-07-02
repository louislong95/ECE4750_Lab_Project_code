#=========================================================================
# beq
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
    csrr  x2, mngr2proc < 2

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    # This branch should be taken
    beq   x1, x2, label_a
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
#-------------------------------------------------------------------------
# gen_src0_dep_taken_test
#-------------------------------------------------------------------------

def gen_src0_dep_taken_test():
  return [
    gen_br2_src0_dep_test( 5, "beq", 1, 1, True ),
    gen_br2_src0_dep_test( 4, "beq", 2, 2, True ),
    gen_br2_src0_dep_test( 3, "beq", 3, 3, True ),
    gen_br2_src0_dep_test( 2, "beq", 4, 4, True ),
    gen_br2_src0_dep_test( 1, "beq", 5, 5, True ),
    gen_br2_src0_dep_test( 0, "beq", 6, 6, True ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_dep_nottaken_test():
  return [
    gen_br2_src0_dep_test( 5, "beq", 1, 2, False ),
    gen_br2_src0_dep_test( 4, "beq", 2, 3, False ),
    gen_br2_src0_dep_test( 3, "beq", 3, 5, False ),
    gen_br2_src0_dep_test( 2, "beq", 4, 7, False ),
    gen_br2_src0_dep_test( 1, "beq", 5, 8, False ),
    gen_br2_src0_dep_test( 0, "beq", 6, 9, False ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------

def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "beq", 7,  7 , True ),
    gen_br2_src1_dep_test( 4, "beq", 9,  9 , True ),
    gen_br2_src1_dep_test( 3, "beq", 10, 10, True ),
    gen_br2_src1_dep_test( 2, "beq", 12, 12, True ),
    gen_br2_src1_dep_test( 1, "beq", 0,  0 , True ),
    gen_br2_src1_dep_test( 0, "beq", 13, 13, True ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "beq", 10, 1, False ),
    gen_br2_src1_dep_test( 4, "beq", 7,  2, False ),
    gen_br2_src1_dep_test( 3, "beq", 4,  3, False ),
    gen_br2_src1_dep_test( 2, "beq", 25, 4, False ),
    gen_br2_src1_dep_test( 1, "beq", 47, 5, False ),
    gen_br2_src1_dep_test( 0, "beq", 66, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "beq", 1, 1, True ),
    gen_br2_srcs_dep_test( 4, "beq", 2, 2, True ),
    gen_br2_srcs_dep_test( 3, "beq", 3, 3, True ),
    gen_br2_srcs_dep_test( 2, "beq", 4, 4, True ),
    gen_br2_srcs_dep_test( 1, "beq", 5, 5, True ),
    gen_br2_srcs_dep_test( 0, "beq", 6, 6, True ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_nottaken_test():
  return [
    gen_br2_srcs_dep_test( 5, "beq", 89, 1, False ),
    gen_br2_srcs_dep_test( 4, "beq", 13, 22, False ),
    gen_br2_srcs_dep_test( 3, "beq", 34, 13, False ),
    gen_br2_srcs_dep_test( 2, "beq", 47, 44, False ),
    gen_br2_srcs_dep_test( 1, "beq", 51, 55, False ),
    gen_br2_srcs_dep_test( 0, "beq", 61, 16, False ),
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "beq", 8,  True ),
    gen_br2_src0_eq_src1_test( "beq", 88,  True ),
    gen_br2_src0_eq_src1_test( "beq", 56, True ),
    gen_br2_src0_eq_src1_test( "beq", 100, True ),
    gen_br2_src0_eq_src1_test( "beq", 137, True ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_br2_value_test( "beq", -1, -2, False ),
    gen_br2_value_test( "beq", -1,  -1, True  ),
    gen_br2_value_test( "beq", -1,  1, False  ),

    gen_br2_value_test( "beq",  0, -1, False  ),
    gen_br2_value_test( "beq",  0,  0, True ),
    gen_br2_value_test( "beq",  0,  1, False  ),

    gen_br2_value_test( "beq",  1, -1, False  ),
    gen_br2_value_test( "beq",  1,  0, False  ),
    gen_br2_value_test( "beq",  0,  1, False ),

    gen_br2_value_test( "beq", 0xfffffff7, 0xfffffff7, True ),
    gen_br2_value_test( "beq", 0x7fffffff, 0x7fffffff, True ),
    gen_br2_value_test( "beq", 0xffffffff, 0xffffffff, True  ),
    gen_br2_value_test( "beq", 0x7fffffff, 0xfffffff7, False  ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(25):
    taken = random.choice([True, False])
    src0  = Bits( 32, random.randint(0,0xffffffff) )
    if taken:
      # Branch taken, operands are equal
      src1 = Bits( 32, src0 )
    else:
      # Branch not taken, operands are not equal
      src1 = Bits( 32, random.randint(0,0xffffffff) )
      if src0 == src1:
        src1 = src0 + 1
    asm_code.append( gen_br2_value_test( "beq", src0.uint(), src1.uint(), taken ) )
  return asm_code
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
