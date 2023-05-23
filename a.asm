	.data 
	str_nl: .asciz "\n" 
	.text

	j Lmain
L0:
	sw ra,(sp)
	
L1:
	li a7, 5
	ecall
	sw a0, -12(gp)
	
L2:
	lw t0, -12(gp)
	li t1, 2
	div t2, t0, t1
	sw t2, -32(sp)
	
L3:
	lw t1, -32(sp)
	sw t1, -16(gp)
	
L4:
	li t0, 2
	lw t1, -16(gp)
	mul t2, t0, t1
	sw t2, -36(sp)
	
L5:
	lw t0, -12(gp)
	lw t1, -36(sp)
	sub t2, t0, t1
	sw t2, -40(sp)
	
L6:
	lw t1, -40(sp)
	sw t1, -20(gp)
	
L7:
	li t1, 0
	sw t1, -24(gp)
	
L8:
	li t1, 1
	sw t1, -28(gp)
	
L9:
	lw t0, -20(gp)
	li t1, 0
	beq t0, t1, L11
	
L10:
	j L13
	
L11:
	lw a0, -24(gp)
	li a7, 1
	ecall
	la a0, str_nl
	li a7, 4
	ecall
	
L12:
	j L14
	
L13:
	lw a0, -28(gp)
	li a7, 1
	ecall
	la a0, str_nl
	li a7, 4
	ecall
	
L14:
	lw ra,(sp)
	jr ra
	
L15:
Lmain:
	addi sp, sp, 12
	mv gp, sp
	
L16:
	addi fp, sp, 44
	sw sp,-4(fp)
	addi sp, sp, 44
	jal L0
	addi sp, sp, -44
	
L17:
	li a0, 0
	li a7, 93
	ecall
	
L18:
	
