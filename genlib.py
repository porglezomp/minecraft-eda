"""
Generate a cell library for redstone circuits
"""

import sys

CELLS = [
    (6,  {'Y': 'A'}),
    (6,  {'Y': '!A'}),
    (12, {'Y': 'A & B'}),
    (12, {'Y': '!(A & B)'}),
    (12, {'Y': 'A | B'}),
    (12, {'Y': '!(A | B)'}),
    (18, {'Y': 'A & B & C'}),
    (18, {'Y': '!(A & B & C)'}),
    (18, {'Y': 'A | B | C'}),
    (18, {'Y': '!(A | B | C)'}),
    (18, {'Y': '(A & B) | C'}),
    (18, {'Y': '(A & B) | !C'}),
    (18, {'Y': '!(A & B) | C'}),
    (18, {'Y': '!(A & B) | !C'}),
    (18, {'Y': '(A | B) & C'}),
    (18, {'Y': '!((A | B) & C)'}),
    (24, {'Y': 'A & B & C & D'}),
    (24, {'Y': '!(A & B & C & D)'}),
    (24, {'Y': 'A | B | C | D'}),
    (24, {'Y': '!(A | B | C | D)'}),
    (24, {'Y': '(A | B) & (C | D)'}),
    (24, {'Y': '!((A | B) & (C | D))'}),
    (24, {'Y': '(A & B) | (C & D)'}),
    (24, {'Y': '(A & B) | !(C & D)'}),
    (24, {'Y': '!(A & B) | !(C & D)'}),
    (24, {'Y': '!((A & B) | !(C & D))'}),
    (24, {'Y': '!(!(A & B) | (C & D))'}),
    (24, {'Y': '!(!(A & B) | !(C & D))'}),
    (24, {'Y': '(A | B) & C & D'}),
    (24, {'Y': '!((A | B) & C & D)'}),
    (24, {'Y': '(A | B) & (C | D)'}),
    (24, {'Y': '!((A | B) & (C | D))'}),
    """
cell(DFF_P) {
  area: 8;
  ff(IQ, IQN) { clocked_on: C; next_state: D; }
  pin(C) { direction: input; clock: true; }
  pin(D) { direction: input; }
  pin(Q) { direction: output; function: "IQ"; }
}
    """,
    """
cell(DFF_N) {
  area: 8;
  ff(IQ, IQN) { clocked_on: "!C"; next_state: D; }
  pin(C) { direction: input; clock: true; }
  pin(D) { direction: input; }
  pin(Q) { direction: output; function: "IQ"; }
}
    """,
]

def find_inputs(eqs):
    inputs = set()
    for eq in eqs.values():
        inputs.update(
            eq.replace('(', ' ').replace(')', ' ')
              .replace('&', ' ').replace('|', ' ')
              .replace('+', ' ').replace('*', ' ')
              .replace('!', ' ').split()
        )
    return inputs

def make_name(eqs):
    return ','.join(
        f"{x}={f.replace(' ', '').replace('|', '+')}"
        for x, f in eqs.items()
    )

def print_lib(lib, defns):
    print(f"library({lib}) {{")
    defined = {}
    for i, defn in enumerate(defns):
        if isinstance(defn, str):
            print('  ' + defn.strip().replace('\n', '\n  '))
        else:
            area, eqs = defn
            name = make_name(eqs)
            if name in defined:
                print(f"Warning: {name} defined at both {defined[name]} and {i}, skipping...", file=sys.stderr)
                continue
            defined[name] = i
            inputs = find_inputs(eqs)
            print(f"""  cell("{name}") {{""")
            print(f"""    area: {area};""")
            for pin in sorted(inputs):
                print(f"    pin({pin}) {{ direction: input; }}")
            for x, f in eqs.items():
                print(f"""    pin({x}) {{ direction: output; function: "{f}"; }}""")
            print("  }")
    print("}")

print_lib("redstone", CELLS)
