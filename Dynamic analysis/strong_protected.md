**Strong Protected Write Up**

Source: https://rev-kids20.forkbomb.ru/tasks/RE5_sprotected
Description: "Figure out where the flag is"

First of all, I ran the binary to see what it was doing, but I didn't see any output in the terminal.

<img width="398" height="226" alt="изображение" src="https://github.com/user-attachments/assets/af965239-e5fd-462b-99d4-75202ec1d73c" />

It's time to open IDA and see what's inside the binary.

The initial function leads to the first function, which has a rather impressive size. And there are dozens of such functions in the binary.

<img width="1910" height="706" alt="изображение" src="https://github.com/user-attachments/assets/ff50fc98-46c3-4d84-aad3-06002bd87e3d" />

I tried to look for some hints of a flag in the lines and my search was immediately crowned with success.

<img width="1499" height="666" alt="изображение" src="https://github.com/user-attachments/assets/284e7bf4-3397-45e0-86b3-3dbabacdfbcd" />

This means the program creates a text file containing the flag in /tmp/flag.txt

But after executing the program, there is no flag in this directory, which means the program creates it and then deletes it.

And apparently it is necessary to set a breakpoint at the moment of execution where the file will already be created but will not be deleted yet. There are no references to this line, so it is difficult to say in which function this line is used. I tried to put a breakpoint on accessing this line in .rodata but after accessing this data the file still did not appear. Perhaps it is extracted from memory in one place and used in another, and therefore searching for this place manually may not be as effective as using the strace utility.

I tried to run straсe and look at the system calls. Here I saw part of the flag, but not all of it.

<img width="680" height="307" alt="изображение" src="https://github.com/user-attachments/assets/46700f41-555c-4d71-8d71-8fcce00e6b07" />

To see the rest I just used the -string-limit option.

<img width="698" height="301" alt="изображение" src="https://github.com/user-attachments/assets/2265b7fd-656a-4ced-9f1c-fe7051153f05" />

The flag has been received.
