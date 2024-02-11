//Ruohao Chen
//z5111287

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>
#include<stdbool.h>
#include"function4.h"

int main() {
	//Function1
	StronglyConnectivity("busStops.txt", "BusNames.txt", "BusRoutes.txt", "Distance.txt");
	//Function2
	maximalStronlyComponents("busStops.txt", "BusNames.txt", "BusRoutes.txt", "Distance.txt");
	//Function3
	reachableStops("George Street","busStops.txt", "BusNames.txt", "BusRoutes.txt", "Distance.txt");
	//Function4
	TravelRoute("Cumberland","South Head","busStops.txt", "BusNames.txt", "BusRoutes.txt", "Distance.txt");
	return 0;
}