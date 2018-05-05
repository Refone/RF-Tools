#ifndef _H_AES_NI_H_
#define _H_AES_NI_H_

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <wmmintrin.h>

#if !defined (ALIGN16)
# if defined (__GNUC__)
# define ALIGN16 __attribute__((aligned(16)))
# else
# define ALIGN16 __declspec(align(16))
# endif
#endif

typedef struct KEY_SCHEDULE{
    ALIGN16 unsigned char KEY[16*15];
    unsigned int nr;
}AES_KEY;

static unsigned char aes_key[16] =  {
			0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
			0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff};

extern int check_cpu_support(void);
extern int do_setkey(AES_KEY *enc_key, AES_KEY *dec_key);
extern void aes_ni_enc(AES_KEY *key, unsigned char *in, unsigned char *out, int len);
extern void aes_ni_dec(AES_KEY *key, unsigned char *in, unsigned char *out, int len);

#endif /* _H_AES_NI_H_ */
