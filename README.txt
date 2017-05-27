# Machine_to_Assembly
Converts a hex machine code instruction into LC-3 Assembly language.

In the C version:
Given a filename and memory address as a Command-Line argument, the program will read hex codes from the specified file.
If the code it reads is one it knows how to deal with, it will convert it into an LC-3 assembly instruction.
   Eg. 0x1283 would become ADD R1,R2,R3
This program only works for ADD, AND, JMP and BR instructions, and will know that there is a code it cannot deal with for the others.

In the Python version:
Adjust the numbers that are passed to the display() function, down the bottom of the code. 
So far, this is complete except for direct addressing in Branch instructions.
