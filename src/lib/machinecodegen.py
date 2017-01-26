#
# @author:Don Dennis
# MachineCodeGen.py
#
# Conver the tokenized assembly instruction to
# corresponding machine code

from lib.cprint import cprint as cp
from lib.machinecodeconst import MachineCodeConst


class MachineCodeGenerator:
    CONST = MachineCodeConst()

    def __init__(self):
        '''
        Class that implements the machine code generation part
        for RV32I subset.
        '''
        pass

    def get_bin_register(self, r):
        '''
        converts the register in format
        r'[0-9][0-9]?' to its equivalent
        binary
        '''
        r = r[1:]
        try:
            r = int(r)
        except:
            cp.cprint_fail("Internal Error: get_bin_register:" +
                          " Register could not be parsed")
        assert(r >= 0)
        assert(r < 32)
        rbin = format(r, '05b')
        return rbin

    def op_lui(self, tokens):
        '''
        imm[31:12] rd opcode
        '''
        bin_opcode = None
        bin_rd = None
        rd = None
        imm = None

        try:
            bin_opcode = self.CONST.BOP_LUI
            rd = tokens['rd']
            bin_rd = self.get_bin_register(rd)
            imm = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: LUI: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm + bin_rd + bin_opcode
        assert(len(bin_str) == 32)

        tok_dict = {
            'opcode': bin_opcode,
            'rd': bin_rd,
            'imm': imm
        }
        return bin_str, tok_dict

    def op_auipc(self, tokens):
        '''
        imm[31:12] rd opcode
        '''
        bin_opcode = None
        bin_rd = None
        rd = None
        imm = None

        try:
            bin_opcode = self.CONST.BOP_AUIPC
            rd = tokens['rd']
            bin_rd = self.get_bin_register(rd)
            imm = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: AUIPC: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm + bin_rd + bin_opcode
        assert(len(bin_str) == 32)

        tok_dict = {
            'opcode': bin_opcode,
            'rd': bin_rd,
            'imm': imm
        }
        return bin_str, tok_dict

    def op_jal(self, tokens):
        '''
        imm[20] imm[10:1] imm[11] imm[19:12] rd opcode
        immediate is already shuffled in tokens
        '''
        bin_opcode = None
        bin_rd = None
        rd = None
        imm = None

        try:
            bin_opcode = self.CONST.BOP_JAL
            rd = tokens['rd']
            bin_rd = self.get_bin_register(rd)
            imm = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: AUIPC: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm + bin_rd + bin_opcode
        assert(len(bin_str) == 32)

        tok_dict = {
            'opcode': bin_opcode,
            'rd': bin_rd,
            'imm': imm
        }
        return bin_str, tok_dict

    def op_jalr(self, tokens):
        opcode = tokens['opcode']
        '''
        imm[11:0] rs1 funct3 rd opcode
        '''
        opcode = tokens['opcode']
        bin_opcode = None
        funct = None
        rs1 = None
        bin_rs1 = None
        bin_rd = None
        rd = None
        imm = None

        try:
            funct = self.CONST.FUNCT3_JALR[opcode]
            bin_opcode = self.CONST.BOP_JALR
            rs1 = tokens['rs1']
            bin_rs1 = self.get_bin_register(rs1)
            rd = tokens['rd']
            bin_rd = self.get_bin_register(rd)
            imm = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: JALR: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm + bin_rs1 + funct + bin_rd + bin_opcode
        assert(len(bin_str) == 32)

        if imm[-2:] != '00':
            cp.cprint_warn_32("32_Warning:" + str(tokens['lineno']) +
                              ": Missaligned address." +
                              " Address should be 4 bytes aligned.")

        tok_dict = {
            'opcode': bin_opcode,
            'funct': funct,
            'rs1': bin_rs1,
            'rd': bin_rd,
            'imm': imm
        }
        return bin_str, tok_dict

    def op_branch(self, tokens):
        '''
        imm[12|10:5] rs2 rs1 funct3 imm[4:1|11] opcode
        immediates returned in tokens as touple (imm_12_10_5, imm_4_1_11)
        '''
        opcode = tokens['opcode']
        imm_12_10_5 = None
        imm_4_1_11 = None
        funct3 = None
        rs1 = None
        rs2 = None
        bin_rs1 = None
        bin_rs2 = None
        try:
            funct3 = self.CONST.FUNCT3_BRANCH[opcode]
            bin_opcode = self.CONST.BOP_BRANCH
            rs1 = tokens['rs1']
            bin_rs1 = self.get_bin_register(rs1)
            rs2 = tokens['rs2']
            bin_rs2 = self.get_bin_register(rs2)
            imm_12_10_5, imm_4_1_11 = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: BRANCH: could not parse" +
                           " tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm_12_10_5 + bin_rs2 + bin_rs1 + funct3
        bin_str += imm_4_1_11 + bin_opcode
        if imm_4_1_11[-2] != '0':
            cp.cprint_warn_32("32_Warning:" + str(tokens['lineno']) +
                              ": Missaligned address." +
                              " Address should be 4 bytes aligned.")
        assert(len(bin_str) == 32)
        tok_dict = {
            'opcode': bin_opcode,
            'funct': funct3,
            'rs1': bin_rs1,
            'rs2': bin_rs2,
            'imm_12_10_5': imm_12_10_5,
            'imm_4_1_11': imm_4_1_11
        }

        return bin_str, tok_dict

    def op_load(self, tokens):
        opcode = tokens['opcode']
        '''
        imm[11:0] rs1 funct3 rd opcode
        '''
        opcode = tokens['opcode']
        bin_opcode = None
        funct3 = None
        rs1 = None
        bin_rs1 = None
        bin_rd = None
        rd = None
        imm = None

        try:
            funct3 = self.CONST.FUNCT3_LOAD[opcode]
            bin_opcode = self.CONST.BOP_LOAD
            rs1 = tokens['rs1']
            bin_rs1 = self.get_bin_register(rs1)
            rd = tokens['rd']
            bin_rd = self.get_bin_register(rd)
            imm = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: LOAD: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm + bin_rs1 + funct3 + bin_rd + bin_opcode
        assert(len(bin_str) == 32)

        if imm[-2:] != '00':
            cp.cprint_warn_32("32_Warning:" + str(tokens['lineno']) +
                              ": Missaligned address." +
                              " Address should be 4 bytes aligned.")

        tok_dict = {
            'opcode': bin_opcode,
            'funct': funct3,
            'rs1': bin_rs1,
            'rd': bin_rd,
            'imm': imm
        }
        return bin_str, tok_dict

    def op_store(self, tokens):
        '''
        imm[11:5] rs2 rs1 funct3 imm[4:0] opcode
        immediates returned in tokens as touple (imm_11_5, imm_4_0)
        '''
        opcode = tokens['opcode']
        imm_11_5 = None
        imm_4_0 = None
        funct3 = None
        rs1 = None
        bin_rs1 = None
        bin_rs2 = None
        rs2 = None
        try:
            funct3 = self.CONST.FUNCT3_STORE[opcode]
            bin_opcode = self.CONST.BOP_STORE
            rs1 = tokens['rs1']
            bin_rs1 = self.get_bin_register(rs1)
            rs2 = tokens['rs2']
            bin_rs2 = self.get_bin_register(rs2)
            imm_11_5, imm_4_0 = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: STORE: could not parse" +
                           " tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm_11_5 + bin_rs2 + bin_rs1 + funct3 + imm_4_0 + bin_opcode
        assert(len(bin_str) == 32)

        if imm_4_0[-2:] != '00':
            cp.cprint_warn_32("32_Warning:" + str(tokens['lineno']) +
                              ": Missaligned address." +
                              " Address should be 4 bytes aligned.")

        tok_dict = {
            'opcode': bin_opcode,
            'funct': funct3,
            'rs1': bin_rs1,
            'rs2': bin_rs2,
            'imm_11_5': imm_11_5,
            'imm_4_0': imm_4_0
        }

        return bin_str, tok_dict

    def op_arithi(self, tokens):
        '''
        imm[11:0]   rs1 funct3   rd  opcode

        The immediate for SLLI and SRLI needs to have the upper
        7 bets set to 0 and for SRAI, it needs to be set to
        0100000
        '''
        opcode = tokens['opcode']
        bin_opcode = None
        funct3 = None
        rs1 = None
        bin_rs1 = None
        bin_rd = None
        rd = None
        imm = None

        try:
            funct3 = self.CONST.FUNCT3_ARITHI[opcode]
            bin_opcode = self.CONST.BOP_ARITHI
            rs1 = tokens['rs1']
            bin_rs1 = self.get_bin_register(rs1)
            rd = tokens['rd']
            bin_rd = self.get_bin_register(rd)
            imm = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: ARITHI: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm + bin_rs1 + funct3 + bin_rd + bin_opcode
        assert(len(bin_str) == 32)

        if opcode in (self.CONST.INSTR_SLLI,
                      self.CONST.INSTR_SRLI):
            if imm[0:7] != '0000000':
                cp.cprint_warn("Warning:" + str(tokens['lineno']) +
                               ": Upper 7 bits of immediate should be 0")

        if opcode in (self.CONST.INSTR_SRAI):
            if imm[0:7] != '0100000':
                cp.cprint_warn("Warning:" + str(tokens['lineno']) +
                               ": Upper 7 bits of immediate should be " +
                               "01000000")

        tok_dict = {
            'opcode': bin_opcode,
            'funct3': funct3,
            'rs1': bin_rs1,
            'rd': bin_rd,
            'imm': imm
        }
        return bin_str, tok_dict

    def op_arith(self, tokens):
        '''
        funct7  rs2 rs1 funct3  rd  opcode
        '''
        opcode = tokens['opcode']
        bin_opcode = None
        funct3 = None
        funct7 = None
        rs1 = None
        rs2 = None
        rd = None
        bin_rs1 = None
        bin_rs2 = None
        bin_rd = None

        try:
            funct3 = self.CONST.FUNCT3_ARITH[opcode]
            funct7 = self.CONST.FUNCT7_ARITH[opcode]
            bin_opcode = self.CONST.BOP_ARITH
            rs1 = tokens['rs1']
            rs2 = tokens['rs2']
            rd = tokens['rd']
            bin_rs1 = self.get_bin_register(rs1)
            bin_rs2 = self.get_bin_register(rs2)
            bin_rd = self.get_bin_register(rd)
        except:
            cp.cprint_fail("Internal Error: ARITH: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = funct7 + bin_rs2 + bin_rs1 + funct3 + bin_rd + bin_opcode
        assert(len(bin_str) == 32)

        tok_dict = {
            'opcode': bin_opcode,
            'funct3': funct3,
            'funct7': funct7,
            'rs1': bin_rs1,
            'rd': bin_rd,
            'rs2': bin_rs2
        }
        return bin_str, tok_dict

    def convert_to_binary(self, tokens):
        '''
        The driver function for converting tokens to machine code.
        Takes the tokens parsed by the lexer and returns the
        binary equivalent.

        Returns a touple (instr, dict),
        where instr is the binary string of the instruction
        and the dict is the tokens converted individually
        '''
        try:
            opcode = tokens['opcode']
        except KeyError:
            print("Internal Error: Key not found (opcode)")
            return None

        if opcode in self.CONST.INSTR_BOP_LUI:
            return self.op_lui(tokens)
        elif opcode in self.CONST.INSTR_BOP_AUIPC:
            return self.op_auipc(tokens)
        elif opcode in self.CONST.INSTR_BOP_JAL:
            return self.op_jal(tokens)
        elif opcode in self.CONST.INSTR_BOP_JALR:
            return self.op_jalr(tokens)
        elif opcode in self.CONST.INSTR_BOP_BRANCH:
            return self.op_branch(tokens)
        elif opcode in self.CONST.INSTR_BOP_LOAD:
            return self.op_load(tokens)
        elif opcode in self.CONST.INSTR_BOP_STORE:
            return self.op_store(tokens)
        elif opcode in self.CONST.INSTR_BOP_ARITHI:
            return self.op_arithi(tokens)
        elif opcode in self.CONST.INSTR_BOP_ARITH:
            return self.op_arith(tokens)
        else:
            cp.cprint_fail("Error:" + str(tokens['lineno']) +
                           ": Opcode: '%s' not implemented" % opcode)
            return None

        print("Internal Error: Control should not reach here!")
        return None


mcg = MachineCodeGenerator()
