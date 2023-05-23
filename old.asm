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
	li t1, 1
	sw t1, -20(gp)
	
L3:
	li t1, 1
	sw t1, -16(gp)
	
L4:
	lw t0, -16(gp)
	lw t1, -12(gp)
	ble t0, t1, L6
	
L5:
	j L11
	
L6:
	lw t0, -20(gp)
	lw t1, -16(gp)
	mul t2, t0, t1
	sw t2, -24(sp)
	
L7:
	lw t1, -24(sp)
	sw t1, -20(gp)
	
L8:
	lw t0, -16(gp)
	addi t1, t0, 1
	sw t1, -28(sp)
	
L9:
	lw t1, -28(sp)
	sw t1, -16(gp)
	
L10:
	j L4
	
L11:
	lw a0, -20(gp)
	li a7, 1
	ecall
	la a0, str_nl
	li a7, 4
	ecall
	
L12:
	lw ra,(sp)
	jr ra
	
L13:
	sw ra,(sp)
	
L14:
	lw t0, -12(sp)
	li t1, 1
	ble t0, t1, L16
	
L15:
	j L18
	
L16:
	lw t1, -12(sp)
	lw t0, -8(sp)
	sw t1, (t0)
	lw ra,(sp)
	jr ra
	
L17:
	j L28
	
L18:
	lw t0, -12(sp)
	addi t1, t0, -1
	sw t1, -16(sp)
	
L19:
	addi fp, sp, 36
	lw t0, -16(sp)
	sw t0, -12(fp)
	
L20:
	addi t0, sp, -20
	sw t0, -8(fp)
	
L21:
	addi fp, sp, 36
	sw sp,-4(fp)
	addi sp, sp, 36
	jal L13
	addi sp, sp, -36
	
L22:
	lw t0, -12(sp)
	addi t1, t0, -2
	sw t1, -24(sp)
	
L23:
	addi fp, sp, 36
	lw t0, -24(sp)
	sw t0, -12(fp)
	
L24:
	addi t0, sp, -28
	sw t0, -8(fp)
	
L25:
	addi fp, sp, 36
	sw sp,-4(fp)
	addi sp, sp, 36
	jal L13
	addi sp, sp, -36
	
L26:
	lw t0, -20(sp)
	lw t1, -28(sp)
	add t2, t0, t1
	sw t2, -32(sp)
	
L27:
	lw t1, -32(sp)
	lw t0, -8(sp)
	sw t1, (t0)
	lw ra,(sp)
	jr ra
	
L28:
	lw ra,(sp)
	jr ra
	
L29:
	sw ra,(sp)
	
L30:
	li a7, 5
	ecall
	sw a0, -12(gp)
	
L31:
	addi fp, sp, 36
	lw t0, -12(gp)
	sw t0, -12(fp)
	
L32:
	addi t0, sp, -16
	sw t0, -8(fp)
	
L33:
	addi fp, sp, 36
	sw sp,-4(fp)
	addi sp, sp, 36
	jal L13
	addi sp, sp, -36
	
L34:
	lw a0, -16(sp)
	li a7, 1
	ecall
	la a0, str_nl
	li a7, 4
	ecall
	
L35:
	lw ra,(sp)
	jr ra
	
L36:
	sw ra,(sp)
	
L37:
	li a7, 5
	ecall
	sw a0, -12(gp)
	
L38:
	li t1, 0
	sw t1, -16(gp)
	
L39:
	lw t0, -12(gp)
	li t1, 0
	bgt t0, t1, L41
	
L40:
	j L46
	
L41:
	lw t0, -12(gp)
	li t1, 10
	div t2, t0, t1
	sw t2, -20(sp)
	
L42:
	lw t1, -20(sp)
	sw t1, -12(gp)
	
L43:
	lw t0, -16(gp)
	addi t1, t0, 1
	sw t1, -24(sp)
	
L44:
	lw t1, -24(sp)
	sw t1, -16(gp)
	
L45:
	j L39
	
L46:
	lw a0, -16(gp)
	li a7, 1
	ecall
	la a0, str_nl
	li a7, 4
	ecall
	
L47:
	lw ra,(sp)
	jr ra
	
L48:
	sw ra,(sp)
	
L49:
	lw t0, -16(sp)
	lw t1, -12(sp)
	div t2, t0, t1
	sw t2, -20(sp)
	
L50:
	lw t0, -20(sp)
	lw t1, -12(sp)
	mul t2, t0, t1
	sw t2, -24(sp)
	
L51:
	lw t0, -16(sp)
	lw t1, -24(sp)
	beq t0, t1, L53
	
L52:
	j L55
	
L53:
	li t1, 1
	lw t0, -8(sp)
	sw t1, (t0)
	lw ra,(sp)
	jr ra
	
L54:
	j L56
	
L55:
	li t1, 0
	lw t0, -8(sp)
	sw t1, (t0)
	lw ra,(sp)
	jr ra
	
L56:
	lw ra,(sp)
	jr ra
	
L57:
	sw ra,(sp)
	
L58:
	li t1, 2
	sw t1, -16(sp)
	
L59:
	lw t0, -16(sp)
	lw t1, -12(sp)
	blt t0, t1, L61
	
L60:
	j L71
	
L61:
	addi fp, sp, 28
	lw t0, -16(sp)
	sw t0, -12(fp)
	
L62:
	lw t0, -12(sp)
	sw t0, -16(fp)
	
L63:
	addi t0, sp, -20
	sw t0, -8(fp)
	
L64:
	addi fp, sp, 28
	sw sp,-4(fp)
	addi sp, sp, 28
	jal L48
	addi sp, sp, -28
	
L65:
	lw t0, -20(sp)
	li t1, 1
	beq t0, t1, L67
	
L66:
	j L68
	
L67:
	li t1, 0
	lw t0, -8(sp)
	sw t1, (t0)
	lw ra,(sp)
	jr ra
	
L68:
	lw t0, -16(sp)
	addi t1, t0, 1
	sw t1, -24(sp)
	
L69:
	lw t1, -24(sp)
	sw t1, -16(sp)
	
L70:
	j L59
	
L71:
	li t1, 1
	lw t0, -8(sp)
	sw t1, (t0)
	lw ra,(sp)
	jr ra
	
L72:
	lw ra,(sp)
	jr ra
	
L73:
	sw ra,(sp)
	
L74:
	li t1, 2
	sw t1, -12(gp)
	
L75:
	lw t0, -12(gp)
	li t1, 30
	blt t0, t1, L77
	
L76:
	j L86
	
L77:
	addi fp, sp, 28
	lw t0, -12(gp)
	sw t0, -12(fp)
	
L78:
	addi t0, sp, -16
	sw t0, -8(fp)
	
L79:
	addi fp, sp, 28
	sw sp,-4(fp)
	addi sp, sp, 28
	jal L57
	addi sp, sp, -28
	
L80:
	lw t0, -16(sp)
	li t1, 1
	beq t0, t1, L82
	
L81:
	j L83
	
L82:
	lw a0, -12(gp)
	li a7, 1
	ecall
	la a0, str_nl
	li a7, 4
	ecall
	
L83:
	lw t0, -12(gp)
	addi t1, t0, 1
	sw t1, -20(sp)
	
L84:
	lw t1, -20(sp)
	sw t1, -12(gp)
	
L85:
	j L75
	
L86:
	lw ra,(sp)
	jr ra
	
L87:
Lmain:
	addi sp, sp, 12
	mv gp, sp
	
L88:
	addi fp, sp, 32
	sw sp,-4(fp)
	addi sp, sp, 32
	jal L0
	addi sp, sp, -32
	
L89:
	addi fp, sp, 20
	sw sp,-4(fp)
	addi sp, sp, 20
	jal L29
	addi sp, sp, -20
	
L90:
	addi fp, sp, 28
	sw sp,-4(fp)
	addi sp, sp, 28
	jal L36
	addi sp, sp, -28
	
L91:
	addi fp, sp, 24
	sw sp,-4(fp)
	addi sp, sp, 24
	jal L73
	addi sp, sp, -24
	
L92:
	li a0, 0
	li a7, 93
	ecall
	
L93:
	
