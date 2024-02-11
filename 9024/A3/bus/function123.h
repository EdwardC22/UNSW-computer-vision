//Ruohao Chen
//z5111287

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>
#include<stdbool.h>

#define Max_Node 100
#define NodeType int
#define WeightType int
#define NodeNum 2
#define EdgeNum 3
#define MaxSize 10 

bool visitedBFS[Max_Node]; 
int Visit[Max_Node];
int count=0;
int count1=0;
int Index=0;
int LOW[Max_Node];
int DFN[Max_Node];
int Stack[Max_Node];  

typedef struct ENode{
	NodeType adjvex;
	WeightType weight;
	struct ENode *next;
}ENode;

typedef struct VNode{
	NodeType data;
	ENode *FirstNode;
}VNode,AdjList[Max_Node];

typedef struct GraphList{
	AdjList adjlist;
	int NodeNums;
	int Edges;
}GraphList;

//main function declaration
int StronglyConnectivity(const char *busStops, const char *BusNames, const char *BusRoutes, const char *Distance);
void maximalStronlyComponents(const char *busStops, const char *BusNames, const char *BusRoutes, const char *Distance);
void reachableStops(const char *sourceStop, const char *busStops, const char *BusNames, const char *BusRoutes, const char *Distance);

// auxiliary function declaration
int Locate(GraphList G,NodeType Node);
int Count_Row(const char *filename);
void CreateGraph(GraphList *G, const char *busStops, const char *Distance);
void TarJan(int i,GraphList *G, const char *filename);
void TarJan1(int i,GraphList *G, const char *filename);
int search(const char *name, const char *busStops);
void BFS_Graph(GraphList g,int v,const char *busStops);


int search(const char *name, const char *busStops) {
	FILE *fp = fopen(busStops, "r");
	char buf2[100];
	const char *delim =":";
	while (fgets(buf2,100,fp) != NULL) {
		char *p2;
		char *p1;
		p1 = strtok(buf2,delim);
		int num = atoi(p1);
		p2 = strtok(NULL,delim);
		if (strncmp (name, p2, (strlen(p2) -1)) == 0) {
			return num;
		}
		if (strcmp(name,p2) == 0) {
			return num;
		}
	}
	return -1;
}

int Count_Row(const char *filename) {
    FILE *fp = fopen(filename, "r");
    char buf[100];
    int i = 0;
    while (fgets(buf,100,fp) != NULL) {
        i++;
    }
	fclose(fp);
    return i;
}

int Locate(GraphList G,NodeType Node) {
	for(int i = 0; i < G.NodeNums; i++)
		if(Node == G.adjlist[i].data)
			return i;
}

void CreateGraph(GraphList *G, const char *busStops, const char *Distance) {
	int StartPoint,EndPoint,Weight;
	int PosStartPoint,PosEndPoint;
	ENode* p;
    int num = Count_Row(busStops);
	char bufs[NodeNum];
	int PointList[num];
	int k=0;
    int Edges = Count_Row(Distance);
	FILE *fp1 = fopen(busStops, "r");

	while ( fgets(bufs, 100, fp1) != NULL) {
		if ( sscanf(bufs, "%2d", &PointList[k]) == 1){ 
			k++; 
		}
	}
	int n=0;
	char buf[100];
	int EdgeList[Edges][3]; 
	memset(EdgeList,0,sizeof(EdgeList));
	const char *delim = "-:";
	FILE *fp = fopen(Distance, "r");
	while ( fgets(buf, 100, fp) != NULL) {
		char *p;
		p = strtok(buf,delim);
		int j=0;
		int temp[EdgeNum][1];
		memset(temp,0,sizeof(temp));
  		while(p != NULL){
  			int c[1];
  			memset(c,0,sizeof(c));
			sscanf(p,"%d",c);
			temp[j][0] = c[0];
  			p = strtok(NULL,delim);
  			j++;
		}
		for(int i=0;i<EdgeNum;i++){
			EdgeList[n][i] = temp[i][0];
		}		
		n++;
	}
	G->NodeNums = Max_Node;
	G->Edges = Edges;
	for(int i=0;i<G->NodeNums;i++){
		G->adjlist[i].data = PointList[i];
		G->adjlist[i].FirstNode = NULL;
	}
	for(int i=0;i<G->Edges;i++){
		StartPoint = EdgeList[i][0];
		EndPoint = EdgeList[i][1];
		Weight = EdgeList[i][2];
		PosStartPoint = Locate(*G,StartPoint);
		PosEndPoint = Locate(*G,EndPoint);
		p = (ENode *)malloc(sizeof(ENode));
		p->adjvex = EndPoint;
		p->weight = Weight;
		p->next = G->adjlist[PosStartPoint].FirstNode;
		G->adjlist[PosStartPoint].FirstNode = p;
	} 
	
} 

void TarJan(int i,GraphList *G, const char *filename){
	int j;
	int num = Count_Row(filename);

	if (i >= num) {
		return;
	}

	DFN[i] = LOW[i] = ++Index;
	Stack[Index-1] = G->adjlist[i].data;
	Visit[i] = 1;
	ENode* p;
	p = G->adjlist[i].FirstNode;
	while(p){
		j=Locate(*G,p->adjvex);
		if(DFN[j]==0){
			TarJan(j,G, filename);
			LOW[i] = LOW[j]>LOW[i]?LOW[i]:LOW[j];
		}
		else if(Visit[j]==1){
			LOW[i] = LOW[i]>DFN[j]?DFN[j]:LOW[i];
		}
		p = p->next;
	}

	if(DFN[i]==LOW[i]){
		count++;
		int m=0;
		for(m;m<10;m++){
			if(G->adjlist[i].data==Stack[m]){
				break;
			}
		}
		int k=0;
		int top = Index-1; 
		printf("Strongly connected component %d: \n",count);
		for(k=m;k<=top;k++){
			printf("bus stop%d of this strongly connected component ;\n",Stack[k]);
			Visit[Locate(*G,Stack[k])] = 0;
			Stack[k] = -1;
			--Index;
		}
		printf("\n");
	}
}

void TarJan1(int i,GraphList *G, const char *filename) {
	int j;
	int num = Count_Row(filename);

	if (i >= num) {
		return;
	}

	DFN[i] = LOW[i] = ++Index;
	Stack[Index-1] = G->adjlist[i].data;
	Visit[i] = 1;
	ENode* p;
	p = G->adjlist[i].FirstNode;
	while(p){
		j=Locate(*G,p->adjvex);
		if(DFN[j]==0){
			TarJan1(j,G,filename);
			LOW[i] = LOW[j]>LOW[i]?LOW[i]:LOW[j];
		}
		else if(Visit[j]==1){
			LOW[i] = LOW[i]>DFN[j]?DFN[j]:LOW[i];
		}
		p = p->next;
	}
	if(DFN[i]==LOW[i]) {
		count1++;
		int m=0;
		for(m;m<10;m++) {
			if(G->adjlist[i].data==Stack[m]){
				break;
			}
		}
		int k=0;
		int top = Index-1; 
		for(k=m;k<=top;k++) {
			Visit[Locate(*G,Stack[k])] = 0;
			Stack[k] = -1;
			--Index;
		}
	}
}

int StronglyConnectivity(const char *busStops, const char *BusNames, const char *BusRoutes, const char *Distance) {
	memset(DFN,0,sizeof(DFN));
	memset(LOW,0,sizeof(LOW));
	memset(Stack,-1,sizeof(Stack));
	memset(Visit,0,sizeof(Visit));
	
	static GraphList Graph;
	CreateGraph(&Graph, busStops, Distance);
	
	for(int i=0;i<(&Graph)->NodeNums;i++) {
		if(DFN[i]==0){
			TarJan1(i,(&Graph), busStops);
		}
	}
	
	if(count1>1){
		return 0;
	}
    return 1;
}

void maximalStronlyComponents(const char *busStops, const char *BusNames, const char *BusRoutes, const char *Distance) {
	memset(DFN,0,sizeof(DFN));
	memset(LOW,0,sizeof(LOW));
	memset(Stack,-1,sizeof(Stack));
	memset(Visit,0,sizeof(Visit));
	
	GraphList Graph;
	CreateGraph(&Graph, busStops, Distance);
	
	for(int i=0;i < (&Graph)->NodeNums;i++){
		if(DFN[i]==0){
			TarJan(i,(&Graph),busStops);
		}
	}
}


void BFS_Graph(GraphList g,int v,const char *busStops) {
	int n2=0;
	char buf2[100];
    int count1 = Count_Row(busStops);
	char name2[count1][20];
	char *delim = ":";
	FILE *fp = fopen(busStops, "r");
	while (fgets(buf2,100,fp) != NULL) {
		char *p2;
		p2 = strtok(buf2,delim);
		p2 = strtok(NULL,delim);
		strcpy(name2[n2],p2);	
		n2++; 
	}
	visitedBFS[v]=true;
	ENode *p;
	int que[MaxSize];
	int front=0,rear=0;
	rear=(rear+1)%MaxSize;
	que[rear]= v;
	int j;
	while(rear!=front){
		front=(front+1)%MaxSize;
		j =que[front];
		p = g.adjlist[j].FirstNode;
		while(p!=NULL){
			if(!visitedBFS[p->adjvex]){			
				printf("%s\n",name2[g.adjlist[p->adjvex].data]);
				visitedBFS[p->adjvex]=true;
				rear=(rear+1)%MaxSize;
				que[rear]=p->adjvex; 
			}
			p=p->next;	
		}	
	} 
}

void reachableStops(const char *sourceStop, const char *busStops, const char *BusNames, const char *BusRoutes , const char *Distance){
	int busnum = search(sourceStop, busStops);
    if (busnum == -1) {
        printf("bus stop do not exist.");
        return;
    }
	GraphList Graph;

	printf("The reachable stops are:\n");
	BFS_Graph(Graph,busnum,busStops);
} 