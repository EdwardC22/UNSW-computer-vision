#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MaxVertexNum 100  
#define MaxSize 10 
//������Ŀ�����ֵ 
bool visitedBFS[MaxVertexNum]; 

typedef  char VertexType;
typedef int EdgeType; 

typedef struct ArcNode{
	EdgeType adjNode;
	ArcNode *next; 
}ArcNode; 

typedef struct VN{
	VertexType data;
	ArcNode *first;
}VN,Adj[MaxVertexNum];

typedef struct ALGraph{
	Adj vertices;
	int vexnum,arcnum;
}ALGraph;
 
void createGraph(ALGraph &g){
	int n,m;
	n=46;
	m=55;
	g.vexnum=n;
	g.arcnum=m;
	for(int i=0;i<g.vexnum;i++){
		g.vertices[i].data=i;
		g.vertices[i].first=NULL; 
	}
	int x,y;
	int n1=0;
	char buf[100];
	int EdgeList[55][3]; 
	memset(EdgeList,0,sizeof(EdgeList));
	const char *delim = "-:";
	FILE *fp = fopen("Distance.txt", "r");
	while ( fgets(buf,100, fp) != NULL) {
		char *p1;
		p1 = strtok(buf,delim);
		int j=0;
		int temp[EdgeNum][1];
		memset(temp,0,sizeof(temp));
  		while(p1 != NULL){
  			int c[1];
  			memset(c,0,sizeof(c));
			sscanf(p1,"%d",c);
			temp[j][0] = c[0];
  			p1 = strtok(NULL,delim);
  			j++;
		}
		for(int i=0;i<EdgeNum;i++){
			EdgeList[n1][i] = temp[i][0];
		}		
		n1++;
	}
	for(int i=0;i<g.arcnum;i++){
		x = EdgeList[i][0];
		y = EdgeList[i][1];
		ArcNode *p =(ArcNode*)malloc(sizeof(ArcNode));
		p->adjNode=y;
		p->next=g.vertices[x].first;
		g.vertices[x].first=p;
		
		ArcNode *q=(ArcNode*)malloc(sizeof(ArcNode));
		q->adjNode=x;
		q->next=g.vertices[y].first;
		g.vertices[y].first=q;
	}
} 
 
void BFS_Graph(ALGraph g,int v){
	int n2=0;
	char buf2[100];
	char name2[46][20];
	const char *delim =":";
	FILE *fp = fopen("BusStops.txt", "r");
	while (fgets(buf2,100,fp) != NULL) {
		char *p2;
		p2 = strtok(buf2,delim);
		p2 = strtok(NULL,delim);
		strcpy(name2[n2],p2);	
		n2++; 
	}
	visitedBFS[v]=true;
	ArcNode *p;
	int que[MaxSize];
	int front=0,rear=0;
	rear=(rear+1)%MaxSize;
	que[rear]= v;
	int j;
	while(rear!=front){
		front=(front+1)%MaxSize;
		j =que[front];
		p =g.vertices[j].first;
		while(p!=NULL){
			if(!visitedBFS[p->adjNode]){
			
				printf("%s\n",name2[g.vertices[p->adjNode].data]);
				
				visitedBFS[p->adjNode]=true;
				rear=(rear+1)%MaxSize;
				que[rear]=p->adjNode; 
			}
			p=p->next;	
		}	
	} 
} 
  
void reachableStops(int x){
	int busname;
	ALGraph g;
	createGraph(g);
	busname = x;
	printf("\nBreadth first traversal order:\n");
	BFS_Graph(g,busname); 
} 

