#=========================================================================
# BlockingCacheFL_test.py
#=========================================================================

from __future__ import print_function

import pytest
import random
import struct
import math
import random

random.seed(0xa4e28cc2)

from pymtl      import *
from pclib.test import mk_test_case_table, run_sim
from pclib.test import TestSource
from pclib.test import TestMemory

from pclib.ifcs import MemMsg,    MemReqMsg,    MemRespMsg
from pclib.ifcs import MemMsg4B,  MemReqMsg4B,  MemRespMsg4B
from pclib.ifcs import MemMsg16B, MemReqMsg16B, MemRespMsg16B

from TestCacheSink   import TestCacheSink
from lab3_mem.BlockingCacheFL import BlockingCacheFL

# We define all test cases here. They will be used to test _both_ FL and
# RTL models.
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
# will be misses, whereas in RTL model we must set check_test to be True
# so that the test sink will know if we hit the cache properly.

#-------------------------------------------------------------------------
# TestHarness
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

#----------------------------------------------------------------------
# Test Case: read hit path
#----------------------------------------------------------------------
# The test field in the response message: 0 == MISS, 1 == HIT

def read_hit_1word_clean( base_addr ):
  return [
    #    type  opq  addr      len data                 type  opq  test len data
    req( 'in', 0x00, base_addr, 0, 0xdeadbeef ), resp( 'in', 0x00, 0,   0,  0          ),
    req( 'rd', 0x01, base_addr, 0, 0          ), resp( 'rd', 0x01, 1,   0,  0xdeadbeef ),
  ]

def read_hit_1word_dirty(base_addr):
  return [
  #    type  opq  addr      len data                 type  opq  test len data
  req( 'wr', 0x00, base_addr, 0, 0x00000111 ), resp( 'wr', 0x00, 0,   0,  0          ),
  req( 'wr', 0x01, base_addr, 0, 0x00001111 ), resp( 'wr', 0x01, 1,   0,  0          ),
  req( 'rd', 0x02, base_addr, 0, 0          ), resp( 'rd', 0x02, 1,   0,  0x00001111 ),
  ]
 
#----------------------------------------------------------------------
# Test Case: read hit path -- for set-associative cache
#----------------------------------------------------------------------
# This set of tests designed only for alternative design  /////////////////////take care of it later
# The test field in the response message: 0 == MISS, 1 == HIT

def read_hit_asso( base_addr ):
  return [
    #     type  opq  addr       len data                 type  opq  test len data
    req( 'wr', 0x00, 0x00000000, 0, 0xdeadbeef ), resp( 'wr', 0x00, 0,   0,  0          ),
    req( 'wr', 0x01, 0x00000004, 0, 0x00c0ffee ), resp( 'wr', 0x01, 1,   0,  0          ),
    req( 'rd', 0x02, 0x00000000, 0, 0          ), resp( 'rd', 0x02, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x03, 0x00000004, 0, 0          ), resp( 'rd', 0x03, 1,   0,  0x00c0ffee ),
  ]

def read_miss_asso( base_addr ):
  return [
    #     type  opq  addr       len data                 type  opq  test len data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp( 'rd', 0x00, 0,   0,  0xdeadbeef ),
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp( 'rd', 0x01, 1,   0,  0x00c0ffee ),
    req( 'rd', 0x02, 0x00000008, 0, 0          ), resp( 'rd', 0x02, 1,   0,  0x00000011 ),
    req( 'rd', 0x03, 0x0000000c, 0, 0          ), resp( 'rd', 0x03, 1,   0,  0x00000012 ),
    req( 'rd', 0x04, 0x00000010, 0, 0          ), resp( 'rd', 0x04, 0,   0,  0x00000013 ),
  ]
#----------------------------------------------------------------------
# Test Case: read hit path -- for direct-mapped cache
#----------------------------------------------------------------------
# This set of tests designed only for baseline design

def read_hit_dmap( base_addr ):
  return [
    #     type  opq  addr       len data                type  opq  test len data
    req( 'wr', 0x00, 0x00000000, 0, 0xdeadbeef ), resp( 'wr', 0x00, 0,   0,  0          ),
    req( 'wr', 0x01, 0x00000010, 0, 0x00c00001 ), resp( 'wr', 0x01, 0,   0,  0          ),
    req( 'wr', 0x02, 0x00000020, 0, 0x00c00002 ), resp( 'wr', 0x02, 0,   0,  0          ),
    req( 'wr', 0x03, 0x00000030, 0, 0x00c00003 ), resp( 'wr', 0x03, 0,   0,  0          ),
    req( 'wr', 0x04, 0x00000040, 0, 0x00c00004 ), resp( 'wr', 0x04, 0,   0,  0          ),
    req( 'wr', 0x05, 0x00000050, 0, 0x00c00005 ), resp( 'wr', 0x05, 0,   0,  0          ),
    req( 'wr', 0x06, 0x00000060, 0, 0x00c00006 ), resp( 'wr', 0x06, 0,   0,  0          ),
    req( 'wr', 0x07, 0x00000070, 0, 0x00c00007 ), resp( 'wr', 0x07, 0,   0,  0          ),
    req( 'wr', 0x08, 0x00000080, 0, 0x00c0ffee ), resp( 'wr', 0x08, 0,   0,  0          ),
    req( 'wr', 0x09, 0x000000a0, 0, 0x00c0000a ), resp( 'wr', 0x09, 0,   0,  0          ),
    req( 'rd', 0x0a, 0x00000000, 0, 0          ), resp( 'rd', 0x0a, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x0b, 0x00000080, 0, 0          ), resp( 'rd', 0x0b, 1,   0,  0x00c0ffee ),
    req( 'rd', 0x0c, 0x00000010, 0, 0          ), resp( 'rd', 0x0c, 1,   0,  0x00c00001 ),
    req( 'rd', 0x0d, 0x00000020, 0, 0          ), resp( 'rd', 0x0d, 1,   0,  0x00c00002 ),
    req( 'rd', 0x0e, 0x00000030, 0, 0          ), resp( 'rd', 0x0e, 1,   0,  0x00c00003 ),
    req( 'rd', 0x10, 0x00000040, 0, 0          ), resp( 'rd', 0x10, 1,   0,  0x00c00004 ),
    req( 'rd', 0x11, 0x00000050, 0, 0          ), resp( 'rd', 0x11, 1,   0,  0x00c00005 ),
    req( 'rd', 0x12, 0x00000060, 0, 0          ), resp( 'rd', 0x12, 1,   0,  0x00c00006 ),
    req( 'rd', 0x13, 0x00000070, 0, 0          ), resp( 'rd', 0x13, 1,   0,  0x00c00007 ),
    req( 'rd', 0x14, 0x000000a0, 0, 0          ), resp( 'rd', 0x14, 1,   0,  0x00c0000a ),
    
  ]

#-------------------------------------------------------------------------
# Test Case: write hit path
#-------------------------------------------------------------------------

def write_hit_1word_clean( base_addr ):
  return [
    #    type  opq   addr      len data               type  opq   test len data
    req( 'in', 0x00, base_addr, 0, 0x0a0b0c0d ), resp('in', 0x00, 0,   0,  0          ), # write word  0x00000000
    req( 'wr', 0x01, base_addr, 0, 0xbeefbeeb ), resp('wr', 0x01, 1,   0,  0          ), # write word  0x00000000
    req( 'rd', 0x02, base_addr, 0, 0          ), resp('rd', 0x02, 1,   0,  0xbeefbeeb ), # read  word  0x00000000
  ]

def write_hit_1word_dirty( base_addr ):
  return [
    #    type  opq   addr      len data               type  opq   test len data
    req( 'in', 0x00, base_addr, 0, 0x0a0b0c0d ), resp('in', 0x00, 0,   0,  0          ), # write word  0x00000000
    req( 'wr', 0x01, base_addr, 0, 0xbeefbeeb ), resp('wr', 0x01, 1,   0,  0          ), # write word  0x00000000
    req( 'wr', 0x02, base_addr, 0, 0x12345678 ), resp('wr', 0x02, 1,   0,  0          ), # read  word  0x00000000
    req( 'rd', 0x03, base_addr, 0, 0          ), resp('rd', 0x03, 1,   0,  0x12345678 ), # write word  0x00000000
  ]


#-------------------------------------------------------------------------
# Test Case: read miss path
#-------------------------------------------------------------------------

def read_miss_refill_no_eviction( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000010, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), #test 1
    req( 'rd', 0x01, 0x00001010, 0, 0          ), resp('rd', 0x01, 0, 0, 0x11111111 ), 
    req( 'rd', 0x02, 0x00001014, 0, 0          ), resp('rd', 0x02, 1, 0, 0x22222222 ),  
    req( 'rd', 0x03, 0x00001018, 0, 0          ), resp('rd', 0x03, 1, 0, 0x33333333 ),
    req( 'rd', 0x04, 0x0000101c, 0, 0          ), resp('rd', 0x04, 1, 0, 0x55555555 ), 
    req( 'rd', 0x05, 0x00000020, 0, 0          ), resp('rd', 0x05, 0, 0, 0x00000000 ), #test 2
    req( 'rd', 0x06, 0x00001020, 0, 0          ), resp('rd', 0x06, 0, 0, 0x00000001 ),
    req( 'rd', 0x07, 0x00001024, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000002 ),  
    req( 'rd', 0x08, 0x00001028, 0, 0          ), resp('rd', 0x08, 1, 0, 0x00000003 ),
    req( 'rd', 0x09, 0x0000102c, 0, 0          ), resp('rd', 0x09, 1, 0, 0x00000005 ), 
  ]

# Data to be loaded into memory before running the test

def read_miss_refill_no_eviction_mem( base_addr ):
 return [
    # addr      data (in int)
    0x00000010, 0xdeadbeef,
    0x00000020, 0x00000000,
    0x00001010, 0x11111111,
    0x00001014, 0x22222222,
    0x00001018, 0x33333333,
    0x0000101c, 0x55555555,
    0x00001020, 0x00000001,
    0x00001024, 0x00000002,
    0x00001028, 0x00000003,
    0x0000102c, 0x00000005,
  ]

def write_miss_refill_no_eviction( base_addr ):
 return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000020, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0, 0          ), #test 1
    req( 'rd', 0x01, 0x00000020, 0, 0          ), resp('rd', 0x01, 1, 0, 0xdeadbeef ), 
    req( 'rd', 0x02, 0x00000024, 0, 0          ), resp('rd', 0x02, 1, 0, 0x22222222 ),  
    req( 'rd', 0x03, 0x00000028, 0, 0          ), resp('rd', 0x03, 1, 0, 0x33333333 ),
    req( 'rd', 0x04, 0x0000002c, 0, 0          ), resp('rd', 0x04, 1, 0, 0x55555555 ),
    req( 'wr', 0x05, 0x00001020, 0, 0xdeadbbbb ), resp('wr', 0x05, 0, 0, 0          ), #test 2
    req( 'rd', 0x06, 0x00001020, 0, 0          ), resp('rd', 0x06, 1, 0, 0xdeadbbbb ), 
    req( 'rd', 0x07, 0x00001024, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00222222 ),  
    req( 'rd', 0x08, 0x00001028, 0, 0          ), resp('rd', 0x08, 1, 0, 0x00333333 ),
    req( 'rd', 0x09, 0x0000102c, 0, 0          ), resp('rd', 0x09, 1, 0, 0x00555555 ),
  ]

# Data to be loaded into memory before running the test

def write_miss_refill_no_eviction_mem( base_addr ):
 return [
    # addr      data (in int)
    0x00000020, 0xdeadbeef,
    0x00000024, 0x22222222,
    0x00000028, 0x33333333,
    0x0000002c, 0x55555555,
    0x00001020, 0xdeadbbbb,
    0x00001024, 0x00222222,
    0x00001028, 0x00333333,
    0x0000102c, 0x00555555,
  ]

def read_miss_refill_eviction_dmap( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000010, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0, 0          ), 
    req( 'wr', 0x01, 0x00000010, 0, 0xffffffff ), resp('wr', 0x01, 1, 0, 0          ), #become dirty line
    req( 'rd', 0x02, 0x00001010, 0, 0          ), resp('rd', 0x02, 0, 0, 0x11111111 ), #eviction 
    req( 'rd', 0x03, 0x00001014, 0, 0          ), resp('rd', 0x03, 1, 0, 0x22222222 ),
    req( 'rd', 0x04, 0x00001018, 0, 0          ), resp('rd', 0x04, 1, 0, 0x33333333 ), 
    req( 'rd', 0x05, 0x0000101c, 0, 0          ), resp('rd', 0x05, 1, 0, 0x55555555 ), 
    req( 'rd', 0x06, 0x00000010, 0, 0          ), resp('rd', 0x06, 0, 0, 0xffffffff ), #check the memory if it is updated
  ]

# Data to be loaded into memory before running the test

def read_miss_refill_eviction_dmap_mem( base_addr ):
 return [
    # addr      data (in int)
    0x00000010, 0xdeadbeef,
    0x00001010, 0x11111111,
    0x00001014, 0x22222222,
    0x00001018, 0x33333333,
    0x0000101c, 0x55555555,
  ]

def read_miss_refill_eviction_assoc( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000010, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0, 0          ), 
    req( 'wr', 0x01, 0x00000010, 0, 0xffffffff ), resp('wr', 0x01, 1, 0, 0          ), # hit fill in way 0
    req( 'wr', 0x02, 0x00001010, 0, 0xaaaaaaaa ), resp('wr', 0x02, 0, 0, 0          ), # miss, fill in way 1
    req( 'rd', 0x03, 0x00001014, 0, 0          ), resp('rd', 0x03, 1, 0, 0x22222222 ),
    req( 'rd', 0x04, 0x00001018, 0, 0          ), resp('rd', 0x04, 1, 0, 0x33333333 ), 
    req( 'rd', 0x05, 0x0000101c, 0, 0          ), resp('rd', 0x05, 1, 0, 0x55555555 ), 
    req( 'rd', 0x06, 0x00002010, 0, 0          ), resp('rd', 0x06, 0, 0, 0x00000011 ), # miss, evict way 0
    req( 'rd', 0x07, 0x00002014, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000022 ), 
    req( 'rd', 0x08, 0x00002018, 0, 0          ), resp('rd', 0x08, 1, 0, 0x00000033 ), 
    req( 'rd', 0x09, 0x0000201c, 0, 0          ), resp('rd', 0x09, 1, 0, 0x00000044 ),
    req( 'rd', 0x0a, 0x00000010, 0, 0          ), resp('rd', 0x0a, 0, 0, 0xffffffff ),
    req( 'rd', 0x0b, 0x00002090, 0, 0          ), resp('rd', 0x0b, 0, 0, 0x00000333 ), # important
    req( 'rd', 0x0c, 0x00002094, 0, 0          ), resp('rd', 0x0c, 1, 0, 0x00000444 ),
    req( 'rd', 0x0d, 0x00002098, 0, 0          ), resp('rd', 0x0d, 1, 0, 0x0000ffff ),
    req( 'rd', 0x0e, 0x00000010, 0, 0          ), resp('rd', 0x0e, 1, 0, 0xffffffff ),
  ]

# Data to be loaded into memory before running the test

def read_miss_refill_eviction_assoc_mem( base_addr ):
 return [
    # addr      data (in int)
    0x00000010, 0xdeadbeef,
    0x00001010, 0x11111111,
    0x00001014, 0x22222222,
    0x00001018, 0x33333333,
    0x0000101c, 0x55555555,
    0x00002010, 0x00000011,
    0x00002014, 0x00000022,
    0x00002018, 0x00000033,
    0x0000201c, 0x00000044,
    0x00002090, 0x00000333,
    0x00002094, 0x00000444,
    0x00002098, 0x0000ffff,
  ]
  
def write_miss_refill_eviction_dmap( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000010, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0, 0          ), 
    req( 'wr', 0x01, 0x00000010, 0, 0x00000fff ), resp('wr', 0x01, 1, 0, 0          ), # hit,dirty way 
    req( 'wr', 0x02, 0x00001010, 0, 0x00000aaa ), resp('wr', 0x02, 0, 0, 0          ), # miss,refill
    req( 'rd', 0x03, 0x00001014, 0, 0          ), resp('rd', 0x03, 1, 0, 0x00000222 ),
    req( 'rd', 0x04, 0x00001018, 0, 0          ), resp('rd', 0x04, 1, 0, 0x00000333 ), 
    req( 'rd', 0x05, 0x0000101c, 0, 0          ), resp('rd', 0x05, 1, 0, 0x00000555 ), 
    req( 'rd', 0x06, 0x00000010, 0, 0          ), resp('rd', 0x06, 0, 0, 0x00000fff ), #check memory whether it is updated
  ]

# Data to be loaded into memory before running the test

def write_miss_refill_eviction_dmap_mem( base_addr ):
 return [
    # addr      data (in int)
    0x00000010, 0x00000009,
    0x00001010, 0x11111111,
    0x00001014, 0x00000222,
    0x00001018, 0x00000333,
    0x0000101c, 0x00000555,
  ]

def write_miss_refill_eviction_assoc( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000010, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0, 0          ), # miss, fill way 0
    req( 'wr', 0x01, 0x00000010, 0, 0x000eefff ), resp('wr', 0x01, 1, 0, 0          ), # hit,dirty way
    req( 'rd', 0x03, 0x00000014, 0, 0          ), resp('rd', 0x03, 1, 0, 0x0000000a ),
    req( 'rd', 0x04, 0x00000018, 0, 0          ), resp('rd', 0x04, 1, 0, 0x0000000b ), 
    req( 'rd', 0x05, 0x0000001c, 0, 0          ), resp('rd', 0x05, 1, 0, 0x0000000c ), 
    req( 'wr', 0x02, 0x00003010, 0, 0x000eeaaa ), resp('wr', 0x02, 0, 0, 0          ), # miss,fill way 1
    req( 'rd', 0x03, 0x00003014, 0, 0          ), resp('rd', 0x03, 1, 0, 0x00000222 ),
    req( 'rd', 0x04, 0x00003018, 0, 0          ), resp('rd', 0x04, 1, 0, 0x00000333 ), 
    req( 'rd', 0x05, 0x0000301c, 0, 0          ), resp('rd', 0x05, 1, 0, 0x00000555 ), 
    req( 'wr', 0x06, 0x00004010, 0, 0x77777888 ), resp('wr', 0x06, 0, 0, 0          ), # miss, eviction and refill way 0
    req( 'rd', 0x07, 0x00004010, 0, 0          ), resp('rd', 0x07, 1, 0, 0x77777888 ),
    req( 'rd', 0x0b, 0x00000010, 0, 0          ), resp('rd', 0x0b, 0, 0, 0x000eefff ),
  ]

# Data to be loaded into memory before running the test

def write_miss_refill_eviction_assoc_mem( base_addr ):
 return [
    # addr      data (in int)
    0x00000010, 0x00000009,
    0x00000014, 0x0000000a,
    0x00000018, 0x0000000b,
    0x0000001c, 0x0000000c,
    0x00003010, 0x11111111,
    0x00003014, 0x00000222,
    0x00003018, 0x00000333,
    0x0000301c, 0x00000555,
    0x00004010, 0x00000011,
  ]

def capacity_miss_dmap( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0x00000009 ), # miss, fill line0
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x0000000a ), 
    req( 'rd', 0x03, 0x00000008, 0, 0          ), resp('rd', 0x03, 1, 0, 0x0000000b ),
    req( 'rd', 0x04, 0x0000000c, 0, 0          ), resp('rd', 0x04, 1, 0, 0x0000000c ), 
    req( 'rd', 0x05, 0x00000010, 0, 0          ), resp('rd', 0x05, 0, 0, 0x00000019 ), # miss, fill line1
    req( 'rd', 0x06, 0x00000014, 0, 0          ), resp('rd', 0x06, 1, 0, 0x0000001a ), 
    req( 'rd', 0x07, 0x00000018, 0, 0          ), resp('rd', 0x07, 1, 0, 0x0000001b ),
    req( 'rd', 0x08, 0x0000001c, 0, 0          ), resp('rd', 0x08, 1, 0, 0x0000001c ), 
    req( 'rd', 0x09, 0x00000020, 0, 0          ), resp('rd', 0x09, 0, 0, 0x00000029 ), # miss, fill line2
    req( 'rd', 0x0a, 0x00000024, 0, 0          ), resp('rd', 0x0a, 1, 0, 0x0000002a ), 
    req( 'rd', 0x0b, 0x00000028, 0, 0          ), resp('rd', 0x0b, 1, 0, 0x0000002b ),
    req( 'rd', 0x0c, 0x0000002c, 0, 0          ), resp('rd', 0x0c, 1, 0, 0x0000002c ), 
    req( 'rd', 0x0d, 0x00000030, 0, 0          ), resp('rd', 0x0d, 0, 0, 0x00000039 ), # miss, fill line3
    req( 'rd', 0x0e, 0x00000034, 0, 0          ), resp('rd', 0x0e, 1, 0, 0x0000003a ), 
    req( 'rd', 0x0f, 0x00000038, 0, 0          ), resp('rd', 0x0f, 1, 0, 0x0000003b ),
    req( 'rd', 0x10, 0x0000003c, 0, 0          ), resp('rd', 0x10, 1, 0, 0x0000003c ), 
    req( 'rd', 0x11, 0x00000040, 0, 0          ), resp('rd', 0x11, 0, 0, 0x00000049 ), # miss, fill line4
    req( 'rd', 0x12, 0x00000044, 0, 0          ), resp('rd', 0x12, 1, 0, 0x0000004a ), 
    req( 'rd', 0x13, 0x00000048, 0, 0          ), resp('rd', 0x13, 1, 0, 0x0000004b ),
    req( 'rd', 0x14, 0x0000004c, 0, 0          ), resp('rd', 0x14, 1, 0, 0x0000004c ), 
    req( 'rd', 0x15, 0x00000050, 0, 0          ), resp('rd', 0x15, 0, 0, 0x00000059 ), # miss, fill line5
    req( 'rd', 0x16, 0x00000054, 0, 0          ), resp('rd', 0x16, 1, 0, 0x0000005a ), 
    req( 'rd', 0x17, 0x00000058, 0, 0          ), resp('rd', 0x17, 1, 0, 0x0000005b ),
    req( 'rd', 0x18, 0x0000005c, 0, 0          ), resp('rd', 0x18, 1, 0, 0x0000005c ), 
    req( 'rd', 0x19, 0x00000060, 0, 0          ), resp('rd', 0x19, 0, 0, 0x00000069 ), # miss, fill line6
    req( 'rd', 0x1a, 0x00000064, 0, 0          ), resp('rd', 0x1a, 1, 0, 0x0000006a ), 
    req( 'rd', 0x1b, 0x00000068, 0, 0          ), resp('rd', 0x1b, 1, 0, 0x0000006b ),
    req( 'rd', 0x1c, 0x0000006c, 0, 0          ), resp('rd', 0x1c, 1, 0, 0x0000006c ), 
    req( 'rd', 0x1d, 0x00000070, 0, 0          ), resp('rd', 0x1d, 0, 0, 0x00000079 ), # miss, fill line7
    req( 'rd', 0x1e, 0x00000074, 0, 0          ), resp('rd', 0x1e, 1, 0, 0x0000007a ), 
    req( 'rd', 0x1f, 0x00000078, 0, 0          ), resp('rd', 0x1f, 1, 0, 0x0000007b ),
    req( 'rd', 0x20, 0x0000007c, 0, 0          ), resp('rd', 0x20, 1, 0, 0x0000007c ), 
    req( 'rd', 0x21, 0x00000080, 0, 0          ), resp('rd', 0x21, 0, 0, 0x00000089 ), # miss, fill line8
    req( 'rd', 0x22, 0x00000084, 0, 0          ), resp('rd', 0x22, 1, 0, 0x0000008a ), 
    req( 'rd', 0x23, 0x00000088, 0, 0          ), resp('rd', 0x23, 1, 0, 0x0000008b ),
    req( 'rd', 0x24, 0x0000008c, 0, 0          ), resp('rd', 0x24, 1, 0, 0x0000008c ), 
    req( 'rd', 0x25, 0x00000090, 0, 0          ), resp('rd', 0x25, 0, 0, 0x00000099 ), # miss, fill line9
    req( 'rd', 0x26, 0x00000094, 0, 0          ), resp('rd', 0x26, 1, 0, 0x0000009a ), 
    req( 'rd', 0x27, 0x00000098, 0, 0          ), resp('rd', 0x27, 1, 0, 0x0000009b ),
    req( 'rd', 0x28, 0x0000009c, 0, 0          ), resp('rd', 0x28, 1, 0, 0x0000009c ), 
    req( 'rd', 0x29, 0x000000a0, 0, 0          ), resp('rd', 0x29, 0, 0, 0x000000a9 ), # miss, fill line10
    req( 'rd', 0x2a, 0x000000a4, 0, 0          ), resp('rd', 0x2a, 1, 0, 0x000000aa ), 
    req( 'rd', 0x2b, 0x000000a8, 0, 0          ), resp('rd', 0x2b, 1, 0, 0x000000ab ),
    req( 'rd', 0x2c, 0x000000ac, 0, 0          ), resp('rd', 0x2c, 1, 0, 0x000000ac ), 
    req( 'rd', 0x2d, 0x000000b0, 0, 0          ), resp('rd', 0x2d, 0, 0, 0x000000b9 ), # miss, fill line11
    req( 'rd', 0x2e, 0x000000b4, 0, 0          ), resp('rd', 0x2e, 1, 0, 0x000000ba ), 
    req( 'rd', 0x2f, 0x000000b8, 0, 0          ), resp('rd', 0x2f, 1, 0, 0x000000bb ),
    req( 'rd', 0x30, 0x000000bc, 0, 0          ), resp('rd', 0x30, 1, 0, 0x000000bc ), 
    req( 'rd', 0x31, 0x000000c0, 0, 0          ), resp('rd', 0x31, 0, 0, 0x000000c9 ), # miss, fill line12
    req( 'rd', 0x32, 0x000000c4, 0, 0          ), resp('rd', 0x32, 1, 0, 0x000000ca ), 
    req( 'rd', 0x33, 0x000000c8, 0, 0          ), resp('rd', 0x33, 1, 0, 0x000000cb ),
    req( 'rd', 0x34, 0x000000cc, 0, 0          ), resp('rd', 0x34, 1, 0, 0x000000cc ), 
    req( 'rd', 0x35, 0x000000d0, 0, 0          ), resp('rd', 0x35, 0, 0, 0x000000d9 ), # miss, fill line13
    req( 'rd', 0x36, 0x000000d4, 0, 0          ), resp('rd', 0x36, 1, 0, 0x000000da ), 
    req( 'rd', 0x37, 0x000000d8, 0, 0          ), resp('rd', 0x37, 1, 0, 0x000000db ),
    req( 'rd', 0x38, 0x000000dc, 0, 0          ), resp('rd', 0x38, 1, 0, 0x000000dc ), 
    req( 'rd', 0x39, 0x000000e0, 0, 0          ), resp('rd', 0x39, 0, 0, 0x000000e9 ), # miss, fill line14
    req( 'rd', 0x3a, 0x000000e4, 0, 0          ), resp('rd', 0x3a, 1, 0, 0x000000ea ), 
    req( 'rd', 0x3b, 0x000000e8, 0, 0          ), resp('rd', 0x3b, 1, 0, 0x000000eb ),
    req( 'rd', 0x3c, 0x000000ec, 0, 0          ), resp('rd', 0x3c, 1, 0, 0x000000ec ), 
    req( 'rd', 0x3d, 0x000000f0, 0, 0          ), resp('rd', 0x3d, 0, 0, 0x000000f9 ), # miss, fill line15
    req( 'rd', 0x3e, 0x000000f4, 0, 0          ), resp('rd', 0x3e, 1, 0, 0x000000fa ), 
    req( 'rd', 0x3f, 0x000000f8, 0, 0          ), resp('rd', 0x3f, 1, 0, 0x000000fb ),
    req( 'rd', 0x40, 0x000000fc, 0, 0          ), resp('rd', 0x40, 1, 0, 0x000000fc ), 
    req( 'rd', 0x41, 0x00010010, 0, 0          ), resp('rd', 0x41, 0, 0, 0x00001009 ), # miss, capacity miss, refill line1
    req( 'rd', 0x42, 0x00010014, 0, 0          ), resp('rd', 0x42, 1, 0, 0x0000100a ), # check if refilled
    req( 'rd', 0x43, 0x00010018, 0, 0          ), resp('rd', 0x43, 1, 0, 0x0000100b ),
    req( 'rd', 0x44, 0x0001001c, 0, 0          ), resp('rd', 0x44, 1, 0, 0x0000100c ), 
    req( 'rd', 0x05, 0x00000010, 0, 0          ), resp('rd', 0x05, 0, 0, 0x00000019 ), # check is line1 is replaced

    
  ]

# Data to be loaded into memory before running the test

def capacity_miss_dmap_mem( base_addr ):
 return [
    # addr      data (in int)
    0x00000000, 0x00000009,
    0x00000004, 0x0000000a,
    0x00000008, 0x0000000b,
    0x0000000c, 0x0000000c,
    0x00000010, 0x00000019,
    0x00000014, 0x0000001a,
    0x00000018, 0x0000001b,
    0x0000001c, 0x0000001c,
    0x00000020, 0x00000029,
    0x00000024, 0x0000002a,
    0x00000028, 0x0000002b,
    0x0000002c, 0x0000002c,
    0x00000030, 0x00000039,
    0x00000034, 0x0000003a,
    0x00000038, 0x0000003b,
    0x0000003c, 0x0000003c,
    0x00000040, 0x00000049,
    0x00000044, 0x0000004a,
    0x00000048, 0x0000004b,
    0x0000004c, 0x0000004c,
    0x00000050, 0x00000059,
    0x00000054, 0x0000005a,
    0x00000058, 0x0000005b,
    0x0000005c, 0x0000005c,
    0x00000060, 0x00000069,
    0x00000064, 0x0000006a,
    0x00000068, 0x0000006b,
    0x0000006c, 0x0000006c,
    0x00000070, 0x00000079,
    0x00000074, 0x0000007a,
    0x00000078, 0x0000007b,
    0x0000007c, 0x0000007c,
    0x00000080, 0x00000089,
    0x00000084, 0x0000008a,
    0x00000088, 0x0000008b,
    0x0000008c, 0x0000008c,
    0x00000090, 0x00000099,
    0x00000094, 0x0000009a,
    0x00000098, 0x0000009b,
    0x0000009c, 0x0000009c,
    0x000000a0, 0x000000a9,
    0x000000a4, 0x000000aa,
    0x000000a8, 0x000000ab,
    0x000000ac, 0x000000ac,
    0x000000b0, 0x000000b9,
    0x000000b4, 0x000000ba,
    0x000000b8, 0x000000bb,
    0x000000bc, 0x000000bc,
    0x000000c0, 0x000000c9,
    0x000000c4, 0x000000ca,
    0x000000c8, 0x000000cb,
    0x000000cc, 0x000000cc,
    0x000000d0, 0x000000d9,
    0x000000d4, 0x000000da,
    0x000000d8, 0x000000db,
    0x000000dc, 0x000000dc,
    0x000000e0, 0x000000e9,
    0x000000e4, 0x000000ea,
    0x000000e8, 0x000000eb,
    0x000000ec, 0x000000ec,
    0x000000f0, 0x000000f9,
    0x000000f4, 0x000000fa,
    0x000000f8, 0x000000fb,
    0x000000fc, 0x000000fc,
    0x00010010, 0x00001009,
    0x00010014, 0x0000100a,
    0x00010018, 0x0000100b,
    0x0001001c, 0x0000100c,
  ]
  
def capacity_miss_assoc( base_addr ):
 return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0x00000009 ), # miss, fill line0 way0
    req( 'rd', 0x01, 0x00001000, 0, 0          ), resp('rd', 0x01, 0, 0, 0x0000000a ), # miss, fill line0 way1
    req( 'rd', 0x02, 0x00000010, 0, 0          ), resp('rd', 0x02, 0, 0, 0x00000019 ), # miss, fill line1 way0
    req( 'rd', 0x03, 0x00001010, 0, 0          ), resp('rd', 0x03, 0, 0, 0x0000001a ), # miss, fill line1 way1
    req( 'rd', 0x04, 0x00000020, 0, 0          ), resp('rd', 0x04, 0, 0, 0x00000029 ), # miss, fill line2 way0
    req( 'rd', 0x05, 0x00001020, 0, 0          ), resp('rd', 0x05, 0, 0, 0x0000002a ), # miss, fill line2 way1
    req( 'rd', 0x06, 0x00000030, 0, 0          ), resp('rd', 0x06, 0, 0, 0x00000039 ), # miss, fill line3 way0
    req( 'rd', 0x07, 0x00001030, 0, 0          ), resp('rd', 0x07, 0, 0, 0x0000003a ), # miss, fill line3 way1
    req( 'rd', 0x08, 0x00000040, 0, 0          ), resp('rd', 0x08, 0, 0, 0x00000049 ), # miss, fill line4 way0
    req( 'rd', 0x09, 0x00001040, 0, 0          ), resp('rd', 0x09, 0, 0, 0x0000004a ), # miss, fill line4 way1
    req( 'rd', 0x0a, 0x00000050, 0, 0          ), resp('rd', 0x0a, 0, 0, 0x00000059 ), # miss, fill line5 way0
    req( 'rd', 0x0b, 0x00001050, 0, 0          ), resp('rd', 0x0b, 0, 0, 0x0000005a ), # miss, fill line5 way1
    req( 'rd', 0x0c, 0x00000060, 0, 0          ), resp('rd', 0x0c, 0, 0, 0x00000069 ), # miss, fill line6 way0
    req( 'rd', 0x0d, 0x00001060, 0, 0          ), resp('rd', 0x0d, 0, 0, 0x0000006a ), # miss, fill line6 way1
    req( 'rd', 0x0e, 0x00000070, 0, 0          ), resp('rd', 0x0e, 0, 0, 0x00000079 ), # miss, fill line7 way0
    req( 'rd', 0x0f, 0x00001070, 0, 0          ), resp('rd', 0x0f, 0, 0, 0x0000007a ), # miss, fill line7 way1
    req( 'rd', 0x10, 0x00010010, 0, 0          ), resp('rd', 0x10, 0, 0, 0x00000089 ), # capacity miss, refill line1 way0
    req( 'rd', 0x11, 0x00010014, 0, 0          ), resp('rd', 0x11, 1, 0, 0x0000008a ), # check refill
    req( 'rd', 0x12, 0x00010018, 0, 0          ), resp('rd', 0x12, 1, 0, 0x0000008b ),
    req( 'rd', 0x13, 0x0001001c, 0, 0          ), resp('rd', 0x13, 1, 0, 0x0000008c ),
    req( 'rd', 0x14, 0x00000010, 0, 0          ), resp('rd', 0x14, 0, 0, 0x00000019 ), # check if line1 way0 is missed
  ]

# Data to be loaded into memory before running the test

def capacity_miss_assoc_mem( base_addr ):
 return [
    # addr      data (in int)
    0x00000000, 0x00000009,
    0x00000010, 0x00000019,
    0x00000020, 0x00000029,
    0x00000030, 0x00000039,
    0x00000040, 0x00000049,
    0x00000050, 0x00000059,
    0x00000060, 0x00000069,
    0x00000070, 0x00000079,
    0x00001000, 0x0000000a,
    0x00001010, 0x0000001a,
    0x00001020, 0x0000002a,
    0x00001030, 0x0000003a,
    0x00001040, 0x0000004a,
    0x00001050, 0x0000005a,
    0x00001060, 0x0000006a,
    0x00001070, 0x0000007a,
    0x00010010, 0x00000089,
    0x00010014, 0x0000008a,
    0x00010018, 0x0000008b,
    0x0001001c, 0x0000008c,
  ]
  
def conflict_miss_dmap( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000030, 0, 0          ), resp('rd', 0x00, 0, 0, 0x00000001 ), 
    req( 'rd', 0x01, 0x00000034, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00000002 ),
    req( 'rd', 0x02, 0x00000038, 0, 0          ), resp('rd', 0x02, 1, 0, 0x00000003 ), 
    req( 'rd', 0x03, 0x0000003c, 0, 0          ), resp('rd', 0x03, 1, 0, 0x00000004 ),
    req( 'rd', 0x04, 0x00001030, 0, 0          ), resp('rd', 0x04, 0, 0, 0x00000011 ),  # read conflict 
    req( 'rd', 0x05, 0x00001034, 0, 0          ), resp('rd', 0x05, 1, 0, 0x00000012 ),
    req( 'rd', 0x06, 0x00001038, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000013 ), 
    req( 'rd', 0x07, 0x0000103c, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000014 ),
  ]

# Data to be loaded into memory before running the test

def conflict_miss_dmap_mem( base_addr ):
 return [
    # addr      data (in int)
    0x00000030, 0x00000001,
    0x00000034, 0x00000002,
    0x00000038, 0x00000003,
    0x0000003c, 0x00000004,
    0x00001030, 0x00000011,
    0x00001034, 0x00000012,
    0x00001038, 0x00000013,
    0x0000103c, 0x00000014,
  ]

def conflict_miss_assoc( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000030, 0, 0          ), resp('rd', 0x00, 0, 0, 0x00000001 ), # miss, fill line3 way0
    req( 'rd', 0x01, 0x00000034, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00000002 ),
    req( 'rd', 0x02, 0x00000038, 0, 0          ), resp('rd', 0x02, 1, 0, 0x00000003 ), 
    req( 'rd', 0x03, 0x0000003c, 0, 0          ), resp('rd', 0x03, 1, 0, 0x00000004 ),
    req( 'rd', 0x04, 0x00001030, 0, 0          ), resp('rd', 0x04, 0, 0, 0x00000011 ), # miss, fill line3 way1
    req( 'rd', 0x05, 0x00001034, 0, 0          ), resp('rd', 0x05, 1, 0, 0x00000012 ),
    req( 'rd', 0x06, 0x00001038, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000013 ), 
    req( 'rd', 0x07, 0x0000103c, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000014 ),
    req( 'rd', 0x08, 0x00002030, 0, 0          ), resp('rd', 0x08, 0, 0, 0x00000021 ), # miss, conflict, fill line3 way0
    req( 'rd', 0x09, 0x00002034, 0, 0          ), resp('rd', 0x09, 1, 0, 0x00000022 ),
    req( 'rd', 0x0a, 0x00002038, 0, 0          ), resp('rd', 0x0a, 1, 0, 0x00000023 ), 
    req( 'rd', 0x0b, 0x0000203c, 0, 0          ), resp('rd', 0x0b, 1, 0, 0x00000024 ),
  ]

# Data to be loaded into memory before running the test

def conflict_miss_assoc_mem( base_addr ):
 return [
    # addr      data (in int)
    0x00000030, 0x00000001,
    0x00000034, 0x00000002,
    0x00000038, 0x00000003,
    0x0000003c, 0x00000004,
    0x00001030, 0x00000011,
    0x00001034, 0x00000012,
    0x00001038, 0x00000013,
    0x0000103c, 0x00000014,
    0x00002030, 0x00000021,
    0x00002034, 0x00000022,
    0x00002038, 0x00000023,
    0x0000203c, 0x00000024,
  ]

def LRU_assoc( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000030, 0, 0          ), resp('rd', 0x00, 0, 0, 0x00000001 ), # miss, fill line3 way0
    req( 'rd', 0x01, 0x00000034, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00000002 ), # check
    req( 'rd', 0x02, 0x00000038, 0, 0          ), resp('rd', 0x02, 1, 0, 0x00000003 ), # check
    req( 'rd', 0x03, 0x0000003c, 0, 0          ), resp('rd', 0x03, 1, 0, 0x00000004 ), # check
    req( 'rd', 0x04, 0x00001030, 0, 0          ), resp('rd', 0x04, 0, 0, 0x00000011 ), # miss, fill line3 way1
    req( 'rd', 0x05, 0x00001034, 0, 0          ), resp('rd', 0x05, 1, 0, 0x00000012 ), # check
    req( 'rd', 0x06, 0x00001038, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000013 ), # check
    req( 'rd', 0x07, 0x0000103c, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000014 ), # check
    req( 'rd', 0x08, 0x00000030, 0, 0          ), resp('rd', 0x08, 1, 0, 0x00000001 ), # hit way0, U = 0
    req( 'rd', 0x09, 0x00003030, 0, 0          ), resp('rd', 0x09, 0, 0, 0x00000031 ), # miss, fill line3 way1, U = 1
    req( 'rd', 0x04, 0x00001030, 0, 0          ), resp('rd', 0x04, 0, 0, 0x00000011 ), # miss way0, fill way0
    req( 'rd', 0x04, 0x00001034, 0, 0          ), resp('rd', 0x04, 1, 0, 0x00000012 ), # check way0
    req( 'rd', 0x0a, 0x00003034, 0, 0          ), resp('rd', 0x0a, 1, 0, 0x00000032 ), # check way1
    req( 'rd', 0x0b, 0x00003038, 0, 0          ), resp('rd', 0x0b, 1, 0, 0x00000033 ), # check way1
    req( 'rd', 0x0c, 0x0000303c, 0, 0          ), resp('rd', 0x0c, 1, 0, 0x00000034 ), # check way1
  ]

# Data to be loaded into memory before running the test

def LRU_assoc_mem( base_addr ):
 return [
    # addr      data (in int)
    0x00000030, 0x00000001,
    0x00000034, 0x00000002,
    0x00000038, 0x00000003,
    0x0000003c, 0x00000004,
    0x00001030, 0x00000011,
    0x00001034, 0x00000012,
    0x00001038, 0x00000013,
    0x0000103c, 0x00000014,
    0x00002030, 0x00000021,
    0x00002034, 0x00000022,
    0x00002038, 0x00000023,
    0x0000203c, 0x00000024,
    0x00003030, 0x00000031,
    0x00003034, 0x00000032,
    0x00003038, 0x00000033,
    0x0000303c, 0x00000034,
  ]
  
def Entire_cache_dmap( base_addr ):
 return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0x000fffee ), resp('wr', 0x00, 0, 0, 0          ), # miss, line0
    req( 'rd', 0x01, 0x00000000, 0, 0          ), resp('rd', 0x01, 1, 0, 0x000fffee ),
    req( 'rd', 0x02, 0x00000004, 0, 0          ), resp('rd', 0x02, 1, 0, 0x000fffe1 ), # check line0 refill
    req( 'rd', 0x03, 0x00000008, 0, 0          ), resp('rd', 0x03, 1, 0, 0x000fffe2 ), # check line0 refill
    req( 'rd', 0x04, 0x0000000c, 0, 0          ), resp('rd', 0x04, 1, 0, 0x000fffe3 ), # check line0 refill
    req( 'wr', 0x05, 0x00000010, 0, 0x00ffffee ), resp('wr', 0x05, 0, 0, 0          ), # miss, line1
    req( 'rd', 0x06, 0x00000010, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00ffffee ),
    req( 'rd', 0x07, 0x00000014, 0, 0          ), resp('rd', 0x07, 1, 0, 0x000ffff1 ), # check line1 refill
    req( 'rd', 0x08, 0x00000018, 0, 0          ), resp('rd', 0x08, 1, 0, 0x000ffff2 ), # check line1 refill
    req( 'rd', 0x09, 0x0000001c, 0, 0          ), resp('rd', 0x09, 1, 0, 0x000ffff3 ), # check line1 refill
    req( 'rd', 0x0a, 0x00000020, 0, 0          ), resp('rd', 0x0a, 0, 0, 0x00ffffee ), # miss, line2
    req( 'rd', 0x0b, 0x00000024, 0, 0          ), resp('rd', 0x0b, 1, 0, 0x00fffff1 ), # check line1 refill
    req( 'rd', 0x0c, 0x00000028, 0, 0          ), resp('rd', 0x0c, 1, 0, 0x00fffff2 ), # check line1 refill
    req( 'rd', 0x0d, 0x0000002c, 0, 0          ), resp('rd', 0x0d, 1, 0, 0x00fffff3 ), # check line1 refill
    req( 'wr', 0x0e, 0x00000030, 0, 0xaaaaaaaa ), resp('wr', 0x0e, 0, 0, 0          ), # miss, write lin3
    req( 'rd', 0x0f, 0x00000030, 0, 0          ), resp('rd', 0x0f, 1, 0, 0xaaaaaaaa ), # hit , read lin3
    req( 'rd', 0x10, 0x00001030, 0, 0          ), resp('rd', 0x10, 0, 0, 0xaaaaa000 ), # miss, line3 refill
    req( 'rd', 0x11, 0x00001034, 0, 0          ), resp('rd', 0x11, 1, 0, 0xaaaaa001 ), # check line3 refill
    req( 'wr', 0x12, 0x00000040, 0, 0xbbbbbbbb ), resp('wr', 0x12, 0, 0, 0          ), # miss, write line4
    req( 'wr', 0x13, 0x00000040, 0, 0xcccccccc ), resp('wr', 0x13, 1, 0, 0          ), # hit,  write line4, dirty line
    req( 'rd', 0x14, 0x00001040, 0, 0          ), resp('rd', 0x14, 0, 0, 0xaaaaafff ), # miss, refill line4
    req( 'rd', 0x15, 0x00001044, 0, 0          ), resp('rd', 0x15, 1, 0, 0xaaaaffff ), # check line4 refill
    req( 'wr', 0x16, 0x00001050, 0, 0xaaaaaff1 ), resp('wr', 0x16, 0, 0, 0          ), # miss, refill line5
    req( 'rd', 0x17, 0x00001050, 0, 0          ), resp('rd', 0x17, 1, 0, 0xaaaaaff1 ), # hit, line5
    req( 'wr', 0x18, 0x00002060, 0, 0xaaaaaff2 ), resp('wr', 0x18, 0, 0, 0          ), # miss, refill line6
    req( 'rd', 0x19, 0x00002060, 0, 0          ), resp('rd', 0x19, 1, 0, 0xaaaaaff2 ), # hit, line6
    req( 'wr', 0x1a, 0x000020a0, 0, 0xaaaaaffd ), resp('wr', 0x1a, 0, 0, 0          ), # miss, refill line6
    req( 'rd', 0x1b, 0x000020a0, 0, 0          ), resp('rd', 0x1b, 1, 0, 0xaaaaaffd ), # hit, line6
  ]

# Data to be loaded into memory before running the test

def Entire_cache_dmap_mem( base_addr ):
 return [
    # addr      data (in int)
    0x00000004, 0x000fffe1,
    0x00000008, 0x000fffe2,
    0x0000000c, 0x000fffe3,
    0x00000014, 0x000ffff1,
    0x00000018, 0x000ffff2,
    0x0000001c, 0x000ffff3,
    0x00000020, 0x00ffffee,
    0x00000024, 0x00fffff1,
    0x00000028, 0x00fffff2,
    0x0000002c, 0x00fffff3,
    0x00001030, 0xaaaaa000,
    0x00001034, 0xaaaaa001,
    0x00001034, 0xaaaaa001,
    0x00001040, 0xaaaaafff,
    0x00001044, 0xaaaaffff,
  ]

#for test
def te_for_tem( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0x00000001 ), resp('rd', 0x00, 0, 0, 0          ), # miss, fill line3 way0
    req( 'rd', 0x01, 0x00000000, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00000001 ),
    req( 'rd', 0x02, 0x00000004, 0, 0          ), resp('rd', 0x02, 1, 0, 0x000fffe1 ), # check
    req( 'rd', 0x03, 0x00000008, 0, 0          ), resp('rd', 0x03, 1, 0, 0x000fffe2 ), # check
    req( 'rd', 0x04, 0x0000000c, 0, 0          ), resp('rd', 0x04, 1, 0, 0x000fffe3 ), # check
    req( 'wr', 0x05, 0x00000000, 0, 0x00000002 ), resp('rd', 0x05, 1, 0, 0          ), # miss, fill line3 way0
    req( 'rd', 0x06, 0x00000000, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000002 ),
    req( 'rd', 0x07, 0x00000004, 0, 0          ), resp('rd', 0x07, 1, 0, 0x000fffe1 ), # check
    req( 'rd', 0x08, 0x00000008, 0, 0          ), resp('rd', 0x08, 1, 0, 0x000fffe2 ), # check
    req( 'rd', 0x09, 0x0000000c, 0, 0          ), resp('rd', 0x09, 1, 0, 0x000fffe3 ), # check
    req( 'wr', 0x0a, 0x00000000, 0, 0x00000003 ), resp('rd', 0x0a, 1, 0, 0          ), # miss, fill line3 way0
    req( 'rd', 0x0b, 0x00000000, 0, 0          ), resp('rd', 0x0b, 1, 0, 0x00000003 ),
    req( 'rd', 0x0c, 0x00000004, 0, 0          ), resp('rd', 0x0c, 1, 0, 0x000fffe1 ), # check
    req( 'rd', 0x0d, 0x00000008, 0, 0          ), resp('rd', 0x0d, 1, 0, 0x000fffe2 ), # check
    req( 'rd', 0x0e, 0x0000000c, 0, 0          ), resp('rd', 0x0e, 1, 0, 0x000fffe3 ), # check
    req( 'wr', 0x0f, 0x00000000, 0, 0x00000004 ), resp('rd', 0x0f, 1, 0, 0          ), # miss, fill line3 way0
    req( 'rd', 0x10, 0x00000000, 0, 0          ), resp('rd', 0x10, 1, 0, 0x00000004 ),
    req( 'rd', 0x11, 0x00000004, 0, 0          ), resp('rd', 0x11, 1, 0, 0x000fffe1 ), # check
    req( 'rd', 0x12, 0x00000008, 0, 0          ), resp('rd', 0x12, 1, 0, 0x000fffe2 ), # check
    req( 'rd', 0x13, 0x0000000c, 0, 0          ), resp('rd', 0x13, 1, 0, 0x000fffe3 ), # check
  ]

def te_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0x00000044,
    0x00000004, 0x000fffe1,
    0x00000008, 0x000fffe2,
    0x0000000c, 0x000fffe3,
  ]
# above is test

# below are bank test for dmap
def read_hit_dmap_2bank( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0x00000001 ), resp('rd', 0x00, 0, 0, 0          ), #wr bank0 line6
    req( 'wr', 0x01, 0x00000100, 0, 0x00000002 ), resp('rd', 0x01, 0, 0, 0          ), #wr bank0 line8
    req( 'rd', 0x02, 0x00000004, 0, 0          ), resp('rd', 0x02, 1, 0, 0x000fffe1 ), # check
    req( 'rd', 0x03, 0x00000008, 0, 0          ), resp('rd', 0x03, 1, 0, 0x000fffe2 ), # check
    req( 'rd', 0x04, 0x0000000c, 0, 0          ), resp('rd', 0x04, 1, 0, 0x000fffe3 ), # check
    req( 'rd', 0x05, 0x00000104, 0, 0          ), resp('rd', 0x05, 1, 0, 0x000ffee1 ), # check
    req( 'rd', 0x06, 0x00000108, 0, 0          ), resp('rd', 0x06, 1, 0, 0x000ffee2 ), # check
    req( 'rd', 0x07, 0x0000010c, 0, 0          ), resp('rd', 0x07, 1, 0, 0x000ffee3 ), # check
    
  ]

def read_hit_dmap_2bank_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0x00000044,
    0x00000004, 0x000fffe1,
    0x00000008, 0x000fffe2,
    0x0000000c, 0x000fffe3,
    0x00000100, 0x00000044,
    0x00000104, 0x000ffee1,
    0x00000108, 0x000ffee2,
    0x0000010c, 0x000ffee3,
  ]
  
def read_hit_dmap_4bank( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0x00000001 ), resp('rd', 0x00, 0, 0, 0          ), #wr bank0 line6
    req( 'wr', 0x01, 0x00000200, 0, 0x00000002 ), resp('rd', 0x01, 0, 0, 0          ), #wr bank1 line6
    req( 'rd', 0x02, 0x00000004, 0, 0          ), resp('rd', 0x02, 1, 0, 0x000fffe1 ), # check
    req( 'rd', 0x03, 0x00000008, 0, 0          ), resp('rd', 0x03, 1, 0, 0x000fffe2 ), # check
    req( 'rd', 0x04, 0x0000000c, 0, 0          ), resp('rd', 0x04, 1, 0, 0x000fffe3 ), # check
    req( 'rd', 0x05, 0x00000204, 0, 0          ), resp('rd', 0x05, 1, 0, 0x000ffee1 ), # check
    req( 'rd', 0x06, 0x00000208, 0, 0          ), resp('rd', 0x06, 1, 0, 0x000ffee2 ), # check
    req( 'rd', 0x07, 0x0000020c, 0, 0          ), resp('rd', 0x07, 1, 0, 0x000ffee3 ), # check
    
  ]

def read_hit_dmap_4bank_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0x00000044,
    0x00000004, 0x000fffe1,
    0x00000008, 0x000fffe2,
    0x0000000c, 0x000fffe3,
    0x00000200, 0x00000044,
    0x00000204, 0x000ffee1,
    0x00000208, 0x000ffee2,
    0x0000020c, 0x000ffee3,
  ]

def read_miss_asso_2bank( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp( 'rd', 0x00, 0,   0,  0xdeadbeef ),
    req( 'rd', 0x01, 0x00000100, 0, 0          ), resp( 'rd', 0x01, 0,   0,  0x00c0ffee ),
    req( 'rd', 0x02, 0x00000080, 0, 0          ), resp( 'rd', 0x02, 0,   0,  0x00000011 ),
    req( 'rd', 0x03, 0x00000180, 0, 0          ), resp( 'rd', 0x03, 0,   0,  0x00000012 ),
    req( 'rd', 0x04, 0x00000004, 0, 0          ), resp( 'rd', 0x04, 1,   0,  0x00000014 ),
    req( 'rd', 0x05, 0x00000104, 0, 0          ), resp( 'rd', 0x05, 1,   0,  0x00000015 ),
    req( 'rd', 0x06, 0x00000084, 0, 0          ), resp( 'rd', 0x06, 1,   0,  0x00000016 ),
    req( 'rd', 0x07, 0x00000184, 0, 0          ), resp( 'rd', 0x07, 1,   0,  0x00000017 ),
    
  ]

def read_miss_asso_2bank_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00000014,
    0x00000080, 0x00000011,
    0x00000084, 0x00000016,
    0x00000100, 0x00c0ffee,
    0x00000104, 0x00000015,
    0x00000180, 0x00000012,
    0x00000184, 0x00000017,
  ]
  
def read_miss_asso_4bank( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp( 'rd', 0x00, 0,   0,  0xdeadbeef ),
    req( 'rd', 0x01, 0x00000200, 0, 0          ), resp( 'rd', 0x01, 0,   0,  0x00c0ffee ),
    req( 'rd', 0x02, 0x00000100, 0, 0          ), resp( 'rd', 0x02, 0,   0,  0x00000011 ),
    req( 'rd', 0x03, 0x00000300, 0, 0          ), resp( 'rd', 0x03, 0,   0,  0x00000012 ),
    req( 'rd', 0x04, 0x00000004, 0, 0          ), resp( 'rd', 0x04, 1,   0,  0x00000014 ),
    req( 'rd', 0x05, 0x00000204, 0, 0          ), resp( 'rd', 0x05, 1,   0,  0x00000015 ),
    req( 'rd', 0x06, 0x00000104, 0, 0          ), resp( 'rd', 0x06, 1,   0,  0x00000016 ),
    req( 'rd', 0x07, 0x00000304, 0, 0          ), resp( 'rd', 0x07, 1,   0,  0x00000017 ),
    
  ]

def read_miss_asso_4bank_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00000014,
    0x00000100, 0x00000011,
    0x00000104, 0x00000016,
    0x00000200, 0x00c0ffee,
    0x00000204, 0x00000015,
    0x00000300, 0x00000012,
    0x00000304, 0x00000017,
  ]

def random_dmap( base_addr ):
  #cache = []
  #for i in xrange (0,16):
  # cache.append({0})
  cache = [ {} for _ in xrange(0,16)]
  
  test = []

  mem = []
  for j in xrange (0,0x000fffee):
    mem.append(0)#random.randint(0,0xffffffff)

  for i in xrange(0, 16):
    data = random.randint(0, 0xffffffff)
    addr = random.randint(0, 0x000ffff)
    op_type = random.randint(0, 2)

    tag  = addr

    index = ((addr) & 0xf)

    if tag == cache[index]:
      hit = 1
    else:
      hit = 0
    
    if op_type == 1:
      op = 'wr'
      datareq = data
      dataresp = 0
    else:
      op = 'rd'
      datareq = 0
      dataresp = mem[addr]

    if hit == 0:
      if (len(cache[index]) >= 1):
        del cache[index][list(cache[index].keys())[0]]
        cache[index][tag] = tag
      else:
        cache[index][tag] = tag
    
    if op == 'wr':
      mem[addr] = data 

    test.append(req (op, i, addr*4,  0, datareq ))
    test.append(resp(op, i,    hit,  0, dataresp)) 

  return test
  
def random_assoc( base_addr ):
  #cache = []
  #for i in xrange (0,8):
  #  cache.append({})
  cache = [ {} for _ in xrange(0,8)]
  
  LRU = []
  for k in xrange (0,8):
    LRU.append(0)

  test = []

  mem = []
  for j in xrange (0,0x000fffee):
    mem.append(0)

  for i in xrange(0, 16):
    data = random.randint(0, 0xffffffff)
    addr = random.randint(0, 0x000ffff)
    op_type = random.randint(0, 2)

    tag  = addr

    index = ((addr) & 0x7)
    
    if tag in cache[index]:
      hit = 1
    else:
      hit = 0
    
    if op_type == 1:
      op = 'wr'
      datareq = data
      dataresp = 0
    else:
      op = 'rd'
      datareq = 0
      dataresp = mem[addr]
      
    
      
    if hit:
      if tag == cache[index].key()[0]:
        LRU[index] = 1
      else:
        LRU[index] = 0

    if hit == 0:
      if (len(cache[index]) >= 2):
        del cache[index][list(cache[index].keys())[LRU[index]]]
      #LRU[index] = not LRU[index]
        if LRU[index] == 0:
          LRU[index] = LRU[index]
        else:
          LRU[index] = not LRU[index]
        cache[index][tag] = tag
      else:
        cache[index][tag] = tag

    if op == 'wr':
      mem[addr] = data 

    test.append(req (op, i, addr*4,  0, datareq ))
    test.append(resp(op, i,    hit,  0, dataresp)) 

  return test

  
def read_miss_1word_msg( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ),
  ]
# Data to be loaded into memory before running the test

def read_miss_1word_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
    0x00000008, 0x00000011,
    0x0000000c, 0x00000012,
    0x00000010, 0x00000013,
  ]
  
def eva_test_write_1( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0x00000001 ), resp('wr', 0x00, 0, 0, 0 ), # read word  0x00000000
    req( 'wr', 0x01, 0x00000010, 0, 0x00000002 ), resp('wr', 0x01, 0, 0, 0 ),
    req( 'wr', 0x02, 0x00000020, 0, 0x00000003 ), resp('wr', 0x02, 0, 0, 0 ),
    req( 'wr', 0x03, 0x00000030, 0, 0x00000004 ), resp('wr', 0x03, 0, 0, 0 ),
    req( 'wr', 0x04, 0x00000040, 0, 0x00000005 ), resp('wr', 0x04, 0, 0, 0 ), # read word  0x00000000
    req( 'wr', 0x05, 0x00000050, 0, 0x00000006 ), resp('wr', 0x05, 0, 0, 0 ),
    req( 'wr', 0x06, 0x00000060, 0, 0x00000007 ), resp('wr', 0x06, 0, 0, 0 ),
    req( 'wr', 0x07, 0x00000070, 0, 0x00000008 ), resp('wr', 0x07, 0, 0, 0 ),
    req( 'wr', 0x08, 0x00000100, 0, 0x00000009 ), resp('wr', 0x08, 0, 0, 0 ), # read word  0x00000000
    req( 'wr', 0x09, 0x00000110, 0, 0x0000000a ), resp('wr', 0x09, 0, 0, 0 ),
    req( 'wr', 0x0a, 0x00000120, 0, 0x0000000b ), resp('wr', 0x0a, 0, 0, 0 ),
    req( 'wr', 0x0b, 0x00000130, 0, 0x0000000c ), resp('wr', 0x0b, 0, 0, 0 ),
    req( 'wr', 0x0c, 0x00000140, 0, 0x0000000d ), resp('wr', 0x0c, 0, 0, 0 ), # read word  0x00000000
    req( 'wr', 0x0d, 0x00000150, 0, 0x0000000e ), resp('wr', 0x0d, 0, 0, 0 ),
    req( 'wr', 0x0e, 0x00000160, 0, 0x0000000f ), resp('wr', 0x0e, 0, 0, 0 ),
    req( 'wr', 0x0f, 0x00000170, 0, 0x000000010), resp('wr', 0x0f, 0, 0, 0 ),
    
    req( 'wr', 0x10, 0x00000000, 0, 0x00000001 ), resp('wr', 0x10, 1, 0, 0 ), # read word  0x00000000
    req( 'wr', 0x11, 0x00000010, 0, 0x00000002 ), resp('wr', 0x11, 1, 0, 0 ),
    req( 'wr', 0x12, 0x00000020, 0, 0x00000003 ), resp('wr', 0x12, 1, 0, 0 ),
    req( 'wr', 0x13, 0x00000030, 0, 0x00000004 ), resp('wr', 0x13, 1, 0, 0 ),
    req( 'wr', 0x14, 0x00000040, 0, 0x00000005 ), resp('wr', 0x14, 1, 0, 0 ), # read word  0x00000000
    req( 'wr', 0x15, 0x00000050, 0, 0x00000006 ), resp('wr', 0x15, 1, 0, 0 ),
    req( 'wr', 0x16, 0x00000060, 0, 0x00000007 ), resp('wr', 0x16, 1, 0, 0 ),
    req( 'wr', 0x17, 0x00000070, 0, 0x00000008 ), resp('wr', 0x17, 1, 0, 0 ),
    req( 'wr', 0x18, 0x00000100, 0, 0x00000009 ), resp('wr', 0x18, 1, 0, 0 ), # read word  0x00000000
    req( 'wr', 0x19, 0x00000110, 0, 0x0000000a ), resp('wr', 0x19, 1, 0, 0 ),
    req( 'wr', 0x1a, 0x00000120, 0, 0x0000000b ), resp('wr', 0x1a, 1, 0, 0 ),
    req( 'wr', 0x1b, 0x00000130, 0, 0x0000000c ), resp('wr', 0x1b, 1, 0, 0 ),
    req( 'wr', 0x1c, 0x00000140, 0, 0x0000000d ), resp('wr', 0x1c, 1, 0, 0 ), # read word  0x00000000
    req( 'wr', 0x1d, 0x00000150, 0, 0x0000000e ), resp('wr', 0x1d, 1, 0, 0 ),
    req( 'wr', 0x1e, 0x00000160, 0, 0x0000000f ), resp('wr', 0x1e, 1, 0, 0 ),
    req( 'wr', 0x1f, 0x00000170, 0, 0x000000010), resp('wr', 0x1f, 1, 0, 0 ),
  ]
# Data to be loaded into memory before running the test

def eva_test_write_1_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0x00000001,
    0x00000010, 0x00000002,
    0x00000020, 0x00000003,
    0x00000030, 0x00000004,
    0x00000040, 0x00000005,
    0x00000050, 0x00000006,
    0x00000060, 0x00000007,
    0x00000070, 0x00000008,
    0x00000100, 0x00000009,
    0x00000110, 0x0000000a,
    0x00000120, 0x0000000b,
    0x00000130, 0x0000000c,
    0x00000140, 0x0000000d,
    0x00000150, 0x0000000e,
    0x00000160, 0x0000000f,
    0x00000170, 0x00000010,
  ]

def eva_test_write_confe( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0x00000001 ), resp('wr', 0x00, 0, 0, 0 ), # read word  0x00000000
    req( 'rd', 0x01, 0x00000080, 0, 0          ), resp('rd', 0x01, 0, 0, 0x00000002 ),
    req( 'wr', 0x02, 0x00000100, 0, 0x00000003 ), resp('wr', 0x02, 0, 0, 0 ),
    
    req( 'rd', 0x03, 0x00000000, 0, 0          ), resp('rd', 0x03, 0, 0, 0x00000001 ),
    req( 'wr', 0x04, 0x00000080, 0, 0x00000002 ), resp('wr', 0x04, 0, 0, 0 ), # read word  0x00000000
    req( 'rd', 0x05, 0x00000100, 0, 0          ), resp('rd', 0x05, 0, 0, 0x00000003 ),
    
    req( 'rd', 0x06, 0x00000000, 0, 0          ), resp('rd', 0x06, 0, 0, 0x00000001 ),
    req( 'wr', 0x07, 0x00000080, 0, 0x00000002 ), resp('wr', 0x07, 0, 0, 0 ),
    req( 'wr', 0x08, 0x00000100, 0, 0x00000003 ), resp('wr', 0x08, 0, 0, 0 ), # read word  0x00000000
    
    req( 'wr', 0x09, 0x00000000, 0, 0x00000001 ), resp('wr', 0x09, 0, 0, 0 ),
    req( 'wr', 0x0a, 0x00000080, 0, 0x00000002 ), resp('wr', 0x0a, 0, 0, 0 ),
    req( 'wr', 0x0b, 0x00000100, 0, 0x00000003 ), resp('wr', 0x0b, 0, 0, 0 ),
    
    req( 'wr', 0x0c, 0x00000000, 0, 0x00000001 ), resp('wr', 0x0c, 0, 0, 0 ), # read word  0x00000000
    req( 'rd', 0x0d, 0x00000080, 0, 0          ), resp('rd', 0x0d, 0, 0, 0x00000002 ),
    req( 'wr', 0x0e, 0x00000100, 0, 0x00000003 ), resp('wr', 0x0e, 0, 0, 0 ),
    
    req( 'wr', 0x0f, 0x00000000, 0, 0x00000001 ), resp('wr', 0x0f, 0, 0, 0 ), # read word  0x00000000
    req( 'wr', 0x10, 0x00000080, 0, 0x00000002 ), resp('wr', 0x10, 0, 0, 0 ),
    req( 'rd', 0x11, 0x00000100, 0, 0          ), resp('rd', 0x11, 0, 0, 0x00000003 ),
  ]
# Data to be loaded into memory before running the test

def eva_test_write_confe_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0x00000001,
    0x00000080, 0x00000002,
    0x00000100, 0x00000003,

  ]

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK: Add more test cases
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#----------------------------------------------------------------------
# Banked cache test
#----------------------------------------------------------------------
# The test field in the response message: 0 == MISS, 1 == HIT

# This test case is to test if the bank offset is implemented correctly.
#f (tag_match1 && valid_bits1[idx])

# The idea behind this test case is to differentiate between a cache
# with no bank bits and a design has one/two bank bits by looking at cache
# request hit/miss status.

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK:
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# Test table for generic test
#-------------------------------------------------------------------------

test_case_table_generic = mk_test_case_table([
  (                                   "msg_func                          mem_data_func                     nbank stall lat src sink"),
  [ "read_hit_1word_clean",           read_hit_1word_clean,              None,                             0,    0.0,  0,  0,  0    ],
  [ "read_hit_1word_dirty",           read_hit_1word_dirty,              None,                             0,    0.0,  0,  0,  0    ],
  [ "write_hit_1word_clean",          write_hit_1word_clean,             None,                             0,    0.0,  0,  0,  0    ],
  [ "write_hit_1word_dirty",          write_hit_1word_dirty,             None,                             0,    0.0,  0,  0,  0    ],
  [ "read_miss_1word",                read_miss_1word_msg,               read_miss_1word_mem,              0,    0.0,  0,  0,  0    ],
  [ "read_miss_refill_no_eviction",   read_miss_refill_no_eviction,      read_miss_refill_no_eviction_mem, 0,    0.0,  0,  0,  0    ], #
  [ "write_miss_refill_no_eviction",  write_miss_refill_no_eviction,     write_miss_refill_no_eviction_mem,0,    0.0,  0,  0,  0    ], #
  [ "read_hit_1word_4bank",           read_hit_1word_clean,              None,                             4,    0.0,  0,  0,  0    ],
  [ "read_hit_1word_4bank",           read_hit_1word_dirty,              None,                             4,    0.0,  0,  0,  0    ],
  [ "read_hit_1word_clean",           read_hit_1word_clean,              None,                             0,    0.0,  1,  2,  3    ], # below are add delays
  [ "read_hit_1word_dirty",           read_hit_1word_dirty,              None,                             0,    0.0,  2,  3,  3    ],
  [ "write_hit_1word_clean",          write_hit_1word_clean,             None,                             0,    0.0,  1,  4,  5    ],
  [ "write_hit_1word_dirty",          write_hit_1word_dirty,             None,                             0,    0.0,  6,  6,  0    ],
  [ "read_miss_1word",                read_miss_1word_msg,               read_miss_1word_mem,              0,    0.0,  7,  0,  0    ],
  [ "read_miss_refill_no_eviction",   read_miss_refill_no_eviction,      read_miss_refill_no_eviction_mem, 0,    0.0,  0,  4,  0    ], 
  [ "write_miss_refill_no_eviction",  write_miss_refill_no_eviction,     write_miss_refill_no_eviction_mem,0,    0.0,  1,  9,  8    ],
  [ "read_hit_1word_4bank",           read_hit_1word_clean,              None,                             4,    0.0,  2,  2,  2    ],
  [ "read_hit_1word_4bank",           read_hit_1word_dirty,              None,                             4,    0.0,  3,  3,  3    ],
  [ "read_hit_1word_clean",           read_hit_1word_clean,              None,                             0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ], # below are random delays
  [ "read_hit_1word_dirty",           read_hit_1word_dirty,              None,                             0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "write_hit_1word_clean",          write_hit_1word_clean,             None,                             0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "write_hit_1word_dirty",          write_hit_1word_dirty,             None,                             0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "read_miss_1word",                read_miss_1word_msg,               read_miss_1word_mem,              0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "read_miss_refill_no_eviction",   read_miss_refill_no_eviction,      read_miss_refill_no_eviction_mem, 0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "write_miss_refill_no_eviction",  write_miss_refill_no_eviction,     write_miss_refill_no_eviction_mem,0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "read_hit_1word_4bank",           read_hit_1word_clean,              None,                             4,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "read_hit_1word_4bank",           read_hit_1word_dirty,              None,                             4,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],


  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add test cases to this table
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

@pytest.mark.parametrize( **test_case_table_generic )
def test_generic( test_params, dump_vcd ):
  msgs = test_params.msg_func( 0 )
  if test_params.mem_data_func != None:
    mem = test_params.mem_data_func( 0 )
  # Instantiate testharness
  harness = TestHarness( msgs[::2], msgs[1::2],
                         test_params.stall, test_params.lat,
                         test_params.src, test_params.sink,
                         BlockingCacheFL, test_params.nbank,
                         False, dump_vcd )
  # Load memory before the test
  if test_params.mem_data_func != None:
    harness.load( mem[::2], mem[1::2] )
  # Run the test
  run_sim( harness, dump_vcd )

#-------------------------------------------------------------------------
# Test table for set-associative cache (alternative design)
#-------------------------------------------------------------------------

test_case_table_set_assoc = mk_test_case_table([
  (                                     "msg_func                             mem_data_func                          nbank stall lat src sink"),
  [ "read_hit_asso",                    read_hit_asso,                        None,                                  0,    0.0,  0,  0,  0    ],
  [ "read_miss_asso",                   read_miss_asso,                       read_miss_1word_mem,                   0,    0.0,  0,  0,  0    ],
  [ "read_miss_refill_eviction_assoc",  read_miss_refill_eviction_assoc,      read_miss_refill_eviction_assoc_mem,   0,    0.0,  0,  0,  0    ],
  [ "write_miss_refill_eviction_assoc", write_miss_refill_eviction_assoc,     write_miss_refill_eviction_assoc_mem,  0,    0.0,  0,  0,  0    ],
  [ "capacity_miss_assoc",              capacity_miss_assoc,                  capacity_miss_assoc_mem,               0,    0.0,  0,  0,  0    ],
  [ "conflict_miss_assoc",              conflict_miss_assoc,                  conflict_miss_assoc_mem,               0,    0.0,  0,  0,  0    ],
  [ "LRU_assoc",                        LRU_assoc,                            LRU_assoc_mem,                         0,    0.0,  0,  0,  0    ],
  [ "random_assoc",                     random_assoc,                         None,                                  0,    0.0,  0,  0,  0    ],
  [ "read_miss_asso_2bank",             read_miss_asso_2bank,                 read_miss_asso_2bank_mem,              2,    0.0,  0,  0,  0    ],
  [ "read_miss_asso_4bank",             read_miss_asso_4bank,                 read_miss_asso_4bank_mem,              4,    0.0,  0,  0,  0    ],
  [ "read_hit_asso",                    read_hit_asso,                        None,                                  0,    0.0,  1,  1,  1    ], # below are add delays
  [ "read_miss_asso",                   read_miss_asso,                       read_miss_1word_mem,                   0,    0.0,  3,  3,  3    ],
  [ "read_miss_refill_eviction_assoc",  read_miss_refill_eviction_assoc,      read_miss_refill_eviction_assoc_mem,   0,    0.0,  2,  7,  9    ],
  [ "write_miss_refill_eviction_assoc", write_miss_refill_eviction_assoc,     write_miss_refill_eviction_assoc_mem,  0,    0.0,  1,  5,  0    ],
  [ "capacity_miss_assoc",              capacity_miss_assoc,                  capacity_miss_assoc_mem,               0,    0.0,  0,  2,  7    ],
  [ "conflict_miss_assoc",              conflict_miss_assoc,                  conflict_miss_assoc_mem,               0,    0.0,  0,  0,  1    ],
  [ "LRU_assoc",                        LRU_assoc,                            LRU_assoc_mem,                         0,    0.0,  0,  0,  90   ],
  [ "read_hit_asso",                    read_hit_asso,                        None,                                  0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ], # below are random delays
  [ "read_miss_asso",                   read_miss_asso,                       read_miss_1word_mem,                   0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "read_miss_refill_eviction_assoc",  read_miss_refill_eviction_assoc,      read_miss_refill_eviction_assoc_mem,   0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "write_miss_refill_eviction_assoc", write_miss_refill_eviction_assoc,     write_miss_refill_eviction_assoc_mem,  0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "capacity_miss_assoc",              capacity_miss_assoc,                  capacity_miss_assoc_mem,               0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "conflict_miss_assoc",              conflict_miss_assoc,                  conflict_miss_assoc_mem,               0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "LRU_assoc",                        LRU_assoc,                            LRU_assoc_mem,                         0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "te_for_temp",                      te_for_tem,                           te_mem,                                0,    0.0,  0,  0,  0    ],
  [ "eva_test_write_1",                 eva_test_write_1,                     eva_test_write_1_mem,                  0,    0.0,  0,  0,  0    ],
  [ "eva_test_write_confe",             eva_test_write_confe,                 eva_test_write_confe_mem,              0,    0.0,  0,  0,  0    ],
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add test cases to this table
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

@pytest.mark.parametrize( **test_case_table_set_assoc )
def test_set_assoc( test_params, dump_vcd ):
  msgs = test_params.msg_func( 0 )
  if test_params.mem_data_func != None:
    mem  = test_params.mem_data_func( 0 )
  # Instantiate testharness
  harness = TestHarness( msgs[::2], msgs[1::2],
                         test_params.stall, test_params.lat,
                         test_params.src, test_params.sink,
                         BlockingCacheFL, test_params.nbank,
                         False, dump_vcd )
  # Load memory before the test
  if test_params.mem_data_func != None:
    harness.load( mem[::2], mem[1::2] )
  # Run the test
  run_sim( harness, dump_vcd )


#-------------------------------------------------------------------------
# Test table for direct-mapped cache (baseline design)
#-------------------------------------------------------------------------

test_case_table_dir_mapped = mk_test_case_table([
  (                                   "msg_func                              mem_data_func                             nbank stall lat src sink"),
  [ "read_hit_dmap",                   read_hit_dmap,                        None,                                     0,    0.0,  0,  0,  0    ],
  [ "read_miss_refill_eviction_dmap",  read_miss_refill_eviction_dmap,       read_miss_refill_eviction_dmap_mem,       0,    0.0,  0,  0,  0    ],
  [ "write_miss_refill_eviction_dmap", write_miss_refill_eviction_dmap,      write_miss_refill_eviction_dmap_mem,      0,    0.0,  0,  0,  0    ],
  [ "capacity_miss_dmap",              capacity_miss_dmap,                   capacity_miss_dmap_mem,                   0,    0.0,  0,  0,  0    ],
  [ "conflict_miss_dmap",              conflict_miss_dmap,                   conflict_miss_dmap_mem,                   0,    0.0,  0,  0,  0    ],
  [ "Entire_cache_dmap",               Entire_cache_dmap,                    Entire_cache_dmap_mem,                    0,    0.0,  0,  0,  0    ],
  [ "random_dmap",                     random_dmap,                          None,                                     0,    0.0,  0,  0,  0    ],
  [ "read_hit_dmap_2bank",             read_hit_dmap_2bank,                  read_hit_dmap_2bank_mem,                  2,    0.0,  0,  0,  0    ],
  [ "read_hit_dmap_4bank",             read_hit_dmap_4bank,                  read_hit_dmap_4bank_mem,                  4,    0.0,  0,  0,  0    ],
  [ "read_hit_dmap",                   read_hit_dmap,                        None,                                     0,    0.0,  5,  5,  5    ], # below are add delays
  [ "read_miss_refill_eviction_dmap",  read_miss_refill_eviction_dmap,       read_miss_refill_eviction_dmap_mem,       0,    0.0,  3,  2,  3    ],
  [ "write_miss_refill_eviction_dmap", write_miss_refill_eviction_dmap,      write_miss_refill_eviction_dmap_mem,      0,    0.0,  1,  9,  9    ],
  [ "capacity_miss_dmap",              capacity_miss_dmap,                   capacity_miss_dmap_mem,                   0,    0.0,  2,  6,  6    ],
  [ "conflict_miss_dmap",              conflict_miss_dmap,                   conflict_miss_dmap_mem,                   0,    0.0,  4,  0,  0    ],
  [ "Entire_cache_dmap",               Entire_cache_dmap,                    Entire_cache_dmap_mem,                    0,    0.0,  0,  3,  0    ],
  [ "read_hit_dmap",                   read_hit_dmap,                        None,                                     0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ], # below are random delays
  [ "read_miss_refill_eviction_dmap",  read_miss_refill_eviction_dmap,       read_miss_refill_eviction_dmap_mem,       0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "write_miss_refill_eviction_dmap", write_miss_refill_eviction_dmap,      write_miss_refill_eviction_dmap_mem,      0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "capacity_miss_dmap",              capacity_miss_dmap,                   capacity_miss_dmap_mem,                   0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "conflict_miss_dmap",              conflict_miss_dmap,                   conflict_miss_dmap_mem,                   0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],
  [ "Entire_cache_dmap",               Entire_cache_dmap,                    Entire_cache_dmap_mem,                    0,    0.0,  random.randint(0,100),  random.randint(0,100),  random.randint(0,100)    ],

     
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add test cases to this table
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

@pytest.mark.parametrize( **test_case_table_dir_mapped )
def test_dir_mapped( test_params, dump_vcd ):
  msgs = test_params.msg_func( 0 )
  if test_params.mem_data_func != None:
    mem  = test_params.mem_data_func( 0 )
  # Instantiate testharness
  harness = TestHarness( msgs[::2], msgs[1::2],
                         test_params.stall, test_params.lat,
                         test_params.src, test_params.sink,
                         BlockingCacheFL, test_params.nbank,
                         False, dump_vcd )
  # Load memory before the test
  if test_params.mem_data_func != None:
    harness.load( mem[::2], mem[1::2] )
  # Run the test
  run_sim( harness, dump_vcd )
