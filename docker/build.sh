#!/usr/bin/env bash

docker build --no-cache --tag kexanone/apyllo -f $(dirname "$0")/dockerfile $(dirname "$0")/../..
