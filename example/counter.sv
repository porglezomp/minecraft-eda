module counter #(parameter WIDTH=3, parameter MAX=(1<<WIDTH)-1) (
    input clock,
    input reset,
    output logic [WIDTH-1:0] count,
    output logic max
);

assign max = count == MAX;

always_ff @(posedge clock) begin
    if (reset) count <= 0;
    else if (!max) count <= count + 1;
end

endmodule
