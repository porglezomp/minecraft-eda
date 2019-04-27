synth: example/counter.ys minecraft.lib example/counter.sv
	yosys $<

minecraft.lib: genlib.py
	python3 $< > $@
