#!/bin/bash

sudo su

yum install -y git golang
git clone --recurse-submodules https://github.com/JChubbs/WetLadder-Server
cd WetLadder-Server
echo "APP_ENV=prd" > .env
echo "VPN_HOST=$(dig +short myip.opendns.com @resolver1.opendns.com)" >> .env
yum install -y make
export HOME="/root"
make setup
nohup python3 run.py &
