//=========================================================================
// Verilog Components: Counter
//=========================================================================

`ifndef lab1_imul_COUNTER_V
`define lab1_imul_COUNTER_V

`include "vc/regs.v"

module vc_SmartCounter
#(
  parameter p_count_nbits       = 3,
  parameter p_count_clear_value = 0,
  parameter p_count_max_value   = 4
)(
  input  logic                     clk,
  input  logic                     reset,

  // Operations

  input  logic                     clear,
  input  logic                     increment,
  input  logic                     decrement,
  input  logic                     jump_flag,

  // Outputs

  output logic [p_count_nbits-1:0] count,
  output logic                     count_is_zero,
  output logic                     count_is_max

);

  //----------------------------------------------------------------------
  // State
  //----------------------------------------------------------------------

  logic [p_count_nbits-1:0] count_next;

  vc_ResetReg#( p_count_nbits, p_count_clear_value ) count_reg
  (
    .clk   (clk),
    .reset (reset),
    .d     (count_next),
    .q     (count)
  );

  //----------------------------------------------------------------------
  // Combinational Logic
  //----------------------------------------------------------------------

  logic do_increment_one;
  logic do_increment_two;
  assign do_increment_one = ( increment && (count < p_count_max_value) && !(jump_flag));
  assign do_increment_two = ( increment && (count < p_count_max_value) &&   jump_flag );

  logic do_decrement;
  assign do_decrement = ( decrement && (count > 0) );

  assign count_next
    = clear        ? (p_count_clear_value)
    : do_increment_one ? (count + 1)
    : do_increment_two ? (count + 2)
    : do_decrement ? (count - 1)
    : count;

  assign count_is_zero = (count == 0);
  assign count_is_max  = (count == p_count_max_value || count > p_count_max_value);

  //----------------------------------------------------------------------
  // Assertions
  //----------------------------------------------------------------------

  /*
  always_ff @( posedge clk ) begin
    if ( !reset ) begin
      `VC_ASSERT_NOT_X( increment );
      `VC_ASSERT_NOT_X( decrement );
    end
  end
  */

endmodule

`endif /* VC_COUNTER_V */

