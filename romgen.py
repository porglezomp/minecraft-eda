import argparse
import sys

base = [
    (0, 0,-1, 'stone_slab[type=top]'),
    (0, 1,-1, 'stone_slab[type=top]'),
    (0, 2,-1, 'stone_slab[type=top]'),
    (0, 0, 0, 'air'),
    (0, 1, 0, 'air'),
    (0, 2, 0, 'air'),
    (1, 1, 0, 'stone'),
    (2, 1, 1, 'stone'),
    (2, 2, 1, 'stone'),
    (3, 2, 1, 'stone_slab[type=top]'),
    (1, 2, 2, 'stone'),
]
redstone = [
    (0, 0, 0, 'redstone_wire[north=side,south=side]'),
    (0, 1, 0, 'redstone_wire[east=up,north=side,south=side]'),
    (0, 2, 0, 'redstone_wire[north=side,south=side]'),
    (1, 1, 1, 'redstone_wire[east=up,west=side]'),
    (2, 1, 2, 'redstone_wire[north=none,east=none,south=side,west=side]'),
    (2, 2, 2, 'redstone_wire[north=side,east=side,south=none,west=up]'),
    (3, 2, 2, 'redstone_wire[north=none,east=side,south=none,west=side]'),
    (1, 2, 3, 'redstone_wire[north=none,east=side,south=none,west=side]'),
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate a ROM cell of specified dimensions and contents",
    )
    parser.add_argument(
        '-w', '--width', required=True, type=int,
        help="the number of bits in a word",
    )
    parser.add_argument(
        '-d', '--depth', required=True, type=int,
        help="the number of bits in an address",
    )
    parser.add_argument(
        '-D', '--data', required=True,
        help="the value to initialize the memory to, formatted as a .hex file",
    )
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    words = 2 ** args.depth
    offset = 3 * args.depth + 1
    data = [0] * words
    limit = 2 ** args.width - 1
    with open(args.data, 'r') as f:
        for i, line in enumerate(f):
            if i >= words:
                print(f"Warning: Truncating '{args.data}' to {words} words", file=sys.stderr)
                break
            try:
                val = int(line, 16)
            except:
                print(f"Error: invalid hex on line {i} ({line})", file=sys.stderr)
                sys.exit(1)
            data[i] = val
            if val > limit:
                print(
                    f"Error: hex out of bounds on line {i} ({val:x} > {limit:x})",
                    file=sys.stderr,
                )
                sys.exit(1)
    for word in range(words):
        y0 = word * 3
        for bit in range(args.depth):
            x0 = bit * 3
            for x, y, z, block in base:
                print(x0 + x, y0 + y, z, block)
        for bit in range(args.width):
            x0 = 2 * bit + offset
            print(x0 + 0, y0 + 2, 1, 'stone')
            print(x0 + 1, y0 + 2, 1, 'stone')
    for word in range(words):
        y0 = word * 3
        for bit in range(args.depth):
            x0 = bit * 3
            for x, y, z, block in redstone:
                print(x0 + x, y0 + y, z, block)
        for bit in range(args.width):
            x0 = 2 * bit + offset
            if bit % 8 == 0:
                print(x0 - 1, y0 + 2, 2, 'repeater[facing=west]')
            print(x0 + 0, y0 + 2, 2, 'redstone_wire[east=side,west=side]')
            print(x0 + 1, y0 + 2, 2, 'redstone_wire[east=side,west=side]')
    for bit in range(args.depth):
        x0 = 3 * bit
        print(x0, -1, 0, 'redstone_wire[north=up,south=side]')
        print(x0, -2, 1, 'redstone_wire[north=side,south=side]')
        print(x0, -3, 1, 'redstone_wire[north=side,south=side]')
    for word in range(words):
        y0 = 3 * word
        for bit in range(args.depth):
            x0 = 3 * bit
            if word & (1 << bit):
                print(x0 + 2, y0 + 1, 2, 'redstone_torch')
            else:
                print(x0 + 2, y0 + 1, 1, 'glass')
            if bit % 2 == 1:
                print(x0 + 3, y0 + 2, 2, 'repeater[facing=west]')
            if word % 3 == 0:
                print(x0, y0, 0, 'repeater[facing=north]')
        for bit in range(args.width):
            x0 = 2 * bit + offset
            if data[word] & (1 << bit):
                print(x0 + 0, y0 + 1, 1, 'redstone_wall_torch')
    for bit in range(args.width):
        x0 = 2 * bit + offset
        print(x0, -3, 1, 'redstone_wire[north=side,south=side]')
        print(x0, -2, 1, 'redstone_wire[north=side,south=side]')
        for y0 in range(-1, 3 * words + 1):
            print(x0, y0, -1, 'stone_slab[type=top]')
            if y0 % 15 == 2:
                print(x0, y0, 0, 'repeater[facing=south]')
            else:
                print(x0, y0, 0, 'redstone_wire[north=side,south=side]')
