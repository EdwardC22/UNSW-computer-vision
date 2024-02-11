//Ruohao Chen
//z5111287

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>
#include<stdbool.h>

char *search_name(int i, const char *busStops) {
	FILE *fp = fopen(busStops, "r");
	char buf2[100];
	const char *delim =":";
	while (fgets(buf2,100,fp) != NULL) {
		char *p2;
		char *p1;
		p1 = strtok(buf2,delim);
		int num = atoi(p1);
		p2 = strtok(NULL,delim);
        char *name;
        strncpy(name, p2, (strlen(p2) -1));
		if (num == i) {
			return name;
		}
	}
}

int main() {
	char name[100];
	strcpy(name,search_name(0,"busStops.txt"));
	printf("%s",name);
	printf("\n");
}