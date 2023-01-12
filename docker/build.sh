#!/usr/bin/env bash

NAME="kexanone/apyllo"
VERSION=$(cd $(dirname "$0")/..; python3 -c 'import apyllo; print(apyllo.__version__)')
docker build --no-cache --tag $NAME:latest --tag $NAME:$VERSION -f $(dirname "$0")/dockerfile $(dirname "$0")/../..
