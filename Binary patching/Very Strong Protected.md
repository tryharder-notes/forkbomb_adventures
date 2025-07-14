**"Very Strong Protected" Write Up**

Source: https://rev-kids20.forkbomb.ru/tasks/RE7_very_strong_protected
No description.

This task is very similar to "Strong Protected" and is generally its logical continuation. This time everything is the same, but plus to everything is added anti-debugging, which does not allow to use strace utility as in that task.

If I try to track system outputs through straсe utility, I get the following output:

<img width="680" height="280" alt="изображение" src="https://github.com/user-attachments/assets/147f71c7-8751-4b6f-b18a-62630541143a" />

The message seems to hint that debugging will not help here and therefore it is necessary to bypass anti-debugging.

I opened IDA and tried to find the line that the program outputs.

<img width="1875" height="675" alt="изображение" src="https://github.com/user-attachments/assets/b9d63941-56c5-4448-9cf7-e3c246f81d4a" />

There is such a line and there is a link to it. By clicking on it you can see a conditional transition leading to this message.

<img width="1276" height="516" alt="изображение" src="https://github.com/user-attachments/assets/2ddc622e-d2bc-4959-a7aa-786c197c2904" />

I have highlighted 2 bytes that interest me the most. Here it is enough to change jnz instruction to jz instruction so that the program's behavior changes and when it is launched through strace utility I get a flag.

I patched the program, ran it through strace utility and got the flag.

<img width="728" height="315" alt="изображение" src="https://github.com/user-attachments/assets/9dba8c57-fec9-4fc2-aeaf-e8112a26ebde" />
