	.data 
	str_nl: .asciz "\n" 
	.text

	j Lmain
L0:
	sw ra,(sp)
	
L1:
	li t1, 2
	sw t1, -12(gp)
	
L2:
	lw ra,(sp)
	jr ra
	
L3:
Lmain:
	addi sp, sp, 12
	mv gp, sp
	
L4:
	addi fp, sp, 16
	sw sp,-4(fp)
	addi sp, sp, 16
	jal L0
	addi sp, sp, -16
	
L5:
	li a0, 0
	li a7, 93
	ecall
	
L6:
	
