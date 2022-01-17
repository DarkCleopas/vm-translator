 
from CodeWriter import CodeWriter

with open("vm_example.vm", "r") as vm:
    vm_code = vm.readlines()

print(vm_code)

cw = CodeWriter("vm_example.vm")
cw.write_init()