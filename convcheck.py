#! /usr/bin/env python3
import os
import subprocess
import argparse
import sys
from xml.dom import minidom

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--ifile', action='store', help='inputfile')
parser.add_argument('-o', '--ofile', action='store', help='outputfile')
parser.add_argument('-g', '--gethelp', default=False,  action='store_true', help='help')
parser.add_argument('--codec', action='store', help='choice codec(mpeg4 maybe)')
parser.add_argument('-p', '--path', action='store', help='destination of bin/')
parser.add_argument('-c', '--convert', default=False, action='store_true', help='convert --ifile to --ofile via --codec')


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
        sys.exit(1)


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
        print('going home')
    except:
        print('convert fail')


def check(args):
    try:
        print('parsing mediainfo')
        xmldata = subprocess.check_output(['mediainfo', '-InfoParameters', 
                                     '--Output=XML', '{0}'.format(args.ofile)]).decode('utf-8')
        print(xmldata)
        try:
            xmlstring = minidom.parseString(xmldata)
            form = xmlstring.getElementsByTagName('track')[0].childNodes[3].firstChild.nodeValue
        except Exception as e:
            print(e)
        if form.lower() == realformat.lower():
            print('SUCCESS! Converted file format ({0}) is match with chosen ({1})'.format(form, realformat))
        else:
            print('FAIL! Converted file format ({0}) does not match with chosen ({1})'.format(form, realformat))
            sys.exit(1)
    except:
        sys.exit(1)

def main():
    args = parser.parse_args()
    global mypath
    if args.path is None:
        mypath = os.environ['HOME']
    else:
        mypath = args.path
    global realformat
    try:
        realformat = args.ofile.split('.')[-1]
    except:
        print('cannot get real output format')
        realformat = 'err'
    if args.gethelp is True:
        gethelp(args)
    if args.convert is True:
        convert(args)
        check(args)


if __name__ == "__main__":
    main()
