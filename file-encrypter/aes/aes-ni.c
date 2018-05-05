#include "aes-ni.h"

extern void AES_128_Key_Expansion(const unsigned char *userkey, AES_KEY *key_schedule);
int do_setkey(AES_KEY *enc_key, AES_KEY *dec_key)
{
	// For AES-128 encryption, there are 10 subround 
	int nr = 10;

	if (!enc_key || !dec_key || !aes_key) {
		return -1;
	}
	
	// Set encrypt round key
	AES_128_Key_Expansion(aes_key, enc_key);
	enc_key->nr = nr;

	// Set decrypt round key
	int i;
	__m128i	*enc_round_key = (__m128i*)enc_key->KEY;
	__m128i	*dec_round_key = (__m128i*)dec_key->KEY;
	dec_key->nr = nr;
	dec_round_key[nr] = enc_round_key[0];
	for (i=1;i<nr;i++) {
		dec_round_key[nr-i] = _mm_aesimc_si128(enc_round_key[i]);
	}
	dec_round_key[0] = enc_round_key[nr];

	return 0;
}

extern void AES_ECB_encrypt(const unsigned char *in, 
                            unsigned char *out, 
                            unsigned long length, 
                            const AES_KEY *KS, 
                            int nr);
void aes_ni_enc(AES_KEY *key, unsigned char *in, unsigned char *out, int len)
{
    AES_ECB_encrypt(in, out, len, key, 10);
}

extern void AES_ECB_decrypt(const unsigned char *in, 
                            unsigned char *out, 
                            unsigned long length, 
                            const AES_KEY *KS, 
                            int nr);
void aes_ni_dec(AES_KEY *key, unsigned char *in, unsigned char *out, int len)
{
    AES_ECB_decrypt(in, out, len, key, 10);
}
