#!/bin/bash

# 현재 시간 기준 60초 뒤의 Unix Epoch 시간 계산
expires=$(date -d "+60 seconds" +%s)

# MD5 해시 생성
md5=$(echo -n "/download${expires} secret" | \
    openssl md5 -binary | openssl base64 | tr +/ -_ | tr -d =)

# 결과 출력 (MD5 해시와 만료 시간)
echo "MD5: $md5"
echo "Expires: $expires"