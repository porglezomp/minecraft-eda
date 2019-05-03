module counter #(parameter WIDTH=4) (
    input clock,
    input reset,
    input enable,
    output logic [WIDTH-1:0] count,
);

always_ff @(posedge clock) begin
    if (reset) count <= 0;
    else if (enable) count <= count + 1;
end

endmodule
