Link to N-TEA specifications: https://docs.google.com/document/d/1tEcc_vdRTd_nN5Cux7oWXvK_KLFdmpyIQ8oaS4kIMKE/edit?usp=sharing

Link to project preview: https://html-preview.github.io/?url=https://github.com/Xachaeus/Personal-Portfolio/blob/main/N-TEA/index.html

N-TEA (Non-Trivial Educational Architecture) began as a summer project to help me
build my understanding of computer architectures. The attatched HTML project includes
an assembler for writing N-TEA programs, a window to demonstrate the results of the
assembly process, a window to show the binary output, and an emulator that inteprets
that binary while simulating a 16-bit computing system.

The assembler takes a file written in specification-defined N-TEA assembly, and first
appends the source code for the OS to the beginning of the program. The assembly
instructions are then preprocessed, with comments being removed, constants defined in
binary or hexadecimal decoded, and Assembly instructions without hardware counterparts
expanded. Aliases are also replaced during this stage. The preprocessed assembly is
then run through a resolver, which replaces all label references in the program with
the constant values that are required for branching to occur properly. Finally, the
resolved assembly is translated one-to-one into its binary representation.

The simulated computer consists of 32 registers, 64 KiB of RAM, a specialized flag
register, and a 32-bit I/O bus. When a compiled binary program is to be run, it is
loaded into the beginning of memory, where the operating system code is run first.
Currently, the OS only handles launching the user-written program, allocating and
managing heap memory, and ending instruction execution once the program has finished.

Using the program is simple. First, write your assembly program in the top-left window.
Then, in order, press the pre-process, resolve, and assemble buttons, which execute each
step of the assembler. Finally, load the program to put the compiled binary into memory,
and then you can either increment through each step of the program (a window at the bottom
of the screen will show the next instruction to be executed, while another window shows the 
current value of each register as a signed 16-bit integer), or you can run the program as a 
whole, which will continue to execute instructions until the value 0xffff is placed in the 
16-bit bus. Note that an explicit end point must be specified in the program for this to
function as intended, or else the empty memory will be interpreted as instructions and the
program will run until the memory bounds are reached.
