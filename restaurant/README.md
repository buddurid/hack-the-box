
the given binary is **no pie** and has **no canaries** so we can use the functions in the binary . how ? 

![ida](/img/ida-resto.png)

there is a clear and huge bufferoverflow in the fill function . but the program has only one iteration so after leaking libc using 
puts(any-got-adress-of-any-function) , we need to restart the program by calling the entry point instead of main (recalling main will often crash). by restarting the program , we can re-do the BOF but now by calling **system("/bin/sh")**. 

![ida](/img/win-resto.png)

