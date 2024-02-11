//Ruohao Chen
//z5111287

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<stdbool.h>
#include"function123.h"

#define MAXVEX 100
#define INFI 999

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
		if (num == i) {
			return p2;
		}
	}
    fclose(fp);
}
				
void ShortestPath_Dijkstra(MGraph *G,int v0,Path *P,ShortPathTable *D,int vd,Bus *bus,int numS, const char *busStops)
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
			for(j1 = 0;j1<numS;j1++){
				if(bus[j1].index1==(*P)[i1]){
					if(bus[j1].index2==i1){
						printf("%d ",bus[j1].data);
					}
				}
			}
            char name1[100];
            char name2[100];
            strcpy(name1,search_name((*P)[i1],busStops));
            strcpy(name2,search_name(i1,busStops));
			printf("(%s,%s)\n",name1,name2);
		}
		for(j1 = 0;j1<numS;j1++){
			if(bus[j1].index1==v0){
				if(bus[j1].index2==i1){
					printf("%d ",bus[j1].data);
				}
			}
		}
        char name1[100];
        char name2[100];
        strcpy(name1,search_name(v0,busStops));
        strcpy(name2,search_name(i1,busStops));
		printf("(%s,%s)\n",name1,name2);
	}
}

void CreateMGraph(MGraph *G,int n,int e, const char *Distance){
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
    int numE = Count_Row(Distance);
	int EdgeList[numE][3];
	memset(EdgeList,0,sizeof(EdgeList));
	char *delim = "-: ";
	FILE *fp = fopen(Distance, "r");
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
	for(int i=0;i<numE;i++){
		int t1,t2,t3;
		t1 = EdgeList[i][0];
		t2 = EdgeList[i][1];
		t3 = EdgeList[i][2];
		G->arc[t1][t2]=t3;
	}		
}
void TravelRoute(const char *sourceStop, const char *destinationStop, const char *busStops, const char *BusNames, const char *BusRoutes, const char *Distance){
	int en = Count_Row(Distance);
	
	int dn = Count_Row(busStops);
		
	int i,j,v0,vd;
	v0 = search(sourceStop,busStops);
	vd = search(destinationStop,busStops);
	int k=0;
	int count1=0;
	int maxbuflen=0;
	int sumpoint=0;
	char buf1[100];
	char *delim = ":,";
	FILE *filep = fopen(BusRoutes, "r");
	while (fgets(buf1,100, filep) != NULL) {
		char *p1;
		char *p;
		int rangenum=0;
		char temp[100];
		strcpy(temp,buf1);
		p1 = strtok(temp,delim);
		while(p1 != NULL){
			rangenum++;
	 		p1 = strtok(NULL,delim);
		}
		int busname[1];
		int point[rangenum-1];
		if(maxbuflen == 0){
			maxbuflen = rangenum-1;
		}
		else if(rangenum-1 > maxbuflen){
			maxbuflen = rangenum-1;
		}
		sumpoint += rangenum-2;
		p = strtok(buf1,delim);
		int srange=0;
		while(p != NULL){
	 		int c[1];
	 		memset(c,0,sizeof(c));
			sscanf(p,"%d",c);
	 		if(srange==0){
	  			busname[0] = c[0]; 
			}
			else{
				point[srange-1] = c[0];
			}
			srange++;
			p = strtok(NULL,delim);
		}
		count1++;
	}
	int numS = count1*maxbuflen;
	Bus bus[numS];
	int a[count1][maxbuflen];
	memset(a,0,sizeof(a));
	for(int i=0;i<count1;i++){
		for(int j=0;j<maxbuflen;j++){
			a[i][j]=-2;
		}
	}
	int b[count1];
	memset(b,0,sizeof(b));
	fclose(filep);
	FILE *filep1 = fopen(BusRoutes, "r");
	int count2=0;
	while ( fgets(buf1,100, filep1) != NULL) {
		char *p1;
		char *p;
		int rangenum=0;
		char temp[100];
		strcpy(temp,buf1);
		p1 = strtok(temp,delim);
		while(p1 != NULL){
			rangenum++;
	 		p1 = strtok(NULL,delim);
		}
		int point[rangenum-1];
		p = strtok(buf1,delim);
		int srange=0;
		while(p != NULL){
	 		int c[1];
	 		memset(c,0,sizeof(c));
			sscanf(p,"%d",c);
	 		if(srange==0){
				b[count2] = c[0]; 
			}
			else{
				point[srange-1] = c[0];
				a[count2][srange-1] = c[0];
			}
			srange++;
			p = strtok(NULL,delim);
		}
		count2++;
	
	} 
	fclose(filep1);
	for(i=0;i<count1;i++){
		for(j=0;j<maxbuflen;j++){
			bus[k].index1=a[i][j];
			bus[k].index2=a[i][j+1];
			bus[k].data=b[i];
			k++;
		}
	}
	MGraph G;
	Path P;
	ShortPathTable D;
	CreateMGraph(&G,dn,en,Distance);
	ShortestPath_Dijkstra(&G, v0, &P, &D,vd,bus,numS,busStops);	
}
