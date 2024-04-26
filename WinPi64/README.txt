Link to project download:
https://github.com/Xachaeus/WinPi64/releases/tag/v0.2.0-beta

Link to project repository (does not contain full project due to size restrictions):


WinPi64 is a project I developed for my class in Assembly to make it
easier to write my own assembly code. My class was taught in 64-bit
ARM assembly, and in order to write assembly for this architecture,
my university set up a small network of Raspberry Pis that students
could SSH into in order to do their coursework. This had several
drawbacks, however, as a constant and consistent internet connection 
was required to do work, and the Raspberry Pis (being very small and
not at all powerful computers) could barely keep up with all of the 
traffic and usage they were receiving. To remedy this, I built an
emulation system using the QEMU emulator tool so that I could 
simulate a 64-bit ARM architecture to write Assembly on. The tool
consists of the full QEMU (open-source) software required for ARM
emulation, a pre-formatted image of the Raspberry Pi OS Lite system
with the image size adjusted for QEMU and a username-password file
manually placed in the filesystem, other miscellanious files required
from the OS image by QEMU for the emulation (kernal images, etc.),
and a custom Python program I wrote to transfer files between the
host computer and the virtual machine.

As mentioned above, the OS image has to be modified in order to run
through QEMU, as the base image of Raspberry Pi OS (and its variants)
do not contain a default username and password by themselves. This
is added to the image when it is burned onto an SD card by the
Raspberry Pi imager, which adds whatever preset username and password
the user has entered to the image that it burns. However, because I 
was working on a Windows 10 PC, I could not natively mount the OS image 
to add the required file myself, because the image used an EXT4 
filesystem and Windows is built on NTFS. Instead, I created an Ubuntu
virtual machine with VirtualBox, mounted the image from within the VM,
and added the required username:hashed-password combination in the
necessary location. After adding some extra flags to my run script, the
emulator could run successfully and could even use the host machine's
internet connection, which was paramount to the functioning of my file
transfer program.

My file transfer program, written in Python, uses the SFTP suite of
tools to transfer files to and from the virtual machine while it is
running. This way, it is not necessary to create a second VM to mount
the EXT4 filesystem and exchange files, and the emulated Raspberry Pi
can be left running while file transfers happen. The program displays
all folders and files within the currently selected path on both 
machines, and allows the user to manually enter a new path (for either
the host machine or VM individually) directly, or click on the
folders/filenames displayed to navigate through the filesystems of both
machines. To transfer files, users can simply select the file in one
path, select the destination path on the other machine, and click the
"Quick Transfer to Host" or "Quick Transfer to Virtual Machine" button
to transfer the file from the source machine to the destination machine.
There are still some issues with this program; it doesn't allow the 
transfer of multiple files or folders (only individual files, one at a
time), and if the user has a file selected on both machines when they
try to perform a transfer, the transfer will possibly fail because the 
program will try to put the transferred file into the other file as if 
it were a folder. Luckily, this does not always and (and usually 
succeeds, though the file will not appear to have been transferred in
the program), but these issues will be addressed in future versions of
the software.