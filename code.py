#! /usr/bin/env python3
import os
import shutil
import subprocess
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--download', default=False, action='store_true', help='download, configure new package')
parser.add_argument('-f', '--file', action='store', help='directory to file for check')
parser.add_argument('-c', '--check', default=False, action='store_true', help='check starting')

def prepare():
    try:
        shutil.rmtree('./ffmpeg_source')
        print('clear old files')
    except:
        d = os.listdir('.')
        if 'ffmpeg_source' not in d:
            print('dir is not exist')
        else:
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
        os.chdir('./ffmpeg')
        print('changed workingdir to "./ffmpeg"')
    except:
        print('extract error')
        sys.exit(1)
    try:
        st = os.stat('configure')
        os.chmod('configure', st.st_mode|0o111)
        print('doing chmod to "configure"')
    except:
        print('chmod for "configure" fail')
        sys.exit(1)


def configure():
    varpath = os.environ["PATH"]
    varhome = os.environ["HOME"]
    path = '{0}/bin:{1}'.format(varhome, varpath)
    os.environ['PATH'] = path
    pkgpath = '{0}/ffmpeg_build/lib/pkgconfig'.format(varhome)
    os.environ['PKG_CONFIG_PATH'] = pkgpath
    configure = ['./configure', '--prefix={0}/ffmpeg_build'.format(varhome), '--pkg-config-flags=--static', \
        '--extra-cflags=-I{0}/ffmpeg_build/include'.format(varhome), '--extra-ldflags=-L{0}/ffmpeg_build/lib'.format(varhome), \
        '--extra-libs=-lpthread -lm', '--bindir={0}/bin'.format(varhome), '--enable-nonfree']
    hashcom = ['hash', '-r']
    try:
        subprocess.check_call(configure)
        print('configure package')
    except:
        print('configure error')
        sys.exit(1)
    path = '{0}/bin:{1}'.format(varhome, varpath)
    os.environ["PATH"] = path
    makecom = ['make']
    try:
        subprocess.check_call(makecom)
        print('make success')
    except:
        print('make error')
        sys.exit(1)
    makecom2 = ['make', 'install']
    try:
        subprocess.check_call(makecom2)
        print('install success')
    except:
        print('install error')
        sys.exit(1)
    hashcom = ['hash', '-r']
    try:
        subprocess.check_call(hashcom)
        print('hash success')
    except:
        print('hash error')
        #sys.exit(1)


def main():
    args = parser.parse_args()
    print(args.download, args.file)
    if args.download is True:
        print('installing new package of ffmpeg:')
        prepare()
        downloading()
        unpack()
        configure()
    else:
        varhome = os.environ['HOME']
        path = '{0}/bin'.format(varhome)
        comforcheck = ['./ffmpeg', '-version']
        if args.check is True:
            try:
                os.chdir(path)
                subprocess.check_call(comforcheck, timeout=10)
                print('check is success')
            except:
                print('check failed')
        if args.file is None:
            sys.exit(0)
        if args.file is not None:
            print('video must be converted, but i cant yet')


if  __name__ ==  "__main__" : main()
