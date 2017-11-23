#! /usr/bin/env python3

import subprocess
import sys

try:
    subprocess.check_call(['apt-get', 'update'])
    subprocess.check_call(['apt-get', '-y', 'install', 'autoconf', 'automake', 'build-essential', 'cmake', 
                          'git', 'libass-dev', 'libfreetype6-dev', 'libsdl2-dev', 'libtheora-dev', 'libtool',
                          'libva-dev', 'libvdpau-dev', 'libvorbis-dev', 'libxcb1-dev', 'libxcb-shm0-dev', 
                          'libxcb-xfixes0-dev', 'mercurial', 'pkg-config', 'texinfo', 'wget', 'zlib1g-dev', 
                          'mediainfo'])
except:
    print('preparing fail')
    sys.exit(1)
