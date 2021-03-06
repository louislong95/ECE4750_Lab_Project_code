#=========================================================================
# BlockingCacheBaseRTL_test.py
#=========================================================================

from __future__ import print_function

import pytest
import random
import struct

from pymtl      import *
from pclib.test import mk_test_case_table, run_sim
from pclib.test import TestSource
from pclib.test import TestMemory

from pclib.ifcs import MemMsg,    MemReqMsg,    MemRespMsg
from pclib.ifcs import MemMsg4B,  MemReqMsg4B,  MemRespMsg4B
from pclib.ifcs import MemMsg16B, MemReqMsg16B, MemRespMsg16B

from TestCacheSink        import TestCacheSink
from BlockingCacheFL_test import test_case_table_generic
from BlockingCacheFL_test import test_case_table_dir_mapped
from BlockingCacheFL_test import TestHarness

from lab3_mem.BlockingCacheBaseRTL import BlockingCacheBaseRTL

# We import tests defined in BlockingCacheFL_test.py. The idea is we can
# use the same tests for both FL and RTL model.
#
# Notice the difference between the TestHarness instances in FL and RTL.
#
# class TestHarness( Model ):
#   def __init__( s, src_msgs, sink_msgs, stall_prob, latency,
#                 src_delay, sink_delay, CacheModel, check_test, dump_vcd )
#
# The last parameter of TestHarness, check_test is whether or not we
# check the test field in the cacheresp. In FL model we don't care about
# test field and we set cehck_test to be False because FL model is just
# passing through cachereq to mem, so all cachereq sent to the FL model
# will be misses, whereas in RTL model we must set cehck_test to be True
# so that the test sink will know if we hit the cache properly.

#-------------------------------------------------------------------------
# Generic tests for both baseline and alternative design
#-------------------------------------------------------------------------

class TestHarness( Model ):

  def __init__( s, src_msgs, sink_msgs, stall_prob, latency,
                src_delay, sink_delay, 
                CacheModel, num_banks, check_test, dump_vcd ):

    # Messge type

    cache_msgs = MemMsg4B()
    mem_msgs   = MemMsg16B()

    # Instantiate models

    s.src   = TestSource   ( cache_msgs.req,  src_msgs,  src_delay  )
    s.cache = CacheModel   ( num_banks = num_banks )
    s.mem   = TestMemory   ( mem_msgs, 1, stall_prob, latency )
    s.sink  = TestCacheSink( cache_msgs.resp, sink_msgs, sink_delay, check_test )

    # Dump VCD

    if dump_vcd:
      s.cache.vcd_file = dump_vcd

    # Connect

    s.connect( s.src.out,       s.cache.cachereq  )
    s.connect( s.sink.in_,      s.cache.cacheresp )

    s.connect( s.cache.memreq,  s.mem.reqs[0]     )
    s.connect( s.cache.memresp, s.mem.resps[0]    )

  def load( s, addrs, data_ints ):
    for addr, data_int in zip( addrs, data_ints ):
      data_bytes_a = bytearray()
      data_bytes_a.extend( struct.pack("<I",data_int) )
      s.mem.write_mem( addr, data_bytes_a )

  def done( s ):
    return s.src.done and s.sink.done

  def line_trace( s ):
    return s.src.line_trace() + " " + s.cache.line_trace() + " " \
         + s.mem.line_trace() + " " + s.sink.line_trace()

#-------------------------------------------------------------------------
# make messages
#-------------------------------------------------------------------------

def req( type_, opaque, addr, len, data ):
  msg = MemReqMsg4B()

  if   type_ == 'rd': msg.type_ = MemReqMsg.TYPE_READ
  elif type_ == 'wr': msg.type_ = MemReqMsg.TYPE_WRITE
  elif type_ == 'in': msg.type_ = MemReqMsg.TYPE_WRITE_INIT

  msg.addr   = addr
  msg.opaque = opaque
  msg.len    = len
  msg.data   = data
  return msg

def resp( type_, opaque, test, len, data ):
  msg = MemRespMsg4B()

  if   type_ == 'rd': msg.type_ = MemRespMsg.TYPE_READ
  elif type_ == 'wr': msg.type_ = MemRespMsg.TYPE_WRITE
  elif type_ == 'in': msg.type_ = MemRespMsg.TYPE_WRITE_INIT

  msg.opaque = opaque
  msg.len    = len
  msg.test   = test
  msg.data   = data
  return msg


def read_hit_1word_clean( base_addr ):
  return [
    #    type  opq  addr      len data                type  opq  test len data
    req( 'in', 0x0, base_addr, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'rd', 0x1, base_addr, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xdeadbeef ),
  ]

def read_hit_1word_dirty(base_addr):
  return [
    #    type  opq  addr      len data                type  opq  test len data
    req( 'wr', 0x0, base_addr, 0, 0x00000111 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, base_addr, 0, 0x00001111 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'rd', 0x2, base_addr, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x00001111 ),
  ]
  
@pytest.mark.parametrize( **test_case_table_generic )
def test_generic( test_params, dump_vcd ):
  msgs = test_params.msg_func( 0 )
  if test_params.mem_data_func != None:
    mem = test_params.mem_data_func( 0 )
  # Instantiate testharness
  harness = TestHarness( msgs[::2], msgs[1::2],
                         test_params.stall, test_params.lat,
                         test_params.src, test_params.sink,
                         BlockingCacheBaseRTL, test_params.nbank,
                         True, dump_vcd )
  # Load memory before the test
  if test_params.mem_data_func != None:
    harness.load( mem[::2], mem[1::2] )
  # Run the test
  run_sim( harness, dump_vcd )
  
test_case_table_generic = mk_test_case_table([
  (                                   "msg_func                          mem_data_func                     nbank stall lat src sink"),
  [ "read_hit_1word_clean",           read_hit_1word_clean,              None,                             0,    0.0,  0,  0,  0    ],
  [ "read_hit_1word_dirty",           read_hit_1word_dirty,              None,                             0,    0.0,  0,  0,  0    ],
  #[ "write_hit_1word_clean",          read_hit_1word_clean,              None,                             0,    0.0,  0,  0,  0    ],
  #[ "write_hit_1word_dirty",          read_hit_1word_dirty,              None,                             0,    0.0,  0,  0,  0    ],
  #[ "read_miss_1word",                read_miss_1word_msg,               read_miss_1word_mem,              0,    0.0,  0,  0,  0    ],
  #[ "read_miss_refill_no_eviction",   read_miss_refill_no_eviction,      read_miss_refill_no_eviction_mem, 0,    0.0,  0,  0,  0    ],
  #[ "write_miss_refill_no_eviction",  write_miss_refill_no_eviction,     write_miss_refill_no_eviction_mem,0,    0.0,  0,  0,  0    ],
  #[ "read_hit_1word_4bank",           read_hit_1word_clean,              None,                             4,    0.0,  0,  0,  0    ],
  ])
#-------------------------------------------------------------------------
# Tests only for direct-mapped cache
#-------------------------------------------------------------------------


@pytest.mark.parametrize( **test_case_table_dir_mapped )
def test_dir_mapped( test_params, dump_vcd ):
  msgs = test_params.msg_func( 0 )
  if test_params.mem_data_func != None:
    mem  = test_params.mem_data_func( 0 )
  # Instantiate testharness
  harness = TestHarness( msgs[::2], msgs[1::2],
                         test_params.stall, test_params.lat,
                         test_params.src, test_params.sink,
                         BlockingCacheBaseRTL, test_params.nbank,
                         True, dump_vcd )
  # Load memory before the test
  if test_params.mem_data_func != None:
    harness.load( mem[::2], mem[1::2] )
  # Run the test
  run_sim( harness, dump_vcd )


#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
