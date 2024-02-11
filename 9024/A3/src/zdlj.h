#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define MAXVEX 46
#define INFI 666

typedef int Status;
typedef struct
{
	int vex[MAXVEX];
	int arc[MAXVEX][MAXVEX];
	int numV;
	int numEdges;
}MGraph;

typedef struct
{
	int data;
	int index1;
	int index2; 
}Bus;

typedef int Path[MAXVEX];
typedef int ShortPathTable[MAXVEX];
				
void ShortestPath_Dijkstra(MGraph *G,int v0,Path *P,ShortPathTable *D,int vd,Bus *bus)
{
	int final[MAXVEX] = {0};
	int i,w,k = 0,min;
	for(i = 0;i < G->numV; i++){
		final[i] = 0;
		(*D)[i] = G->arc[v0][i];
		(*P)[i] = 0;
	}
	(*D)[v0]=0;
	final[v0] = 1;
	(*P)[v0] = -1;
	for(i = 1;i<G->numV;i++){
		min = INFI;
		for(w=0;w<G->numV;w++){
			if(final[w]==0 && (*D)[w]<min){
				k = w;
				min = (*D)[w];
			}
		}
		final[k] = 1;
		for(w=0;w<G->numV;w++){
			if(!final[w] && (min + G->arc[k][w]<(*D)[w])){
				(*D)[w] = min + G->arc[k][w];
				(*P)[w] = k;
			}
		}
	}
	if((*D)[vd]==INFI){
		printf("No route exists from %d to %d\n",v0,vd); 
		return;
	}
	else{
		int j1,i1;
		int k1 = vd;
		printf("Travel route from %d to %d:",v0,vd);
		for( i1=k1;i1>v0+1;i1--){
			for(j1 = 0;j1<86;j1++){
				if(bus[j1].index1==(*P)[i1]){
					if(bus[j1].index2==i1){
						printf("%d ",bus[j1].data);
					}
				}
			}
			printf("(%d,%d)",(*P)[i1],i1);
		}
		for(j1 = 0;j1<86;j1++){
			if(bus[j1].index1==v0){
				if(bus[j1].index2==i1){
					printf("%d ",bus[j1].data);
				}
			}
		}
		printf("(%d,%d)",v0,i1);
	}
}

void CreateMGraph(MGraph *G,int n,int e){
	int i,j;
	G->numV = n;
	G->numEdges = e;
	for(i=0;i<G->numV;i++){
		G->vex[i]=i;
	}
	for(i=0;i<G->numV;i++){
		for(j=0;j<G->numV;j++){
			if(i==j) 
				G->arc[i][j]=0; 
			else 
				G->arc[i][j]=INFI;
		}
	}	
	int x=0;
	char buf[100];
	int EdgeList[55][3];
	memset(EdgeList,0,sizeof(EdgeList));
	const char *delim = "-: ";
	FILE *fp = fopen("Distance.txt", "r");
	while ( fgets(buf,100, fp) != NULL) {
		char *p;
		p = strtok(buf,delim);
		int j=0;
		int temp[3][1];
		memset(temp,0,sizeof(temp));
  		while(p != NULL){
  			int c[1];
  			memset(c,0,sizeof(c));
			sscanf(p,"%d",c);
			temp[j][0] = c[0];
  			p = strtok(NULL,delim);
  			j++;
		}
		for(int i=0;i<3;i++){
			EdgeList[x][i] = temp[i][0];
		}		
		x++;
	}
	for(int i=0;i<55;i++){
		int t1,t2,t3;
		t1 = EdgeList[i][0];
		t2 = EdgeList[i][1];
		t3 = EdgeList[i][2];
		G->arc[t1][t2]=t3;
	}		
}

void TravelRoute(int sourceStop,int destinationStop){
	int i,j;
	Bus bus[86];
	int a[][16] = {{0,1,2,3,0,99,99,99,99,99,99,99,99,99,99,99},
	{6,7,8,9,10,11,6,99,99,99,99,99,99,99,99,99},
	{4,5,6,7,8,9,12,13,14,4,99,99,99,99,99,99},
	{15,16,17,18,19,20,15,99,99,99,99,99,99,99,99,99},
	{19,20,21,22,23,24,19,99,99,99,99,99,99,99,99,99},
	{19,39,40,26,25,23,24,19,99,99,99,99,99,99,99,99},
	{26,27,28,29,39,40,26,99,99,99,99,99,99,99,99,99},
	{39,40,26,27,41,42,43,44,45,29,39,99,99,99,99,99},
	{29,30,31,32,33,43,44,45,29,99,99,99,99,99,99,99},
	{17,31,32,33,34,35,36,37,38,17,99,99,99,99,99,99},
	{26,27,41,42,43,34,35,36,37,38,17,18,19,39,40,26}};
	int b[11]={102,15,303,101,200,105,126,101,98,501,505};
	int k=0;
	for(i=0;i<11;i++){
		for(j=0;j<16;j++){
			bus[k].index1=a[i][j];
			bus[k].index2=a[i][j+1];
			bus[k].data=b[i];
			k++;
		}
	}
	int v0,n,e;
	MGraph G;
	Path P;
	ShortPathTable D;
	n=46;
	e=55;
	int vd;
	CreateMGraph(&G,n,e);
	v0 = sourceStop;
	vd = destinationStop;
	ShortestPath_Dijkstra(&G, v0, &P, &D,vd,bus);	
}
