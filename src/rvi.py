#!/root/.virtualenv/btp/bin/python
# @author:Don Dennis
# rvi.py
#
# The RISC-V assembler for subset of instructions.

from lib.parser import parser
from lib.machinecodegen import mcg
from lib.cprint import cprint as cp
import argparse
from pprint import pprint


def get_arguments():
    descr = '''
    RVI -
    A simple RV32I assembler developed for testing
    RV32I targetted hardware designs.
    '''
    ap = argparse.ArgumentParser(description=descr)
    ap.add_argument("INFILE", help="Input file containing assembly code.")
    ap.add_argument('-o', "--outfile",
                    help="Output file name.", default = 'a.b')
    ap.add_argument('-e', "--echo", help="Echo converted code to console",
                    action="store_true")
    ap.add_argument('-nc', "--no-color", help="Turn off color output.",
                    action="store_true")
    ap.add_argument('-n32', "--no-32", help="Turn of 32 bit core warnings.",
                    action="store_true")
    ap.add_argument('-x', "--hex", action="store_true",
                    help="Output generated code in hexadecimal format" +
                    " instead of binary.")
    ap.add_argument('-t', '--tokenize', action="store_true",
                    help="Echo tokenized instructions to console" +
                    " for debugging.")
    args = ap.parse_args()
    return args


def main():
    args = get_arguments()
    infile = args.INFILE
    if args.no_color:
        cp.no_color = True
    if args.no_32:
        cp.warn32 = False
    fin = None
    try:
        fin = open(infile, 'r')
    except IOError:
        cp.cprint_fail("Error: File does not seem to exist or" +
                       " you do not have the required permissions.")
        return 1

    outfile = args.outfile
    fout = None
    try:
        fout = open(outfile, 'w')
    except IOError:
        cp.cprint_fail("Error: Could not create '" + outfile + "' for output")
        return 1

    for line in fin:
        result = parser.parse(line)
        instr = None
        if result:
            instr, instr_dict = mcg.convert_to_binary(result)
        if not instr:
            continue

        # Use hex instead of binary
        if args.hex:
            instr = '%08X' % int(instr, 2)
        # Echo to console
        if args.echo:
            cp.cprint_msgb(str(result['lineno']) + " " + str(instr))
        if args.tokenize:
            pprint(instr_dict)

        fout.write(instr + '\n')
    fout.close()
    fin.close()


if __name__ == '__main__':
    main()
