from pwn import * 

p=remote("83.136.253.251",45075)

def f(input):
	n=len(input)
	p.recvuntil("0. Exit")
	p.sendline("3")
	p.recvuntil("Enter parameters: ")
	p.sendline(f"naive2 {n}")
	
	p.sendline(input)
	if b"Found at i=" in p.recvline():
		return 1 
	return 0
print(f(b"aaaaa"))

p.interactive()