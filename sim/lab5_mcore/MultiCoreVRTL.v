//========================================================================
// 1-Core Processor-Cache-Network
//========================================================================

`ifndef LAB5_MCORE_MULTI_CORE_V
`define LAB5_MCORE_MULTI_CORE_V

`include "vc/mem-msgs.v"
`include "vc/trace.v"
`include "lab2_proc/ProcAltVRTL.v"
`include "lab3_mem/BlockingCacheAltVRTL.v"
`include "lab4_net/BusNetVRTL.v" //Can be changed
`include "lab5_mcore/McoreDataCacheVRTL.v"
`include "lab5_mcore/MemNetVRTL.v"


//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include components
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab5_mcore_MultiCoreVRTL
(
  input  logic                       clk,
  input  logic                       reset,

  input  logic [c_num_cores-1:0][31:0] mngr2proc_msg,
  input  logic [c_num_cores-1:0]       mngr2proc_val,
  output logic [c_num_cores-1:0]       mngr2proc_rdy,

  output logic [c_num_cores-1:0][31:0] proc2mngr_msg,
  output logic [c_num_cores-1:0]       proc2mngr_val,
  input  logic [c_num_cores-1:0]       proc2mngr_rdy,

  output mem_req_16B_t                 imemreq_msg,
  output logic                         imemreq_val,
  input  logic                         imemreq_rdy,

  input  mem_resp_16B_t                imemresp_msg,
  input  logic                         imemresp_val,
  output logic                         imemresp_rdy,

  output mem_req_16B_t                 dmemreq_msg,
  output logic                         dmemreq_val,
  input  logic                         dmemreq_rdy,

  input  mem_resp_16B_t                dmemresp_msg,
  input  logic                         dmemresp_val,
  output logic                         dmemresp_rdy,

  //  Only takes Core 0's stats_en to the interface
  output logic                         stats_en,
  output logic [c_num_cores-1:0]       commit_inst,
  output logic [c_num_cores-1:0]       icache_miss,   // we need to cal
  output logic [c_num_cores-1:0]       icache_access, // we need to cal
  output logic [c_num_cores-1:0]       dcache_miss,
  output logic [c_num_cores-1:0]       dcache_access
);

  localparam c_num_cores = 4;


  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Instantiate modules and wires
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  mem_req_4B_t  [c_num_cores-1:0] proc2icache_req_msg;
  logic         [c_num_cores-1:0] proc2icache_req_val;
  logic         [c_num_cores-1:0] proc2icache_req_rdy;

  mem_resp_4B_t [c_num_cores-1:0] proc2icache_resp_msg;
  logic         [c_num_cores-1:0] proc2icache_resp_val;
  logic         [c_num_cores-1:0] proc2icache_resp_rdy;

  mem_req_4B_t  [c_num_cores-1:0] proc2dcache_req_msg;
  logic         [c_num_cores-1:0] proc2dcache_req_val;
  logic         [c_num_cores-1:0] proc2dcache_req_rdy;

  mem_resp_4B_t [c_num_cores-1:0] proc2dcache_resp_msg;
  logic         [c_num_cores-1:0] proc2dcache_resp_val;
  logic         [c_num_cores-1:0] proc2dcache_resp_rdy;

  logic         [c_num_cores-1:0] stats_en_4pro;

  mem_req_16B_t  [c_num_cores-1:0] icache2memnet_req_msg;
  logic          [c_num_cores-1:0] icache2memnet_req_val;
  logic          [c_num_cores-1:0] icache2memnet_req_rdy;

  mem_resp_16B_t [c_num_cores-1:0] icache2memnet_resp_msg;
  logic          [c_num_cores-1:0] icache2memnet_resp_val;
  logic          [c_num_cores-1:0] icache2memnet_resp_rdy;

  mem_req_16B_t                    mcoreDcache2mainmem_req_msg;
  logic                            mcoreDcache2mainmem_req_val;
  logic                            mcoreDcache2mainmem_req_rdy;

  mem_resp_16B_t                   mcoreDcache2mainmem_resp_msg;
  logic                            mcoreDcache2mainmem_resp_val;
  logic                            mcoreDcache2mainmem_resp_rdy;

  mem_req_16B_t  [c_num_cores-1:0] MemNet2mainmem_req_msg;
  logic          [c_num_cores-1:0] MemNet2mainmem_req_val;
  logic          [c_num_cores-1:0] MemNet2mainmem_req_rdy;

  mem_resp_16B_t [c_num_cores-1:0] MemNet2mainmem_resp_msg;
  logic          [c_num_cores-1:0] MemNet2mainmem_resp_val;
  logic          [c_num_cores-1:0] MemNet2mainmem_resp_rdy;

  genvar i;

  generate
    for ( i = 0; i < c_num_cores; i = i + 1 ) begin: processor_icaches

      lab2_proc_ProcAltVRTL #(c_num_cores) proc (
        .clk(clk)         ,
        .reset(reset)     ,
        .core_id(i[31:0]) ,
        .mngr2proc_msg(mngr2proc_msg[i]),
        .mngr2proc_val(mngr2proc_val[i]),
        .mngr2proc_rdy(mngr2proc_rdy[i]),

        .proc2mngr_msg(proc2mngr_msg[i]),
        .proc2mngr_val(proc2mngr_val[i]),
        .proc2mngr_rdy(proc2mngr_rdy[i]),

        .imemreq_msg(proc2icache_req_msg[i]),
        .imemreq_val(proc2icache_req_val[i]),
        .imemreq_rdy(proc2icache_req_rdy[i]),

        .imemresp_msg(proc2icache_resp_msg[i]),
        .imemresp_val(proc2icache_resp_val[i]),
        .imemresp_rdy(proc2icache_resp_rdy[i]),

        .dmemreq_msg(proc2dcache_req_msg[i]),
        .dmemreq_val(proc2dcache_req_val[i]),
        .dmemreq_rdy(proc2dcache_req_rdy[i]),

        .dmemresp_msg(proc2dcache_resp_msg[i]),
        .dmemresp_val(proc2dcache_resp_val[i]),
        .dmemresp_rdy(proc2dcache_resp_rdy[i]),

        .commit_inst(commit_inst[i]),
        .stats_en(stats_en_4pro[i])
      );
      //assign icache_miss[i] = icache2memnet_resp_rdy[i] && icache2memnet_resp_val[i] && (!proc2icache_resp_msg[i].test[0] ); // need to atention
      assign icache_miss[i] = proc2icache_resp_rdy[i] && proc2icache_resp_val[i] && (!proc2icache_resp_msg[i].test[0] ); // need to atention
      assign icache_access[i] = proc2icache_req_rdy[i] && proc2icache_req_val[i];
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Instantiate caches and connect them to cores
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
      lab3_mem_BlockingCacheAltVRTL icache (
        .clk(clk)         ,
        .reset(reset)     ,
        .cachereq_msg(proc2icache_req_msg[i]),
        .cachereq_val(proc2icache_req_val[i]),
        .cachereq_rdy(proc2icache_req_rdy[i]),

        .cacheresp_msg(proc2icache_resp_msg[i]),
        .cacheresp_val(proc2icache_resp_val[i]),
        .cacheresp_rdy(proc2icache_resp_rdy[i]),

        .memreq_msg(icache2memnet_req_msg[i]),
        .memreq_val(icache2memnet_req_val[i]),
        .memreq_rdy(icache2memnet_req_rdy[i]),

        .memresp_msg(icache2memnet_resp_msg[i]),
        .memresp_val(icache2memnet_resp_val[i]),
        .memresp_rdy(icache2memnet_resp_rdy[i])
      );
    end
  endgenerate
  // Only takes proc0's stats_en
  assign stats_en = stats_en_4pro[0];
  /*
  assign icache_miss[0] = icache2memnet_resp_val[0] & (icache2memnet_resp_msg[0].test[0] );
  assign icache_access[0] = icache2memnet_req_rdy[0] & icache2memnet_req_val[0];
  assign icache_miss[1] = icache2memnet_resp_val[1] & (icache2memnet_resp_msg[1].test[0] );
  assign icache_access[1] = icache2memnet_req_rdy[1] & icache2memnet_req_val[1];
  assign icache_miss[2] = icache2memnet_resp_val[2] & (icache2memnet_resp_msg[2].test[0] );
  assign icache_access[2] = icache2memnet_req_rdy[2] & icache2memnet_req_val[2];
  assign icache_miss[3] = icache2memnet_resp_val[3] & (icache2memnet_resp_msg[3].test[0] );
  assign icache_access[3] = icache2memnet_req_rdy[3] & icache2memnet_req_val[3];
  */
  lab5_mcore_McoreDataCacheVRTL   dcache (
    .clk(clk),
    .reset(reset),

    .procreq_msg(proc2dcache_req_msg),
    .procreq_val(proc2dcache_req_val),
    .procreq_rdy(proc2dcache_req_rdy),

    .procresp_msg(proc2dcache_resp_msg),
    .procresp_val(proc2dcache_resp_val),
    .procresp_rdy(proc2dcache_resp_rdy),

    .mainmemreq_msg(dmemreq_msg),
    .mainmemreq_val(dmemreq_val),
    //.mainmemreq_rdy(mcoreDcache2mainmem_req_rdy),
    .mainmemreq_rdy(dmemreq_rdy),

    //.mainmemresp_msg(mcoreDcache2mainmem_resp_msg),
    //.mainmemresp_val(mcoreDcache2mainmem_resp_val),
    .mainmemresp_msg(dmemresp_msg),
    .mainmemresp_val(dmemresp_val),
    .mainmemresp_rdy(dmemresp_rdy),

    .dcache_miss(dcache_miss),
    .dcache_access(dcache_access)

  );

  //assign dmemreq_msg = mcoreDcache2mainmem_req_msg;
  //assign dmemreq_val = mcoreDcache2mainmem_req_val;
  //assign dmemreq_rdy = mcoreDcache2mainmem_req_rdy;

  //assign dmemresp_msg = mcoreDcache2mainmem_resp_msg;
  //assign dmemresp_val = mcoreDcache2mainmem_resp_val;
  //assign dmemresp_rdy = mcoreDcache2mainmem_resp_rdy;

  lab5_mcore_MemNetVRTL           MemNet(
    .clk(clk),
    .reset(reset),
    .memreq_msg(icache2memnet_req_msg),
    .memreq_val(icache2memnet_req_val),
    .memreq_rdy(icache2memnet_req_rdy),

    .memresp_msg(icache2memnet_resp_msg),
    .memresp_val(icache2memnet_resp_val),
    .memresp_rdy(icache2memnet_resp_rdy),

    .mainmemreq_msg(MemNet2mainmem_req_msg),
    .mainmemreq_val(MemNet2mainmem_req_val),
    .mainmemreq_rdy(MemNet2mainmem_req_rdy),

    .mainmemresp_msg(MemNet2mainmem_resp_msg),
    .mainmemresp_val(MemNet2mainmem_resp_val),
    //.mainmemresp_msg(imemresp_msg),
    //.mainmemresp_val(imemresp_val),
    .mainmemresp_rdy(MemNet2mainmem_resp_rdy)
  );

  assign imemreq_msg = MemNet2mainmem_req_msg[0];
  assign imemreq_val = MemNet2mainmem_req_val[0];  //tested
  assign MemNet2mainmem_req_rdy[0] = imemreq_rdy;

  assign MemNet2mainmem_resp_msg[0] = imemresp_msg;
  assign MemNet2mainmem_resp_val[0] = imemresp_val;
  assign imemresp_rdy = MemNet2mainmem_resp_rdy[0];

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: hook up stats and add icache stats
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  `VC_TRACE_BEGIN
  begin

    // This is staffs' line trace, which assume the processors and icaches
    // are instantiated in using generate statement, and the data cache
    // system is instantiated with the name dcache. You can add net to the
    // line trace.
    // Feel free to revamp it or redo it based on your need.

    //processor_icaches[0].icache.line_trace( trace_str );
    processor_icaches[0].proc.line_trace( trace_str );
    //processor_icaches[1].icache.line_trace( trace_str );
    //processor_icaches[1].proc.line_trace( trace_str );
    //processor_icaches[2].icache.line_trace( trace_str );
    //processor_icaches[2].proc.line_trace( trace_str );
    //processor_icaches[3].icache.line_trace( trace_str );
    //processor_icaches[3].proc.line_trace( trace_str );

    dcache.line_trace( trace_str );
  end
  `VC_TRACE_END

endmodule

`endif /* LAB5_MCORE_MULTI_CORE_V */
