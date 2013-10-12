#!/bin/bash

DATADIR="data"

if [ ! -d $DATADIR ]; then
    mkdir data;
fi

cd data;

for url in `cat ../urls`; do
    wget "$url"
done
