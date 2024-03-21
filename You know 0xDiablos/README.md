the arch for the binary is 32 bits (not cringe at all) but we are provided with a win_function and a straight forward BOF . 

![gets](/img/gets-diablos.png)

what i would usually do is bypass the checks in the win function . but lets have a look . 

![win](/img/ida-diablos.png) 

this guy not only he made our life miserable by compiling it as 32 bits binary , he also made the **read(flag)** before the checks so you cant just pass over them . so we'll have to comply and answer for the required parameters . luckily the calling convention for 32 bits is this ez 
**function -> ret_adress -> param1 -> param2 -> param3 -> ...** 
-559038737 is **0xdeadbeef** and -1059139571 is **0xc0ded00d**

look up the script in sol.py