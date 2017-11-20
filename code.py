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
parser.add_argument('--libx265', default=False, action='store_true', help='download and install libx265')

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
        os.chdir('..')
        cwd = os.getcwd()
        print('you are in {0}'.format(cwd))
    except:
        print('download error!')
        sys.exit(1)


def unpack():
    try:
        os.chdir('./ffmpeg_source')
        tar = tarfile.open('./ffmpeg-snapshot.tar.bz2', 'r:bz2')
        tar.extractall()
        print('extract success')
        os.chdir('..')
        cwd = os.getcwd()
        print('you are in {0}'.format(cwd))
    except:
        print('extract error')
        sys.exit(1)


def configure(args):
    os.chdir('./ffmpeg_source/ffmpeg')
    try:
        cwd = os.getcwd()
        print('configure in {0}'.format(cwd))
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
        os.chdir('..')
        os.chdir('..')
        cwd = os.getcwd()
        print('you are in {0}'.format(cwd))
    except:
        print('install error')
        sys.exit(1)


def libx264(args):
    if 'ffmpeg_source' not in os.listdir('.'):
        os.mkdir('ffmpeg_source')
    os.chdir('./ffmpeg_source')
    print('workingdir is changed to "./ffmpeg_source"')
    if args.path is None:
        varhome = os.environ["HOME"]
    else:
        varhome = args.path
    for f in os.listdir('.'):
        if 'x264' in f:
            try:
                shutil.rmtree(f)
                print('removed: {0}'.format(f))
            except NotADirectoryError:
                pass
    print('downloading sources')
    try:
        url = 'ftp://ftp.videolan.org/pub/x264/snapshots/last_x264.tar.bz2'
        urllib.request.urlretrieve(url, 'last_x264.tar.bz2')
        print('download is ok!')
    except:
        print('download error!')
        sys.exit(1)
    try:
        tar = tarfile.open('./last_x264.tar.bz2', 'r:bz2')
        tar.extractall()
        print('extract success')
        d = os.listdir('.')
        for f in d:
            if 'x264' in f:
                try:
                    os.chdir(f)
                    print('changed workingdir to "{0}"'.format(f))
                except NotADirectoryError:
                    pass
    except:
        print('extract error')
        sys.exit(1)
    varpath = os.environ['PATH']
    path = '{0}/bin:{1}'.format(varhome, varpath)
    varpath = os.environ['PATH']
    pkgpath = '{0}/ffmpeg_build/lib/pkgconfig'.format(varhome)
    confcode = ['./configure', '--prefix={0}/ffmpeg_build'.format(varhome), '--bindir={0}/bin'.format(varhome), '--enable-static']
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
    os.chdir('..')
    os.chdir('..')
    cwd = os.getcwd()
    print('you are in {0}'.format(cwd))


def libx265(args):
    if 'ffmpeg_source' not in os.listdir('.'):
        os.mkdir('ffmpeg_source')
    os.chdir('./ffmpeg_source')
    print('workingdir is changed to "./ffmpeg_source"')
    for f in os.listdir('.'):
        if 'x265' in f:
            try:
                shutil.rmtree(f)
                print('removed: {0}'.format(f))
            except NotADirectoryError:
                pass
#    os.mkdir('x265')
#    print('create x265 dir')
    if args.path is None:
        varhome = os.environ['HOME']
    else:
        varhome = args.path
    varpath = os.environ['PATH']
    path = '{0}/bin:{1}'.format(varhome, varpath)
    os.environ['PATH'] = path
    print('downloading sources')
    try:
        url = 'http://ftp.videolan.org/pub/videolan/x265/x265_2.5.tar.gz'
        urllib.request.urlretrieve(url, 'x265_2.5.tar.gz')
        print('download is ok!')
    except:
        print('download error!')
        sys.exit(1)
    print('unpacking sources')
    try:
        tar = tarfile.open('x265_2.5.tar.gz', 'r:gz')
        tar.extractall()
        print('extract success')
        d = os.listdir('.')
        for f in d:
            if 'x265' in f:
                try:
                    os.chdir(f)
                    print('changed workingdir to "{0}"'.format(f))
                except NotADirectoryError:
                    pass
    except:
        print('extract error')
#    try:
#        subprocess.check_call(['hg', 'clone', 'https://bitbucker.org/multicoreware/x265'])
#    except:
#        print('hg clone fail')
#        sys.exit(1)
    os.chdir('source')
    print('going to source')
    try:
        subprocess.check_call(['cmake', '-G', 'Unix Makefiles', '-DCMAKE_INSTALL_PREFIX={0}/ffmpeg_build'.format(varhome),
        '-DENABLE_SHARED:bool=off' '../../source'])
        print('cmake success')
    except:
        print('cmake fail')
        sys.exit(1)
    varpath = os.environ['PATH']
    path = '{0}/bin:{1}'.format(varhome, varpath)
    os.environ['PATH'] = path
    try:
        subprocess.check_call(['make'])
        print('make success')
    except:
        print('make error')
    try:
        subprocess.check_call(['make', 'install'])
        print('make install success')
    except:
        print('make install error')
        sys.exit(1)
    os.chdir('../../..')
    cwd = os.getcwd()
    print('you are in {0}'.format(cwd))


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
    if args.libx265 is True:
        libx265(args)
    if args.check is True:
        checking(args)
    if args.ifile is not None:
        print('inputfile choised, but functional is not ready')
        sys.exit(0)
#    if args.ofile is not None:
#        print('outputfile choised, but functional is not ready')


if  __name__ ==  "__main__" :
    main()
