//========================================================================
// Integer Multiplier Fixed-Latency Implementation
//========================================================================
//newest
`ifndef LAB1_IMUL_INT_MUL_ALT_V
`define LAB1_IMUL_INT_MUL_ALT_V

`include "vc/trace.v"

// the lib below is added by Yibang Xiao
`include "vc/muxes.v"
`include "vc/arithmetic.v"
`include "vc/regs.v"
`include "vc/counters.v"
`include "lab1_imul/SmartCounter.v"

// ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// Define datapath and control unit here.
// '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

//========================================================================
// Integer Multiplier Fixed-Latency Implementation
//========================================================================

module IntMulAlt_Datapath
(
  input logic clk,
  input logic reset,
  
  input logic [63:0] req_msg,
  output logic [31:0] resp_msg,
  
  input logic a_mux_sel,
  input logic b_mux_sel,
  input logic result_mux_sel,
  input logic add_mux_sel,
  input logic result_en,
  
  output logic        b_lsb,
  output logic        shifted_two_flag

);
  
  logic [31:0] b_reg_in;
  logic [31:0] b_reg_out; // the same as b_lsb
  logic [31:0] b_right_shift_out;
  logic [31:0] a_reg_in;
  logic [31:0] a_reg_out; // the same as b_lsb
  logic [31:0] a_left_shift_out;
  logic [31:0] result_reg_in;
  logic [31:0] result_reg_out;
  logic [31:0] add_mux_out;
  logic [31:0] add_mux_in0;
  logic [1:0]  b_lsb2;
  logic        a;
  logic        b;
  logic [1:0]  shamt;
  logic        shifted_two_flag;
  
   vc_Mux2#(32) b_mux
   (
      .in0(b_right_shift_out), // this should be the output of shift reg
      .in1(req_msg[31:0]),
      .sel(b_mux_sel), // this should be b_mux_sel//req_val
      .out(b_reg_in) 
   );
   
   vc_Reg#(32) b_reg
   (
      .clk(clk),
      .q(b_reg_out),
      .d(b_reg_in)
   );

   vc_RightLogicalShifter#(32, 2) b_right_shift
   (
      .in(b_reg_out),
      .shamt(shamt),
      .out(b_right_shift_out)
   );
   
   assign b_lsb2 = b_reg_out[1:0] & 2'b11;
   assign a = ~(b_lsb2[1]);
   assign b = b_lsb2[1];
   assign shamt = {a,b};


   vc_Mux2#(32) a_mux
   (
      .in0(a_left_shift_out), // this should be the output of left reg
      .in1(req_msg[63:32]),
      .sel(a_mux_sel), // this should be a_mux_sel
      .out(a_reg_in) 
   );
   
   vc_Reg#(32) a_reg
   (
      .clk(clk),
      .q(a_reg_out),
      .d(a_reg_in)
   ); 
   
   vc_LeftLogicalShifter#(32, 2) a_left_shift
   (
      .in(a_reg_out),
      .shamt(shamt),
      .out(a_left_shift_out)
   );
   
   vc_Mux2#(32) result_mux
   (
      .in0(add_mux_out), 
      .in1(32'd0),  // this should be output of add_mux
      .sel(result_mux_sel), // this should be result_mux_sel or resp_rdy
      .out(result_reg_in)
   );
   
   vc_EnReg#(32) result_reg
   (
      .clk(clk),
      .q(result_reg_out),
      .d(result_reg_in),
      .en(result_en),  // !!!!!!!!!!!!!!!!!!!!!!!!!!Caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
      .reset(reset)
   );
   
   vc_Adder#(32) result_adder
   (
      .in0(a_reg_out),
      .in1(result_reg_out),
      .cin(1'b0),
      .out(add_mux_in0),
      .cout()
   );
   
   vc_Mux2#(32) add_mux
   (
      .in0(add_mux_in0),
      .in1(result_reg_out),
      .sel(add_mux_sel),  // this should be add_mux_sel//b_lsb
      .out(add_mux_out)
   );

   assign b_lsb    = b_reg_out[0] && 1'b1; 
   assign b_lsb2   = b_reg_out[1:0] & 2'b11;
   assign a        = ~b_lsb2[1];            // see the truth table in lab report
   assign b        =  b_lsb2[1];
   assign shamt    = {a, b};
   assign shifted_two_flag = (shamt == 2'b10);  // if we need to shift two bits, raise this flag for counter to plus two
   assign resp_msg = result_reg_out;

endmodule



module IntMulAlt_Control
(
   input logic clk,
   input logic reset,
   
   input logic req_val,
   output logic req_rdy,
   output logic resp_val,
   input logic resp_rdy,
   
   output logic a_mux_sel,
   output logic b_mux_sel,
   output logic result_mux_sel,
   output logic add_mux_sel,
   output logic result_en,
   
   input logic b_lsb,
   input logic shifted_two_flag,

   output logic [5:0] counter_count_output

);
//ave three parts: a sequential concurrent block for the state, a combinational concurrent
//block for the state transitions, and a combinational concurrent block for the state outputs.
   
   logic [5:0] counter_count;
   logic [5:0] counter_detect;
   logic       counter_is_zero;
   logic       counter_is_max;
   logic       counter_clear;

   vc_SmartCounter#(6, 0, 32) counter
   (
      .clk(clk),
      .reset(0),
      .clear(counter_is_max || counter_clear),  
      .increment(1'b1),
      .decrement(1'b0),
      .jump_flag(shifted_two_flag),    // this new flag is to detect the shift amount is 1 or 2, if 2, the counter = counter + 2
                                       // if shift amount is 1, the counter = counter + 1
      .count(counter_count),       //output
      .count_is_zero(counter_is_zero),  //output
      .count_is_max(counter_is_max)  //output

   );
 
    localparam  IDLE_STATE = 2'b00;
    localparam  CALC_STATE = 2'b01;
    localparam  DONE_STATE = 2'b10;
    
    logic [1:0] current_state;
    logic [1:0] next_state;
    
    logic req_go;
    logic resp_go;
    logic calc_done;
    
    assign req_go       = req_val  && req_rdy;
    assign resp_go      = resp_val && resp_rdy;
    assign calc_done    = (counter_is_max);
    assign counter_count_output = counter_count;
    
    always_ff @ (posedge clk) begin
      if (reset) begin
         current_state <= IDLE_STATE;
      end
      else begin
         current_state <= next_state;
      end
    end
    //------state transitions
    always_comb begin

     // next_state = current_state;
      case (current_state)
        
         IDLE_STATE: if (req_go)    begin    
                                      next_state = CALC_STATE;
                                      assign counter_clear = 1'b1;
                                    end
         
         CALC_STATE: if (calc_done) begin
                                      next_state = DONE_STATE;
                                      assign counter_clear = 1'b0;
                                    end
         
         DONE_STATE: if (resp_go)   begin
                                      next_state = IDLE_STATE;
                                      assign counter_clear = 1'b1;
                                    end

         default:     next_state = IDLE_STATE;
         
       endcase
    end
        
    //-----------   State Outputs ----------
    
    
    task cs
    (
        input logic  cs_req_rdy,
        input logic  cs_resp_val,
        input logic  cs_a_mux_sel,
        input logic  cs_b_mux_sel,
        input logic  cs_result_mux_sel,
        input logic  cs_add_mux_sel,
        input logic  cs_result_en,
        input logic  cs_counter_clear
    );
     begin
        req_rdy        = cs_req_rdy;
        resp_val       = cs_resp_val;
        a_mux_sel      = cs_a_mux_sel;
        b_mux_sel      = cs_b_mux_sel;
        result_mux_sel = cs_result_mux_sel;
        add_mux_sel    = cs_add_mux_sel;
        result_en      = cs_result_en;
        counter_clear  = cs_counter_clear;
     end
     endtask
     
     logic do_add_shift;
     logic do_only_shift;
     
     assign do_add_shift  = (!counter_is_max) && (b_lsb == 1);
     assign do_only_shift = (!counter_is_max) && (b_lsb == 0);
     
     //req_rdy | resp_val | a_mux_sel | b_mux_sel | result_mux_sel | add_mux_sel | result_en | counter clear
     always_comb begin
        cs(0, 0, 'x, 'x, 'x, 0, 'x, 1);
        case(current_state)
         //                                req resp   a    b   rlt   add   rlt   counter
         //                                rdy val    sel  sel sel   sel   en    clear
          IDLE_STATE:                    cs(1,   0,   1,   1,   1,   1,    1,     1);  
          CALC_STATE: if (do_add_shift)  cs(0,   0,   0,   0,   0,   0,    1,     0);
                 else if (do_only_shift) cs(0,   0,   0,   0,   0,   1,    1,     0);
          DONE_STATE:                    cs(0,   1,   1,   1,   0,   1,    0,     1);
          default                        cs(1,   0,   1,   1,   1,   1,    1,     1);
        endcase
     end

endmodule


module lab1_imul_IntMulAltVRTL
(
  input  logic        clk,
  input  logic        reset,

  input  logic        req_val,
  output logic        req_rdy,
  input  logic [63:0] req_msg,

  output logic        resp_val,
  input  logic        resp_rdy,
  output logic [31:0] resp_msg
  
  //input logic [5:0] counter_count_input
);

  /* logic a_mux_sel_inner;
   logic b_mux_sel_inner;
   logic result_mux_sel_ineer;
   logic add_mux_sel_ineer;
   logic result_en_inner;
   logic b_lsb_inner; */
   
   logic  a_mux_sel;
   logic  b_mux_sel;
   logic  result_mux_sel;
   logic  add_mux_sel;
   logic  result_en;
   logic  b_lsb;
   logic  [5:0] counter_count_output;
   logic  shifted_two_flag;

   /*IntMulBase_Datapath datapath
   (
      .clk            (clk),
      .reset          (reset),
      .req_msg        (req_msg),
      .a_mux_sel      (a_mux_sel_inner),
      .b_mux_sel      (b_mux_sel_inner),
      .result_mux_sel (result_mux_sel_ineer),
      .add_mux_sel    (add_mux_sel_ineer),
      .result_en      (result_en_inner),
      
      .b_lsb          (b_lsb_inner),
      .resp_msg       (resp_msg)
   );
   
   IntMulBase_Control control
   (
      .clk            (clk),
      .reset          (reset),
      .req_val        (req_val),
      .resp_rdy       (resp_rdy),
      .b_lsb          (b_lsb_inner),
      
      .req_rdy        (req_rdy),
      .resp_val       (resp_val),
      
      .a_mux_sel      (a_mux_sel_inner),
      .b_mux_sel      (b_mux_sel_inner),
      .result_mux_sel (result_mux_sel_ineer),
      .add_mux_sel    (add_mux_sel_ineer),
      .result_en      (result_en_inner)
   );  */
   
   IntMulAlt_Datapath datapath
   (
      .*
   );
   
   IntMulAlt_Control control
   (
      .*
   );
  
  
    
    
  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    $sformat( str, "%x", req_msg );
    vc_trace.append_val_rdy_str( trace_str, req_val, req_rdy, str );

    vc_trace.append_str( trace_str, "(" );

    // ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Add additional line tracing using the helper tasks for
    // internal state including the current FSM state.000004 > 0000000300000004()         >         
 // 6: 000000
    // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

   $sformat( str, "%x %d %d %d %d %d %d %d", req_msg, a_mux_sel, b_mux_sel, result_mux_sel, add_mux_sel, result_en, b_lsb, counter_count_output );
   vc_trace.append_str( trace_str, str );

    vc_trace.append_str( trace_str, ")" );

   // $sformat( str, "%x", resp_msg );
   // vc_trace.append_val_rdy_str( trace_str, resp_val, resp_rdy, str );
   
   $sformat( str, "%x", req_msg[63:32] );
    vc_trace.append_val_rdy_str( trace_str, req_val, req_rdy, str );
    
    vc_trace.append_str( trace_str, "(" );
    vc_trace.append_str( trace_str, ")" );
    
    $sformat( str, "%x", req_msg[31:0] );
    vc_trace.append_val_rdy_str( trace_str, req_val, req_rdy, str );
    
     vc_trace.append_str( trace_str, "(" );
    vc_trace.append_str( trace_str, ")" );
    
    $sformat( str, "%x",  resp_msg);
    vc_trace.append_val_rdy_str( trace_str, req_val, req_rdy, str );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* LAB1_IMUL_INT_MUL_BASE_V */

