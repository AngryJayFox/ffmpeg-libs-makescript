#! /usr/bin/env python3
import os
import shutil
import subprocess
try:
    shutil.rmtree('./ffmpeg_source')
    print('clear old files')
except:
    print('dir is not exist')
os.mkdir('./ffmpeg_source')
print('create new dir')
os.chdir('./ffmpeg_source')
print('changed workingdir to "ffmpeg_source"')
print('downloading sources')
wgetcom = []
wgetcom.extend(['wget', '-O', './ffmpeg-snapshot.tar.bz2', 'http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2'])
try:
    subprocess.check_call(wgetcom)
    print('download is ok!')
except:
    print('download error!')
tarcom = []
tarcom.extend(['tar', 'xjvf', './ffmpeg-snapshot.tar.bz2'])
try:
    subprocess.check_call(tarcom)
    print('extract success')
except:
    print('extract error')
