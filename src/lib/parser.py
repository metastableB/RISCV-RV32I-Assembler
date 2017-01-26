#
# @author:Don Dennis
# parser.py
#
# Parser for a simple assembler for subset of RV32I

import ply.yacc as yacc
import sys
# This is required by design
from lib.tokenizer import tokens
from lib.tokenizer import reset_lineno
from lib.machinecodegen import mcg
from lib.cprint import cprint as cp
from lib.machinecodeconst import MachineCodeConst
from pprint import pprint

mcc = MachineCodeConst()
'''
Grammar
-------
program: statement

statement: OPCODE register COMMA register COMMA register NEWLINE
        | OPCODE register COMMA register COMMA IMM_I NEWLINE
        | NEWLINE

NOTE: We parse the porgram line by line Hence we don't
need to recursively define the program interms of statements
'''


def p_program_statement(p):
    'program : statement'
    p[0] = {
        'type': 'non_label',
        'tokens': p[1]
    }


def p_program_label(p):
    'program : LABEL COLUMN NEWLINE'
    dict = {
        'label': p[1],
        'lineno': p.lineno(1)
    }
    p[0] = {
        'type': 'label',
        'tokens': dict
    }


def p_statement_R(p):
    'statement : OPCODE register COMMA register COMMA register NEWLINE'
    if p[1] not in mcc.INSTR_TYPE_R:
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ": Incorrect opcode or arguments")
        raise SyntaxError
    p[0] = {
        'opcode': p[1],
        'rd': p[2],
        'rs1': p[4],
        'rs2': p[6],
        'lineno': p.lineno(1)
    }


def p_statement_I_S_SB(p):
    'statement : OPCODE register COMMA register COMMA IMMEDIATE NEWLINE'
    if (p[1] not in mcc.INSTR_TYPE_I) and (p[1] not in mcc.INSTR_TYPE_S)and (p[1] not in mcc.INSTR_TYPE_SB):
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ": Incorrect opcode or arguments")
        raise SyntaxError
    elif p[1] in mcc.INSTR_TYPE_I:
        ret, imm, msg = get_imm_I(p[6], p.lineno(6))
        if not ret:
            cp.cprint_fail("Error:" + str(p.lineno(6)) + ":" + msg)
            raise SyntaxError

        p[0] = {
            'opcode': p[1],
            'rd': p[2],
            'rs1': p[4],
            'imm': imm,
            'lineno': p.lineno(1)
        }
    elif p[1] in mcc.INSTR_TYPE_S:
        ret, imm, msg = get_imm_S(p[6], p.lineno(6))
        if not ret:
            cp.cprint_fail("Error:" + str(p.lineno(1)) + ":" + msg)
            raise SyntaxError
        p[0] = {
            'opcode': p[1],
            'rs1': p[2],
            'rs2': p[4],
            'imm': imm,
            'lineno': p.lineno(1)
        }
    else:  # SB (BRANCH)
        ret, imm, msg = get_imm_SB(p[6], p.lineno(6))
        if not ret:
            cp.cprint_fail("Error:" + str(p.lineno(1)) + ":" + msg)
            raise SyntaxError
        p[0] = {
            'opcode': p[1],
            'rs1': p[2],
            'rs2': p[4],
            'imm': imm,
            'lineno': p.lineno(1)
        }


def p_statement_U_UJ(p):
    'statement : OPCODE register COMMA IMMEDIATE NEWLINE'

    if (p[1] not in mcc.INSTR_TYPE_U) and (p[1] not in mcc.INSTR_TYPE_UJ):
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ": Incorrect opcode or arguments")
        raise SyntaxError
    elif p[1] in mcc.INSTR_TYPE_U:
        ret, imm, msg = get_imm_U(p[4], p.lineno(4))
        if not ret:
            cp.cprint_fail("Error:" + str(p.lineno(1)) + ":" + msg)
            raise SyntaxError
        p[0] = {
            'opcode': p[1],
            'rd': p[2],
            'imm': imm,
            'lineno': p.lineno(1)
        }
    else:  # UJ Type
        ret, imm, msg = get_imm_UJ(p[4], p.lineno(4))
        if not ret:
            cp.cprint_fail("Error:" + str(p.lineno(1)) + ":" + msg)
            raise SyntaxError
        p[0] = {
            'opcode': p[1],
            'rd': p[2],
            'imm': imm,
            'lineno': p.lineno(1)
        }


def p_statement_UJ_LABEL(p):
    'statement : OPCODE register COMMA LABEL NEWLINE'

    if (p[1] not in mcc.INSTR_TYPE_UJ):
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ": Incorrect opcode or arguments")
        raise SyntaxError
    else:  # UJ Type
        p[0] = {
            'opcode': p[1],
            'rd': p[2],
            'label': p[4],
            'lineno': p.lineno(1)
        }


def p_statement_SB__JALR_LABEL(p):
    'statement : OPCODE register COMMA register COMMA LABEL NEWLINE'
    # Branch and JALR
    if (p[1] not in mcc.INSTR_TYPE_SB) and (p[1] != mcc.INSTR_JALR):
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ": Incorrect opcode or arguments")
        raise SyntaxError
    if p[1] in mcc.INSTR_TYPE_SB:
        p[0] = {
            'opcode': p[1],
            'rs1': p[2],
            'rs2': p[4],
            'label': p[6],
            'lineno': p.lineno(1)
        }
    elif p[1] == mcc.INSTR_JALR:
        p[0] = {
            'opcode': p[1],
            'rd': p[2],
            'rs1': p[4],
            'label': p[6],
            'lineno': p.lineno(1)
        }


def p_register(p):
    'register : REGISTER'
    r = p[1]
    r = r[1:]
    r = int(r)
    if (r < 0) or (r > 31):
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ":Invalid register index.")
        raise SyntaxError
    p[0] = p[1]


def p_statement_none(p):
    'statement : NEWLINE'
    p[0] = None


def get_imm_I(imm10, lineno):
    try:
        imm10 = int(imm10)
    except:
        msg = "Invalid immediate specified."
        return False, imm10, msg
    '''
    The I type immediates occur in all immediate arithmetic
    and logic operations, JALR, LW, LB, LH, LBU and LHU

    In the arithmetic/logic instructions, SLTUI is the only
    unsigned operation. Even in SLTUI, the immediate is
    sign extended first before an unsigned comparison is made
    hence for our purposes, the immediate is a signed 12 bit
    binary number.

    For JALR, the 12 bit immediate is sign extended and the CPU
    sets the lowest bit to 0 on its own before jumping. If a misaligned
    address is provided, it is the CPU's job to generate exceptions.
    Hence we check again for a 12 bit signed immediate.

    For LW, LB, LH, LBU and LHU, the address is a signed 12 bit
    number. Since the ISA allows misaligned loads, we need not check
    for alignment. Again, the CPU generates a misaligned instruction
    exception if required.

    Since I am generating a assembler for a 32 bit architecture, a warning
    is generated for misaligned loads in the binary generation phase.
    '''
    IMM_MAX = 0b011111111111
    IMM_MIN = -0b100000000000

    if (imm10 > IMM_MAX) or (imm10 < IMM_MIN):
        cp.cprint_warn("Warning:" + str(lineno) + ":" +
                       "Immediate is too big, will overflow.")
    # Conver to 2's complement binary
    imm2 = format(imm10 if imm10 >= 0 else (1 << 12) + imm10, '012b')
    imm2 = imm2[-12:]
    # Convert immediate back to base 10 from base 2
    # p[0] = int(imm2, 2)
    assert(len(imm2) == 12)
    return True, imm2, p_statement_none


def get_imm_U(imm10, lineno):
    try:
        imm10 = int(imm10)
    except:
        msg = "Invalid immediate specified."
        return False, imm10, msg
    '''
    The U type immediate occurs in LUI and AUIPC instructions.
    From the point of a compiler/assembler, there is nothing in
    particular that has to be checked about this immediate except
    that it fits into the 20 bit width.
    '''
    IMM_MAX = 0b01111111111111111111
    IMM_MIN = -0b10000000000000000000

    if (imm10 > IMM_MAX) or (imm10 < IMM_MIN):
        cp.cprint_warn("Warning:" + str(p.lineno(1)) + ":" +
                       "Immediate is too big, will overflow.")
    # Conver to 2's complement binary
    imm2 = format(imm10 if imm10 >= 0 else (1 << 20) + imm10, '020b')
    imm2 = imm2[-20:]
    # Convert immediate back to base 10 from base 2
    # p[0] = int(imm2, 2)
    assert(len(imm2) == 20)
    return True, imm2, None


def get_imm_UJ(imm10, lineno):
    try:
        imm10 = int(imm10)
    except:
        msg = "Invalid immediate specified."
        return False, imm10, msg
    '''
    The UJ Type immediate encodes a 2 byte aligned address.
    Hence its last bit has to be zero. We do not encode this
    last bit in the instruction and the CPU assumes the last
    bit to be zero.
    The immediate is reshuffled and looks like the following.

    imm[20] imm[10:1] imm[11] imm[19:12]
    Note that imm[0] is not encoded.

    From the parsers point of view, we accept an (21 bit) immediate
    check if its a multiple of 2 (report and error)
    and then shuffle it as required
    '''
    # Effectively we are addressing 21 bits
    IMM_MAX = 0b011111111111111111110
    IMM_MIN = -0b100000000000000000000

    if (imm10 > IMM_MAX) or (imm10 < IMM_MIN):
        cp.cprint_warn("Warning:" + str(lineno) + ":" +
                       "Immediate is too big, will overflow.")
    # Conver to 2's complement binary
    imm2 = format(imm10 if imm10 >= 0 else (1 << 21) + imm10, '021b')
    if imm2[-1:] != '0':
        cp.cprint_warn("Warning:" + str(lineno) + ":" +
                       "Immediate not 2 bytes aligned. Last bit will" +
                       "be dropped.")
    imm2 = imm2[0:-1]
    assert(len(imm2) == 20)
    # Shuffling the immediate
    # imm[20] imm[10:1] imm[11] imm[19:12]
    # Indexing in reverse order
    # imm[20] in is imm2[0] = imm2[-20] of imm string
    shf_imm = imm2[0] + imm2[10:20] + imm2[9] + imm2[1:9]
    assert(len(shf_imm) == 20)
    return True, shf_imm, None


def get_imm_S(imm10, lineno):
    try:
        imm10 = int(imm10)
    except:
        msg = "Invalid immediate specified."
        return False, imm10, msg
    '''
    The S type encodes instructions SW, SB and SH.
    Similar to loads, SW, SB and SH the address offset is a signed 12 bit
    number. Since the ISA allows misaligned stores, we need not check
    for alignment. Again, the CPU generates a misaligned instruction
    exception if required.

    Since I am generating a assembler for a 32 bit architecture, a warning
    is generated for misaligned stores in the binary generation phase.

    Also, in S type, the immediate is split into two parts - one part
    holding bits [11:5] in the immediate ordering(MSB-LSB from left to right)
    and the other part holding bits [4:0].
    We split the immediate into two portions hence.
    '''
    IMM_MAX = 0b011111111111
    IMM_MIN = -0b100000000000

    if (imm10 > IMM_MAX) or (imm10 < IMM_MIN):
        cp.cprint_warn("Warning:" + str(lineno) + ":" +
                       " Immediate is too big, will overflow.")
    # Convert to 2's complement binary
    imm2 = format(imm10 if imm10 >= 0 else (1 << 12) + imm10, '012b')
    if imm2[-1] != 0:
        cp.cprint_warn("Warning:" + str(lineno) + ":" +
                       "Immediate not 2 bytes aligned. Last bit will" +
                       "be dropped.")
    imm2 = imm2[0:12]
    # Convert immediate back to base 10 from base 2
    # p[0] = int(imm2, 2)
    assert(len(imm2) == 12)
    imm_11_5 = imm2[:7]
    imm_4_0 = imm2[7:]
    assert(len(imm_11_5) + len(imm_4_0) == 12)
    return True, (imm_11_5, imm_4_0), p_statement_none


def get_imm_SB(imm10, lineno):
    try:
        imm10 = int(imm10)
    except:
        msg = "Invalid immediate specified."
        return False, imm10, msg
    '''
    The SB type encodes instructions BEQ, BNE, BLT, BLTU, BGE, BGEU.
    The 12 bit immediate is encodes a signed offset in multiples of two.
    Hence the last bit will be 0 and we ignore this in the encoding
    effectively allowing encoding up to 13 bits.
    '''
    # 13 bit encoding
    IMM_MAX = 0b0111111111110
    IMM_MIN = -0b1000000000000

    if (imm10 > IMM_MAX) or (imm10 < IMM_MIN):
        cp.cprint_warn("Warning:" + str(lineno) + ":" +
                       "Immediate is too big, will overflow.")
    # Convert to 2's complement binary
    imm2 = format(imm10 if imm10 >= 0 else (1 << 13) + imm10, '013b')
    if imm2[-1] != '0':
        cp.cprint_warn("Warning:" + str(lineno) + ":" +
                       "Immediate not 2 bytes aligned. Last bit will" +
                       "be dropped.")
    imm2 = imm2[0:12]
    # Convert immediate back to base 10 from base 2
    # p[0] = int(imm2, 2)
    assert(len(imm2) == 12)
    imm_12_10_5 = imm2[-12] + imm2[-10:-4]
    imm_4_1_11 = imm2[-4:] + imm2[-11]
    assert(len(imm_12_10_5) + len(imm_4_1_11) == 12)
    return True, (imm_12_10_5, imm_4_1_11), None

'''
For this simple parser, I have not implemented error
recovery rules and I have decided to keep only the line
number for debugging errors.
'''


def p_error(p):
    lineno = ''
    if p:
        lineno = str(p.lineno)
        cp.cprint_fail("Error:" + lineno + ": Invalid or incomplete token" +
                       " found '" + str(p.value) + "'")
    else:
        cp.cprint_fail("Error: Invalid or incomplete token found " +
                       "Did you end with a newline?")


def encode_offset(ltokens, address, target):
    '''
    In instructions having label, this function calculates
    the value of the offset that has to be encoded inplace of the
    the label.
    It uses the current address of the instruction and the target address
    to calculate the difference and encode the offset in binary

    returns: immediate offset in binary
    '''
    # Offset address, should be divisible by 2 (2-byte aligned)
    offset = target - address
    assert(offset % 2 == 0)
    lineno = ltokens['lineno']
    if ltokens['opcode'] == mcc.INSTR_JAL:
        ret, imm, msg = get_imm_UJ(offset, lineno)
        if not ret:
            # Label translation should not raise errors,
            # Warnings make sense.
            cp.cprint_fail("Internal error:" +
                           str(tokens['lineno']) + ":" + msg)
            exit(1)
        result = {
            'opcode': ltokens['opcode'],
            'rd': ltokens['rd'],
            'imm': imm,
            'lineno': lineno
        }

    elif ltokens['opcode'] in mcc.INSTR_TYPE_SB:
        ret, imm, msg = get_imm_SB(offset, lineno)
        if not ret:
            cp.cprint_fail("Internal error:" + str(lineno) + ":" + msg)
            exit(1)
        result = {
            'opcode': ltokens['opcode'],
            'rs1': ltokens['rs1'],
            'rs2': ltokens['rs2'],
            'imm': imm,
            'lineno': lineno
        }
    elif ltokens['opcode'] == mcc.INSTR_JALR:
        ret, imm, msg = get_imm_I(offset, lineno)
        if not ret:
            cp.cprint_fail("Error:" + str(lineno) + ":" + msg)
            raise SyntaxError

        result = {
            'opcode': ltokens['opcode'],
            'rd': ltokens['rd'],
            'rs1': ltokens['rs1'],
            'imm': imm,
            'lineno': lineno
        }
    else:
        cp.cprint_fail("Error: " + str(lineno) + " : " +
                       "Label not supported in '" +
                       str(ltokens['opcode']) + "'")

    return result


parser = yacc.yacc()

'''
First pass of assembling:
Address and label resolution
'''


def parse_pass_one(fin, args):
    address = 0
    symbols_table = {}
    # Suppress instruction warnings
    prev_warn = cp.warn
    prev_warn32 = cp.warn32
    cp.warn = False
    cp.warn32 = False
    for line in fin:
        result = parser.parse(line)
        if result["tokens"] is None:
            continue

        if result['type'] is 'non_label':
            address += 4
            continue

        if not result['tokens']['label'] in symbols_table:
            symbols_table[result['tokens']['label']] = address
        else:
            cp.cprint_fail("Error: " + str(result['tokens']['lineno']) +
                           " : Redeclaration of label '" +
                           str(result['tokens']) + "'.")
            exit(1)
    # Restore warning state
    cp.warn = prev_warn
    cp.warn32 = prev_warn32
    if args['echo_symbols']:
        cp.cprint_msgb("Symbols and Addresses:")
        cp.cprint_msgb(str(symbols_table))
    return symbols_table


def parse_pass_two(fin, fout, symbols_table, args):
    fin.seek(0, 0)
    # Reset line number state
    reset_lineno()
    address = 0
    for line in fin:
        result = parser.parse(line)
        if result["tokens"] is None:
            continue

        if result['type'] is 'label':
            continue

        instr = None
        result = result['tokens']
        if 'label' in result:
            if result['label'] not in symbols_table:
                cp.cprint_fail("Error: " + str(result['lineno']) +
                               " : Label used but never defined '" +
                               str(result['label']) + "'.")
                exit(1)
            result = encode_offset(
                result, address, symbols_table[result['label']])
        if result:
            instr, instr_dict = mcg.convert_to_binary(result)
        if not instr:
            continue

        # Use hex instead of binary
        if args['hex']:
            instr = '%08X' % int(instr, 2)
        # Echo to console
        if args['echo']:
            cp.cprint_msgb(str(result['lineno']) + " " + str(instr))
        if args['tokenize']:
            cp.cprint_msgb(str(result['lineno']))
            pprint(instr_dict)

        fout.write(instr + '\n')
        address += 4


def parse_input(infile, **kwargs):
    if kwargs['no_color']:
        cp.no_color = True
    if kwargs['no_32']:
        cp.warn32 = False
    fin = None
    try:
        fin = open(infile, 'r')
    except IOError:
        cp.cprint_fail("Error: File does not seem to exist or" +
                       " you do not have the required permissions.")
        return 1

    outfile = kwargs['outfile']
    fout = None
    try:
        fout = open(outfile, 'w')
    except IOError:
        cp.cprint_fail("Error: Could not create '" + outfile + "' for output")
        return 1

    # Pass 1: Address resolution of labels
    symbols_table = parse_pass_one(fin, kwargs)
    # Pass 2: Mapping instructions to binary coding
    parse_pass_two(fin, fout, symbols_table, kwargs)
    fout.close()
    fin.close()


def main():
    if len(sys.argv) <= 1:
        exit("Error: No file specified")
    fin = None
    try:
        fin = open(sys.argv[1], 'r')
    except IOError:
        cp.cprint_fail("File does not seem to exist or" +
                       " you do not have the required permissions.")
        return 1

    for line in fin:
        result = parser.parse(line)
        if result:
            print(result)


if __name__ == '__main__':
    main()
