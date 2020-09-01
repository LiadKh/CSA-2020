#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include "graphkdr.h"

typedef unsigned int word;
typedef unsigned int boolean;

extern void CP_InitRndT(word seed);
extern	void US_InitRndT(boolean randomize);
extern	int CP_RndT(void);

typedef struct
{
  int 	chosenshapenum;
} statetype;


typedef	struct
{
	unsigned char  key[16];
	int key_index;
	unsigned char second_flag[24];
} gametype;

typedef struct rc2_key_st {
    unsigned short xkey[64];
} RC2_Schedule;