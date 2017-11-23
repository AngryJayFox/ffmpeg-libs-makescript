#! /usr/bin/env python3
import os
import subprocess
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--ifile', action='store', help='inputfile')
parser.add_argument('--ofile', action='store', help='outputfile')
parser.add_argument('--gethelp', default=False,  action='store_true', help='help')
parser.add_argument('--codec', action='store', help='choice codec(mpeg4 maybe)')
parser.add_argument('--path', action='store', help='destination of bin/')
parser.add_argument('--convert', default=False, action='store_true', help='convert --ifile to --ofile via --codec')


def gethelp(args):
    try:
        os.chdir('{0}/bin'.format(mypath))
        print('getting LD_LIBRARY_PATH')
        os.environ['LD_LIBRARY_PATH'] = '{0}/ffmpeg_build/lib'.format(mypath)
        print('success')
        print('getting help')
        subprocess.check_call(['./ffmpeg', '-h'])
        print('ready!')
    except:
        print('something wrong...')


def convert(args):
    if args.ifile is not None:
        ifile = args.ifile
    else:
        print('not enough arguments')
        sys.exit(1)
    if args.ofile is not None:
        ofile = args.ofile
    else:
        ofile = '{0)/converted.avi'.format(mypath)
    if args.codec is not None:
        codec = args.codec
    else:
        codec = 'mpeg4'
    try:
        print('trying to convert...')
        os.chdir('{0}/bin'.format(mypath))
        print('path is changed to {0}'.format(mypath))
        os.environ['LD_LIBRARY_PATH'] = '{0}/ffmpeg_build/lib'.format(mypath)
        print('LD_LIBRARY_PATH is got')
        subprocess.check_call(['./ffmpeg', '-i', '{0}'.format(ifile), '-vcodec', '{0}'.format(codec), '-b', '4000k',
                             '-acodec', 'mp2', '-ab', '320k', '{0}'.format(ofile)])
        print('converting success')
        os.chdir(mypath)
        print('go home')
        out = subprocess.check_output(['mediainfo', '-InfoParameters', '--Output=XML', '{0}'.format(ofile)])
        print('got mediainfo')
        out = out.decode('utf-8').split()
        for o in out:
            if '<Format>' in o:
                if '</Format>' in o:
                    o = o.replace('<', ' ').replace('>', ' ').split()[1]
                    if o == 'AVI':
                        print('Test is success! Format {0}'.format(o))
    except:
        print('something wrong')


def main():
    args = parser.parse_args()
    global mypath
    if args.path is None:
        mypath = os.environ['HOME']
    else:
        mypath = args.path
    if args.gethelp is True:
        gethelp(args)
    if args.convert is True:
        convert(args)

#convert


if __name__ == "__main__":
    main()
