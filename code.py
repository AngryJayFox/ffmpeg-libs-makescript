#! /usr/bin/env python3
import os
import os.path
import shutil
import subprocess
import sys
import argparse
import urllib.request
import tarfile


parser = argparse.ArgumentParser()
parser.add_argument('--nasm', default=False, action='store_true',
                    help='download and install nasm')
parser.add_argument('--yasm', default=False, action='store_true',
                    help='download and install yasm')
parser.add_argument('--path', action='store',
                    help='destination path')
parser.add_argument('--libx264', default=False, action='store_true',
                    help='download and install libx264')
parser.add_argument('--libx265', default=False, action='store_true',
                    help='download and install libx265')
parser.add_argument('--libvpx', default=False, action='store_true',
                    help='download and install libvpx')
parser.add_argument('--libfdkaac', default=False, action='store_true',
                    help='download and install libfdk-aac')
parser.add_argument('--libmp3lame', default=False, action='store_true',
                    help='download and install libmp3lame')
parser.add_argument('--libopus', default=False, action='store_true',
                    help='download and install libopus')
parser.add_argument('--ffmpeg', default=False, action='store_true',
                    help='download and install ffmpeg')

parser.add_argument('--shared', default=False, action='store_true',
                    help='switch to "shared" build. "static" in default configuration')
parser.add_argument('--check', default=False, action='store_true',
                    help='check starting')
parser.add_argument('--mytest', default=False, action='store_true',
                    help='mine start vo download of libs')

"""
SUPPORT FUNCTIONS
"""


def getvars(args):
    if args.path is None:
        varhome = os.environ['HOME']
    else:
        varhome = args.path
    varpath = os.environ['PATH']
    path = '{0}/bin:{1}'.format(varhome, varpath)
    os.environ['PATH'] = path
    varpath = os.environ['PATH']
    pkgpath = '{0}/ffmpeg_build/lib/pkgconfig'.format(varhome)
    os.environ['PKG_CONFIG_PATH'] = pkgpath
    ldlib = '{0}/ffmpeg_build/lib'.format(varhome)
    os.environ['LD_LIBRARY_PATH'] = ldlib
    return varpath, varhome


def checkfolder():
    os.chdir(mydir)
    if not os.path.isdir('ffmpeg_source'):
            os.mkdir('ffmpeg_source')
    os.chdir('./ffmpeg_source')
    print('workingdir is changed to {0}'.format(os.getcwd()))


def downloadsource(name, url, file):
    try:
        print('downloading sources of {0}'.format(name))
        urllib.request.urlretrieve(url, file)
        print('download is ok!')
    except:
        print('download fail!')
        sys.exit(1)


def rmoldsource(name):
    for f in os.listdir('.'):
        if name in f:
            try:
                shutil.rmtree(f)
                print('removed: {0}'.format(f))
            except NotADirectoryError:
                pass


def extracting(file, type):
    try:
        print('extracting archive{0}...'.format(file))
        tar = tarfile.open(file, type)
        tar.extractall()
        print('success!')
    except:
        print('extract fail!')
        sys.exit(1)


def changedirtosource(name):
    for f in os.listdir('.'):
        if name in f:
            try:
                os.chdir(f)
                print('changed workingdir to "{0}"'.format(os.getcwd()))
            except NotADirectoryError:
                pass
            except FileNotFoundError:
                pass

def configurechmod():
    try:
        print('chmod to configure...')
        st = os.stat('configure')
        os.chmod('configure', st.st_mode | 0o111)
        print('success!')
    except:
        print('chmod to "configure" fail')
        sys.exit(1)


def subprocesscom(name, com):
    try:
        print('trying to {0} in {1}'.format(name, os.getcwd()))
        varpath, varhome = getvars(args)
        subprocess.check_call(com)
        print('success!')
    except:
        print('{0} fail!'.format(name))
        sys.exit(1)


"""
INSTALL MAIN LIBS FUNCTIONS
"""


def nasm(args):
    checkfolder()
    downloadsource('nasm', 'http://www.nasm.us/pub/nasm/releasebuilds/2.13.01/nasm-2.13.01.tar.bz2',
                   'nasm-2.13.01.tar.bz2')
    rmoldsource('nasm')
    extracting('nasm-2.13.01.tar.bz2', 'r:bz2')
    changedirtosource('nasm')
    com = ['./autogen.sh']
    subprocesscom('./autogen.sh nasm', com)
    configurechmod()
    varpath, varhome = getvars(args)
    subprocesscom('configure nasm', ['./configure', '--prefix={0}/ffmpeg_build'.format(varhome),
                                     '--bindir={0}/bin'.format(varhome)])
    getvars(args)
    subprocesscom('make nasm', ['make'])
    subprocesscom('make install nasm', ['make', 'install'])


def yasm(args):
    checkfolder()
    downloadsource('yasm', 'http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz', 'yasm-1.3.0.tar.gz')
    rmoldsource('yasm')
    extracting('yasm-1.3.0.tar.gz', 'r:gz')
    changedirtosource('yasm')
    configurechmod()
    varpath, varhome = getvars(args)
    subprocesscom('configure yasm', ['./configure', '--prefix={0}/ffmpeg_build'.format(varhome),
                                     '--bindir={0}/bin'.format(varhome)])
    getvars(args)
    subprocesscom('make yasm', ['make'])
    subprocesscom('make install yasm', ['make', 'install'])



def libx264(args):
    checkfolder()
    downloadsource('libx264', 'ftp://ftp.videolan.org/pub/x264/snapshots/last_x264.tar.bz2',
                   'last_x264.tar.bz2')
    rmoldsource('x264')
    extracting('last_x264.tar.bz2', 'r:bz2')
    changedirtosource('x264')
    configurechmod()
    varpath, varhome = getvars(args)
    subprocesscom('configure libx264', ['./configure', '--prefix={0}/ffmpeg_build'.format(varhome),
                                        '--bindir={0}/bin'.format(varhome), '--enable-static'])
    getvars(args)
    subprocesscom('make libx264', ['make'])
    subprocesscom('make install libx264', ['make', 'install'])


def libx265(args):
    checkfolder()
    downloadsource('libx265', 'http://ftp.videolan.org/pub/videolan/x265/x265_2.5.tar.gz', 'x265_2.5.tar.gz')
    rmoldsource('x265')
    extracting('x265_2.5.tar.gz', 'r:gz')
    changedirtosource('x265')
    os.chdir('source')
    varpath, varhome = getvars(args)
    subprocesscom('cmake libx265', ['cmake', '-G', 'Unix Makefiles',
                                    '-DCMAKE_INSTALL_PREFIX={0}/ffmpeg_build'.format(varhome),
                                    '-DENABLE_SHARED:bool=off' '../../source'])
    getvars(args)
    subprocesscom('make libx265', ['make'])
    subprocesscom('make install libx265', ['make', 'install'])


def libvpx(args):
    checkfolder()
    downloadsource('libvpx', 'https://github.com/webmproject/libvpx/archive/v1.6.1.tar.gz', 'v1.6.1.tar.gz')
    rmoldsource('libvpx')
    extracting('v1.6.1.tar.gz', 'r:gz')
    changedirtosource('libvpx')
    configurechmod()
    varpath, varhome = getvars(args)
    subprocesscom('configure libvpx', ['./configure', '--prefix={0}/ffmpeg_build'.format(varhome), '--disable-examples',
                               '--disable-unit-tests', '--enable-vp9-highbitdepth', '--as=yasm'])
    getvars(args)
    subprocesscom('make libvpx', ['make'])
    subprocesscom('make install libvpx', ['make', 'install'])


def libfdkaac(args):
    checkfolder()
    rmoldsource('fdk-aac')
    subprocesscom('git clone libfdk-aac', ['git', 'clone', '--depth', '1', 'https://github.com/mstorsjo/fdk-aac'])
    changedirtosource('fdk-aac')
    subprocesscom('autoreconf -fiv', ['autoreconf', '-fiv'])
    configurechmod()
    varpath, varhome = getvars(args)
    subprocesscom('configure libfdk-aac', ['./configure', '--prefix={0}/ffmpeg_build'.format(varhome),
                                           '--disable-shared'])
    getvars(args)
    subprocesscom('make libfdk-aac', ['make'])
    subprocesscom('make install libfdk-aac', ['make', 'install'])


def libmp3lame(args):
    checkfolder()
    rmoldsource('lame-3.100')
    downloadsource('libmp3lame', 'http://downloads.sourceforge.net/project/lame/lame/3.100/lame-3.100.tar.gz',
                   'lame-3.100.tar.gz')
    extracting('lame-3.100.tar.gz', 'r:gz')
    changedirtosource('lame-3.100')
    configurechmod()
    varpath, varhome = getvars(args)
    subprocesscom('configure libmp3lame', ['./configure', '--prefix={0}/ffmpeg_build'.format(varhome),
                                           '--bindir={0}/bin'.format(varhome), '--disable-shared', '--enable-nasm'])
    getvars(args)
    subprocesscom('make libmp3lame', ['make'])
    subprocesscom('make install libmp3lame', ['make', 'install'])


def libopus(args):
    checkfolder()
    rmoldsource('opus')
    subprocesscom('git clone libopus', ['git', 'clone', '--depth', '1', 'https://github.com/xiph/opus.git'])
    changedirtosource('opus')
    subprocesscom('./autogen.sh libopus', ['./autogen.sh'])
    configurechmod()
    varpath, varhome = getvars(args)
    subprocesscom('configure libopus', ['./configure', '--prefix={0}/ffmpeg_build'.format(varhome), '--disable-shared'])
    getvars(args)
    subprocesscom('make libmp3lame', ['make'])
    subprocesscom('make install libmp3lame', ['make', 'install'])


def ffmpeg(args):
    checkfolder()
    downloadsource('ffmpeg', 'http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2', 'ffmpeg-snapshot.tar.bz2')
    rmoldsource('ffmpeg')
    extracting('ffmpeg-snapshot.tar.bz2', 'r:bz2')
    changedirtosource('ffmpeg')
    configurechmod()
    varpath, varhome = getvars(args)
    configure = ['./configure', '--prefix={0}/ffmpeg_build'.format(varhome), '--pkg-config-flags=--static',
                     '--extra-cflags=-I{0}/ffmpeg_build/include'.format(varhome),
                     '--extra-ldflags=-L{0}/ffmpeg_build/lib'.format(varhome),
                     '--extra-libs=-lpthread -lm', '--bindir={0}/bin'.format(varhome), '--enable-nonfree']
    if args.shared is True:
        configure.extend(['--disable-static', '--enable-shared'])
    else:
        configure.extend(['--disable-shared', '--enable-static'])
    if args.libx264 is True:
        configure.append('--enable-libx264')
        if '--enable-gpl' not in configure:
            configure.append('--enable-gpl')
    if args.libx264 is True:
        configure.append('--enable-libx265')
    if args.libvpx is True:
        configure.append('--enable-libvpx')
    if args.libfdkaac is True:
        configure.append('--enable-libfdk-aac')
        if '--enable-gpl' not in configure:
            configure.append('--enable-gpl')
    if args.libmp3lame is True:
        configure.append('--enable-libmp3lame')
    if args.libopus is True:
        configure.append('--enable-libopus')
    if args.mytest is True:
        configure.extend(['--enable-libx264', '--enable-gpl', '--enable-libx265', '--enable-libvpx',
                          '--enable-libfdk-aac', '--enable-gpl', '--enable-libopus'])
    subprocesscom('configure ffmpeg', configure)
    getvars(args)
    subprocesscom('make ffmpeg', ['make'])
    subprocesscom('make install ffmpeg', ['make', 'install'])


def checking(args):
    varpath, varhome = getvars(args)
    os.chdir('{0}/bin'.format(varhome))
    subprocesscom('checking ffmpeg', ['./ffmpeg', '-version'])


def main():
    global mydir
    mydir = os.getcwd()
    global args
    args = parser.parse_args()
    if args.nasm is True:
        nasm(args)
    if args.yasm is True:
        yasm(args)
    if args.libx264 is True:
        libx264(args)
    if args.libx265 is True:
        libx265(args)
    if args.libvpx is True:
        libvpx(args)
    if args.libfdkaac is True:
        libfdkaac(args)
    if args.libmp3lame is True:
        libmp3lame(args)
    if args.libopus is True:
        libopus(args)
    if args.ffmpeg is True:
        ffmpeg(args)
    if args.check is True:
        checking(args)


if  __name__ ==  "__main__" :
    main()
