#include<stdio.h>
#include<stdlib.h>
#include"StronglyConnectivity.h"
#include"gdbl.h" 
#include"zdlj.h"

int main(){
	//Function1
	int x,v0,vd;
	StronglyConnectivity();
	//Function2
	maximalStronlyComponents();
	//Function3
	printf("Please enter the starting vertex\n");
	scanf("%d",&x);
	reachableStops(x);
	//Function4
	printf("Please enter the starting vertex\n");
	scanf("%d",&v0);
	printf("Please enter the starting vertex\n");
	scanf("%d",&vd);
	TravelRoute(v0,vd);
	
	return 0;
}
