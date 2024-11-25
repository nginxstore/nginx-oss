#!/bin/bash
echo -n '/download2147483647 secret' | \
    openssl md5 -binary | openssl base64 | tr +/ -_ | tr -d =