#
# @author:Don Dennis
# machinecodeconst.py
#
# Constants and variable declaring various
# machine instructions


class MachineCodeConst:
    # Definition of opcodes used in assembly language instructions
    INSTR_LUI = 'lui'
    INSTR_AUIPC = 'auipc'
    INSTR_JAL = 'jal'
    INSTR_JALR = 'jalr'
    INSTR_BEQ = 'beq'
    INSTR_BNE = 'bne'
    INSTR_BLT = 'blt'
    INSTR_BGE = 'bge'
    INSTR_BLTU = 'bltu'
    INSTR_BGEU = 'bgeu'
    INSTR_LB = 'lb'
    INSTR_LH = 'lh'
    INSTR_LW = 'lw'
    INSTR_LBU = 'lbu'
    INSTR_LHU = 'lhu'
    INSTR_SB = 'sb'
    INSTR_SH = 'sh'
    INSTR_SW = 'sw'
    INSTR_ADDI = 'addi'
    INSTR_SLTI = 'slti'
    INSTR_SLTIU = 'sltiu'
    INSTR_XORI = 'xori'
    INSTR_ORI = 'ori'
    INSTR_ANDI = 'andi'
    INSTR_SLLI = 'slli'
    INSTR_SRLI = 'srli'
    INSTR_SRAI = 'srai'
    INSTR_ADD = 'add'
    INSTR_SUB = 'sub'
    INSTR_SLL = 'sll'
    INSTR_SLT = 'slt'
    INSTR_SLTU = 'sltu'
    INSTR_XOR = 'xor'
    INSTR_SRL = 'srl'
    INSTR_SRA = 'sra'
    INSTR_OR = 'or'
    INSTR_AND = 'and'

    # All reserved opcodes
    ALL_INSTR = [INSTR_LUI, INSTR_AUIPC, INSTR_JAL,
                 INSTR_JALR, INSTR_BEQ, INSTR_BNE, INSTR_BLT,
                 INSTR_BGE, INSTR_BLTU, INSTR_BGEU, INSTR_LB,
                 INSTR_LH, INSTR_LW, INSTR_LBU, INSTR_LHU,
                 INSTR_SB, INSTR_SH, INSTR_SW, INSTR_ADDI,
                 INSTR_SLTI, INSTR_SLTIU, INSTR_XORI,
                 INSTR_ORI, INSTR_ANDI, INSTR_SLLI,
                 INSTR_SRLI, INSTR_SRAI, INSTR_ADD,
                 INSTR_SUB, INSTR_SLL, INSTR_SLT,
                 INSTR_SLTU, INSTR_XOR, INSTR_SRL,
                 INSTR_SRA, INSTR_OR, INSTR_AND
                 ]
    # All instruction in a type
    INSTR_TYPE_U = [INSTR_LUI, INSTR_AUIPC]
    INSTR_TYPE_UJ = [INSTR_JAL]
    INSTR_TYPE_S = [INSTR_SW, INSTR_SB, INSTR_SH]
    INSTR_TYPE_SB = [INSTR_BEQ, INSTR_BNE, INSTR_BLT,
                     INSTR_BLTU, INSTR_BGE, INSTR_BGEU]
    INSTR_TYPE_I = [INSTR_ADDI, INSTR_SLTI, INSTR_SLTIU,
                    INSTR_ORI, INSTR_XORI, INSTR_ANDI,
                    INSTR_SLLI, INSTR_SRLI, INSTR_SRAI,
                    INSTR_JALR, INSTR_LW, INSTR_LB,
                    INSTR_LH, INSTR_LBU, INSTR_LHU]
    INSTR_TYPE_R = [INSTR_ADD, INSTR_SUB, INSTR_SLL,
                    INSTR_SLT, INSTR_SLTU, INSTR_XOR,
                    INSTR_SRL, INSTR_SRA, INSTR_OR, INSTR_AND]

    # Binary Opcodes
    BOP_LUI = '0110111'
    BOP_AUIPC = '0010111'
    BOP_JAL = '1101111'
    BOP_JALR = '1100111'
    BOP_BRANCH = '1100011'
    BOP_LOAD = '0000011'
    BOP_STORE = '0100011'
    BOP_ARITHI = '0010011'
    BOP_ARITH = '0110011'
    # Not supported
    # [FENCE, FENCE.I]
    BOP_MISCMEM = '0001111'
    # [ ECALL, EBREAK, CSRRW, CSRRS, cSRRC, CSRRWI, CSRRSI, CSRRCI]
    BOP_SYSTEM = '1110011'

    # The instruction in each distinct binary opcode
    INSTR_BOP_LUI = [INSTR_LUI]
    INSTR_BOP_AUIPC = [INSTR_AUIPC]
    INSTR_BOP_JAL = [INSTR_JAL]
    INSTR_BOP_JALR = [INSTR_JALR]
    INSTR_BOP_BRANCH = [INSTR_BEQ, INSTR_BNE, INSTR_BLT,
                        INSTR_BLTU, INSTR_BGE, INSTR_BGEU]
    INSTR_BOP_LOAD = [INSTR_LW, INSTR_LB,
                      INSTR_LH, INSTR_LBU, INSTR_LHU]
    INSTR_BOP_STORE = [INSTR_SW, INSTR_SB, INSTR_SH]
    INSTR_BOP_ARITHI = [INSTR_ADDI, INSTR_SLTI, INSTR_SLTIU,
                        INSTR_ORI, INSTR_XORI, INSTR_ANDI,
                        INSTR_SLLI, INSTR_SRLI, INSTR_SRAI]
    INSTR_BOP_ARITH = [INSTR_ADD, INSTR_SUB, INSTR_SLL,
                       INSTR_SLT, INSTR_SLTU, INSTR_XOR,
                       INSTR_SRL, INSTR_SRA, INSTR_OR, INSTR_AND]

    # FUNCT for each instruction type
    FUNCT3_ARITHI = {
        INSTR_ADDI: '000',
        INSTR_SLTI: '010',
        INSTR_SLTIU: '011',
        INSTR_ORI: '110',
        INSTR_XORI: '100',
        INSTR_ANDI: '111',
        INSTR_SLLI: '001',
        INSTR_SRLI: '101',
        INSTR_SRAI: '101'
    }

    FUNCT3_JALR = {
        INSTR_JALR: '000'
    }

    FUNCT3_LOAD = {
        INSTR_LB: '000',
        INSTR_LH: '001',
        INSTR_LW: '010',
        INSTR_LBU: '100',
        INSTR_LHU: '101'
    }

    FUNCT3_ARITH = {
        INSTR_ADD: '000',
        INSTR_SUB: '000',
        INSTR_SLL: '001',
        INSTR_SLT: '010',
        INSTR_SLTU: '011',
        INSTR_XOR: '100',
        INSTR_SRL: '101',
        INSTR_SRA: '101',
        INSTR_OR: '110',
        INSTR_AND: '111'
    }

    FUNCT7_ARITH = {
        INSTR_ADD: '0000000',
        INSTR_SUB: '0100000',
        INSTR_SLL: '0000000',
        INSTR_SLT: '0000000',
        INSTR_SLTU: '0000000',
        INSTR_XOR: '0000000',
        INSTR_SRL: '0000000',
        INSTR_SRA: '0100000',
        INSTR_OR: '0000000',
        INSTR_AND: '0000000'
    }

    FUNCT3_STORE = {
        INSTR_SB: '000',
        INSTR_SH: '001',
        INSTR_SW: '010'
    }

    FUNCT3_BRANCH = {
        INSTR_BEQ: '000',
        INSTR_BNE: '001',
        INSTR_BLT: '100',
        INSTR_BGE: '101',
        INSTR_BLTU: '110',
        INSTR_BGEU: '111'
    }
