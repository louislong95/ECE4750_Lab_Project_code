#=========================================================================
# bltu
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
    bltu   x2, x1, label_a
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
    gen_br2_src0_dep_test( 5, "bltu", 1, 2, True ),
    gen_br2_src0_dep_test( 4, "bltu", 2, 3, True ),
    gen_br2_src0_dep_test( 3, "bltu", 3, 4, True ),
    gen_br2_src0_dep_test( 2, "bltu", 4, 5, True ),
    gen_br2_src0_dep_test( 1, "bltu", 5, 6, True ),
    gen_br2_src0_dep_test( 0, "bltu", 6, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_dep_nottaken_test():
  return [
    gen_br2_src0_dep_test( 5, "bltu", 1, 1, False ),
    gen_br2_src0_dep_test( 4, "bltu", 2, 2, False ),
    gen_br2_src0_dep_test( 3, "bltu", 3, 2, False ),
    gen_br2_src0_dep_test( 2, "bltu", 4, 3, False ),
    gen_br2_src0_dep_test( 1, "bltu", 5, 4, False ),
    gen_br2_src0_dep_test( 0, "bltu", 6, 5, False ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------

def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "bltu", 7, 10, True ),
    gen_br2_src1_dep_test( 4, "bltu", 7, 11, True ),
    gen_br2_src1_dep_test( 3, "bltu", 7, 12, True ),
    gen_br2_src1_dep_test( 2, "bltu", 7, 13, True ),
    gen_br2_src1_dep_test( 1, "bltu", 7, 15, True ),
    gen_br2_src1_dep_test( 0, "bltu", 7, 70, True ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "bltu", 100, 11, False ),
    gen_br2_src1_dep_test( 4, "bltu", 120, 22, False ),
    gen_br2_src1_dep_test( 3, "bltu", 130, 33, False ),
    gen_br2_src1_dep_test( 2, "bltu", 140, 44, False ),
    gen_br2_src1_dep_test( 1, "bltu", 150, 55, False ),
    gen_br2_src1_dep_test( 0, "bltu", 160, 66, False ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bltu", 11, 222, True ),
    gen_br2_srcs_dep_test( 4, "bltu", 22, 333, True ),
    gen_br2_srcs_dep_test( 3, "bltu", 33, 444, True ),
    gen_br2_srcs_dep_test( 2, "bltu", 45, 555, True ),
    gen_br2_srcs_dep_test( 1, "bltu", 56, 666, True ),
    gen_br2_srcs_dep_test( 0, "bltu", 69, 777, True ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_nottaken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bltu", 100, 10, False ),
    gen_br2_srcs_dep_test( 4, "bltu", 200, 22, False ),
    gen_br2_srcs_dep_test( 3, "bltu", 300, 34, False ),
    gen_br2_srcs_dep_test( 2, "bltu", 400, 41, False ),
    gen_br2_srcs_dep_test( 1, "bltu", 500, 57, False ),
    gen_br2_srcs_dep_test( 0, "bltu", 600, 69, False ),
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "bltu", 1,   False ),
    gen_br2_src0_eq_src1_test( "bltu", 50,  False ),
    gen_br2_src0_eq_src1_test( "bltu", 700, False ),
    gen_br2_src0_eq_src1_test( "bltu", 999, False ),
    gen_br2_src0_eq_src1_test( "bltu", 814, False ),
    gen_br2_src0_eq_src1_test( "bltu", 331, False ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_br2_value_test( "bltu", 0xfffffff7, 0xfffffff7, False ),
    gen_br2_value_test( "bltu", 0x7fffffff, 0x7fffffff, False ),
    gen_br2_value_test( "bltu", 0xfffffff7, 0x7fffffff, False  ),
    gen_br2_value_test( "bltu", 0x7fffffff, 0xfffffff7, True  ),
    gen_br2_value_test( "bltu", 0xffffffff, 0xfffffffe, False  ),
    gen_br2_value_test( "bltu", 0xfffffffd, 0xffffffff, True  ),
    gen_br2_value_test( "bltu", 0xffffff00, 0xffffff77, True  ),

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
      if src1 == 0x00000000:
        src1 = src1 + 0x00000001
        src0 = src1 - 0x00000001
      else:
        src0 = src1 - 0x00000001
    else:
      # Branch not taken, operands are equal
      if src1 == 0xffffffff:
        src0 = src1
      else:
        src0 = src1 + 0x00000001
    asm_code.append( gen_br2_value_test( "bltu", src0.uint(), src1.uint(), taken ) )
  return asm_code
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
