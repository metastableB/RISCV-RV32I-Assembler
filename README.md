# RVI
A simple assembler for the `RV32I` instruction subset. This project in no sense is aimed at being a full assembler and the primary motive for developing this is so that it serves as an aid for the hardware development project we are doing. This assembler does not support any form of stack manipulation, space allocation and other essential features of any regular assembler and does not intend to support these 'essential' features in the near future. My primary motivation for building this assembler was to make one to one mappings between assembly level coding and the corresponding binary level coding. This is particularly useful when simulating or testing a new RV32I hardware design that only partially supports the instruction set.

Here you can perform the one to one mapping as well as see the tokenized values independently to verify whether your processor is treating the binary values as it ought to. Further, simple self contained programs can be run - those programs that do not assume a stack setup or a external call to its `main` or `start` label.

The assembler aims to allow for selectively turning off instruction and easily modify instruction opcodes - a feature currently not fully supported.

## Supported Instructions

|Sl. No| I Type| R Type | U Type | UJ Type| S Type| SB Type|
|------|-------|--------|--------|--------|-------|--------|
|1     |addi   |add     |lui     |jal     |sw     |beq     |
|2     |slti   |sub     |auipc   |        |sb     |bne     |
|3     |sltiu  |sll     |        |        |sh     |blt     |
|4     |ori    |slt     |        |        |       |bltu    |
|5     |xori   |sltu    |        |        |       |bge     |
|6     |andi   |xor     |        |        |       |bgeu    |
|7     |slli   |srl     |        |        |       |        |
|8     |srli   |sra     |        |        |       |        |
|9     |srai   |or      |        |        |       |        |
|10    |jalr   |and     |        |        |       |        |
|11    |lw     |        |        |        |       |        |
|12    |lb     |        |        |        |       |        |
|13    |lh     |        |        |        |       |        |
|14    |lbu    |        |        |        |       |        |
|15    |lhu    |        |        |        |       |        |


## Installation
### Windows

#### Step 1:
The assembler works on `Python3`. Please down the python3 installer for your machine from here.
#### Step 2:
The python package installed in the above should have installed a shell/command prompt. Open it up and `cd` to the `src/assembler` directory. Type 
(make sure you are in `src/assembler`)

    pip install -r requirements.txt

This will install some required libraries for the assembler to work. If the installation works without any error, you are done!


## Usage

In the simplest case, the usage is as follows. Open up the python shell and `cd` to the `src/assembler` directory. To assemble a input file `INP.rvi`, type

    $ python rvi.py INP.rvi

where the `.rvi` extension has no special meaning, and any type of file will actually do.

This will create a output file named `a.b` with the binary code. If you want to specify a custom output file name, please use the `-o OUTFILE` option as follows.

    $ python rvi.py INP.rvi -o OUTFILE

This will write the output to OUTFILE instead of `a.b`. 

By default, the output is written in binary - one instruction per line. If you want the output to be in hex rather than in binary, please use the `-x` flag as follows.

    $ python rvi.py -o OUTFILE -x INP.rvi

More options can be viewd in the below help text which you can obtaining by 

    $ python rvi.py -h


```
usage: rvi.py [-h] [-o OUTFILE] [-e] [-nc] [-n32] [-x] [-t] INFILE

RVI 0.1 - A simple RV32I assembler developed for testing RV32I targeted hardware
designs.

positional arguments:
  INFILE                Input file containing assembly code.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Output file name.
  -e, --echo            Echo converted code to console
  -nc, --no-color       Turn off color output.
  -n32, --no-32         Turn of 32 bit core warnings.
  -x, --hex             Output generated code in hexadecimal format instead of
                        binary.
  -t, --tokenize        Echo tokenized instructions to console for debugging.
```

## Programming in Assembly
The language I have codded for is similar to MIPS assembly and I have included some `samples/` for your perusal. Each statement should be in one line and the new line character is used to mark the end of a statement.

**WARNING** I have not tested how the assembler behaves in Windows line endings. I have tried to make sure this does not become a problem but in case you face any problem, please use an editor which supports UNIX file ending like *notepad++* or *sublimetext* and raise an issue regarding the same.

## TODO
- [X] In the parser, for each statement, check if all the tokens are valid
- [X] In parser, move immediate checking to different function (I Type)
- [X] recheck if the all type encoding is correct [PRIORITY]
- [ ] Write test suit
- [X] Support labels and label based jumps
- [ ] Test with windows
- [ ] Support turning on and off of instruction selectively
- [X] Implement `jalr`
- [ ] Implement remaining instructions
- [ ] Improve README
- [ ] Document installation instructions
- [ ] Support `include` directives

Don Dennis,
2016