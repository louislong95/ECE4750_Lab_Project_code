//========================================================================
// Integer Multiplier Fixed-Latency Implementation
//========================================================================

`ifndef LAB1_IMUL_INT_MUL_BASE_V
`define LAB1_IMUL_INT_MUL_BASE_V

`include "vc/trace.v"

// the lib below is added by Yibang Xiao
`include "vc/muxes.v"
`include "vc/arithmetic.v"
`include "vc/regs.v"
`include "vc/counters.v"

// ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// Define datapath and control unit here.
// '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

//========================================================================
// Integer Multiplier Fixed-Latency Implementation
//========================================================================

module IntMulBase_Datapath
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
  
  output logic        b_lsb

);
  
  logic [31:0] b_reg_in;
  logic [31:0] b_reg_out; 
  logic [31:0] b_right_shift_out;
  logic [31:0] a_reg_in;
  logic [31:0] a_reg_out; 
  logic [31:0] a_left_shift_out;
  logic [31:0] result_reg_in;
  logic [31:0] result_reg_out;
  logic [31:0] add_mux_out;
  logic [31:0] add_mux_in0;
  
   vc_Mux2#(32) b_mux
   (
      .in0(b_right_shift_out), 
      .in1(req_msg[31:0]),
      .sel(b_mux_sel), 
      .out(b_reg_in) 
   );
   
   vc_Reg#(32) b_reg
   (
      .clk(clk),
      .q(b_reg_out),
      .d(b_reg_in)
   );

   vc_RightLogicalShifter#(32, 1) b_right_shift
   (
      .in(b_reg_out),
      .shamt(1'b1),
      .out(b_right_shift_out)
   );
   
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
   
   vc_LeftLogicalShifter#(32, 1) a_left_shift
   (
      .in(a_reg_out),
      .shamt(1'b1),
      .out(a_left_shift_out)
   );
   
   vc_Mux2#(32) result_mux
   (
      .in0(add_mux_out), 
      .in1(32'd0),  
      .sel(result_mux_sel),
      .out(result_reg_in)
   );
   
   vc_EnReg#(32) result_reg
   (
      .clk(clk),
      .q(result_reg_out),
      .d(result_reg_in),
      .en(result_en),  
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

   assign b_lsb    = b_reg_out[0] && 1'b1;    // detect the last significant bit of b
   assign resp_msg = result_reg_out;        // assign the result to the ouput

endmodule



module IntMulBase_Control   // control module starts
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

   output logic [5:0] counter_count_output

);
//ave three parts: a sequential concurrent block for the state, a combinational concurrent
//block for the state transitions, and a combinational concurrent block for the state outputs.
   
   logic [5:0] counter_count;
   logic       counter_is_zero;
   logic       counter_is_max;
   logic       counter_clear;
   //logic       counter_clear;

   vc_BasicCounter#(6, 0, 32) counter   
   (  // used to count the counter 
      .clk(clk),
      .reset(0),
      .clear(counter_is_max || counter_clear),  // if the counter clear flag is raised
      .increment(1'b1),
      .decrement(1'b0),
      .count(counter_count),       //output
      .count_is_zero(counter_is_zero),  //output
      .count_is_max(counter_is_max)  //output

   );
 
    localparam  IDLE_STATE = 2'b00;
    localparam  CALC_STATE = 2'b01;
    localparam  DONE_STATE = 2'b10;   // define the state
    
    logic [1:0] current_state;
    logic [1:0] next_state;
    
    logic req_go;       // define the action
    logic resp_go;
    logic calc_done;
    
    assign req_go       = req_val  && req_rdy;
    assign resp_go      = resp_val && resp_rdy;
    assign calc_done    = (counter_is_max);

    // sequential state 
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
                                      assign counter_clear = 1'b1;  // clear the counter
                                    end
         
         CALC_STATE: if (calc_done) begin
                                      next_state = DONE_STATE;
                                      assign counter_clear = 1'b0;  // start the counter
                                    end
         
         DONE_STATE: if (resp_go)   begin
                                      next_state = IDLE_STATE;
                                      assign counter_clear = 1'b1;
                                    end

         default:     next_state = IDLE_STATE;    // initial state is IDLE_STATE
         
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
    );    // these are the control signal sent back to the datapath
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
     
     assign do_add_shift  = (!counter_is_max) && (b_lsb == 1);   // if last bit is 1, add and shift
     assign do_only_shift = (!counter_is_max) && (b_lsb == 0);   // if last bit is 0, only shift
     
     //req_rdy | resp_val | a_mux_sel | b_mux_sel | result_mux_sel | add_mux_sel | result_en
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
    
   /* always @ (posedge clk)
    begin    
       case (STATE)
         IDLE_STATE:
         begin
           a_mux_sel        <= 1'b1;
           b_mux_sel        <= 1'b1;
           result_mux_sel   <= 1'b1;
           add_mux_sel      <= 1'b1;
           req_rdy          <= 1'b1;     
           resp_val         <= 1'b0;  
           if (req_val == 1'b0)
             STATE     <= IDLE_STATE;
           else
             STATE     <= CALC_STATE;
         end
         
         CALC_STATE:
         begin
           a_mux_sel        <= 1'b0;
           b_mux_sel        <= 1'b0;
           result_mux_sel   <= 1'b0;
           add_mux_sel      <= 0;
           req_rdy          <= 1'b0;
           resp_val         <= 1'b0;
           counter <= 6'd0;
           if (counter < 32 && b_lsb)
           begin
             add_mux_sel <= 0'b0; 
             counter <= counter + 1;
             STATE  <= CALC_STATE;
           end
           else if (counter < 32 && !b_lsb)
           begin
             add_mux_sel    <= 1'b1;
             counter <= counter + 1;
             STATE  <= CALC_STATE;
           end
           else if (counter == 32)
           begin
             STATE     <= DONE_STATE;
           end
         end
         
         DONE_STATE:
         begin
           a_mux_sel        <= 1'b1;
           b_mux_sel        <= 1'b1;
           result_mux_sel   <= 1'b0;
           add_mux_sel      <= 1'b1;
           req_rdy          <= 1'b0;
           resp_val         <= 1'b1;
           if (!resp_rdy)
             STATE <= DONE_STATE;
           else if (resp_rdy)
             STATE <= IDLE_STATE;
         end
         
         default: 
         begin
           STATE <= IDLE_STATE;
         end
       endcase
       
    end  */
    assign counter_count_output = counter_count;
endmodule


module lab1_imul_IntMulBaseVRTL
(
  input  logic        clk,
  input  logic        reset,

  input  logic        req_val,
  output logic        req_rdy,
  input  logic [63:0] req_msg,

  output logic        resp_val,
  input  logic        resp_rdy,
  output logic [31:0] resp_msg
  
);
   
   logic  a_mux_sel;
   logic  b_mux_sel;
   logic  result_mux_sel;
   logic  add_mux_sel;
   logic  result_en;
   logic  b_lsb;
   logic  [5:0] counter_count_output;

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
   
   IntMulBase_Datapath datapath
   (
      .*
   );
   
   IntMulBase_Control control
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


