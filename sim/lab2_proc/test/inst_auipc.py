#=========================================================================
# auipc
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    auipc x1, 0x00010                       # PC=0x200
    nop   # 0x204
    nop  # 0x208
    nop   # 0x20c
    nop   # 0x210
    nop   # 0x214
    nop   # 0x218
    nop   # 0x21c
    nop
    csrw  proc2mngr, x1 > 0x00010200
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
def gen_no_nop_after():
  return """
    auipc x1, 0xFFFFF                      # PC=0x200
    csrw  proc2mngr, x1 > 0xFFFFF200
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
