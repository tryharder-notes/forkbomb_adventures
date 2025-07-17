**Battle Write Up**

Source: https://rev-kids20.forkbomb.ru/tasks/RE9_battle

First of all, it is worth understanding what is .apk?

APK - Android Package Kit - an executable file format for Android. Each application contains a DEX file, which contains the code, a manifest file in .xml format, library files, etc.

The APK itself is an archive containing all the files necessary for the application to work, and therefore it can, for example, be easily unzipped using 7z:

```7z e example.apk```

But the most convenient thing, of course, is to use something that will also allow you to read the contents of these files.

For example, Bytecode Viewer (https://github.com/konloch/bytecode-viewer/releases) allows you to analyze the internals of an application.

Let's take a look at a small application (https://rev-kids20.forkbomb.ru/tasks/RE9_battle), which accepts a password and, depending on whether it is correct or not, gives us 'Correct!' or 'Wrong!'

First of all, of course, you need to somehow launch the application; I use the emulator in Android Studio for this.

<img width="627" height="953" alt="изображение" src="https://github.com/user-attachments/assets/6f70510e-0d4d-4c0d-868f-854e43123887" />

To install the application, simply drag the .apk file from Explorer to the emulator screen.

So I entered a test string and the application responded "Wrong!"

<img width="617" height="943" alt="изображение" src="https://github.com/user-attachments/assets/7bea4395-7ae4-4b33-a0fa-ea965bdd3cc2" />

There is no more interesting functionality here, so it's time to head to the Bytecode Viewer and see what's going on there:

We load .apk into it and the next question is where to go next. Here everything is the same as with native binaries - you need to look for main, and to do this, you need to open Plugins -> View Manifest:

In the manifest we find ```<activity android:name>``` and see what is written there:

<img width="756" height="187" alt="изображение" src="https://github.com/user-attachments/assets/89e3cf0e-e78f-4ccc-b540-465398780a13" />

In my case it says "com.hackbattle.task.MainActivity"

We follow this path in the file manager and see MainActivity:

<img width="265" height="418" alt="изображение" src="https://github.com/user-attachments/assets/1b15543e-b566-4d40-9c16-2ea77aa195d3" />

Open:

<img width="1914" height="1038" alt="изображение" src="https://github.com/user-attachments/assets/33308469-2ed5-4e27-ae23-94d6708f70a6" />

And we see the code. In the left window is the decompiled Java code, on the right is the disassembled JVM (Java Virtual Machine) code

You can also select different decompilers to compare their output, or you can save a separate file as .jar and feed it to Java Decompiler (https://java-decompiler.github.io/) - sometimes the code looks more readable there

Now that I have a full working environment, it's time to read the code. To be honest, I've never written anything in Java and have never studied this language, but I still get the gist of the code - this is not Erlang, not Go - here the syntax is close to the languages I write in - C, Python.

First of all, let's pay attention to the first function:

<img width="713" height="268" alt="изображение" src="https://github.com/user-attachments/assets/3d2ef715-4846-4862-acd3-3a496ca94b68" />

It simply decodes the strings that enter it from base64 and xorizes them byte by byte with the number 255

Let's move on and see this block of code:

<img width="618" height="137" alt="изображение" src="https://github.com/user-attachments/assets/a694c57d-45b6-4782-b2d6-1907431d368e" />

I think it is clear what open is, we come across the already familiar b64e function, apparently the name of the file that the program will open is encrypted here.

Without thinking twice, we go and find out what kind of file this is:

<img width="725" height="474" alt="изображение" src="https://github.com/user-attachments/assets/e01aa238-abc8-41fd-acb6-7473dd64d774" />

And we get the output "file.bin"

Further in the code there are similarly obfuscated classes, files, etc. You can find a mention of Dalvik - this is a virtual machine for running applications on Android.

We go down to the end of the try/catch block and see the while block following it:

<img width="573" height="767" alt="изображение" src="https://github.com/user-attachments/assets/623447bd-4aaf-49b2-a249-e1b2d559cebd" />

var2 is obviously a counter, var3 is the contents of file.bin

And what we see here is that each byte of file.bin is xored with the number 237, i.e. not only the file name is obfuscated, but the file itself. The file itself is decrypted during execution, so we can only look into it if we repeat the decryption process, and we already know it. Let's go decrypt the file:

<img width="569" height="505" alt="изображение" src="https://github.com/user-attachments/assets/e2a28d8d-0bc5-4fd0-80e8-2089a467a256" />

Then we can assume that it is a .DEX file, after all there must be some code in there.

Therefore, we rename file_encoded.bin to file_encoded.dex and throw it into the Bytecode Viewer:

<img width="275" height="417" alt="изображение" src="https://github.com/user-attachments/assets/8b6cb701-2626-4a88-8b0b-d12c7cd81e6f" />

If the program understood what it is and it is readable, then we did everything correctly.

Now we need to examine the contents of the decrypted file:

<img width="790" height="449" alt="изображение" src="https://github.com/user-attachments/assets/494d4674-7142-413d-ac7e-8999f41446ea" />

C.class contains the logic for checking and outputting the result - those same lines "Correct!" and "Wrong!"

You can see that var1 is compared to what this.bb returns, and this.bb is formed in B.class apparently.

This is what B.class looks like:

<img width="629" height="315" alt="изображение" src="https://github.com/user-attachments/assets/a0e8cec1-064d-4cf2-9de3-2a9802468302" />

Two strings are entered here, they are concatenated and the function returns a string that is then compared with what the user entered.

Here you can already understand the password format: "%something there% %something there% Green"

You need to find 2 strings.

Let's go back to main and see what exactly is being passed here:

<img width="567" height="148" alt="изображение" src="https://github.com/user-attachments/assets/79ea6c62-1329-4bf6-8910-3b874f181882" />

It is clear that 2 numbers go in, and below you can see exactly those numbers that the program sends to the encrypted part of the code. But here the obfuscation is notable in that many objects are assigned an ID, by which they can be found in other classes or other parts of the application.

You can wander through the classes and find R$array.class with the following contents:

<img width="571" height="126" alt="изображение" src="https://github.com/user-attachments/assets/a468676f-9148-49e5-b0a1-dacb11699656" />

Here you can see that two variables are assigned ID

Now you can go to res.values and look for arrays.xml or something like that.

And such a file is found, its contents are as follows:

<img width="333" height="409" alt="изображение" src="https://github.com/user-attachments/assets/89e1798d-2f9b-4798-8d0d-ab85d0f43303" />

We need to decode the strings that are in the string-array, obviously this is Base64:

<img width="569" height="444" alt="изображение" src="https://github.com/user-attachments/assets/578c15f3-6926-4d81-8e14-6b03f2c70268" />

We get the following conclusion:

<img width="464" height="281" alt="изображение" src="https://github.com/user-attachments/assets/ea54a741-47c8-448a-ba9b-cf754b1b88f7" />

There are already some meaningful lines - that means the solution is already somewhere close.

Now we need to figure out what an integer-array is

We can assume that the program takes a string from the string-array by the integer-array index, which means that this is the 4th and 9th string ('Android', 'sup3r').

So the password is 'Android sup3r Green'.

Let's check:

<img width="624" height="947" alt="изображение" src="https://github.com/user-attachments/assets/5cf41477-163d-4f46-8e53-cf4ecc36948b" />

The password works :)
