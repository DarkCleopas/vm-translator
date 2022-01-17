
class CodeWriter:

    def __init__(self, file_path):

        self.file_path = f"{file_path}.hack"
        self.module_name = file_path.split("/")[-1].replace(".vm", "")
        self.func_name = ""
        self.label_count = 0
        self.call_count = 0
        self.return_sub_count = 0

        with open(self.file_path, "w") as f:
            f.write("")
    

    def write_line(self, line):

        with open(self.file_path, "a") as f:
            f.write(line + "\n")
    
    def segment_pointer(self, segment, index):
        if segment == "local":
            return "LCL"
        elif segment == "argument":
            return "ARG"
        elif segment == "this" or segment == "that":
            return segment.upper()
        elif segment == "temp":
            return f"R{5+index}"
        elif segment == "pointer":
            return f"R{3+index}"
        elif segment == "static":
            return f"{self.module_name}.{index}" 
        else:
            return "ERROR"

    def write_init(self):
        self.write_line("@256")
        self.write_line("D=A")
        self.write_line("@SP")
        self.write_line("M=D")
        self.write_call("Sys.init", 0)
        self.write_sub_rotine_return()
        self.write_sub_arithmetic_lt()
        self.write_sub_arithmetic_gt()
        self.write_sub_arithmetic_eq()
        self.write_sub_frame()


    def write_sub_frame(self):

        self.write_line("($FRAME$)")
        self.write_line("@R15")
        self.write_line("M=D")

        self.write_frame_push("LCL")
        self.write_frame_push("ARG")
        self.write_frame_push("THIS")
        self.write_frame_push("THAT")

        self.write_line("@R15")
        self.write_line("A=M")
        self.write_line("0;JMP")


    def write_sub_rotine_return(self):

        self.write_line("($RETURN$)")
        self.write_line("@R15")
        self.write_line("M=D")

        self.write_line("@LCL") # FRAME = LCL
        self.write_line("D=M")

        self.write_line("@R13") # R13 -> FRAME
        self.write_line("M=D")

        self.write_line("@5") # RET = *(FRAME-5)
        self.write_line("A=D-A")
        self.write_line("D=M")
        self.write_line("@R14") # R14 -> RET
        self.write_line("M=D")

        self.write_line("@SP") # *ARG = pop()
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@ARG")
        self.write_line("A=M")
        self.write_line("M=D")

        self.write_line("D=A") # SP = ARG+1
        self.write_line("@SP")
        self.write_line("M=D+1")

        self.write_line("@R13") # THAT = *(FRAME-1)
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@THAT")
        self.write_line("M=D")

        self.write_line("@R13") # THIS = *(FRAME-2)
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@THIS")
        self.write_line("M=D")

        self.write_line("@R13") # ARG = *(FRAME-3)
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@ARG")
        self.write_line("M=D")

        self.write_line("@R13") # LCL = *(FRAME-4)
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@LCL")
        self.write_line("M=D")

        self.write_line("@R14") # goto RET
        self.write_line("A=M")
        self.write_line("0;JMP")

        self.write_line("@R15")
        self.write_line("A=M")
        self.write_line("0;JMP")


    def write_sub_arithmetic_eq(self):

        self.write_line("($EQ$)")
        self.write_line("@R15")
        self.write_line("M=D")

        label = f"JEQ_{self.module_name}_{self.label_count}"
        self.write_line("@SP // eq")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@SP")
        self.write_line("AM=M-1")
        self.write_line("D=M-D")
        self.write_line("@" + label)
        self.write_line("D;JEQ")
        self.write_line("D=1")
        self.write_line("(" + label + ")")
        self.write_line("D=D-1")
        self.write_line("@SP")
        self.write_line("A=M")
        self.write_line("M=D")
        self.write_line("@SP")
        self.write_line("M=M+1")

        self.label_count += 1

        self.write_line("@R15")
        self.write_line("A=M")
        self.write_line("0;JMP")
    

    def write_sub_arithmetic_gt(self):

        self.write_line("($GT$)")
        self.write_line("@R15")
        self.write_line("M=D")

        label_true = f"JGT_TRUE_{self.module_name}_{self.label_count}"
        label_false = f"JGT_FALSE_{self.module_name}_{self.label_count}"

        self.write_line("@SP // gt")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@SP")
        self.write_line("AM=M-1")
        self.write_line("D=M-D")
        self.write_line("@" + label_true)
        self.write_line("D;JGT")
        self.write_line("D=0")
        self.write_line("@" + label_false)
        self.write_line("0;JMP")
        self.write_line("(" + label_true + ")")
        self.write_line("D=-1")
        self.write_line("(" + label_false + ")")
        self.write_line("@SP")
        self.write_line("A=M")
        self.write_line("M=D")
        self.write_line("@SP")
        self.write_line("M=M+1")

        self.label_count += 1

        self.write_line("@R15")
        self.write_line("A=M")
        self.write_line("0;JMP")


    def write_sub_arithmetic_lt(self):

        self.write_line("($LT$)")
        self.write_line("@R15")
        self.write_line("M=D")

        label_true = f"JLT_TRUE_{self.module_name}_{self.label_count}"
        label_false = f"JLT_FALSE_{self.module_name}_{self.label_count}"

        self.write_line("@SP // lt")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("@SP")
        self.write_line("AM=M-1")
        self.write_line("D=M-D")
        self.write_line("@" + label_true + "")
        self.write_line("D;JLT")
        self.write_line("D=0")
        self.write_line("@" + label_false + "")
        self.write_line("0;JMP")
        self.write_line("(" + label_true + ")")
        self.write_line("D=-1")
        self.write_line("(" + label_false + ")")
        self.write_line("@SP")
        self.write_line("A=M")
        self.write_line("M=D")
        self.write_line("@SP")
        self.write_line("M=M+1")

        self.label_count += 1

        self.write_line("@R15")
        self.write_line("A=M")
        self.write_line("0;JMP")
    

    def write_push(self, seg, index):

        if seg == "constant":
            self.write_line(f"@{index} // push {seg} {index}")
            self.write_line("D=A")
            self.write_line("@SP")
            self.write_line("A=M")
            self.write_line("M=D")
            self.write_line("@SP")
            self.write_line("M=M+1")
        elif seg == "static" or seg == "temp" or seg == "pointer":
            self.write_line(f"@{self.segmentPointer(seg, index)} // push {seg} {index}")
            self.write_line("D=M")
            self.write_line("@SP")
            self.write_line("A=M")
            self.write_line("M=D")
            self.write_line("@SP")
            self.write_line("M=M+1")
        elif seg == "local" or seg == "argument" or seg == "this" or seg == "that":
            self.write_line(f"@{self.segmentPointer(seg, index)} // push {seg} {index}")
            self.write_line("D=M")
            self.write_line(f"@{index}")
            self.write_line("A=D+A")
            self.write_line("D=M")
            self.write_line("@SP")
            self.write_line("A=M")
            self.write_line("M=D")
            self.write_line("@SP")
            self.write_line("M=M+1")
        else:
            pass
   
    
    def write_pop(self, seg, index):
        if seg == "static" or seg == "temp" or seg == "pointer":
            self.write_line(f"@SP // pop {seg} {index}")
            self.write_line("M=M-1")
            self.write_line("A=M")
            self.write_line("D=M")
            self.write_line(f"@{self.segmentPointer(seg, index)}")
            self.write_line("M=D")
        elif seg == "local" or seg == "argument" or seg == "this" or seg == "that":
            self.write_line(f"@{self.segmentPointer(seg, index)} // pop {seg} {index}")
            self.write_line("D=M")
            self.write_line(f"@{index}")
            self.write_line("D=D+A")
            self.write_line("@R13")
            self.write_line("M=D")
            self.write_line("@SP")
            self.write_line("M=M-1")
            self.write_line("A=M")
            self.write_line("D=M")
            self.write_line("@R13")
            self.write_line("A=M")
            self.write_line("M=D")
        else:
            pass


    def write_arithmetic(self, cmd):
        if cmd["name"] == "add":
            self.write_arithmetic_add()
        elif cmd["name"] == "sub":
            self.write_arithmetic_sub()
        elif cmd["name"] == "neg":
            self.write_arithmetic_neg()
        elif cmd["name"] == "eq":
            self.write_arithmetic_eq()
        elif cmd["name"] == "gt":
            self.write_arithmetic_gt()
        elif cmd["name"] == "lt":
            self.write_arithmetic_lt()
        elif cmd["name"] == "and":
            self.write_arithmetic_and()
        elif cmd["name"] == "or":
            self.write_arithmetic_or()
        elif cmd["name"] == "not":
            self.write_arithmetic_not()
        else:
            pass


    def write_binary_arithmetic(self):
        self.write_line("@SP")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("A=A-1")


    def write_arithmetic_add(self):
        self.write_binary_arithmetic()
        self.write_line("M=D+M")


    def write_arithmetic_sub(self):
        self.write_binary_arithmetic()
        self.write_line("M=M-D")


    def write_arithmetic_and(self):
        self.write_binary_arithmetic()
        self.write_line("M=D&M")


    def write_arithmetic_or(self):
        self.write_binary_arithmetic()
        self.write_line("M=D|M")


    def write_unary_arithmetic(self):
        self.write_line("@SP")
        self.write_line("A=M")
        self.write_line("A=A-1")


    def write_arithmetic_neg(self):
        self.write_unary_arithmetic()
        self.write_line("M=-M")


    def write_arithmetic_not(self):
        self.write_unary_arithmetic()
        self.write_line("M=!M")


    def write_arithmetic_eq(self):
        return_addr = f"$RET{self.return_sub_count}"
        self.write_line(f"@{return_addr}")
        self.write_line("D=A")
        self.write_line("@$EQ$")
        self.write_line("0;JMP")
        self.write_line(f"({return_addr})")
        self.return_sub_count += 1


    def write_arithmetic_gt(self):
        return_addr = f"$RET{self.return_sub_count}"
        self.write_line(f"@{return_addr}")
        self.write_line("D=A")
        self.write_line("@$GT$")
        self.write_line("0;JMP")
        self.write_line(f"({return_addr})")
        self.return_sub_count += 1


    def write_arithmetic_lt(self):
        return_addr = f"$RET{self.return_sub_count}"
        self.write_line(f"@{return_addr}")
        self.write_line("D=A")
        self.write_line("@$LT$")
        self.write_line("0;JMP")
        self.write_line(f"({return_addr})")
        self.return_sub_count += 1


    def write_label(self, label):

        new_label = f"{self.func_name}${label}"

        self.write_line("(" + new_label + ")")


    def write_goto(self, label):
        new_label = f"{self.func_name}${label}"
        self.write_line("@" + new_label)
        self.write_line("0;JMP")


    def write_if(self, label):

        new_label = f"{self.func_name}${label}"

        self.write_line("@SP")
        self.write_line("AM=M-1")
        self.write_line("D=M")
        self.write_line("M=0")
        self.write_line("@" + new_label)
        self.write_line("D;JNE")


    def write_function(self, func_name, n_locals):

        loop_label = func_name + "_INIT_LOCALS_LOOP"
        loop_end_label = func_name + "_INIT_LOCALS_END"

        self.func_name = func_name

        self.write_line("(" + func_name + ")" + "// initializa local variables")
        self.write_line(f"@{n_locals}")
        self.write_line("D=A")
        self.write_line("@R13") # temp
        self.write_line("M=D")
        self.write_line("(" + loop_label + ")")
        self.write_line("@" + loop_end_label)
        self.write_line("D;JEQ")
        self.write_line("@0")
        self.write_line("D=A")
        self.write_line("@SP")
        self.write_line("A=M")
        self.write_line("M=D")
        self.write_line("@SP")
        self.write_line("M=M+1")
        self.write_line("@R13")
        self.write_line("MD=M-1")
        self.write_line("@" + loop_label)
        self.write_line("0;JMP")
        self.write_line("(" + loop_end_label + ")")


    def write_frame_push(self, value):
        self.write_line("@" + value)
        self.write_line("D=M")
        self.write_line("@SP")
        self.write_line("A=M")
        self.write_line("M=D")
        self.write_line("@SP")
        self.write_line("M=M+1")


    def write_call(self, func_name, num_args):

        comment = f"// call {func_name} {num_args}"

        return_addr = f"{func_name}_RETURN_{self.call_count}"
        self.call_count += 1

        self.write_line(f"@{return_addr} {comment}") # push return-addr
        self.write_line("D=A")
        self.write_line("@SP")
        self.write_line("A=M")
        self.write_line("M=D")
        self.write_line("@SP")
        self.write_line("M=M+1")

        return_frame = f"$RET{self.return_sub_count}"
        self.write_line(f"@{return_frame}")
        self.write_line("D=A")
        self.write_line("@$FRAME$")
        self.write_line("0;JMP")
        self.write_line(f"({return_frame})")
        self.return_sub_count += 1

        self.write_line(f"@{num_args}") # ARG = SP-n-5
        self.write_line("D=A")
        self.write_line("@5")
        self.write_line("D=D+A")
        self.write_line("@SP")
        self.write_line("D=M-D")
        self.write_line("@ARG")
        self.write_line("M=D")

        self.write_line("@SP") # LCL = SP
        self.write_line("D=M")
        self.write_line("@LCL")
        self.write_line("M=D")

        self.write_line("@" + func_name)
        self.write_line("0;JMP")

        self.write_line("(" + return_addr + ")") # (return-address)


    def write_return(self):
        return_addr = f"$RET{self.return_sub_count}"
        self.write_line(f"@{return_addr}")
        self.write_line("D=A")
        self.write_line("@$RETURN$")
        self.write_line("0;JMP")
        self.write_line(f"({return_addr})")
        self.return_sub_count += 1



    	    

	