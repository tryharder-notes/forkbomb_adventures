**rootybooty Write Up**

Source: https://rev-kids20.forkbomb.ru/tasks/RE7_rootybooty

Description: "/!\ Warning: it's a bad bad malware, run only on a virtual machine."

The description says that the binary contains some malicious functionality. First of all, I ran it in an isolated environment.

<img width="499" height="128" alt="изображение" src="https://github.com/user-attachments/assets/cd083206-c18a-4383-b437-1a0258709d91" />

At first the binary asked to run it as root and I decided that this could generally be done in an isolated environment. After I ran the binary again my virtual machine turned off.

Next I launched the binary in IDA and began analyzing the contents.

I immediately noticed the block with the string that I saw when I first launched the binary. Before this block there is a conditional transition in which the second branch goes to the main functionality of main().

<img width="1909" height="707" alt="изображение" src="https://github.com/user-attachments/assets/b2e47876-f418-405c-b7cc-31894ce0c885" />

I also noticed a reboot system call, which performs a reboot that prevents the flag from being received. The flag is encrypted and placed in the CRYPT() function, at the output of which the flag should, in theory, be printed in the terminal, but everything breaks off on reboot due to the reboot() system call.

<img width="1514" height="700" alt="изображение" src="https://github.com/user-attachments/assets/30000894-ac2f-4b1e-b7ac-d44bae0cebb4" />

There are only 2 links to reboot(). You can find these 2 calls and simply erase them with nop instructions.

<img width="690" height="191" alt="изображение" src="https://github.com/user-attachments/assets/9451c8f9-b8e7-4b26-9af7-e79d515a1c8d" />

I patched 10 bytes, launched it, and received a flag.

<img width="380" height="102" alt="изображение" src="https://github.com/user-attachments/assets/42a4c5ab-7a7d-479f-8e2c-5b0d21b7615c" />
