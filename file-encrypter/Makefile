CFLAGS=-maes -msse4 -lpthread
COMMON_OBJ = aes/aes-ni.o aes/aes-ni-asm.o  aes/checkcpu.o filestate.o
ENC_OBJ = enc-main.o 
DEC_OBJ = dec-main.o

all:
	make encrypt
	make decrypt

encrypt: $(ENC_OBJ) $(COMMON_OBJ)
	gcc -g -o $@ $^ $(CFLAGS)

decrypt: $(DEC_OBJ) $(COMMON_OBJ)
	gcc -g -o $@ $^ $(CFLAGS)

.PHONY: clean

clean:
	rm *.o
	rm aes/*.o
	rm encrypt decrypt
