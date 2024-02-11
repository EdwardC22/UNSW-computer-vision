#include<stdio.h>
#include<stdlib.h>

int
main(int argc, char* argv[])
{
    char * line = NULL;
    size_t len = 0;
    ssize_t read_len;
    while ((read_len=getline(&line, &len, stdin)) != -1) 
    {   
        if (read_len > 0 && line[read_len-1] == '\n')
        {   
            line[read_len-1] = '\0';
            read_len -= 1;  
        }   
        printf("%s\n", line);

    }   
    return 0;
}