#!/usr/bin/env bash
# name src_start src_dur
set -e
N=$1; SS=$2; T=$3
ffmpeg -v error -y -ss $SS -t $T -i canva-reel.mp4 -an -c:v libx264 -crf 12 -preset veryfast raw_$N.mp4
ffmpeg -v error -y -i raw_$N.mp4 -vf vidstabdetect=shakiness=6:accuracy=15:result=$N.trf -f null -
ffmpeg -v error -y -i raw_$N.mp4 -vf "vidstabtransform=input=$N.trf:smoothing=24:zoom=6:optzoom=0,unsharp=5:5:0.4,hqdn3d=2:2:5:5,eq=gamma=1.12:contrast=1.04:saturation=0.92,colorbalance=rs=0.05:gs=0.01:bs=-0.05:rm=0.04:bm=-0.04,setpts=PTS/0.6,fps=30,scale=1080:1920:flags=lanczos" -c:v libx264 -crf 15 -pix_fmt yuv420p -preset medium seg_$N.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 seg_$N.mp4
