/* Handed a hex code, reassemble into the appropriate assembly intruction */
/* DTHO410      817483811       CS210 Assignment 3 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

int add_and(int base);                  // Function declarations
int op_code_det(int base, int counter);
int jmp(int base);
int bin_hex_conv(int hex, int counter);
int immediate_addressing(int base);
int br(int base, int counter);
int direct_addressing(int base, int counter);

int add_and(base) {
    int dest = 0b0000111000000000, src1 = 0b0000000111000000, src2 = 0b000000000000000111, dir_addr = 0b0000000000100000, op_c = 0b1111000000000000;
    int direct_addr, dest_reg, src1_reg, src2_reg, opcode_r = 0;        // Initialise variables
    char assembly[50] = "";
    char string_print;
    dest_reg = base & dest;     // And operation to isolate specific bits in accordance with the initialised values above.
    src1_reg = base & src1;
    src2_reg = base & src2;
    direct_addr = base & dir_addr;
    opcode_r = base & op_c;
    if (opcode_r == 0b0001000000000000) {
        printf("add ");
    }
    else if (opcode_r == 0b0101000000000000) {      // Which of ADD or AND is relevant
        printf("and ");
    }
    printf("r%d,", dest_reg >> 9);                  // The destination register
    printf("r%d,", src1_reg >> 6);                  // The first source register
    if (direct_addr == 0b0000000000100000) {
        immediate_addressing(base);
    } else {
        printf("r%d\n", src2_reg);                  // The second source register
    }
    return 0;
}

int jmp(base) {
    int src = 0b0000000111000000;       // Relevant bits for JMP
    int src_reg;
    src_reg = base & src;               // Which register is src
    printf("jmp r%d\n", src_reg >> 6);
    return 0;
}

int br(base, counter) {
    int src = 0b1111000111111111;
    int src_reg;
    char assembly[50] = "br";
    src_reg = base | src;
    if (src_reg == 0b1111000111111111) { strcat(assembly, "r0"); }
    else if (src_reg == 0b1111100111111111) { strcat(assembly, "n "); }     // Decide which bits are selected and add n,z,p as appropriate
    else if (src_reg == 0b1111010111111111) { strcat(assembly, "z "); }
    else if (src_reg == 0b1111001111111111) { strcat(assembly, "p "); }
    else if (src_reg == 0b1111110111111111) { strcat(assembly, "nz "); }
    else if (src_reg == 0b1111101111111111) { strcat(assembly, "np "); }
    else if (src_reg == 0b1111011111111111) { strcat(assembly, "zp "); }
    else if (src_reg == 0b1111111111111111) { strcat(assembly, "nzp "); }
    strcat(assembly, "0x");
    printf("%s", assembly);
    direct_addressing(base, counter);
    return 0;
}


int op_code_det(base, counter) {
    int op_c = 0b1111000000000000;                     // Relevant bits for the op code
    int opcode_r = 0;
    opcode_r = base & op_c;
    if (opcode_r == 0b0001000000000000) { add_and(base); }         // add op code
    else if (opcode_r == 0b0101000000000000) { add_and(base); }    // and op code
    else if (opcode_r == 0b1100000000000000) { jmp(base); }        // jmp op code
    else if (opcode_r == 0b0000000000000000) { br(base, counter); }         // br op code
    else { printf("This is not a currently supported hex code.\n"); }
}

int bin_hex_conv(hex, counter) {
    int binary = 0b0;                   // Initialise empty binary number
    int bin_conv = binary | hex;        // convert existing hex number to binary through OR
    op_code_det(bin_conv, counter);              // pass on to determine the op code
    return 0;
}

int immediate_addressing(base) {
    int address_bits = 0b0000000000001111;      // Separate the four-bit number
    int negative = 0b0000000000010000;          // Use this to determine whether negative or not
    int number = address_bits & base;
    int n_check = negative & base;
    if (n_check == 0b0000000000010000) {
        number = number - 0b10000;              // Minus 16 if it's a negative
        printf("%d\n", number);
    } else {
        printf("%d\n", number);                 // print as decimal in either case
    }
    return 0;
}

int direct_addressing(base, counter) {
    int address_bits = 0b0000000011111111;      // Separate the nine-bit number
    int negative = 0b0000000100000000;          // Use this to determine whether negative or not
    int number = address_bits & base;
    int n_check = negative & base;
    if (n_check == 0b0000000100000000) {
        number = number - 0b100000000;              // Minus 256 if it's a negative
        number = number + (counter + 3000 - 50);
        printf("%d\n", number);
    } else {
        number = number + (counter + 3000 - 50);
        printf("%d\n", number);                 // print as decimal in either case
    }
    return 0;
}

int main(int argc, char *argv[]) {
    FILE *file;
    char line[20];
    int hex;
    int counter=0;
	if (argc != 3)
		printf("usage: %s File MemoryStartAddress\n", argv[0]);        // Check to make sure CLA is used corrrectly
	else {
	    file = fopen(argv[1], "r"); // open the file to read
	    counter = *argv[2];
        // read through each line of the file until the end of the file
        while (fscanf(file, "%x", &hex)!= EOF) { // Reads in a hex value (0xXXXX)
        bin_hex_conv(hex, counter);
        counter ++;
        }                    // Pass it on to the converter function
        fclose(file);
	}
	return 0;
}
