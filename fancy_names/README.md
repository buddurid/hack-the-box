this is a basic heap exploit , to be precise a UAF to corrupt the tcache , there is also a window for a **House of force** attack but i got so close and didnt manage to do it that way , i'll be writing what i tried to do at the end so if yoo have a way to solve it please tell me . 
let's break down the program first . 
1. the program gives you a randomly generated name and asks if you want to get another randomly generated name or inout your own name (both options are allowed at most once  and you can skip both options)
2. the user asks for size then allocates that size for you and lets you read **size+8** (for some reason) in the allocated chunk . this is done exactly 4 times . 

### leaks : 
1. a one time leak . notice the string we read into is on the stack in a memory that is not yet nulled out with memset . 

![bug1](/img/ida-bug-fancy.png)

you could breakpoint at that point and see what values you could leak . the possibilities were a heap,stack and libc leak . Given that we can only leak one i chose the libc leak as it's self sufficient . 

2. notice **free(dest);** and **free(s2);** ? well yes the program keep copying and inputting data to these variables after freeing them in 2024 xD
. well all we need is free **dest** then free **s2** then overwrite s2 with a desired pointer and we will get that pointer as allocation after 2 mallocs with the same size as s2 (which is 0x60) . 

### exploit : 

given that we have only libc leak , no heap no stack no base for our binary , we could overwrite the **malloc hook** . in short its a pointer withing **rw-** in libc that gets called when we call malloc with the same parameter passed to malloc . So if overwrite this pointer with **system** , if we call **malloc(10)** whats gonna actually happen is **system(10)** , ofc we will change change the 10 to a pointer to "bin/sh"
as we can control the long we pass to malloc . 
Something to notice is that this vuln is patched in later libc version (2.34 i think) and its only possible because we are running on libc 2.27. 

### help me please :
so another way to do after leaking the libc would be like this :
1. allocate a chunk of size 0x....8 and with unique size then previously allocated chunks (mostly by the fprintf function) , this way we can overwrite the **wilderness** chunk . If you have no idea about this technique read more at * [House of force](https://adamgold.github.io/posts/basic-heap-exploitation-house-of-force/) . the last 8 bytes will be written in the wilderness chunk and we want them to be 0xffffffffffffffff. 

2. although we have no heap leak , we can get a heap allocation within the heap wherever we want based on offset (it could be negative too ). so what i aimed for was the tcache entry where it stores the head of the linked list of freed chunk . 

3. i get an allocation at that pointer then i overwrite it with **malloc_hook** address . With that ,the next allocation with that size will point to **malloc_hook** and we overwrite it with **system**

to this point everything is just fine . Until i realised i have no more mallocs to do , even the strings that fprintf use after arent long enough to call malloc (and they dont print my input too ), i looked for other things to overwrite in libc (found something like **exit_hook** but wasn't possible with my ressources) . this is where i got stuck . any help is much appreciated .


![win](/img/win-fancy.png)

