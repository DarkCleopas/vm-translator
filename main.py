 
from CodeWriter import CodeWriter
from Parser import Parser

# with open("vm_example.vm", "r") as vm:
#     vm_code = vm.readlines()

# print(vm_code)

# cw = CodeWriter("vm_example.vm")
# cw.write_init()

ARITHMETICS = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]


def translate(path, code: CodeWriter):

    p = Parser(path)
    
    while p.has_more_commands():

        command = p.get_command()

        if command[0] == "push":

            code.write_push(command[1], command[2])

        elif command[0] in ARITHMETICS:

            code.write_arithmetic(command)

        elif command[0] == "pop":
            
            code.write_pop(command[1], command[2])
        
        elif command[0] == "label":
            
            code.write_label(command[1])

        elif command[0] == "goto":

            code.write_goto(command[1])

        elif command[0] == "if-goto":

            code.write_if(command[1])

        elif command[0] == "return":

            code.write_return()

        elif command[0] == "call":

            code.write_call(command[1], command[2])

        elif command[0] == "function":

            code.write_function(command[1], command[2])

        else:
            
            print('Command unexpected', command)


def main():

    path = "vm_example.vm"

    code = CodeWriter(path)

    translate(path, code)


if __name__ == "__main__":

    main()