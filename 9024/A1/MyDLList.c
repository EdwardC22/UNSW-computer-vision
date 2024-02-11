// Author: Ruohao Chen
// Student ID: z5111287
// Platform: Windows
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

// all the basic data structures and functions are included in this template
// you can add your own auxiliary functions as you like 
#include <string.h>
// data structures representing DLList

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

// create a DLList from a text file
// put your time complexity analysis for CreateDLListFromFileDlist() here
// the time complexity of part 1 is O(n*1*1) = O(n).
// the time complexity of part 2 is O(1*1*n) = O(n).
// so the total time complexity for CreateDLListFromFileDlist() is max (part 1, part 2) = O(n)
DLList *CreateDLListFromFileDlist(const char *filename)
{
 // put your code here
	FILE *fp;
    DLList *L1 = newDLList();
	DLListNode *head = newDLListNode(0);
	L1->first = head;
    if (strcmp(filename,"stdin") == 0) {	//part 1
        char ch1[100];
		while(scanf("%s",ch1) !=EOF) {
			if (!strcmp(ch1,"end")) {
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
    } else {	//part 2
		fp = fopen(filename, "r");
		if (!fp) {
			printf("Invalid input! \n");
			return NULL;
		} else {
    		int temp;
			char *str = (char*) malloc (10*sizeof(char));

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
// the time complexity for cloneList() is O(n)
DLList *cloneList(DLList *u)
{
 // put your code here
	DLListNode *copy = u->first;
	DLList *L1 = newDLList();
	L1->size = u->size;
	DLListNode *head = newDLListNode(0);
	L1->first = head;
	while (copy != NULL) {
		DLListNode *node1 = newDLListNode(0);
		head->value = copy->value;
		head->next = node1;
		node1->prev = head;
		head = head->next;
		copy = copy->next;
	}
	L1->last = head->prev;
    L1->last->next = NULL;
    free (head);
	return L1;
}

// compute the longest sublist
// put your time complexity analysis for longestSublist() here
// the time complexity of part 1 is O(1*logn*1*1) = O(logn).
// the time complexity of part 2 is O(1).
// the time complexity of part 3 is O(n*1*1) = O(n).
// so the total time complexity for longestSublist() is max (part 1, part 2, part 3) = O(logn)
DLList *longestSublist(DLList *u)
{
  // put your code here
  	DLList *sub = newDLList();
  	DLListNode *temp = u->first;
	DLListNode *head = newDLListNode(0);
	sub->first = head;

	int i, j, k;
	int list[100000] = {0};
	int a = 2;

	while (temp != NULL) {	//part 1
		k = temp->value;
		if (k < 0) {
			k = -k;
		}
		for (j = 1; j * j < k; j++) {
			if (k % j == 0) {
				list[j]++;
				list[k/j]++;
			}
		}
		if (k == j*j) {
			list[j]++;
		}
		temp = temp->next;
	}

    for (i = 2; i < 100000; i++) {	//part 2
        if(list[a] < list[i]) {
            a = i;
        }
    }

	temp = u->first;
	sub->size = list[a];

	while (temp != NULL) {	//part 3
		int num = temp->value;
		if (num < 0) {
			num = -num;
		}
		if (num % a == 0) {
			DLListNode *node1 = newDLListNode(0);
			head->value = temp->value;
			head->next = node1;
			node1->prev = head;
			head = head->next;
		}
		temp = temp->next;
	}
	sub->last = head->prev;
    sub->last->next = NULL;
    free (head);
	return sub;
}

// compute the union of two DLLists u and v
// put your time complexity analysis for setUnion() here
// the time complexity for setUnion() is O(n*n*1*1) = O(n^2)
DLList *setUnion(DLList *u, DLList *v)
{
 // put your code here
	DLList *unionL = cloneList(u);
	DLListNode *temp = v->first;
	DLListNode *node1 = newDLListNode(unionL->last->value);

	node1->prev = unionL->last->prev; 
	unionL->last->prev->next = node1;
	unionL->last = NULL;

	while (temp != NULL) {
		DLListNode *temp2 = u->first;
		int i = 0;		
		while (temp2 != NULL){
			if (temp->value == temp2->value){
				temp2 = NULL;
				i = 1;
			} else {
				temp2 = temp2->next;
			}
		}
		if (i == 0) {
			DLListNode *node2 = newDLListNode(temp->value);
			node2->prev = node1;
			node1->next = node2;
			node1 = node1->next;
			unionL->size += 1;
		} else if (i == 1) {
			i = 0;
		}
		temp = temp->next;
	}
	unionL->last = node1;
	return unionL;
}


// compute the insection of two DLLists u and v
// put your time complexity analysis for intersection() here
// the time complexity for intersection() is O(n*n*1*1) = O(n^2)
DLList *setIntersection(DLList *u, DLList *v)
{
  // put your code here
	DLList *intersec = newDLList();
	DLListNode *temp = v->first;
	DLListNode *head = newDLListNode(0);
	intersec->first = head;

	while (temp != NULL) {
		DLListNode *temp2 = u->first;
		while (temp2 != NULL){
			if (temp->value == temp2->value){
				DLListNode *node1 = newDLListNode(0);
				head->value = temp->value;
				head->next = node1;
				node1->prev = head;
				head = head->next;
				intersec->size +=1;
				temp2 = NULL;
			} else {
				temp2 = temp2->next;
			}
		}
		temp = temp->next;
	}

	intersec->last = head->prev;
    intersec->last->next = NULL;
    free (head);
	return intersec;
}

// free up all space associated with list
// put your time complexity analysis for freeDLList() here
// the time complexity for freeDLList() is O(n)
void freeDLList(DLList *L)
{
// put your code here
	DLListNode *del = L->first;
	while (del != NULL)	{
		L->first = del->next;
		free (del);
		del = L->first;
	}
}


// display items of a DLList
// put your time complexity analysis for printDDList() here
// the time complexity for printDDList() is O(n)
void printDLList(DLList *u)
{
 // put your code here
	DLListNode *cur = u->first;
	while (cur != NULL) {
		printf("%d\n", cur->value);
		cur = cur->next;
	} 
}

int main()
{
 DLList *list1, *list2, *list3, *list4;

 list1=CreateDLListFromFileDlist("File1.txt");
 printDLList(list1);

 list2=CreateDLListFromFileDlist("File2.txt");
 printDLList(list2);

 list3=setUnion(list1, list2);
 printDLList(list3);

 list4=setIntersection(list1, list2);
 printDLList(list4);

 printDLList(longestSublist(list4));

 freeDLList(list1);
 freeDLList(list2);
 freeDLList(list3);
 freeDLList(list4);

 printf("please type all the integers of list1\n");
 list1=CreateDLListFromFileDlist("stdin");

 printf("please type all the integers of list2\n");
 list2=CreateDLListFromFileDlist("stdin");

 list3=cloneList(list1);
 printDLList(list3);
 list4=cloneList(list2);
 printDLList(list4);

 freeDLList(list1);
 freeDLList(list2);
 freeDLList(list3);
 freeDLList(list4);

 return 0; 
}
