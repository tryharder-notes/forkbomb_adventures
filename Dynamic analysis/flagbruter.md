**Flagbruiter Write Up**

Source: https://forkbomb.ru/tasks/RE5_flagbruter
Description: "Sometimes the string variable contains flag. Most of times not"

First, I opened IDA to analyze the code decompiled by Hex-Rays.

<img width="886" height="618" alt="изображение" src="https://github.com/user-attachments/assets/17eb6acc-4a7c-41af-bf98-a05299d9174a" />

Well, nothing special. Some variables are initialized, followed by a loop with 99,999 iterations. At the end of each round the "dest" array receives 23 bytes of data and the next round begins. The "dest" array receives data from the "src" array which is populated with values in a while() loop. The "v8" is an array containing three hexadecimal integers that are XORed with the result of the yahoo() function. The resulting value is then stored in the 'src' array until it is completely filled.

There is no need to analyze further because the flag clearly appears in the 'src' array and is transferred to the 'dest' array. The flag is 23 bytes (or 23 characters) long. The key question is: during which loop iteration does the flag appear?

I can try to monitor the contents of the "dest" array. I set a breakpoint on line 30 and set up a remote debug server for remote debugging.

<img width="1904" height="432" alt="изображение" src="https://github.com/user-attachments/assets/e58c45a2-0021-46a9-8100-b651328c578c" />

The "dest" stores raw bytes, a subset of which are ascii-chars.

I can try all 99,999 iterations to find the flag manually, but that's a bad strategy because it takes a lot of time.

This process needs to be automated. First of all, it can be assumed that if I intercept a string, then all 23 bytes should lie within the range from 0x0 to 0x7f inclusive, which simplifies my task - now I know by what criterion I can filter out the results obtained at each iteration.

Next question: "How to do it by IDA?"

The breakpoint condition and IDAPython can help me with it.

The breakpoint condition is a pretty handy feature of breakpoints and it consists in the fact that I can define some condition, upon fulfillment of which the breakpoint will work. Accordingly, if the condition is not fulfilled, the breakpoint will not work.

This is all done in the "Breakpoints" window, I select the desired "breakpoint" with the mouse and click "Edit" in the menu, or press the hotkey Ctrl+E:

<img width="1320" height="475" alt="изображение" src="https://github.com/user-attachments/assets/64f1c87a-eb47-483f-9f78-83f6151ee452" />
<img width="626" height="478" alt="изображение" src="https://github.com/user-attachments/assets/d3c8e3e4-585c-4782-844e-00499a903701" />

Next, in a window like this, I click '...' and the script editor opens.

<img width="957" height="809" alt="изображение" src="https://github.com/user-attachments/assets/b1778599-3c91-43ca-b0ab-10248c29c2b2" />

Don't forget to change the script language from IDC to Python. This is where I can write my condition.

Every time the program execution reaches the breakpoint I set with a condition, the condition script will be executed and if the script ultimately returns True, then the breakpoint will work, if False, then the breakpoint will not work.

Now, I need to think about how to take this frame with the string. Since the variable addresses will change every time I run the program, I will take the stack top address from the RSP register, and then I will count a certain offset from this address to get the address of the beginning of the "dest" array. In this way, I will get the address of the beginning of the dest array every time, since the offset does not change.

I go to the main() stack and look where dest is located:

<img width="764" height="642" alt="изображение" src="https://github.com/user-attachments/assets/8f906224-47e5-4b93-9468-0d592972f2b4" />

So I get a 40 byte offset from the address that will be in the RSP register at the time of main() execution.

Now I'll check how it works:

<img width="1096" height="796" alt="изображение" src="https://github.com/user-attachments/assets/7215c69b-e43c-482d-b887-cff04ac7891c" />

I'll put a breakpoint without conditions on the same line 30 and execute the following script. As a result, I should get the address of the beginning of the array dest in the console:

<img width="1120" height="125" alt="изображение" src="https://github.com/user-attachments/assets/260aac4b-b756-4f48-a172-f561e653438d" />

Now let's see where the "dest" array is:

<img width="1264" height="828" alt="изображение" src="https://github.com/user-attachments/assets/d291e0c2-72fd-4c47-96e0-122b83f7fb41" />

As you can see, the values match, which means I did everything correctly.

And here you need to be very careful with which register you are looking at. RSP is a register for x64, so the address length there will be limited to 8 bytes or 64 bits.

But if you specify in the script for idaapi.get_reg_val() not RSP but ESP - a 32-bit register, then you will get an incomplete address, limited to 4 bytes or 32 bits. And thus, instead of 0x7fff4faa39a0 I could get 0x4faa39a0:

<img width="1704" height="961" alt="изображение" src="https://github.com/user-attachments/assets/e5fddfa5-0b2c-46cc-bff9-d09a8ba6c45f" />

Now that I have decided on finding the address of the beginning of the dest array and how I will filter the results obtained, let's put a breakpoint on line 28, right after the memcpy() function, and write a script to trigger the breakpoint:

<img width="959" height="809" alt="изображение" src="https://github.com/user-attachments/assets/3beeb376-f44b-4dcc-8002-8483b3ad2bc1" />

I launch the program and now I can step away for 10 minutes, when the string I'm looking for appears in dest, the "breakpoint" will work and I'll see a flag in the console:

<img width="1359" height="864" alt="изображение" src="https://github.com/user-attachments/assets/98cf6a35-1af3-4cef-a631-36013f868a14" />
