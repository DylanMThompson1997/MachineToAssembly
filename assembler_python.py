def converter(hex):
	binary = ""
	assembly = ""
	converter_dict = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}
	for digit in hex:
		binary += converter_dict[digit]
	op_code = binary[0:4]
	machine_code_dict = {'0001': 'ADD', '0101': 'AND', '0000': 'BR', '1100': 'JMP'}
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
	return assembly
	
def br_function(binary, assembly, registry_dict):
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
	return assembly
	
print(display('1283'))
print(display('5105'))
print(display('0ffd'))
print(display('0802'))
print(display('1df7'))
print(display('506f'))
print(display('c080'))