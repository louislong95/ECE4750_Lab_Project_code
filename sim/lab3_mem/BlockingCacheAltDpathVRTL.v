//=========================================================================
// Alternative Blocking Cache Datapath
//=========================================================================

`ifndef LAB3_MEM_BLOCKING_CACHE_ALT_DPATH_V
`define LAB3_MEM_BLOCKING_CACHE_ALT_DPATH_V

`include "vc/mem-msgs.v"
`include "vc/muxes.v"
`include "vc/regs.v"
`include "vc/srams.v"
`include "vc/arithmetic.v"

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab3_mem_BlockingCacheAltDpathVRTL
#(
  parameter p_idx_shamt    = 0
)
(
  input  logic                        clk,
  input  logic                        reset,

  // Cache Request

  input  mem_req_4B_t                 cachereq_msg,

  // Cache Response

  output mem_resp_4B_t                cacheresp_msg,

  // Memory Request

  output mem_req_16B_t                memreq_msg,

  // Memory Response

  input  mem_resp_16B_t               memresp_msg,

  input  logic          memresp_en,
  input  logic          write_data_mux_sel,
  input  logic          cachereq_en,
  output logic [2:0]    cachereq_type,
  output logic [31:0]   cachereq_addr,
  input  logic          tag_array_ren,
  input  logic          tag_array_wen1,
  input  logic          tag_array_wen2,                      //change
  input  logic          data_array_ren,
  input  logic          data_array_wen,
  input  logic [15:0]   data_array_wben,
  input  logic          read_data_reg_en,
  output logic          tag_match1,
  output logic          tag_match2,
  input  logic          evict_addr_reg_en,
  input  logic [1:0]    memreq_addr_mux_sel,
  input  logic [2:0]    read_word_mux_sel,
  input  logic [2:0]    cacheresp_type,
  input  logic [1:0]    hit,
  input  logic [2:0]    memreq_type,
  input  logic          idx_fourth
);

  // local parameters not meant to be set from outside
  localparam size = 256;             // Cache size in bytes
  localparam dbw  = 32;              // Short name for data bitwidth
  localparam abw  = 32;              // Short name for addr bitwidth
  localparam o    = 8;               // Short name for opaque bitwidth
  localparam clw  = 128;             // Short name for cacheline bitwidth
  localparam nbl  = size*8/clw;      // Number of blocks in the cache         //in our case=16 bits
  localparam nby  = nbl;             // Number of blocks per way              //in our case=16 bits
  localparam idw  = $clog2(nby) - 1;     // Short name for index bitwidth     //in our case=3 bits
  localparam ofw  = $clog2(clw/8);   // Short name for the offset bitwidth    //in our case=4 bits
  // In this lab, to simplify things, we always use all bits except for the
  // offset in the tag, rather than storing the "normal" 24 bits. This way,
  // when implementing a multi-banked cache, we don't need to worry about
  // re-inserting the bank id into the address of a cacheline.
  localparam tgw  = abw - ofw;       // Short name for the tag bitwidth       //in our case=28 bits

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Implement data-path
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  logic [127:0] memresp_data_reg_in;
  logic [127:0] memresp_data_reg_out;
  assign memresp_data_reg_in = memresp_msg[127:0];
   vc_EnResetReg #(128,0) memresp_data_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (memresp_en),              // this will be a control input
    .d      (memresp_data_reg_in),     //data in figure
    .q      (memresp_data_reg_out)
  );

   logic  [127:0] repl_out;
   logic  [127:0] write_data_mux_out;
   vc_Mux2 #(128) write_data_mux
  (
    .in0  (repl_out),
    .in1  (memresp_data_reg_out),
    .sel  (write_data_mux_sel),     // this will be a control input
    .out  (write_data_mux_out)
  );

  assign  cachereq_opaque_reg_in= cachereq_msg[73:66];
  logic   [7:0]      cachereq_opaque_reg_in;
  logic   [7:0]      cachereq_opaque_reg_out;
  vc_EnResetReg #(8,0) cachereq_opaque_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_en),              // this will be a control input
    .d      (cachereq_opaque_reg_in),
    .q      (cachereq_opaque_reg_out)
  );

  assign  cachereq_type_reg_in= cachereq_msg[76:74];
  logic   [2:0]      cachereq_type_reg_in;

  vc_EnResetReg #(3,0) cachereq_type_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_en),              // this will be a control input
    .d      (cachereq_type_reg_in),
    .q      (cachereq_type)             //this is a output control signal
  );

  assign  cachereq_addr_reg_in= cachereq_msg[65:34];
  logic   [31:0]      cachereq_addr_reg_in;
  logic   [31:0]      cachereq_addr_reg_out;
  vc_EnResetReg #(32,0) cachereq_addr_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_en),              // this will be a control input
    .d      (cachereq_addr_reg_in),
    .q      (cachereq_addr_reg_out)
  );
  assign  cachereq_addr = cachereq_addr_reg_out;

  assign  cachereq_data_reg_in= cachereq_msg[31:0];
  logic   [31:0]      cachereq_data_reg_in;
  logic   [31:0]      cachereq_data_reg_out;
  vc_EnResetReg #(32,0) cachereq_data_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_en),              // this will be a control input
    .d      (cachereq_data_reg_in),
    .q      (cachereq_data_reg_out)
  );

  assign repl_out = {cachereq_data_reg_out,cachereq_data_reg_out,cachereq_data_reg_out,cachereq_data_reg_out}; //This is the function of repl

  logic [idw-1:0] idx;
  logic [27:0] write_data;
  //assign idx = cachereq_addr_reg_out[ (6+p_idx_shamt) : (4+p_idx_shamt)];
  assign idx = cachereq_addr_reg_out[ofw + p_idx_shamt +: idw];
  assign write_data= cachereq_addr_reg_out[31:4];
  logic [27:0] tag_array_out1;
  logic [27:0] tag_array_out2;
  vc_CombinationalBitSRAM_1rw #(28,8) Tag_Array1
  (
    .clk        (clk),
    .reset      (reset),
    .read_en    (tag_array_ren),        //This is a control input signal
    .read_addr  (idx),
    .read_data  (tag_array_out1),
    .write_en   (tag_array_wen1),
    .write_addr (idx),            //the same line as write_addr
    .write_data (write_data)
  );
  
  //change
  vc_CombinationalBitSRAM_1rw #(28,8) Tag_Array2
  (
    .clk        (clk),
    .reset      (reset),
    .read_en    (tag_array_ren),        //This is a control input signal
    .read_addr  (idx),
    .read_data  (tag_array_out2),
    .write_en   (tag_array_wen2),
    .write_addr (idx),            //the same line as write_addr
    .write_data (write_data)
  );
  
  logic [127:0] data_array_out;
  logic [3:0] idx_for_data;
  assign idx_for_data = {idx_fourth, idx};
  
  vc_CombinationalSRAM_1rw #(128,16) Data_Array
  (
   .clk           (clk),
   .reset         (reset),
   .read_en       (data_array_ren),    //This is a input control signal
   .read_addr     (idx_for_data),
   .read_data     (data_array_out),
   .write_en      (data_array_wen),    //This is a input control signal
   .write_byte_en (data_array_wben),   //This is a input control signal
   .write_addr    (idx_for_data),
   .write_data    (write_data_mux_out)
  );
  

  logic [127:0]  read_data_reg_out;
   vc_EnResetReg #(128,0) read_data_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (read_data_reg_en),              // this will be a control input
    .d      (data_array_out),
    .q      (read_data_reg_out)
  );
  
   vc_EqComparator #(28) comp1
  (
    .in0(write_data),
    .in1(tag_array_out1),
    .out(tag_match1)
  );
  
   vc_EqComparator #(28) comp2     // we added here
  (
    .in0(write_data),
    .in1(tag_array_out2),
    .out(tag_match2)
  );
  

  //This is mkaddr 1(up)
  logic [31:0] mkaddr1_out;
  assign mkaddr1_out={tag_array_out1,4'b0000};

  //This is mkaddr 2(down)
  logic [31:0] mkaddr2_out;
  assign mkaddr2_out={write_data,4'b0000};    //write data is addr[31:4]
  
  logic [31:0] mkaddr3_out;                     // changed!!
  assign mkaddr3_out={tag_array_out2,4'b0000};  // new mkaddr for alt

  logic [31:0] evict_addr_reg_out_1;
  vc_EnResetReg #(32,0) evict_addr_reg_1
  (
    .clk    (clk),
    .reset  (reset),
    .en     (evict_addr_reg_en),              // this will be a control input
    .d      (mkaddr1_out),
    .q      (evict_addr_reg_out_1)
  );
  
  logic [31:0] evict_addr_reg_out_2;
  vc_EnResetReg #(32,0) evict_addr_reg_2
  (
    .clk    (clk),
    .reset  (reset),
    .en     (evict_addr_reg_en),              // this will be a control input
    .d      (mkaddr3_out),
    .q      (evict_addr_reg_out_2)
  );

  logic [31:0] memreq_addr_mux_out;
  vc_Mux3 #(32) memreq_addr_mux
  (
    .in0  (evict_addr_reg_out_1),
    .in1  (mkaddr2_out),
    .in2  (evict_addr_reg_out_2),
    .sel  (memreq_addr_mux_sel),     // this will be a control input
    .out  (memreq_addr_mux_out)
  );

  logic [31:0] read_word_mux_out;
  vc_Mux5 #(32) read_word_mux
  (
   .in0       (read_data_reg_out[31:0]),
   .in1       (read_data_reg_out[63:32]),
   .in2       (read_data_reg_out[95:64]),
   .in3       (read_data_reg_out[127:96]),
   .in4       (32'b0),
   .sel       (read_word_mux_sel),     //This is a input control signal
   .out       (read_word_mux_out)
  );

  assign cacheresp_msg = {cacheresp_type, cachereq_opaque_reg_out, hit, 2'b0, read_word_mux_out};
  assign memreq_msg    = {memreq_type, 8'b0, memreq_addr_mux_out, 4'b0, read_data_reg_out};

endmodule

`endif
