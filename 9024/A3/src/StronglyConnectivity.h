#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>


#define Max_Node 46
#define Max_Edges 55
#define NodeType int
#define WeightType int
#define NodeNum 2
#define EdgeNum 3

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

int Locate(GraphList G,NodeType Node){
	for(int i=0;i<G.NodeNums;i++){
		if(Node==G.adjlist[i].data){
			return i;
		}
	}
	return 0;
}
 
void CreateGraph(GraphList *G){
	int StartPoint,EndPoint,Weight;
	int PosStartPoint,PosEndPoint;
	ENode* p;
	char bufs[NodeNum];
	int PointList[Max_Node];
	int k=0;
	FILE *fp1 = fopen("BusStops.txt", "r");
	while ( fgets(bufs, 100, fp1) != NULL) {
		if ( sscanf(bufs,"%2d",&PointList[k]) == 1){ 
			k++; 
		}
	}
	int n=0;
	char buf[100];
	int EdgeList[55][3]; 
	memset(EdgeList,0,sizeof(EdgeList));
	const char *delim = "-:";
	FILE *fp = fopen("Distance.txt", "r");
	while ( fgets(buf,100, fp) != NULL) {
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
	G->Edges = Max_Edges;
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

void TarJan(int i,GraphList *G){
	int j;
	DFN[i] = LOW[i] = ++Index;
	Stack[Index-1] = G->adjlist[i].data;
	Visit[i] = 1;
	ENode* p;
	p = G->adjlist[i].FirstNode;
	while(p){
		j=Locate(*G,p->adjvex);
		if(DFN[j]==0){
			TarJan(j,G);
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

void TarJan1(int i,GraphList *G){
	int j;
	DFN[i] = LOW[i] = ++Index;
	Stack[Index-1] = G->adjlist[i].data;
	Visit[i] = 1;
	ENode* p;
	p = G->adjlist[i].FirstNode;
	while(p){
		j=Locate(*G,p->adjvex);
		if(DFN[j]==0){
			TarJan1(j,G);
			LOW[i] = LOW[j]>LOW[i]?LOW[i]:LOW[j];
		}
		else if(Visit[j]==1){
			LOW[i] = LOW[i]>DFN[j]?DFN[j]:LOW[i];
		}
		p = p->next;
	}
	if(DFN[i]==LOW[i]){
		count1++;
		int m=0;
		for(m;m<10;m++){
			if(G->adjlist[i].data==Stack[m]){
				break;
			}
		}
		int k=0;
		int top = Index-1; 
		for(k=m;k<=top;k++){
			Visit[Locate(*G,Stack[k])] = 0;
			Stack[k] = -1;
			--Index;
		}
	}
}

void StronglyConnectivity(){
	memset(DFN,0,sizeof(DFN));
	memset(LOW,0,sizeof(LOW));
	memset(Stack,-1,sizeof(Stack));
	memset(Visit,0,sizeof(Visit));
	
	static GraphList Graph;
	CreateGraph(&Graph);
	
	for(int i=0;i<(&Graph)->NodeNums;i++){
		if(DFN[i]==0){
			TarJan1(i,(&Graph));
		}
	}
	
	if(count1>1){
		printf("0\n");
	}
	else{
		printf("1\n");
	}
}

void  maximalStronlyComponents(){
	memset(DFN,0,sizeof(DFN));
	memset(LOW,0,sizeof(LOW));
	memset(Stack,-1,sizeof(Stack));
	memset(Visit,0,sizeof(Visit));
	
	GraphList Graph;
	CreateGraph(&Graph);
	
	for(int i=0;i<(&Graph)->NodeNums;i++){
		if(DFN[i]==0){
			TarJan(i,(&Graph));
		}
	}

}



