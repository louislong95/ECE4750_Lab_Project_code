//=========================================================================
// Baseline Blocking Cache Control
//=========================================================================

`ifndef LAB3_MEM_BLOCKING_CACHE_BASE_CTRL_V
`define LAB3_MEM_BLOCKING_CACHE_BASE_CTRL_V

`include "vc/mem-msgs.v"
`include "vc/assert.v"

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab3_mem_BlockingCacheBaseCtrlVRTL
#(
  parameter p_idx_shamt    = 0
)
(
  input  logic                        clk,
  input  logic                        reset,

  // Cache Request

  input  logic                        cachereq_val,
  output logic                        cachereq_rdy,

  // Cache Response

  output logic                        cacheresp_val,
  input  logic                        cacheresp_rdy,

  // Memory Request

  output logic                        memreq_val,
  input  logic                        memreq_rdy,

  // Memory Response

  input  logic                        memresp_val,
  output logic                        memresp_rdy,

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Define additional ports
  output logic                        memresp_en,
  output logic                        write_data_mux_sel,
  output logic                        cachereq_en,
  input  logic [2:0]                  cachereq_type,
  input  logic [31:0]                 cachereq_addr,
  output  logic          tag_array_ren,
  output  logic          tag_array_wen,
  output  logic          data_array_ren,
  output  logic          data_array_wen,
  output  logic [15:0]   data_array_wben,
  output  logic          read_data_reg_en,
  input   logic          tag_match,
  output  logic          evict_addr_reg_en,
  output  logic          memreq_addr_mux_sel,
  output  logic [2:0]    read_word_mux_sel,
  output  logic [2:0]    cacheresp_type,
  output  logic [1:0]    hit,
  output  logic [2:0]    memreq_type
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

 );

  // local parameters not meant to be set from outside
  localparam size = 256;             // Cache size in bytes
  localparam dbw  = 32;              // Short name for data bitwidth
  localparam abw  = 32;              // Short name for addr bitwidth
  localparam o    = 8;               // Short name for opaque bitwidth
  localparam clw  = 128;             // Short name for cacheline bitwidth
  localparam nbl  = size*8/clw;      // Number of blocks in the cache
  localparam nby  = nbl;             // Number of blocks per way
  localparam idw  = $clog2(nby);     // Short name for index bitwidth
  localparam ofw  = $clog2(clw/8);   // Short name for the offset bitwidth
  // In this lab, to simplify things, we always use all bits except for the
  // offset in the tag, rather than storing the "normal" 24 bits. This way,
  // when implementing a multi-banked cache, we don't need to worry about
  // re-inserting the bank id into the address of a cacheline.
  localparam tgw  = abw - ofw;       // Short name for the tag bitwidth

  localparam IDLE_STATE               = 4'b0000;
  localparam TAG_CHECK_STATE          = 4'b0001;
  localparam INIT_DATA_ACCESS_STATE   = 4'b0010;
  localparam WAIT_STATE               = 4'b0011;
  localparam READ_DATA_ACCESS_STATE   = 4'b0100;
  localparam REFILL_REQUEST_STATE     = 4'b0101;
  localparam REFILL_WAIT_STATE        = 4'b0110;
  localparam REFILL_UPDATE_STATE      = 4'b0111;
  localparam WRITE_DATA_ACCESS_STATE  = 4'b1000;
  localparam EVICT_PREPARE_STATE      = 4'b1001;
  localparam EVICT_REQUEST_STATE      = 4'b1010;
  localparam EVICT_WAIT_STATE         = 4'B1011;

  logic [3:0] current_state;
  logic [3:0] next_state;
  logic [15:0] valid_bits;
  logic [15:0] dirty_bits;
  logic [3:0] idx;
  logic       read_hit;
  logic       write_hit;
  logic [1:0] hit_res;
  
  logic       init_transaction;
  logic [1:0] word_offset;
  logic condi_refill_req_state;
  logic condi_evc_pre_state;
  
  

  // condition for state transition signal
  assign init_transaction = (cachereq_type == 3'd2);
  assign read_hit         = tag_match && (cachereq_type == 3'd0) && valid_bits[idx];   // 0 is read, 1 is write
  assign write_hit        = tag_match && (cachereq_type == 3'd1) && valid_bits[idx];
  /*assign hit_res          = {1'b0, read_hit || write_hit};
  assign hit              = {1'b0, read_hit || write_hit}; */

  // condition for dirty bits
  
  //assign dirty_bits[idx]  = write_hit && (cachereq_addr [7:4] == idx);
  assign condi_refill_req_state = (!tag_match  && !dirty_bits[idx]) || (!valid_bits[idx]);
  assign condi_evc_pre_state = (!tag_match && dirty_bits[idx]) || (!valid_bits[idx]);
  assign idx = cachereq_addr [ (7+p_idx_shamt) : (4+p_idx_shamt)];
  assign word_offset = cachereq_addr [3:2];

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Implement control unit

  always_ff @ (posedge clk) begin
    if (reset) begin
       current_state <= IDLE_STATE;
    end
    else begin
       current_state <= next_state;
    end
  end

  always_comb begin
    case (current_state)
       IDLE_STATE:      if (cachereq_val)     begin
                                                next_state = TAG_CHECK_STATE;
                                              end

       TAG_CHECK_STATE: begin
                        hit_res          = {1'b0, read_hit || write_hit};
                        hit              = {1'b0, read_hit || write_hit};
       
                        if (init_transaction) begin
                                                 next_state = INIT_DATA_ACCESS_STATE;
                                              end

                        else if (read_hit)    begin
                                                 next_state = READ_DATA_ACCESS_STATE;
                                              end

                        else if (write_hit)   begin
                                                 next_state = WRITE_DATA_ACCESS_STATE;
                                              end

                        else if (condi_refill_req_state)
                                              begin
                                                 next_state = REFILL_REQUEST_STATE;
                                              end

                        else if (condi_evc_pre_state)
                                              begin
                                                 next_state = EVICT_PREPARE_STATE;
                                              end
                        end
        INIT_DATA_ACCESS_STATE: begin            next_state = WAIT_STATE;
                                                 valid_bits[idx] = 1'b1;  end
                                                 // do we really need dirty_bits=1 ???????!!!!!!!!!!**********
        READ_DATA_ACCESS_STATE: begin            next_state = WAIT_STATE; end

        WRITE_DATA_ACCESS_STATE:begin            next_state = WAIT_STATE;
                                                 valid_bits[idx] = 1'b1;  
                                                 dirty_bits[idx] = 1'b1;  //???????????
                                                end
                                                
        WAIT_STATE:     if (cacheresp_rdy)    begin
                                                 next_state = IDLE_STATE;
                                              end
                        else if(!cacheresp_rdy) begin
                                                next_state=WAIT_STATE;
                                                end

        REFILL_REQUEST_STATE:
                        if (!memreq_rdy)      begin
                                                 next_state = REFILL_REQUEST_STATE;
                                              end

                        else if (memreq_rdy)  begin
                                                 next_state = REFILL_WAIT_STATE;
                                                 valid_bits[idx] = 1'b1;
                                              end

        REFILL_WAIT_STATE:
                        if (!memresp_val)     begin
                                                 next_state = REFILL_WAIT_STATE;
                                              end

                        else if (memresp_val) begin
                                                 next_state = REFILL_UPDATE_STATE;
                                              end

        REFILL_UPDATE_STATE:
                        if (cachereq_type == 3'd0) begin
                                                 next_state = READ_DATA_ACCESS_STATE;
                                                   end

                        else if (cachereq_type == 3'd1) begin
                                                 next_state = WRITE_DATA_ACCESS_STATE;
                                                        end

        EVICT_PREPARE_STATE:                   begin              
                                               next_state = EVICT_REQUEST_STATE;
                                               dirty_bits[idx] = 1'b0; 
                                               end

        EVICT_REQUEST_STATE:
                       if (!memreq_rdy)       begin
                                                 next_state = EVICT_REQUEST_STATE;
                                              end

                       else if (memreq_rdy)   begin
                                                 next_state = EVICT_WAIT_STATE;
                                              end

        EVICT_WAIT_STATE:
                       if (!memresp_val)      begin
                                                 next_state = EVICT_WAIT_STATE;
                                              end

                       else if (memresp_val)  begin
                                                 next_state = REFILL_REQUEST_STATE;
                                              end
       
        default:       next_state = IDLE_STATE;
    endcase
  end

    task cs
    (
        input logic cs_cachereq_rdy,
        input logic cs_cacheresp_val,
        input logic cs_memreq_val,
        input logic cs_memresp_rdy,
        input logic cs_memresp_en,
        input logic cs_write_data_mux_sel,
        input logic cs_cachereq_en,
        input logic cs_tag_array_ren,
        input logic cs_tag_array_wen,
        input logic cs_data_array_ren,
        input logic cs_data_array_wen,
        input logic [15:0] cs_data_array_wben,
        input logic cs_read_data_reg_en,
        input logic cs_evict_addr_reg_en,
        input logic cs_memreq_addr_mux_sel,
        input logic [2:0] cs_read_word_mux_sel,
        input logic [2:0] cs_cacheresp_type,
        input logic [1:0] cs_hit,
        input logic [2:0] cs_memreq_type
    );
    begin
        cachereq_rdy         = cs_cachereq_rdy;
        cacheresp_val        = cs_cacheresp_val;
        memreq_val           = cs_memreq_val;
        memresp_rdy          = cs_memresp_rdy;
        memresp_en           = cs_memresp_en;
        write_data_mux_sel   = cs_write_data_mux_sel;
        cachereq_en          = cs_cachereq_en;
        tag_array_ren        = cs_tag_array_ren;
        tag_array_wen        = cs_tag_array_wen;
        data_array_ren       = cs_data_array_ren;
        data_array_wen       = cs_data_array_wen;
        data_array_wben      = cs_data_array_wben;
        read_data_reg_en     = cs_read_data_reg_en;
        evict_addr_reg_en    = cs_evict_addr_reg_en;
        memreq_addr_mux_sel  = cs_memreq_addr_mux_sel;
        read_word_mux_sel    = cs_read_word_mux_sel;
        cacheresp_type       = cs_cacheresp_type;
        hit                  = cs_hit;
        memreq_type          = cs_memreq_type;
    end
    endtask

    logic [15:0] wben;
    logic [2:0] rwms;
    always_comb begin
      case (word_offset)
         2'b00: wben = 16'h000F;
         2'b01: wben = 16'h00F0;
         2'b10: wben = 16'h0F00;
         2'b11: wben = 16'hF000;
      endcase

      if (cacheresp_type == 3'd1 || cacheresp_type == 3'd2)
       begin
          rwms = 3'd4;
       end
      else
       begin
          rwms = {1'b0, word_offset};
       end
    end

    always_comb begin
        cs(   1,     0,      0,      0,        0,      'x,         1,     0,   0,   0,    0,  16'dx,      0,         0,       'x,         3'dx,     3'dx,           2'dx,    3'dx   );
        case(current_state)
          //                               c_req  c_resp  memreq  memresp   memresp  write_data  c_req  tag  tag  data  data  data  read_data  evict_addr memreq_addr  read_word  c_resp            hit    memreq
          //                                rdy    val     val     rdy       en      mux_sel      en    ren  wen  ren   wen   wben   reg_en     reg_en     mux_sel      mux_sel    type                     type
          IDLE_STATE:                  cs(   1,     0,      0,      0,        0,      'x,         1,     0,   0,   0,    0,  16'dx,      0,         0,       'x,         3'dx,     3'dx,           2'dx,    3'dx   );
          TAG_CHECK_STATE:             cs(   0,     0,      0,      0,        0,      'x,         0,     1,   0,   0,    0,  16'dx,      0,         0,       'x,         3'dx,     3'dx,           2'dx,    3'dx   );
          INIT_DATA_ACCESS_STATE:      cs(   0,     0,      0,      0,        0,       0,         0,     0,   1,   0,    1,   wben,      0,         0,       'x,         3'dx,     3'dx,           2'dx,    3'dx   );
          READ_DATA_ACCESS_STATE:      cs(   0,     0,      0,      0,        0,      'x,         0,     0,   0,   1,    0,  16'dx,      1,         0,       'x,         3'dx,     3'dx,           2'dx,    3'dx   );
          WRITE_DATA_ACCESS_STATE:     cs(   0,     0,      0,      0,        0,       0,         0,     0,   1,   0,    1,   wben,      0,         0,       'x,         3'dx,     3'dx,           2'dx,    3'dx   );
          WAIT_STATE:                  cs(   0,     1,      0,      0,        0,      'x,         0,     0,   0,   0,    0,  16'dx,      0,         0,       'x,         rwms,     cachereq_type,  hit_res, 3'dx   );
          REFILL_REQUEST_STATE:        cs(   0,     0,      1,      0,        0,      'x,         0,     0,   0,   0,    0,  16'dx,      0,         0,        1,         3'dx,     3'dx,           2'dx,    3'd0   );
          REFILL_WAIT_STATE:           cs(   0,     0,      0,      1,        1,      'x,         0,     0,   0,   0,    0,  16'dx,      0,         0,       'x,         3'dx,     3'dx,           2'dx,    3'dx   );
          REFILL_UPDATE_STATE:         cs(   0,     0,      0,      0,        0,       1,         0,     0,   1,   0,    1,  16'hFFFF,   0,         0,       'x,         3'dx,     3'dx,           2'dx,    3'dx   );
          EVICT_PREPARE_STATE:         cs(   0,     0,      0,      0,        0,      'x,         0,     1,   0,   1,    0,  16'dx,      1,         1,       'x,         3'dx,     3'dx,           2'dx,    3'dx   );
          EVICT_REQUEST_STATE:         cs(   0,     0,      1,      0,        0,      'x,         0,     0,   0,   0,    0,  16'dx,      0,         0,        0,         3'dx,     3'dx,           2'dx,    3'd1   );
          EVICT_WAIT_STATE:            cs(   0,     0,      0,      1,        1,      'x,         0,     0,   0,   0,    0,  16'dx,      0,         0,       'x,         3'dx,     3'dx,           2'dx,    3'dx   );
          default                      cs(   1,     0,      0,      0,        0,      'x,         1,     0,   0,   0,    0,  16'dx,      0,         0,       'x,         3'dx,     3'dx,           2'dx,    3'dx   );

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        endcase
    end
    
endmodule

`endif
