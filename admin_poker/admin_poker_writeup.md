**Admin Poker Write Up**

Source: https://rev-kids20.forkbomb.ru/tasks/REX_adminpoker

Description: "I was invited by some hardcore sysadmins to a poker match. They promised me a flag if I could get 500 chips. The problem is, they don't even use Linux... they're too trueЪ for that, they only use FreeBSD"

First, I tried to execute a binary file on FreeBSD. It's a simple command-line poker client.

<img width="576" height="326" alt="изображение" src="https://github.com/user-attachments/assets/7d0fb3c0-ce1d-4d2d-b9ca-70091fe49e8e" />

The program asked me for my bet. When I did, the game started.

<img width="552" height="230" alt="изображение" src="https://github.com/user-attachments/assets/64248b59-2e30-42c1-9b71-62a3960e7acd" />

When all the turns were finished, the program started a new game. Trying to play was a bad idea, because a chances to win are quiet low.

Well, I started by examining the internals of this binary. I opened IDA and tried to find some useful details.

First, I wanted to figure out how the binary checks my balance, if i patch this checks, I might be able to bypass all that logic and get the flag immediately.

But, it didn't worked.

I saw this code. It checks the balance and if it's less than zero, the program reports it to the server.

<img width="894" height="675" alt="изображение" src="https://github.com/user-attachments/assets/494cbeba-b487-4e25-90c7-e29b03325980" />

I patched this code to this:

<img width="1220" height="546" alt="изображение" src="https://github.com/user-attachments/assets/5e30b62e-67db-4a2a-8c68-50326faf26f6" />

There are no checks, the program must prints the flag immediately anyway.

And when i tried to run it, I saw this message from the server.

<img width="648" height="122" alt="изображение" src="https://github.com/user-attachments/assets/2a6376ac-67f8-4484-8ee1-a6be3a0546b9" />

"Plan A" failed, because the server performs these checks as well. I switched to "Plan B". First, I wanted to analyzed network traffic to figure out how the client communicates with the server.

I found the server's IP addres using IDA. 

<img width="425" height="247" alt="изображение" src="https://github.com/user-attachments/assets/64212502-8eab-46f9-b938-2f8bc2dd51af" />

After that I opened Wireshark and analyzed network traffic for this IP addres and saw this:

<img width="1810" height="315" alt="изображение" src="https://github.com/user-attachments/assets/70374924-9f3a-4f9c-88e7-2db17550365c" />

<img width="578" height="144" alt="изображение" src="https://github.com/user-attachments/assets/35949a4b-acc6-48f1-88ea-e10d2ee2d85f" />

The server sent all cards to the client. I can use this to win the game, but doing it manually takes a lot of time. On top of everything, the server has a limited waiting time for client responses.

I also analyzed the traffic to figure out how the client initializes the game.

After that i wrote my own client that can init the game, parse the cards sent by the server, count card combinations and place bets if I have the highest score.

The code of this client is stored in the **adminpoker_solve.py** file.
