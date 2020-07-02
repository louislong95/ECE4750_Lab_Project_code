#=========================================================================
# jal
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0     # 0x0200
                        #
    nop                 # 0x0204
    nop                 # 0x0208
    nop                 # 0x020c
    nop                 # 0x0210
    nop                 # 0x0214
    nop                 # 0x0218
    nop                 # 0x021c
    nop                 # 0x0220
                        #
    jal   x1, label_a   # 0x0224
    addi  x3, x3, 0b01  # 0x0228

    nop   # 0x022c
    nop   # 0x0230
    nop   # 0x0234
    nop   # 0x0238
    nop   # 0x023c
    nop   # 0x0240
    nop   # 0x0244
    nop   # 0x0248

  label_a:
    addi  x3, x3, 0b10    # 0x024c

    # Check the link address
    csrw  proc2mngr, x1 > 0x0228 

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3 > 0b10

  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
def gen_no_nop_test():
  return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0     # 0x0200
    jal   x1, label_a    # 0x0204
    addi  x3, x3, 0b01  # 0x0208

    nop  # 0x020c
    nop  # 0x0210
    nop  # 0x0214
    nop  # 0x0218
    nop  # 0x021c
    nop  # 0x0220
    nop  # 0x0224
    nop  # 0x0228

  label_a:
    addi  x3, x3, 0b10   # 0x022c

    # Check the link address
    csrw  proc2mngr, x1 > 0x0208 

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3 > 0b10

  """

def gen_stall_before_test():
  return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0     # 0x0200
    sub   x1, x1, x3     # 0x0204
    jal   x1, label_a   # 0x0208
    addi  x3, x3, 0b01  # 0x020c

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

    # Check the link address
    csrw  proc2mngr, x1 > 0x020c

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3 > 0b10

  """

def gen_jal_eval_test():
  return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0     # 0x0200
    addi  x1, x0, 1     # 0x0204
    addi  x2, x0, 2     # 0x0208
    bne   x1, x2, label_test   #0x020c
    sub   x4, x4, x3     # 0x0210
    jal   x5, label_a   # 0x0214
    addi  x3, x3, 0b001  # 0x0218

    nop   #0x021c
    nop   #0x0220
    nop   #0x0224
    nop   #0x0228
    nop   #0x022c
    nop   #0x0230
    nop   #0x0234
    nop   #0x0238

  label_a:
    addi  x3, x3, 0b010   #0x023c
    
  label_test:
    addi  x3, x3, 0b100    #0x0240

    # Check the link address
    # csrw  proc2mngr, x5 > 0x020c
    csrw  proc2mngr, x1 > 1  #0x0244

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3 > 0b100

  """
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
