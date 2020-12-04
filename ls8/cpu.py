"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0    
        self.halted = False   
        

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a program into memory."""

        MAR = 0

        try:
            with open(filename) as program:
                for line in program:
                    comment_split = line.split("#")
                    try:
                        MDR = int(comment_split[0], 2)
                        self.ram_write(MDR, MAR)
                        MAR += 1
                    except:
                        continue
        except FileNotFoundError:
            print("File Not Found...")
            sys.exit(1)

        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while not self.halted:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            self.execute_instruction(IR, operand_a, operand_b)

    def execute_instruction(self, IR, operand_a, operand_b):
        number_of_operands = ((IR >> 6) & 0b11)

        branchtable = {
            LDI: self.handle_LDI,
            PRN: self.handle_PRN,
            HLT: self.handle_HLT,
            MUL: self.handle_MUL
        }

        if IR not in branchtable:
            print(f"Unknown instruction {IR}")
            self.halted = True
        else:         
            branchtable[IR](operand_a, operand_b)
            
        
        self.pc += number_of_operands + 1



    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
    
    def handle_PRN(self, operand_a, operand_b):
        print(self.reg[operand_a])

    def handle_HLT(self, operand_a, operand_b):
        self.halted = True
    
    def handle_MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)

    


        
