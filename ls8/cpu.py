"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110 
JMP = 0b01010100

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0x00    
        self.halted = False   
        
        self.stack_pointer_register = 7     
        self.reg[self.stack_pointer_register] = 0xF4
        self.end_of_stack = 0x00       
        

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a program into memory."""

        MAR = 0x00

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

        self.end_of_stack = MAR


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
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
            ADD: self.handle_ALU,
            MUL: self.handle_ALU,
            PUSH: self.handle_PUSH,
            POP: self.handle_POP,
            JMP: self.handle_JUMP
        }

        if IR not in branchtable:
            print(f"Unknown instruction {IR}")
            self.halted = True
        else:    
            if number_of_operands == 2:     
                branchtable[IR](operand_a, operand_b)
            elif number_of_operands == 1:
                branchtable[IR](operand_a)
            else:
                branchtable[IR]()
            
        if IR != JMP:
            self.pc += number_of_operands + 1



    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
    
    def handle_PRN(self, operand_a):
        print(self.reg[operand_a])

    def handle_HLT(self):
        self.halted = True
    
    def handle_ALU(self, operand_a, operand_b):
        IR = self.ram_read(self.pc)
        self.alu(IR, operand_a, operand_b)

    def handle_PUSH(self, operand_a):
        if self.reg[self.stack_pointer_register] - 1 < self.end_of_stack:
            print("STACK OVERFLOW! Exceeded maximum allocated space for the stack...")
            sys.exit(1)
        self.reg[self.stack_pointer_register] -= 1
        value_in_register = self.reg[operand_a]
        self.ram[self.reg[self.stack_pointer_register]] = value_in_register

    def handle_POP(self, operand_a):
        if self.reg[self.stack_pointer_register] < 0xF4:
            value_in_stack_pointer_register = self.ram[self.reg[self.stack_pointer_register]]
            self.reg[operand_a] = value_in_stack_pointer_register
            self.reg[self.stack_pointer_register] += 1
        else:
            print("STACK UNDERFLOW! Stack is empty...")
            sys.exit(1)
    
    def handle_JUMP(self, operand_a):
        address_to_jump_to = self.reg[operand_a]
        self.pc = address_to_jump_to

        
