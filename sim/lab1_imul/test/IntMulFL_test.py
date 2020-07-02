#=========================================================================
# IntMulFL_test
#=========================================================================

import pytest
import random

random.seed(0xdeadbeea)

from pymtl      import *
from pclib.test import mk_test_case_table, run_sim
from pclib.test import TestSource, TestSink

from lab1_imul.IntMulFL   import IntMulFL

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness (Model):

  def __init__( s, imul, src_msgs, sink_msgs,
                src_delay, sink_delay,
                dump_vcd=False, test_verilog=False ):

    # Instantiate models

    s.src  = TestSource ( Bits(64), src_msgs,  src_delay  )
    s.imul = imul
    s.sink = TestSink   ( Bits(32), sink_msgs, sink_delay )

    # Dump VCD

    if dump_vcd:
      s.imul.vcd_file = dump_vcd

    # Translation

    if test_verilog:
      s.imul = TranslationTool( s.imul )

    # Connect

    s.connect( s.src.out,  s.imul.req  )
    s.connect( s.imul.resp, s.sink.in_ )

  def done( s ):
    return s.src.done and s.sink.done

  def line_trace( s ):
    return s.src.line_trace()  + " > " + \
           s.imul.line_trace()  + " > " + \
           s.sink.line_trace()

#-------------------------------------------------------------------------
# mk_req_msg
#-------------------------------------------------------------------------

def req( a, b ):
  msg = Bits( 64 )
  msg[32:64] = Bits( 32, a, trunc=True )
  msg[ 0:32] = Bits( 32, b, trunc=True )
  return msg

def resp( a ):
  return Bits( 32, a, trunc=True )

#----------------------------------------------------------------------
# Test Case: small positive * positive
#----------------------------------------------------------------------

small_pos_pos_msgs = [
  req(  2,  3 ), resp(   6 ),
  req(  4,  5 ), resp(  20 ),
  req(  3,  4 ), resp(  12 ),
  req( 10, 13 ), resp( 130 ),
  req(  8,  7 ), resp(  56 ),
  #req( -1, 268435455       ), resp( -268435455    ),
  req(-1,-1),resp(1),
  
]



# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional lists of request/response messages to create
# additional directed and random test cases.
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#some useful varibles
random_num=10                                             #the amount of random number generated 
intmax= 2147483647;                                       #since python do not have a maximum number in int, we define this!


array=[]                                                  #initilize an array of random numbers
for i in range(0,random_num):
  a=random.randint(0,100)                                 #generate small numbers
  array.append(a)
  
ran_small_pos_pos_msgs = [                                 #verification
  req(  array[0], array[1] ), resp( array[0] * array[1] ),
  req(  array[2], array[3] ), resp( array[2] * array[3] ),
  req(  array[4], array[5] ), resp( array[4] * array[5] ),
  req(  array[6], array[7] ), resp( array[6] * array[7] ),
  req(  array[8], array[9] ), resp( array[8] * array[9] ),
]



zeros_one_negativeone=[
  req( 0, 0 ),  resp(  0 ),
  req( 0, -1),  resp(  0 ),
  req( 1, 0 ),  resp(  0 ),
  req( 1, -1 ),  resp( -1 ),
  req( -1, 1 ),  resp(  -1 ),
  req( -1, -1 ),  resp(  1 ),
]
array2=[]
for i in range(0,random_num):
  b=random.randint(0,2) -1                                     #shift the index so that b is in range(-1,1)
  array2.append(b)
  
ran_zeros_one_negativeone = [
  req(  array2[0], array2[1] ), resp( array2[0] * array2[1] ),
  req(  array2[2], array2[3] ), resp( array2[2] * array2[3] ),
  req(  array2[4], array2[5] ), resp( array2[4] * array2[5] ),
  req(  array2[6], array2[7] ), resp( array2[6] * array2[7] ),
  req(  array2[8], array2[9] ), resp( array2[8] * array2[9] ),
]

smallneg_smallpos=[
  req( -2, 1 ),  resp( -2 ),
  req( -5, 2),  resp(  -10 ),
  req( -9, 9 ),  resp(  -81 ),
  req( -12, 12 ),  resp( -144 ),
  req( -20, 12 ),  resp(  -240 ),
]

array3=[]
for i in range(0,random_num):
  c=random.randint(0,300)          
  if i%2==0:
     c=c*(-1)                                                  #take the negative of c
  array3.append(c)
  
ran_smallneg_smallpos = [
  req(  array3[0], array3[1] ), resp( array3[0] * array3[1] ),
  req(  array3[2], array3[3] ), resp( array3[2] * array3[3] ),
  req(  array3[4], array3[5] ), resp( array3[4] * array3[5] ),
  req(  array3[6], array3[7] ), resp( array3[6] * array3[7] ),
  req(  array3[8], array3[9] ), resp( array3[8] * array3[9] ),
]

smallpos_smallneg=[
  req( 2, -1 ),  resp( -2 ),
  req( 5, -2),  resp(  -10 ),
  req( 9, -9 ),  resp(  -81 ),
  req( 12, -12 ),  resp( -144 ),
  req( 20, -12 ),  resp(  -240 ),
]

array4=[]
for i in range(0,random_num):
  d=random.randint(0,300)          
  if i%2!=0:                                                   #if the array index is even take negative
     d=d*(-1)
  array4.append(d)
  
ran_smallpos_smallneg = [
  req(  array4[0], array4[1] ), resp( array4[0] * array4[1] ),
  req(  array4[2], array4[3] ), resp( array4[2] * array4[3] ),
  req(  array4[4], array4[5] ), resp( array4[4] * array4[5] ),
  req(  array4[6], array4[7] ), resp( array4[6] * array4[7] ),
  req(  array4[8], array4[9] ), resp( array4[8] * array4[9] ),
]


smallneg_smallneg=[
  req( -2, -1 ),  resp( 2 ),
  req( -5, -2),  resp(  10 ),
  req( -9, -9 ),  resp(  81 ),
  req( -12, -12 ),  resp( 144 ),
  req( -20, -12 ),  resp(  240 ),
]

array5=[]
for i in range(0,random_num):
  e=random.randint(0,300)*(-1)
  array5.append(e)
  
ran_smallneg_smallneg = [
  req(  array5[0], array5[1] ), resp( array5[0] * array5[1] ),
  req(  array5[2], array5[3] ), resp( array5[2] * array5[3] ),
  req(  array5[4], array5[5] ), resp( array5[4] * array5[5] ),
  req(  array5[6], array5[7] ), resp( array5[6] * array5[7] ),
  req(  array5[8], array5[9] ), resp( array5[8] * array5[9] ),
]

largepos_largepos=[
  req( 500, 200 ),  resp( 500*200 ),
  req( 1234, 4321),  resp(  1234*4321 ),
  req( 4321, 5432 ),  resp(  4321*5432 ),
  req( 12345, 173900 ),  resp(  12345*173900 ),                        #almost overflow
  req( 12345, 174000 ),  resp(  12345*174000 ),                        #just   overflow
  req( 2147483647, 20000 ),  resp(2147483647*20000 ),
  req( 2147483647, 2147483647 ),  resp(  2147483647*2147483647 ),
  req(2147483447,2147483472),     resp(2147483447*2147483472)
]


array6=[]
for i in range(0,random_num):
  #random.seed(0xdeadbeef)
  f=random.randint(0,300)
  f=intmax-f
  array6.append(f)
  
ran_largepos_largepos = [
  req(  array6[0], array6[1] ), resp( array6[0] * array6[1] ),
  req(  array6[2], array6[3] ), resp( array6[2] * array6[3] ),
  req(  array6[4], array6[5] ), resp( array6[4] * array6[5] ),
  req(  array6[6], array6[7] ), resp( array6[6] * array6[7] ),
  req(  array6[8], array6[9] ), resp( array6[8] * array6[9] ),
]

largepos_largeneg=[
  req( 500, -200 ),  resp( 500*(-200)),
  req( 1234, -4321),  resp(  1234*(-4321) ),
  req( 4321, -5432 ),  resp(  4321*(-5432) ),
  req( 12345, -173900 ),  resp(  12345*(-173900) ),                #almost overflow
  req( 12345, -174000 ),  resp(  12345*(-174000) ),                #just   overflow
  req( 2147483647, -20000 ),  resp(2147483647*(-20000) ),
  req( 2147483647, -2147483647 ),  resp(  2147483647*(-2147483647) ),
]

array7=[]
for i in range(0,random_num):
  g=random.randint(0,300)
  if i%2==0:
    g=intmax-g                                                  #generate a "big" number
  else:
    g=g-intmax
  array7.append(g)
  
ran_largepos_largeneg = [
  req(  array7[0], array7[1] ), resp( array7[0] * array7[1] ),
  req(  array7[2], array7[3] ), resp( array7[2] * array7[3] ),
  req(  array7[4], array7[5] ), resp( array7[4] * array7[5] ),
  req(  array7[6], array7[7] ), resp( array7[6] * array7[7] ),
  req(  array7[8], array7[9] ), resp( array7[8] * array7[9] ),
]

largeneg_largepos=[
  req( -500, 200 ),  resp( (-500)*200),
  req( -1234, 4321),  resp(  (-1234)*4321 ),
  req( -4321, 5432 ),  resp(  (-4321)*5432 ),
  req( -12345, 173900 ),  resp(  (-12345)*173900 ),                #almost overflow
  req( -12345, 174000 ),  resp(  (-12345)*174000 ),                #just   overflow
  req( -2147483647, 20000 ),  resp((-2147483647)*20000 ),
  req( -2147483647, 2147483647 ),  resp(  (-2147483647)*2147483647 ),
]

array8=[]
for i in range(0,random_num):
  h=random.randint(0,300)
  if i%2!=0:
    h=intmax-h
  else:
    h=h-intmax
  array8.append(h)
  
ran_largeneg_largepos = [
  req(  array8[0], array8[1] ), resp( array8[0] * array8[1] ),
  req(  array8[2], array8[3] ), resp( array8[2] * array8[3] ),
  req(  array8[4], array8[5] ), resp( array8[4] * array8[5] ),
  req(  array8[6], array8[7] ), resp( array8[6] * array8[7] ),
  req(  array8[8], array8[9] ), resp( array8[8] * array8[9] ),
]

largeneg_largeneg=[
  req( -500, -200 ),  resp( (500)*200),
  req( -1234, -4321),  resp(  (1234)*4321 ),
  req( -4321, -5432 ),  resp(  (4321)*5432 ),
  req( -12345,-173900 ),  resp(  (12345)*173900 ),                #almost overflow
  req( -12345, -174000 ),  resp(  (12345)*174000 ),                #just   overflow
  req( -2147483647, -20000 ),  resp((2147483647)*20000 ),
  req( -2147483647, -2147483647 ),  resp(  (2147483647)*2147483647 ),
]

array9=[]
for i in range(0,random_num):
  j=random.randint(0,300)
  j=j-intmax
  array9.append(j)
  
ran_largeneg_largeneg = [
  req(  array9[0], array9[1] ), resp( array9[0] * array9[1] ),
  req(  array9[2], array9[3] ), resp( array9[2] * array9[3] ),
  req(  array9[4], array9[5] ), resp( array9[4] * array9[5] ),
  req(  array9[6], array9[7] ), resp( array9[6] * array9[7] ),
  req(  array9[8], array9[9] ), resp( array9[8] * array9[9] ),
]

lower_bits_masked_off=[
  req( 0, 8 ),  resp( 0),
  req( 4, 16),  resp( 64),
  req( -6, 32 ),  resp(  -192 ),
  req( -1234,-128 ),  resp( 1234*128),               
  req( 10,1073741824),  resp(  10737418240 ),                  #1073741824=0x40000000           
  req( -1, 1879048192),  resp(-1879048192),                                              #at the edge of overflow
  req( -60, 1879048192),  resp((-60)*1879048192),              #1879048192=0x70000000    #overflow
  req( -21, -1610612736),  resp((-21)*(-1610612736)),          #-1610612736=0xa0000000
]

array10=[]
for i in range(0,random_num):
  k=random.randint(0,intmax)
  k= k & 4294967040                                            #4294967040=0xffffff00    used to masked off the lower bits
  array10.append(k)
  
ran_lower_bits_masked_off = [
  req(  array10[0], array10[1] ), resp( array10[0] * array10[1] ),
  req(  array10[2], array10[3] ), resp( array10[2] * array10[3] ),
  req(  array10[4], array10[5] ), resp( array10[4] * array10[5] ),
  req(  array10[6], array10[7] ), resp( array10[6] * array10[7] ),
  req(  array10[8], array10[9] ), resp( array10[8] * array10[9] ),
]

middle_bits_masked_off=[
  req( 0, 65280),  resp( 0),
  req( -6, 1048320 ),  resp((-6)*1048320 ),                    #1048320=0x000fff00
  req( -1234,-1048320 ),  resp( 1234*1048320),               
  req( 12,16776960),  resp(12* 16776960),                      #16776960=0x00ffff00      #at the edge of overflow    
  req( 13, 16776960),  resp(13*16776960),                                                #overflow
  req( -2, -16776960),  resp((-2)*(-16776960)),          
]

array11=[]
for i in range(0,random_num):
  l=random.randint(0,intmax)
  l= l & 4293922815                                            #4293922815=0xfff00fff used to mask off the middle bits
  array11.append(l)
  
ran_middle_bits_masked_off = [
  req(  array11[0], array11[1] ), resp( array11[0] * array11[1] ),
  req(  array11[2], array11[3] ), resp( array11[2] * array11[3] ),
  req(  array11[4], array11[5] ), resp( array11[4] * array11[5] ),
  req(  array11[6], array11[7] ), resp( array11[6] * array11[7] ),
  req(  array11[8], array11[9] ), resp( array11[8] * array11[9] ),
]

few_ones=[
  req( 0, 0),  resp( 0),
  req( -6, 15),  resp( -90),                            
  req( 90, 65537 ),  resp(90*65537 ),                        #65537=0x00010001
  req( -125,65537 ),  resp( -125*65537),               
  req( 10920,196609),  resp(10920* 196609),                  #196609=0x00030001         #at the edge of overflow    
  req( 10940,196609),  resp(10940*196609),                                              #overflow
  req( -177, -196609),  resp((-177)*(-196609)),          
]

array12=[]
for i in range(0,random_num):
  m=random.randint(0,intmax)
  m= m & 251658240                                            #251658240=0x0f000000  to maked off 1s 
  array12.append(m)
  
ran_few_ones = [
  req(  array12[0], array12[1] ), resp( array12[0] * array12[1] ),
  req(  array12[2], array12[3] ), resp( array12[2] * array12[3] ),
  req(  array12[4], array12[5] ), resp( array12[4] * array12[5] ),
  req(  array12[6], array12[7] ), resp( array12[6] * array12[7] ),
  req(  array12[8], array12[9] ), resp( array12[8] * array12[9] ),
]

few_zeros=[
  req( 0, 268435455),  resp( 0),                            #268435455=0x0fffffff       
  req( -1, 268435455),  resp( -268435455),                            
  req( 16, 134217727 ),  resp(16*134217727 ),                 #134217727=0x07ffffff       #at the edge of overflow
  req( 18,134217727 ),  resp( 18*134217727),                                              #overflow         
  req( -7,-134217727),  resp( 7* 134217727),                                                                      
  req( 12,(-134217727)),  resp(12*(-134217727)),                                                        
]

array13=[]
for i in range(0,random_num):
  n=random.randint(0,intmax)
  n= n | 4293984255                                           #4293984255=0xfff0ffff
  array13.append(n)
  
ran_few_zeros = [
  req(  array13[0], array13[1] ), resp( array13[0] * array13[1] ),
  req(  array13[2], array13[3] ), resp( array13[2] * array13[3] ),
  req(  array13[4], array13[5] ), resp( array13[4] * array13[5] ),
  req(  array13[6], array13[7] ), resp( array13[6] * array13[7] ),
  req(  array13[8], array13[9] ), resp( array13[8] * array13[9] ),
]



#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                                "msgs                     src_delay sink_delay"),
  [ "small_pos_pos",               small_pos_pos_msgs,         0,        0          ],
  [ "ran_small_pos_pos",           ran_small_pos_pos_msgs,     0,        0          ],
  [ "zeros_one_negativeone",       zeros_one_negativeone,      0,        0          ],
  [ "ran_zeros_one_negativeone",   ran_zeros_one_negativeone,  0,        0          ],
  [ "smallneg_smallpos",           smallneg_smallpos,          5,        0          ],
  [ "ran_smallneg_smallpos",       ran_smallneg_smallpos,      5,        0          ],
  [ "smallpos_smallneg",           smallpos_smallneg,          5,        0          ],
  [ "ran_smallpos_smallneg",       ran_smallpos_smallneg,      0,        0          ],       #largeneg_largepos
  [ "smallneg_smallneg",           smallneg_smallneg,          0,        0          ],
  [ "ran_smallneg_smallneg",       ran_smallneg_smallneg,      0,        0          ],
  [ "largepos_largepos",           largepos_largepos,          0,        0          ],
  [ "ran_largepos_largepos",       ran_largepos_largepos,      0,        0          ],
  [ "largepos_largeneg",           largepos_largeneg,          0,        0          ],
  [ "ran_largepos_largeneg",       ran_largepos_largeneg,      0,        0          ],
  [ "largeneg_largepos",           largeneg_largepos,          0,        0          ],
  [ "ran_largeneg_largepos",       ran_largeneg_largepos,      0,        0          ],
  [ "largeneg_largeneg",           largeneg_largeneg,          0,        0          ],
  [ "ran_largeneg_largeneg",       ran_largeneg_largeneg,      0,        0          ],
  [ "lower_bits_masked_off",       lower_bits_masked_off,      0,        0          ],
  [ "ran_lower_bits_masked_off",   ran_lower_bits_masked_off,  0,        0          ],
  [ "middle_bits_masked_off",      middle_bits_masked_off,     0,        0          ],
  [ "ran_middle_bits_masked_off",  ran_middle_bits_masked_off, 0,        5          ],
  [ "few_ones",                    few_ones,                   0,        0          ],
  [ "ran_few_ones",                ran_few_ones,               0,        0          ],
  [ "few_zeros",                   few_zeros,                  0,        0          ],
  [ "ran_few_zeros",               ran_few_zeros,              0,       0          ], 
  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to leverage the additional lists
  # of request/response messages defined above, but also to test
  # different source/sink random delays.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

#-------------------------------------------------------------------------
# Test cases
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( test_params, dump_vcd ):
  run_sim( TestHarness( IntMulFL(),
                        test_params.msgs[::2], test_params.msgs[1::2],
                        test_params.src_delay, test_params.sink_delay ),
           dump_vcd )

