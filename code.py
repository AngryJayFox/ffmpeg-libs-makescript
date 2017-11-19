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
parser.add_argument('-p', '--path', action='store', help='destination path')
parser.add_argument('--libx264', default=False, action='store_true', help='download and install libx264')

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
    if args.path is None:
        varhome = os.environ["HOME"]
    else:
        varhome = args.path
    path = '{0}/bin:{1}'.format(varhome, varpath)
    os.environ['PATH'] = path
    pkgpath = '{0}/ffmpeg_build/lib/pkgconfig'.format(varhome)
    os.environ['PKG_CONFIG_PATH'] = pkgpath
    configure = ['./configure', '--prefix={0}/ffmpeg_build'.format(varhome), '--pkg-config-flags=--static',
                     '--extra-cflags=-I{0}/ffmpeg_build/include'.format(varhome),
                     '--extra-ldflags=-L{0}/ffmpeg_build/lib'.format(varhome),
                     '--extra-libs=-lpthread -lm', '--bindir={0}/bin'.format(varhome), '--enable-nonfree']
    if args.shared is True:
        configure.extend(['--disable-static', '--enable-shared'])
    else:
        configure.extend(['--disable-shared', '--enable-static'])
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


def libx264(args):
    if args.download is False:
        os.chdir('./ffmpeg_source')
        print('workingdir is changed to "./ffmpeg_source"')
    if args.path is None:
        varhome = os.environ["HOME"]
    else:
        varhome = args.path
    d = os.listdir('.')
    if 'x264' in d:
        shutil.rmtree('x264')
    os.mkdir('x264')
    gitcom = ['git', '-C', 'x264', 'pull', '2>' '/dev/null', '||', 'git', 'clone',
              '--depth', '1', 'http://git.videolan.org/git/x264']
    try:
        print('trying to download libx264 sources')
        subprocess.check_call(gitcom)
        print('success!')
    except:
        print('downloading libx264 sources via git failed')
        sys.exit(1)
    os.chdir('x264')
    print('workingdir is changed to "x264"')
    path = '{0}/bin:{1}'.format(varhome, varpath)
    os.environ['PATH'] = path
    pkgpath = '{0}/ffmpeg_build/lib/pkgconfig'.format(varhome)
    os.environ['PKG_CONFIG_PATH'] = pkgpath
    confcode = ['./configure', '--prefix={0}/ffmpeg_build'.format(varhome), '--bindir={0}/bin', '--enable-static']
    try:
        print('chmod to configure...')
        st = os.stat('configure')
        os.chmod('configure', st.st_mode|0o111)
        print('success!')
    except:
        print('chmod to "configure" fail')
        sys.exit(1)
    try:
        print('trying to configure...')
        subprocess.check_call(confcode)
        print('success!')
    except:
        print('fail!')
        sys.exit(1)
    path = '{0}/bin:{1}'.format(varhome, varpath)
    os.environ['PATH'] = path
    try:
        print('trying to make...')
        subprocess.check_call(['make'])
        print('success!')
        print('trying to make install...')
        subprocess.check_call(['make', 'install'])
        print('success!')
    except:
        print('make error')
        sys.exit(1)


def checking(args):
    if args.path is None:
        varhome = os.environ["HOME"]
    else:
        varhome = args.path
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
    if args.libx264 is True:
        libx264(args)
    if args.check is True:
        checking(args)
    if args.ifile is not None:
        print('inputfile choised, but functional is not ready')
        sys.exit(0)
#    if args.ofile is not None:
#        print('outputfile choised, but functional is not ready')


if  __name__ ==  "__main__" :
    main()
