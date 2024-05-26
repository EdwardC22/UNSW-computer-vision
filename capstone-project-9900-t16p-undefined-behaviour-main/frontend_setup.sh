#!/bin/bash
apt-get update -y 
apt install npm -y
npm install n -g -y
n latest
cd frontend
npm install
mkdir node_modules/.cache && chmod -R 777 node_modules/.cache
npm start
