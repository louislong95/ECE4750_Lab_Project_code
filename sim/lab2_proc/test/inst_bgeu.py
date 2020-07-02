#=========================================================================
# bgeu
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
    bgeu   x1, x2, label_a
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
    gen_br2_src0_dep_test( 5, "bgeu", 1, 1, True ),
    gen_br2_src0_dep_test( 4, "bgeu", 2, 2, True ),
    gen_br2_src0_dep_test( 3, "bgeu", 3, 3, True ),
    gen_br2_src0_dep_test( 2, "bgeu", 4, 4, True ),
    gen_br2_src0_dep_test( 1, "bgeu", 5, 4, True ),
    gen_br2_src0_dep_test( 0, "bgeu", 6, 4, True ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_dep_nottaken_test():
  return [
    gen_br2_src0_dep_test( 5, "bgeu", 1, 2, False ),
    gen_br2_src0_dep_test( 4, "bgeu", 2, 4, False ),
    gen_br2_src0_dep_test( 3, "bgeu", 3, 7, False ),
    gen_br2_src0_dep_test( 2, "bgeu", 4, 6, False ),
    gen_br2_src0_dep_test( 1, "bgeu", 5, 8, False ),
    gen_br2_src0_dep_test( 0, "bgeu", 6, 9, False ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------

def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "bgeu", 7, 1, True ),
    gen_br2_src1_dep_test( 4, "bgeu", 7, 2, True ),
    gen_br2_src1_dep_test( 3, "bgeu", 7, 3, True ),
    gen_br2_src1_dep_test( 2, "bgeu", 7, 4, True ),
    gen_br2_src1_dep_test( 1, "bgeu", 7, 5, True ),
    gen_br2_src1_dep_test( 0, "bgeu", 7, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "bgeu", 10, 11, False ),
    gen_br2_src1_dep_test( 4, "bgeu", 12, 22, False ),
    gen_br2_src1_dep_test( 3, "bgeu", 13, 33, False ),
    gen_br2_src1_dep_test( 2, "bgeu", 14, 44, False ),
    gen_br2_src1_dep_test( 1, "bgeu", 15, 55, False ),
    gen_br2_src1_dep_test( 0, "bgeu", 16, 66, False ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bgeu", 11, 2, True ),
    gen_br2_srcs_dep_test( 4, "bgeu", 22, 3, True ),
    gen_br2_srcs_dep_test( 3, "bgeu", 33, 4, True ),
    gen_br2_srcs_dep_test( 2, "bgeu", 45, 5, True ),
    gen_br2_srcs_dep_test( 1, "bgeu", 56, 6, True ),
    gen_br2_srcs_dep_test( 0, "bgeu", 69, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_nottaken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bgeu", 1, 101, False ),
    gen_br2_srcs_dep_test( 4, "bgeu", 2, 222, False ),
    gen_br2_srcs_dep_test( 3, "bgeu", 3, 345, False ),
    gen_br2_srcs_dep_test( 2, "bgeu", 4, 414, False ),
    gen_br2_srcs_dep_test( 1, "bgeu", 5, 574, False ),
    gen_br2_srcs_dep_test( 0, "bgeu", 6, 696, False ),
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "bgeu", 1,   True ),
    gen_br2_src0_eq_src1_test( "bgeu", 50,  True ),
    gen_br2_src0_eq_src1_test( "bgeu", 700, True ),
    gen_br2_src0_eq_src1_test( "bgeu", 999, True ),
    gen_br2_src0_eq_src1_test( "bgeu", 814, True ),
    gen_br2_src0_eq_src1_test( "bgeu", 331, True ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_br2_value_test( "bgeu", 0xfffffff7, 0xfffffff7, True ),
    gen_br2_value_test( "bgeu", 0x7fffffff, 0x7fffffff, True ),
    gen_br2_value_test( "bgeu", 0xfffffff7, 0x7fffffff, True  ),
    gen_br2_value_test( "bgeu", 0x7fffffff, 0xfffffff7, False  ),
    gen_br2_value_test( "bgeu", 0xffffffff, 0xfffffffe, True  ),
    gen_br2_value_test( "bgeu", 0xfffffffd, 0xffffffff, False  ),

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
      if src1 == 0xffffffff:
        src0 = src1
      else:
        src0 = src1 + 0x00000001
    else:
      # Branch not taken, operands are equal
      if src1 == 0x00000000:
        src1 = src1 + 0x00000001
        src0 = src1 - 0x00000001
      else:
        src0 = src1 - 0x00000001
    asm_code.append( gen_br2_value_test( "bgeu", src0.uint(), src1.uint(), taken ) )
  return asm_code
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
