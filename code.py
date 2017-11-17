#! /usr/bin/env python3
import os
import shutil
import subprocess
import sys


def prepare():
    try:
        shutil.rmtree('./ffmpeg_source')
        print('clear old files')
    except:
        print('dir is not exist')
        sys.exit(1)
    os.mkdir('./ffmpeg_source')
    print('create new dir')
    os.chdir('./ffmpeg_source')
    print('changed workingdir to "ffmpeg_source"')


def downloading():
    print('downloading sources')
    wgetcom = ['wget', '-O',  'ffmpeg-snapshot.tar.bz2', 'http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2']
    try:
        subprocess.check_call(wgetcom)
        print('download is ok!')
    except:
        print('download error!')
        sys.exit(1)


def unpack():
    tarcom = ['tar', 'xjvf', './ffmpeg-snapshot.tar.bz2']
    try:
        subprocess.check_call(tarcom)
        print('extract success')
    except:
        print('extract error')
        sys.exit(1)


def main():
    prepare()
    downloading()
    unpack()
    
main()
