#! /usr/bin/env python3
import os
import shutil
import subprocess
import sys
import argparse
import urllib.request
import tarfile

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--download', default=False, action='store_true', help='download and unpack new package')
parser.add_argument('-c', '--configure', default=False, action='store_true', help='configure and install downloaded package')
parser.add_argument('-if', '--ifile', action='store', help='directory to file for check')
parser.add_argument('-ch', '--check', default=False, action='store_true', help='check starting')
parser.add_argument('--shared', default=False, action='store_true', help='switch to "shared" build. "static" in default configuration')


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
    print('created new dir')


def downloading():
    os.chdir('./ffmpeg_source')
    print('changed workingdir to "ffmpeg_source"')
    print('downloading sources')
    try:
        url = 'http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2'
        urllib.request.urlretrieve(url, 'ffmpeg-snapshot.tar.bz2')
        print('download is ok!')
    except:
        print('download error!')
        sys.exit(1)


def unpack():
    try:
        tar = tarfile.open('./ffmpeg-snapshot.tar.bz2', 'r:bz2')
        tar.extractall()
        print('extract success')
        os.chdir('./ffmpeg')
        print('changed workingdir to "./ffmpeg"')
    except:
        print('extract error')
        sys.exit(1)


def configure(args):
    if args.download is False:
        os.chdir('./ffmpeg_source/ffmpeg')
    try:
        st = os.stat('configure')
        os.chmod('configure', st.st_mode|0o111)
        print('doing chmod to "configure"')
    except:
        print('chmod for "configure" fail')
        sys.exit(1)
    varpath = os.environ["PATH"]
    varhome = os.environ["HOME"]
    path = '{0}/bin:{1}'.format(varhome, varpath)
    os.environ['PATH'] = path
    pkgpath = '{0}/ffmpeg_build/lib/pkgconfig'.format(varhome)
    os.environ['PKG_CONFIG_PATH'] = pkgpath
    configure = ['./configure', '--prefix={0}/ffmpeg_build'.format(varhome), '--pkg-config-flags=--static',
                     '--extra-cflags=-I{0}/ffmpeg_build/include'.format(varhome),
                     '--extra-ldflags=-L{0}/ffmpeg_build/lib'.format(varhome),
                     '--extra-libs=-lpthread -lm', '--bindir={0}/bin'.format(varhome), '--enable-nonfree']
    if args.shared is True:
        configure.extend['--disable-static', '--enable-shared']
    else:
        configure.extend['--disable-shared', '--enable-static']
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


def checking(args):
    varhome = os.environ['HOME']
    path = '{0}/bin'.format(varhome)
    ldlib = '{0}/ffmpeg_build/lib'.format(varhome)
    os.environ['LD_LIBRARY_PATH'] = ldlib
    print(ldlib)
    comforcheck = ['./ffmpeg', '-version']
    try:
        os.chdir(path)
        subprocess.check_call(comforcheck, timeout=10)
        print('check is success')
    except:
        print('check failed')


def main():
    args = parser.parse_args()
    if args.download is True:
        print('installing new package of ffmpeg:')
        prepare()
        downloading()
        unpack()
    if args.configure is True:
        configure(args)
    if args.check is True:
        checking(args)
    if args.ifile is not None:
        print('inputfile choised, but functional is not ready')
        sys.exit(0)
#    if args.ofile is not None:
#        print('outputfile choised, but functional is not ready')


if  __name__ ==  "__main__" :
    main()
