#include <stdio.h>
#include "filestate.h"

void file_size(unsigned long size, char* ret)
{
	double n;
	int l;
	if (size > GB) {
		n = ((double)size)/((double)GB);
		l = sprintf(ret, "%.1fGB", n);
	} else if (size > MB) {
		n = ((double)size)/((double)MB);
		l = sprintf(ret, "%.1fMB", n);
	} else {
		n = ((double)size)/((double)KB);
		l = sprintf(ret, "%.1fKB", n);
	}
	ret[l] = '\0';
}
