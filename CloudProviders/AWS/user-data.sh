#!/bin/bash

sudo su

yum install -y git
git clone https://github.com/JChubbs/WetLadder-Server
cd WetLadder-Server
set my_ip
echo "APP_ENV=prd" > .env
echo "VPN_HOST=$(dig +short myip.opendns.com @resolver1.opendns.com)" >> .env
yum install -y make
make setup
nohup python3 run.py &
