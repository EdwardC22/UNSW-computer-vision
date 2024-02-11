// Author: Ruohao Chen
// Student ID: z5111287
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
// all the basic data structures and functions are included in this template
// you can add your own auxiliary functions as you like 

#define MAX(x, y) ((x > y) ? x : y)             // returns maximum of x and y
#define MIN(x, y) ((x < y) ? x : y)             // returns minimum of x and y
#define HEIGHT(x) ((x) ? (x->height) : -1)

// data type for avl tree nodes
typedef struct AVLTreeNode {
	int key; //key of this item
	int  value;  //value (int) of this item 
	int height; //height of the subtree rooted at this node
	struct AVLTreeNode *parent; //pointer to parent
	struct AVLTreeNode *left; //pointer to left child
	struct AVLTreeNode *right; //pointer to right child
} AVLTreeNode;

//data type for AVL trees
typedef struct AVLTree{
	int  size;      // count of items in avl tree
	AVLTreeNode *root; // root
} AVLTree;

// create a new AVLTreeNode
AVLTreeNode *newAVLTreeNode(int k, int v )
{
	AVLTreeNode *newNode;
	newNode = malloc(sizeof(AVLTreeNode));
	assert(newNode != NULL);
	newNode->key = k;
	newNode->value = v;
	newNode->height = 0; // height of this new node is set to 0
	newNode->left = NULL; // this node has no child
	newNode->right = NULL;
	newNode->parent = NULL; // no parent
	return newNode;
}

// create a new empty avl tree
AVLTree *newAVLTree()
{
	AVLTree *T;
	T = malloc(sizeof (AVLTree));
	assert (T != NULL);
	T->size = 0;
	T->root = NULL;
	return T;
}

// main function declaration
AVLTree *CreateAVLTree(const char *filename);
AVLTree *CloneAVLTree(AVLTree *T);
AVLTree *AVLTreesUnion(AVLTree *T1, AVLTree *T2);
AVLTree *AVLTreesIntersection(AVLTree *T1, AVLTree *T2);
int InsertNode(AVLTree *T, int k, int v);
int DeleteNode(AVLTree *T, int k, int v);
AVLTreeNode *Search(AVLTree *T, int k, int v);
void FreeAVLTree(AVLTree *T);
void PrintAVLTree(AVLTree *T);

// auxiliary function declaration
void LL_Rotation(AVLTree *T, AVLTreeNode *N);
void RR_Rotation(AVLTree *T, AVLTreeNode *N);
AVLTreeNode *TriNode_Re(AVLTree *T, AVLTreeNode *N);
int Insert(AVLTree *T, AVLTreeNode *N, int k, int v);
void Inorder_Array(AVLTreeNode *node, int K[], int V[], int *i);
void PrintNode(AVLTreeNode *node);
int Delete(AVLTree *T, AVLTreeNode *N, int k, int v);
AVLTreeNode *InorderCreate(AVLTree *T, AVLTreeNode *N1, int K[], int V[], int num1, int num2);

// put your time complexity analysis of CreateAVLTree() here
// the time complexity of part 1 is O(1*n)
// part 2 is O(n)
// the time complexity of InsertNode function is O(log(n)), so part 3 is O(n * log(n))
// so the total time complexity is max(part1, part2, part3), which is O(n * log(n))
AVLTree *CreateAVLTree(const char *filename)
{
// put your code here
	FILE *fp;
	AVLTree *T = newAVLTree();
	int list[10000];
    int num1 =0;
	int num2 = 0;
	if (strcmp(filename,"stdin") == 0) {
		int sign = 1;
		char ch1[1000];
		while(scanf("%[^\n]%*c", ch1) == 1){ 		//part 1
        	for (int i = 0; ch1[i] != '\0'; i++) {
            	if (ch1[i] == '-' || (ch1[i] >= '0' && ch1[i] <= '9')) {
                	if (ch1[i + 1] >= '0' && ch1[i + 1] <= '9') {
                    	if (ch1[i] == '-') {
                        	sign = -1;
                    	} else {
                        	num2 = num2 * 10 + (ch1[i] - '0');
                    	}
                	} else {
                    	list[num1++] = sign * (num2 * 10 + (ch1[i] - '0'));
                    	num2 = 0;
                    	sign = 1;
                	}
            	}
        	}
    	}
	} else {		//part 2
		fp = fopen(filename, "r");
		if (!fp) {
			printf("Error! \n");
			return NULL;
		} 
		while (!feof(fp)) {
			if (fscanf(fp, "%d", &num2) == 1) {
            	list[num1++] = num2;
			} else {
				fgetc(fp);
			}
		}
		fclose(fp);
	}

	for (int i = 0; i < num1 - 1; i += 2) {  //part 3
        InsertNode(T, list[i], list[i + 1]);
    }

    return T;
}

// put your time complexity analysis for CloneAVLTree() here
//  the time complexity is O(n) since the recursion of CloneAVLTree is n time
AVLTree *CloneAVLTree(AVLTree *T)
{
 // put your code here
  	AVLTree *clone, *TLeft, *TRight, *cloneL, *cloneR;
	if (T->root == NULL) {
		return T;
	}

	clone = newAVLTree();
	TLeft = newAVLTree();
	TRight = newAVLTree();
	AVLTreeNode *new = newAVLTreeNode(T->root->key,T->root->value);
	clone->root = new;
	new->height = T->root->height;
	TLeft->root = T->root->left;
	TRight->root = T->root->right;

	cloneL = CloneAVLTree(TLeft);
	cloneR = CloneAVLTree(TRight);

	if (cloneL->root != NULL) {
		cloneL->root->parent = new->left;
	}
	if (cloneR->root != NULL) {
		cloneR->root->parent = new->right;
	}
	new->left = cloneL->root;
	new->right = cloneR->root;
	return clone;
}
 
// put your time complexity for ALVTreesUNion() here
// the time complexity of Inorder_Array and InorderCreate function  is O(n)
// the time complexity of part1 is O(m+n)
// part 2 is O(n)
// part 3 is O(m)
// so the total time complexity is O(m+n)
AVLTree *AVLTreesUnion(AVLTree *T1, AVLTree *T2)
{
	//put your code here
	int i = 0;
	//store K and V of T1
	int *K1= malloc(T1->size * sizeof(int)), *V1 = malloc(T1->size * sizeof(int));
	Inorder_Array(T1->root, K1, V1, &i);

	//store K and V of T2
	i = 0;
	int *K2= malloc(T2->size * sizeof(int)), *V2 = malloc(T2->size * sizeof(int));
	Inorder_Array(T2->root, K2, V2, &i);

	int *K = malloc((T1->size + T2->size) * sizeof(int)); 
	int *V = malloc((T1->size + T2->size) * sizeof(int));

	int i1 = 0, i2 = 0;
	i = 0;

	//Union selection
	while (i1 < T1->size && i2 < T2->size) {  	//part1
        if (K1[i1] < K2[i2] || (K1[i1] == K2[i2] && V1[i1] < V2[i2])) {
			K[i] = K1[i1];
            V[i] = V1[i1];
            i1++;
		} else if (K1[i1] > K2[i2] || (K1[i1] == K2[i2] && V1[i1] > V2[i2])) {
			K[i] = K2[i2];
            V[i] = V2[i2];
            i2++;
		}else {
			K[i] = K1[i1];
            V[i] = V1[i1];
            i1++;
            i2++;
		}
		i++;
	}
	// if T1 is bigger tree
	while (i1 < T1->size) {		//part2
        K[i] = K1[i1];
        V[i] = V1[i1];
        i1++;
        i++;
    }
	// if T2 is bigger tree
	while (i2 < T2->size) {		//part3
        K[i] = K2[i2];
        V[i] = V2[i2];
        i2++;
        i++; 
    }

	
	AVLTree *Tu = newAVLTree();
	/*
	for (int j = 0; j < i; j++) {
        InsertNode(Tu, K[j], V[j]);
    }
	*/
	if (i > 0) {
		Tu->root = InorderCreate(Tu, NULL, K, V, 0, i - 1);
		Tu->size = i;
	}
	return Tu;
}
 
// put your time complexity for ALVTreesIntersection() here
// the time complexity of Inorder_Array and InorderCreate function is O(n)
// the time complexity of part1 is O(m+n)
// part 2 is O(n)
// part 3 is O(m)
// so the total time complexity is O(m+n)
AVLTree *AVLTreesIntersection(AVLTree *T1, AVLTree *T2)
{
	//put your code here
	int i = 0;
	//store K and V of T1
	int *K1= malloc(T1->size * sizeof(int)), *V1 = malloc(T1->size * sizeof(int));
	Inorder_Array(T1->root, K1, V1, &i);

	//store K and V of T2
	i = 0;
	int *K2= malloc(T2->size * sizeof(int)), *V2 = malloc(T2->size * sizeof(int));
	Inorder_Array(T2->root, K2, V2, &i);

	int *K = malloc((T1->size + T2->size) * sizeof(int)); 
	int *V = malloc((T1->size + T2->size) * sizeof(int));

	int i1 = 0, i2 = 0;
	i = 0;

	//Intersection selection
	while (i1 < T1->size && i2 < T2->size) {
        if (K1[i1] < K2[i2] || (K1[i1] == K2[i2] && V1[i1] < V2[i2])) {
            i1++;
		} else if (K1[i1] > K2[i2] || (K1[i1] == K2[i2] && V1[i1] > V2[i2])) {
            i2++;
		}else {
			K[i] = K1[i1];
            V[i] = V1[i1];
            i1++;
            i2++;
			i++;
		}
	}

	AVLTree *Ti = newAVLTree();
	/*
	for (int j = 0; j < i; j++) {
        InsertNode(Ti, K[j], V[j]);
    }
	*/

	if (i > 0) {
		Ti->root = InorderCreate(Ti, NULL, K, V, 0, i - 1);
		Ti->size = i;
	}
	return Ti;

}

// put the time complexity analysis for InsertNode() here 
// the time complexity of Insert function is O(log(n))
// if condition take O(1)
// so time complexity of InsertNode is O(log(n))
int InsertNode(AVLTree *T, int k, int v)
{
	//put your code here

	//if root is NULL
	if (T->root == NULL) {
        T->root = newAVLTreeNode(k, v);
        T->size += 1;
        return 1;
    }

	return Insert(T, T->root, k , v);
}

// put your time complexity for DeleteNode() here
//time complexity of Delete Function is O(n)
int DeleteNode(AVLTree *T, int k, int v)
{
	return Delete(T, T->root, k, v);

}

// put your time complexity analysis for Search() here
// time complexity of Search is O(n)
AVLTreeNode *Search(AVLTree *T, int k, int v)
{
// put your code here
	if (T->root == NULL) {
        return NULL;
    }

	AVLTreeNode *search = T->root;

	while (search != NULL) {
		if (k > search->key) {
			search = search->right;
		} else if (k < search->key) {
			search = search->left;
		} else {
			if (v > search->value) {
				search = search->right;
			} else if (v < search->value) {
				search = search->left;
			} else {
				return search;
			}
		}
	}
	return NULL;
}

// put your time complexity analysis for freeAVLTree() here
// time complexity of FreeAVLTree is O(n)
void FreeAVLTree(AVLTree *T)
{
// put your code here
	if (T == NULL) {
		return;
	}
	
	if (T->root == NULL) {
		free(T);
		return;
	}
	AVLTree *TLeft = newAVLTree();
	AVLTree *TRight = newAVLTree();

	if (T->root->left != NULL) {
		TLeft->root = T->root->left;
		T->root->left->parent = NULL;
		T->root->left = NULL;
		FreeAVLTree(TLeft);
	}

	if (T->root->right != NULL) {
		TRight->root = T->root->right;
		T->root->right->parent = NULL;
		T->root->right = NULL;
		FreeAVLTree(TRight);
	}
	free(T->root);
	free(T);
}

// put your time complexity analysis for PrintAVLTree() here
// the time complexity of PrintNode function is O(n)
// if condition take O(1)
// so time complexity of PrintAVLTree is O(n)
void PrintAVLTree(AVLTree *T)
{
 // put your code here
	if (T != NULL) {
		PrintNode(T->root);
	}
	printf("\n");
}

int main() //sample main for testing 
{ int i,j;
 AVLTree *tree1, *tree2, *tree3, *tree4, *tree5, *tree6, *tree7, *tree8;
 AVLTreeNode *node1;
 
 tree1=CreateAVLTree("stdin");
 PrintAVLTree(tree1);
 FreeAVLTree(tree1);
 //you need to create the text file file1.txt
 // to store a set of items without duplicate items
 tree2=CreateAVLTree("file1.txt"); 
 PrintAVLTree(tree2);
 tree3=CloneAVLTree(tree2);
 PrintAVLTree(tree3);
 FreeAVLTree(tree2);
 FreeAVLTree(tree3);
 //Create tree4 
 tree4=newAVLTree();
 j=InsertNode(tree4, 10, 10);
 for (i=0; i<15; i++)
  {
   j=InsertNode(tree4, i, i);
   if (j==0) printf("(%d, %d) already exists\n", i, i);
  }
  PrintAVLTree(tree4);
  node1=Search(tree4,20,20);
  if (node1!=NULL)
    printf("key= %d value= %d\n",node1->key,node1->value);
  else 
    printf("Key 20 does not exist\n");
  
  for (i=17; i>0; i--)
  {
    j=DeleteNode(tree4, i, i);
	if (j==0) 
	  printf("Key %d does not exist\n",i);  
    PrintAVLTree(tree4);
  }
 FreeAVLTree(tree4);
 //Create tree5
 tree5=newAVLTree();
 j=InsertNode(tree5, 6, 25);
 j=InsertNode(tree5, 6, 10);
 j=InsertNode(tree5, 6, 12);
 j=InsertNode(tree5, 6, 20);
 j=InsertNode(tree5, 9, 25);
 j=InsertNode(tree5, 10, 25);
 PrintAVLTree(tree5);
 //Create tree6
 tree6=newAVLTree();
 j=InsertNode(tree6, 6, 25);
 j=InsertNode(tree6, 5, 10);
 j=InsertNode(tree6, 6, 12);
 j=InsertNode(tree6, 6, 20);
 j=InsertNode(tree6, 8, 35);
 j=InsertNode(tree6, 10, 25);
 PrintAVLTree(tree6);
 tree7=AVLTreesIntersection(tree5, tree6);
 tree8=AVLTreesUnion(tree5,tree6);
 PrintAVLTree(tree7);
 PrintAVLTree(tree8);
 return 0; 
}


// Auxiliary functions
//LL Rotation
void LL_Rotation(AVLTree *T, AVLTreeNode *N) {
	AVLTreeNode *node1 = N;
	AVLTreeNode *node2 = N->left;

	node1->left = node2->right;
	node2->right = node1;

	// relocate the parent
	if (node1->parent != NULL) {
		if (node1->parent->left == node1) {
			node1->parent->left = node2;
		} else {
			node1->parent->right = node2;
		}
	}

	node2->parent = node1->parent;
	node1->parent = node2;

	if (node1->left != NULL) {
		node1->left->parent = node1;
	}
	
	// update the heights
	node1->height = MAX(HEIGHT(node1->left), HEIGHT(node1->right)) + 1;
	node2->height = MAX(HEIGHT(node2->left), HEIGHT(node2->right)) + 1;
	
	//reset the root if N is root;
	if (node1 == T->root) {
		T->root = node2;
	}
	N = node2;
	N->right = node1;
}

//RR_Rotation
void RR_Rotation(AVLTree *T, AVLTreeNode *N) {
	AVLTreeNode *node1 = N;
	AVLTreeNode *node2 = N->right;

	node1->right = node2->left;
	node2->left = node1;

	if (node1->parent != NULL) {
		if (node1->parent->left == node1) {
			node1->parent->left = node2;
		} else {
			node1->parent->right = node2;
		}
	}

	node2->parent = node1->parent;
	node1->parent = node2;

	if (node1->left != NULL) {
		node1->left->parent = node1;
	}

	node1->height = MAX(HEIGHT(node1->left), HEIGHT(node1->right)) + 1;
	node2->height = MAX(HEIGHT(node2->left), HEIGHT(node2->right)) + 1;

	if (node1 == T->root) {
		T->root = node2;
	}

	N = node2;
	N->left = node1;
}


//Trinode Restructuring
AVLTreeNode *TriNode_Re(AVLTree *T, AVLTreeNode *N) {
	if (HEIGHT(N->left) > HEIGHT(N->right)) {
		if (HEIGHT(N->left->left) > HEIGHT(N->left->right)) {
			//LL single case
			LL_Rotation(T,N);
			return N;
		}

		//LR double case
		RR_Rotation(T,N->left);
		LL_Rotation(T,N);
		return N;
	}

	if (HEIGHT(N->right) > HEIGHT(N->left)) {
		if (HEIGHT(N->right->right) > HEIGHT(N->right->left)) {
			//RR single case
			RR_Rotation(T,N);
			return N;
		}

		//RL double case
		LL_Rotation(T,N->right);
		RR_Rotation(T,N);
	}
	return N;
}

//Insert Node if root exist;
int Insert(AVLTree *T, AVLTreeNode *N, int k, int v) {
	//duplicate items.
	if (k == N->key && v == N->value) {
		return 0;
	}

	int i;
	if (k < N->key || (k == N->key && v < N->value)) {
		if (N->left != NULL) {
			i = Insert(T, N->left, k, v);
			if (i != 0) {
				//if the height difference is greater than 1
				if (MAX(HEIGHT(N->left), HEIGHT(N->right)) - MIN(HEIGHT(N->left), HEIGHT(N->right)) > 1) {
                    N = TriNode_Re(T, N);
                }
				N->height = MAX(HEIGHT(N->left), HEIGHT(N->right)) + 1;
			}
			return i;
		} else {
			N->left = newAVLTreeNode(k, v);
            N->height = MAX(HEIGHT(N->left), HEIGHT(N->right)) + 1;
            N->left->parent = N;
            T->size += 1;
		}
	} else if (k > N->key || (k == N->key && v > N->value)) {
		if (N->right != NULL) {
			i = Insert(T, N->right, k, v);
			if (i != 0) {
				//if the height difference is greater than 1
				if (MAX(HEIGHT(N->left), HEIGHT(N->right)) - MIN(HEIGHT(N->left), HEIGHT(N->right)) > 1) {
                    N = TriNode_Re(T, N);
                }
				N->height = MAX(HEIGHT(N->left), HEIGHT(N->right)) + 1;
			}
			return i;
		} else {
			N->right = newAVLTreeNode(k, v);
            N->height = MAX(HEIGHT(N->left), HEIGHT(N->right)) + 1;
            N->right->parent = N;
            T->size += 1;
		}
	}
	return 1;
}

int Delete(AVLTree *T, AVLTreeNode *N, int k, int v) {
	if (N == NULL) {
        return 0;
    }

	int i;
	if (k < N->key || (k == N->key && v < N->value)) {
		i = Insert(T, N->left, k, v);
        if (i != 0) {
			if (MAX(HEIGHT(N->left), HEIGHT(N->right)) - MIN(HEIGHT(N->left), HEIGHT(N->right)) > 1) {
                    N = TriNode_Re(T, N);
                }
				N->height = MAX(HEIGHT(N->left), HEIGHT(N->right)) + 1;
			}
		return i;
    } else if (k > N->key || (k == N->key && v > N->value)) {
		i = Insert(T, N->right, k, v);
			if (i != 0) {
				// tri-node restructuring is required if the height difference is greater than 1
				if (MAX(HEIGHT(N->left), HEIGHT(N->right)) - MIN(HEIGHT(N->left), HEIGHT(N->right)) > 1) {
                    N = TriNode_Re(T, N);
                }
				N->height = MAX(HEIGHT(N->left), HEIGHT(N->right)) + 1;
			}
		return i;
	} else{
		if (N->left == NULL && N->right == NULL) {
            // N has no child nodes
            if (N->parent != NULL) {
                if (N->parent->left == N) {
                    N->parent->left = NULL;
                } else {
                    N->parent->right = NULL;
                }
            } else {
				// if N is root node
                T->root = NULL;
            }
            free(N);
            T->size -= 1;
        } else if (N->left != NULL && N->right == NULL) {
            // N only has left child node
            if (N->parent != NULL) {
                N->left->parent = N->parent;
                if (N->parent->left == N) {
                    N->parent->left = N->left;
                } else {
                    N->parent->right = N->left;
                }
            } else {
                // if N is root node
                N->left->parent = NULL;
                T->root = N->left;
            }
            free(N);
            T -> size -= 1;
        } else if (N -> left == NULL && N -> right != NULL) {
            // N only has right child node
            if (N -> parent) {
                N->right->parent = N->parent;
                if (N->parent->left == N) {
                    N->parent->left = N->right;
                } else {
                    N->parent->right = N->right;
                }
            } else {
                // if N is root node
                N->right->parent = NULL;
                T->root = N->right;
            }
            free(N);
            T -> size -= 1;
        } else {
            // N has both left and right child nodes
            AVLTreeNode *N2 = N->right;

            while (N2->left) {
                N2 = N2->left;
            }
            N->key = N2->key;
            N->value = N2->value;

            return Delete(T, N2, N2->key, N2->value);
        }
    }
    return 1;
}

//inorder traversal to tranfer tree into array
void Inorder_Array(AVLTreeNode *node, int K[], int V[], int *i) {

	if (node == NULL) {
		return;
	}

	Inorder_Array(node->left, K, V, i);
	K[*i] = node->key; 
	V[*i] = node->value;
	(*i)++;
	Inorder_Array(node->right, K, V, i);

}

//Print Node
void PrintNode(AVLTreeNode *node) {
	if (node != NULL) {
		PrintNode(node->left);
		printf("(%d, %d)\n", node->key, node->value);
		PrintNode(node->right);
	}
}

// for O(m) time complexity in union and intersection
// after inorder traversal, the mid point of the K & V array is the root of new tree
AVLTreeNode *InorderCreate(AVLTree *T, AVLTreeNode *N1, int K[], int V[], int num1, int num2) {
	if (num2 < num1) {
		return NULL;
	}

	int mid = (num1 + num2) / 2;
	AVLTreeNode *N2 = newAVLTreeNode(K[mid], V[mid]);

	if (N1 == NULL) {
		T->root = N2;
	} 

	N2->left = InorderCreate(T, N2, K, V, num1, mid - 1);
	N2->right = InorderCreate(T, N2, K, V, mid + 1, num2);

	N2->parent = N1;
	N2->height = MAX(HEIGHT(N2->left), HEIGHT(N2->right)) + 1;

	return N2;
}