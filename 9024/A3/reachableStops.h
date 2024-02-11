#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<stdbool.h>

#define MaxVertexNum 100  
#define MaxSize 10 
#define EdgeNum 3

bool visitedBFS[MaxVertexNum]; 

typedef  char VertexType;
typedef int EdgeType; 


typedef struct ArcNode{
	EdgeType adjNode;
	struct ArcNode *next; 
}ArcNode; 

typedef struct VN{
	VertexType data;
	ArcNode *first;
}VN,Adj[MaxVertexNum];

typedef struct ALGraph{
	Adj vertices;
	int vexnum,arcnum;
}ALGraph;

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

void createGraph(ALGraph *g,const char *Distance, const char *busStops){
    int count1 = Count_Row(Distance);
	
    int count2 = Count_Row(busStops);
	
	g->arcnum=count1;
    g->vexnum=count2;

	for(int i=0;i<g->vexnum;i++){
		g->vertices[i].data=i;
		g->vertices[i].first=NULL; 
	}

	int x,y;
	int n1=0;
	char buf[100];
	int EdgeList[count1][3]; 
	memset(EdgeList,0,sizeof(EdgeList));
	char *delim = "-:";
	FILE *fp = fopen(Distance, "r");
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
	for(int i=0;i<g->arcnum;i++){
		x = EdgeList[i][0];
		y = EdgeList[i][1];
		ArcNode *p =(ArcNode*)malloc(sizeof(ArcNode));
		p->adjNode=y;
		p->next=g->vertices[x].first;
		g->vertices[x].first=p;
		
		ArcNode *q=(ArcNode*)malloc(sizeof(ArcNode));
		q->adjNode=x;
		q->next=g->vertices[y].first;
		g->vertices[y].first=q;
	}
} 
 
void BFS_Graph(ALGraph g,int v,const char *busStops){
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


  
void reachableStops(const char *sourceStop, const char *busStops, const char *BusNames, const char *BusRoutes , const char *Distance){
	int busnum = search(sourceStop, busStops);
    if (busnum == -1) {
        printf("bus stop do not exist.");
        return;
    }
	ALGraph g;
	createGraph(&g,Distance,busStops);

	printf("The reachable stops are:\n");
	BFS_Graph(g,busnum,busStops);
} 

