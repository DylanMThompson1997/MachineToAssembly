def converter(hex):
	binary = ""
	assembly = ""
	converter_dict = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}
	for digit in hex:
		binary += converter_dict[digit]
	op_code = binary[0:4]
	machine_code_dict = {'0001': 'ADD', '0101': 'AND', '0000': 'BR', '1100': 'JMP', '0100': 'JSR', '0010': 'LD', '1010': 'LDI', '0110': 'LDR', '1110': 'LEA', '1001': 'NOT', '1000': 'RTI', '0011': 'ST', '1011': 'STI', '0111': 'STR', '1111': 'TRAP', '1101': 'RESERVED'}
	assembly += machine_code_dict[op_code]
	return assembly, binary
	
def add_function(binary, assembly, registry_dict):
	#	0001(4b) DR(3b) SR1(3b) 000 SR2(3b)
	if binary[10] == '0':
		dest1 = binary[4:7]
		src1 = binary[7:10]
		src2 = binary[13:]
		dest1 = registry_dict[dest1]
		src1 = registry_dict[src1]
		src2 = registry_dict[src2]
		assembly += str(" " + dest1 + ",")
		assembly += str(src1+ ",")
		assembly += str(src2)
	if binary[10] == '1':
		dest1 = binary[4:7]
		src1 = binary[7:10]
		dest1 = registry_dict[dest1]
		src1 = registry_dict[src1]
		assembly += str(" " + dest1 + ",")
		assembly += str(src1+ ",")
		src2 = binary_to_decimal(binary[11:])
		assembly += str(src2)
	return assembly
	
def and_function(binary, assembly, registry_dict):
	#	0101(4b) DR(3b) SR1(3b) 000 SR2(3b)
	if binary[10] == '0':
		dest1 = binary[4:7]
		src1 = binary[7:10]
		src2 = binary[13:]
		dest1 = registry_dict[dest1]
		src1 = registry_dict[src1]
		src2 = registry_dict[src2]
		assembly += str(" " + dest1 + ",")
		assembly += str(src1+ ",")
		assembly += str(src2)
	if binary[10] == '1':
		dest1 = binary[4:7]
		src1 = binary[7:10]
		dest1 = registry_dict[dest1]
		src1 = registry_dict[src1]
		assembly += str(" " + dest1 + ",")
		assembly += str(src1+ ",")
		src2 = binary_to_decimal(binary[11:])
		assembly += str(src2)
	return assembly

def binary_to_decimal(binary):
	if binary[0] == '0':
		converted = 0
		if binary[1] == '1':
			converted += 8
		if binary[2] == '1':
			converted += 4
		if binary[3] == '1':
			converted += 2
		if binary[4] == '1':
			converted += 1
	if binary[0] == '1':
		one_comp = ""
		to_convert = binary[1:]
		for item in to_convert:
			if item == '0':
				one_comp += '1'
			elif item == '1':
				one_comp += '0'
		converted = 0
		if one_comp[0] == '1':
			converted += 8
		if one_comp[1] == '1':
			converted += 4
		if one_comp[2] == '1':
			converted += 2
		if one_comp[3] == '1':
			converted += 1
		converted += 1
		converted *= -1
	return converted
	
def binary_to_hex(binary):
	number = binary
	return number
	
def jmp_function(binary, assembly, registry_dict):
	#	1100(4b) 000(3b) SR(3b) 000000(6b)
	base_r = binary[7:10]
	base_r = registry_dict[base_r]
	assembly += str(" " + base_r)
	if binary[7:10] == '111':
		assembly = 'RET R7'
	return assembly
	
def br_function(binary, assembly, registry_dict):
	# 000(3b) n(1b) z(1b) p(1b) PCOffset9(9b)
	if binary[4] == '1':
		assembly += "N"
	if binary[5] == '1':
		assembly += "Z"
	if binary[6] == '1':
		assembly += "P"
	assembly += " "
	offset9 = binary_to_hex(binary[7:])
	assembly += str(offset9)
	return assembly

def jsr_function(binary, assembly, registry_dict):
	# 0100(4b) 1(1b) PCOffset11(11b)
	if binary[4] == '1':
		assembly += "R"
		assembly += " "
		offset11 = binary_to_hex(binary[5:])
		assembly += str(offset11)
	else:
		base_r = binary[7:10]
		base_r = registry_dict[base_r]
		assembly += str(" " + base_r)
	return assembly
	
def ld_function(binary, assembly, registry_dict):
	# 0010(4b) DR(3b) PCOffset9(9b)
	dest1 = binary[4:7]
	dest1 = registry_dict[dest1]
	assembly += str(" " + dest1 + ",")
	assembly += " "
	offset9 = binary_to_hex(binary[7:])
	assembly += str(offset9)
	return assembly
	
def ldi_function(binary, assembly, registry_dict):
	# 1010(4b) DR(3b) PCOffset9(9b)
	dest1 = binary[4:7]
	dest1 = registry_dict[dest1]
	assembly += str(" " + dest1 + ",")
	assembly += " "
	offset9 = binary_to_hex(binary[7:])
	assembly += str(offset9)
	return assembly
	
def ldr_function(binary, assembly, registry_dict):
	# 0110(4b) DR(3b) BaseR(3b) Offset6(6b) 
	dest1 = binary[4:7]
	dest1 = registry_dict[dest1]
	assembly += str(" " + dest1 + ",")
	base_r = binary[7:10]
	base_r = registry_dict[base_r]
	assembly += str(" " + base_r)
	assembly += " "
	offset6 = binary_to_hex(binary[10:])
	assembly += str(offset6)
	return assembly
	
def lea_function(binary, assembly, registry_dict):
	# 1110(4b) DR(3b) PcOffset9(9b)
	dest1 = binary[4:7]
	dest1 = registry_dict[dest1]
	assembly += str(" " + dest1 + ",")
	offset9 = binary_to_hex(binary[7:])
	assembly += str(offset9)
	return assembly
	
def not_function(binary, assembly, registry_dict):
	# 1001(4b) DR(3b) SR(3b) 111111(6b) 
	dest1 = binary[4:7]
	src1 = binary[7:10]
	dest1 = registry_dict[dest1]
	src1 = registry_dict[src1]
	assembly += str(" " + dest1 + ",")
	assembly += str(src1)
	return assembly

def st_function(binary, assembly, registry_dict):
	# 0011(4b) SR(3b) PcOffset9(9b) 
	src1 = binary[4:7]
	src1 = registry_dict[src1]
	assembly += str(" " + src1 + ",")
	offset9 = binary_to_hex(binary[7:])
	assembly += str(offset9)
	return assembly

def sti_function(binary, assembly, registry_dict):
	# 1011(4b) SR(3b) PcOffset9(9b) 
	src1 = binary[4:7]
	src1 = registry_dict[src1]
	assembly += str(" " + src1 + ",")
	offset9 = binary_to_hex(binary[7:])
	assembly += str(offset9)
	return assembly
	
def str_function(binary, assembly, registry_dict):
	# 0111(4b) SR(3b) BaseR(3b) Offset6(6b)
	src1 = binary[4:7]
	src1 = registry_dict[src1]
	assembly += str(" " + src1 + ",")
	base_r = binary[7:10]
	base_r = registry_dict[base_r]
	assembly += str(base_r + ",")
	offset6 = binary_to_hex(binary[10:])
	assembly += str(offset6)	
	return assembly

def trap_function(binary, assembly, registry_dict):
	# 1111(4b) 0000(4b) trapvect(8b)
	assembly += str(" " + binary[8:])
	return assembly
	
def display(hex):
	assembly, binary = converter(hex)
	registry_dict = {'000': 'R0', '001': 'R1', '010': 'R2', '011': 'R3', '100': 'R4', '101': 'R5', '110': 'R6', '111': 'R7'}
	if binary[0:4] == "0001":
		assembly = add_function(binary, assembly, registry_dict)
	if binary[0:4] == "0101":
		assembly = and_function(binary, assembly, registry_dict)
	if binary[0:4] == "1100":
		assembly = jmp_function(binary, assembly, registry_dict)
	if binary[0:4] == "0000":
		assembly = br_function(binary, assembly, registry_dict)
	if binary[0:4] == "0100":
		assembly = jsr_function(binary, assembly, registry_dict)
	if binary[0:4] == "0010":
		assembly = ld_function(binary, assembly, registry_dict)		
	if binary[0:4] == "1010":
		assembly = ldi_function(binary, assembly, registry_dict)
	if binary[0:4] == "0110":
		assembly = ldr_function(binary, assembly, registry_dict)
	if binary[0:4] == "1110":
		assembly = lea_function(binary, assembly, registry_dict)
	if binary[0:4] == "1001":
		assembly = not_function(binary, assembly, registry_dict)
	if binary[0:4] == "0011":
		assembly = st_function(binary, assembly, registry_dict)
	if binary[0:4] == "1011":
		assembly = sti_function(binary, assembly, registry_dict)
	if binary[0:4] == "0111":
		assembly = str_function(binary, assembly, registry_dict)
	if binary[0:4] == "1111":
		assembly = trap_function(binary, assembly, registry_dict)
	return assembly, binary

print(" ------- Machine Code to LC-3 Assembly ------- ")
print()
print(" ------------------- Menu: ------------------- ")
print(" 1. Save a full list of commands to a Text file.")
print(" 2. Print the command for a specific hex number.")
print(" --------------------------------------------- ")
full_architecture = []
output_file = open("LC-3_ISA.txt", "w")
constant = "000"
value_input = input(" Make a choice: ")
if value_input == "1":
	for value in range(0x0000, 0xffff):
		value = hex(value)
		value = str(value)
		value = value[2:]
		value = "000" + value
		value = value[-4:]
		assembly, binary = display(value)
		if assembly not in full_architecture:
			full_architecture.append(assembly)
			instruction = "{0} : {1}.\n" .format(binary, assembly)
			output_file.write(instruction)
	output_file.close()
elif value_input == "2":
	hex_num = input(" Enter a four-digit hex value: ")
	print(display(hex_num))
print(" --------------------------------------------- ")