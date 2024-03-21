this challenge is one of the most creative challenges ive ever seen , but once you understand what actually happens , it becomes ez . 

1. ususally in our programs , we deal with bytes , it means our in/out consists of bytes which are of 8 bits size which means the pool of characters we can interact with is very small (up to 255 characters). unicode actually solves the program by introducing a 32 bits character or in some cases 16 bits . A very quick example would be like this : **'A'** is **\x41** in bytes but is **\U000000041** in 32 bits unicode. 
2. unicode characters have range limit . example **\U12300000** doesnt exist (for now) and you cant send nor receive it . i forgot the limit but i think it doesnt exceed **\U00020000** so we gotta use unicode that is lower than this .
3. the stack still behaves normally and the sizes allocated are counted in bytes , but the sizes that are mentionned in **fgetws** for example are meant to be in unicode size , so to convert it to bytes you have to multipy it by 4 . 

back to our binary . its compiled with **PIE** and **NX** , and we got no leaks . we got a BOF though in Contact support and our input is gonna be copied in the **SupportMsg** variable in **16 bits unicode**. the input provided will be copied into **SupportMessage** in 16 bit unicode chars . this is very import for later.

![ida](/img/ida-evil.png)

how is this an overflow ? the v1 variable is of size **4002x4=16008bytes** , and we are reading into it **4096** unicode characters which as mentionned above is equivalent to **4096*4=16384 bytes** 

in normal conditions we would have the oppurtunity to overwrite the ret adress but it's not the case . or is it ? 
lets look at the setup function 

![ida-setup](/img/ida-setup-diablos.png)

**SupportMessage** is a pointer to an mmaped memory region . the first parameter in the mmap call is the desirable adress for the mmaped memory region , so if not already used , the mmap should return the value specfied in the first paramter . and just like that we know where that memory region is . for **SupportMessage** it's **0x10000** . 
another thing to mention is the permissions requested for those regions , **SupportMessage** for example has permissions of 3 >>> RW- . 
no execute flag , thats so sad . 
how about **AssemblyTestPage** ? it has eveything we need , execute flag + we know where its allocated (0x11000)
so if we managed to write shellcode in this region then make return adress through the BOF point to **0x11100** , BINGO.

now comes the question HOW ? the same way the BOF is happening on the stack , if the input is large , it will overflow the **SupportMessage** variable because our input is copied into it . With that , we end up writing to **AssemblyTestPage** variable

now into how to write the shellcode . suppose that you want to write **b"\x41\x57"** you need to write **U"\U00004157"** and then the **wcharToChar16** will make it like this **u"\u4157"** and just like that you get your shellcode . 

the full script is available above 