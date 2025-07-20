**Elfstaller Write Up**

Source: https://rev-kids20.forkbomb.ru/tasks/RE9_elfstaller

This task is a binary on ```Python```, compiled with ```Pyinstaller```. First of all, you should run it to see its functionality.

<img width="537" height="84" alt="изображение" src="https://github.com/user-attachments/assets/929d4d99-2bc8-4749-9b7e-d7f2b6f643ef" />

As you can see, the binary simply takes a string and if it is not a flag, it tells us so and stops working.

To get to the source code of the program, I used 2 utilities: ```Pyinstxtractor``` and ```pycdc```.

First you need to "unpack" the binary using ```Pyinstxtractor```, this is done like this:

```python3 ./pyinstxtractor.py %path_to_exe%```

After which we get this:

<img width="870" height="296" alt="изображение" src="https://github.com/user-attachments/assets/e3845e9b-4b57-4e69-a356-219ab0d388c6" />

Now you need to look through the files and find a .pyc that looks like the main program code. It can be named the same as the binary, in my case ```pyinstallerelf.pyc```, but it can also be ```main.pyc``` or something like that.

All files will be located in a folder in the same directory as the binary by default.

And such a file is actually present here.

<img width="1275" height="327" alt="изображение" src="https://github.com/user-attachments/assets/f5d0f82b-7c32-445d-af75-df977000dbb5" />

Now you can apply ```pycdc``` to it and see what code it contains.

It is done like this:

```./pycdc %path_to_pyc_file%```

And in the end we get this:

<img width="678" height="315" alt="изображение" src="https://github.com/user-attachments/assets/3915ae48-f02c-4b41-94a1-e99dc6afd1a8" />

As you can see, a set of bytes is taken, some manipulations are performed with it, including bit arithmetic and mathematical operations, after which the result obtained is compared with what the user entered.
If the input matches, the program will respond "Enjoy!".

You can try to write a solution and find out what comes out of a set of bytes.

```
def main():
    
    flag = b'(d=\x01eq\x0c8V1\x10\x03!\x0f 6c\x19fgS\x0f8*?<=%1rfa\x00\x0f\x11;'
    
    res = b''
    
    c = 0
    
    key = b'SPbCTF'
    
    for i in flag:
        
        res += bytes([i ^ key[c % 6]])
        c += 1
       
    print(key + res)

if __name__ == '__main__':
    main()
```

I launch and receive a flag.

<img width="466" height="65" alt="изображение" src="https://github.com/user-attachments/assets/58398104-8243-4062-a65e-f9789b69b16f" />
<img width="476" height="84" alt="изображение" src="https://github.com/user-attachments/assets/b1669452-dff7-4e1c-8a7a-af4ec94b043f" />


