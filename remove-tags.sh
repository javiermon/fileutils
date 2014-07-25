#!/bin/bash
ffmpeg -i $1 -acodec copy copy-$1
mv copy-$1 $1
