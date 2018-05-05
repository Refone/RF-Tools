#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/mman.h>
//#include <conio.h>
#include <pthread.h>
#include <unistd.h>

#include "aes/aes-ni.h"
#include "filestate.h"

#define SIZE_STRING_LEN 20

AES_KEY enc_key;
AES_KEY dec_key;

unsigned char tmp[16]; 
void* in_handler = NULL;
unsigned long i = 0;
unsigned long filesize = -1;  
int enc_end = 0;

void print_rate(void);

int main(int argc, char * argv[])
{
    char *input_file = NULL;
    char *output_file = NULL;
	char sizestr[SIZE_STRING_LEN];
    FILE *in_fp = NULL;
    FILE *out_fp = NULL;
	
	pthread_t thread_print;
	int ret_thread;
	void* status;

    if (argv[1] && argv[2]) {
    } else {
        printf("Usage: ./encrypt <input file> <output file>.\n");
        return 0;
    }

	if (!check_cpu_support()) {
		printf("CPU do not support AESNI.\n");
	}

    input_file = argv[1];
    output_file = argv[2];
    
	in_fp = fopen(input_file, "r");
    out_fp = fopen(output_file, "wb+");
    
	fseek(in_fp, 0L, SEEK_END);  
    filesize = ftell(in_fp); 
	file_size(filesize, sizestr);

	printf("%s ===[encrypt]===> %s [%s]\n", input_file, output_file, sizestr);

    do_setkey(&enc_key, &dec_key);

    in_handler = mmap(0, filesize, PROT_READ, MAP_SHARED, fileno(in_fp), 0);
	
	ret_thread = pthread_create(&thread_print, NULL, (void*)&print_rate, NULL);

	if (ret_thread) {
		printf("Multi thread create failed!\n");
		goto main_end;
	}

    for (i=0; i<filesize; i+=16) {
        aes_ni_enc(&enc_key, in_handler+i, tmp, 16);
        fwrite(tmp, 16, 1, out_fp);
    }

	enc_end = 1;
	
	ret_thread = pthread_join(thread_print, &status);

	printf("Encryption Finished!\n");

main_end:
    fclose(in_fp);
    fclose(out_fp);

    return 0;
}

void print_rate()
{
	int maxchar = 50;
	int current = 0;
	int j;
	char s_now[SIZE_STRING_LEN];
	char s_max[SIZE_STRING_LEN];
	
	file_size(filesize, s_max);

	while (!enc_end) {
		current = maxchar * i / filesize;
		printf("[");
		for (j=0; j<current; j++) {
			printf("#");
		}
		for (;j<maxchar;j++) {
			printf(" ");
		}
		printf("]");

		//memset(s, 0, SIZE_STRING_LEN);
		file_size(i, s_now);
		printf("\t[%s/%s]\t[%d\%]", s_now, s_max, (100 * i / filesize));
		fflush(stdout);
		sleep(1);
		printf("\r");
		fflush(stdout);
	}
	printf("\n");
}
