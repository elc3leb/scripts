#!/usr/bin/python3
# -*- coding: utf-8 -*
#

import re
import os
import time
from subprocess import CalledProcessError, check_output, call
from optparse import OptionParser



usage = '''Usage: %prog [option]'''
parser = OptionParser(usage=usage)

parser.add_option('-i', '--interactive', type='string', dest='i_container',
                      help="* Launch an interactive session on container")
parser.add_option("-l", "--list",
                      action="store_true", dest="list",
                      help="* List actives containers")
parser.add_option("-S", "--share", action="append", dest="s_container", default=[],
                      help="* Save a container to registry Harbor")
parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="* Print more informations")
parser.add_option("-D", "--dryrun",
                      action="store_true", dest="dryrun", default=False,
                      help="* Only print out without actions")

(Options, args) = parser.parse_args()

# List containers
if Options.list :
    if Options.dryrun:
        print("\n \t Will be performed: \tpodman ps -a")
    else:
        try:
            output_bytes = check_output(['podman','ps', '-a'], stderr=None)
            output_string = output_bytes.decode('utf-8')
            returncode = 0
            print("\n")
            for line in output_string.splitlines():
                print(line)
        except CalledProcessError as e:
            output = e.output
            returncode = e.returncode

# Interactive session with container
if Options.i_container:
    container_name = Options.i_container
    if Options.dryrun:
        print("\n \t Will be performed: \tpodman exec -u 0 --interactive --tty {} /bin/bash".format(container_name))
    else:
        call(['podman exec -u 0 --interactive --tty {} /bin/bash'.format(container_name)], shell=True)

# Commit & push container to registry
if Options.s_container:
    if Options.dryrun:
        print("\n\t Will be performed: \tpodman login registry:9001")
        print("\t Will be performed: \tpodman commit --format docker {} localhost{}")
        print("\t Will be performed: \tpodman tag localhost/{} registry:9001/{}$".format(s_container))
        print("\t Will be performed: \tpodman push registry:9001/{}".format(s_container))
    else:
        print("")
