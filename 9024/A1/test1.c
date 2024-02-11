#include<stdio.h>
#include<string.h>
#include <stdlib.h>
#include <assert.h>

// data type for nodes
typedef struct DLListNode {
	int  value;  // value (int) of this list item 
	struct DLListNode *prev;
	// pointer previous node in list
	struct DLListNode *next;
	// pointer to next node in list
} DLListNode;

//data type for doubly linked lists
typedef struct DLList{
	int  size;      // count of items in list
	DLListNode *first; // first node in list
	DLListNode *last;  // last node in list
} DLList;

// create a new DLListNode
DLListNode *newDLListNode(int it)
{
	DLListNode *new;
	new = malloc(sizeof(DLListNode));
	assert(new != NULL);
	new->value = it;
	new->prev = new->next = NULL;
	return new;
}

// create a new empty DLList
DLList *newDLList()
{
	DLList *L;

	L = malloc(sizeof (struct DLList));
	assert (L != NULL);
	L->size = 0;
	L->first = NULL;
	L->last = NULL;
	return L;
}
void printDLList(DLList *u)
{
 // put your code here
	DLListNode *cur = u->first;
	while (cur != NULL) {
		printf("%d\n", cur->value);
		cur = cur->next;
	} 
}

DLList *CreateDLListFromFileDlist(const char *filename) {
	FILE *fp;
    DLList *L1 = newDLList();
	DLListNode *head = newDLListNode(0);
	L1->first = head;
    if (strcmp(filename,"stdin") == 0) {
        char ch1[100];
		while(scanf("%s",ch1)) {
			if (!strcmp(ch1,"end") ){
				L1->last = head->prev;
                L1->last->next = NULL;
                free (head);
				return L1;
			}else {
				int num;
    			num = atoi(ch1);
				DLListNode *node1 = newDLListNode(0);
				head->value = num;
				head->next = node1;
				node1->prev = head;
				head = head->next;
				L1->size +=1;
			}
        }
    } else {
		fp = fopen(filename, "r");
		if (!fp) {
			printf("Invalid input! \n");
			return NULL;
		} else {
    		int temp;
			char *str = (char*)malloc(10*sizeof(char));

			while(EOF != (fscanf(fp, "%s", str))) {
            	temp = atoi(str);
				DLListNode *node1 = newDLListNode(0);
				head->value = temp;
				head->next = node1;
				node1->prev = head;
				head = head->next;
				L1->size +=1;
    		}
			L1->last = head->prev;
            L1->last->next = NULL;
            free (head);
		}
	}
	return L1;
}

// clone a DLList
// put your time complexity analysis for cloneList() here
DLList *cloneList(DLList *u)
{
 // put your code here
  
}
int main(void)
{
    DLList *list1=CreateDLListFromFileDlist("File1.txt");
    //DLListNode *cur = list1->last;
    //printf("%d\n", cur->value);
	printDLList(list1);
}