#!/usr/bin/python3

import re
import sys
import getopt

def usage():
    sys.stderr.write('usage:\n')
    sys.stderr.write(sys.argv[0]+' [-s separator] [-n name] [-z length]\n')
    sys.stderr.write('\t-s specifies what regex should separate output files\n')
    sys.stderr.write('\t-n specifies how output files are named (default: numeric)\n')
    sys.stderr.write('\t-z specifies how long numbered filenames (if any) should be\n')
    sys.stderr.write('\t-i include line containing separator in output files\n')
    sys.stderr.write('\t-q quiet operation\n')
    sys.stderr.write('\toperations are always performed on stdin\n')
    sys.exit(1)

def main():
    bad_usage = False
    try:
        optlist,args = getopt.getopt(sys.argv[1:],'s:n:z:iq')
    except:
        bad_usage = True
    if bad_usage or args:
        usage()
    separator='^$'
    name=''
    zero_pad=0
    include = False
    quiet = False
    for option in optlist:
        if option[0] == '-s':
            separator=option[1]
        elif option[0] == '-n':
            name=option[1]
        elif option[0] == '-z':
            zero_pad = int(option[1])
        elif option[0] == '-i':
            include = True
        elif option[0] == '-q':
            quiet = True
        else:
            raise ValueError('Expected something other than %s in option[0]\n' % option[0])
    rseparator = re.compile(separator)
    numeric_name=0
    if name != '':
        rname = re.compile(name)
    save_name=''
    batch = []
    while True:
        line = sys.stdin.readline()
        if line and name != '':
            rm=rname.match(line)
            if rm:
                save_name=rm.group(1).strip()
                if save_name.find('/') != -1:
                    sys.stderr.write('/ found in name\n')
                    #save_name=regex.gsub('/','-',save_name)
                    save_name=re.sub('/','-',save_name)
        m = rseparator.match(line)
        if not line or m:
            if len(batch) != 0:
                if save_name == '':
                    str_name = str(numeric_name)
                    str_name = (zero_pad - len(str_name)) * '0' + str_name
                    if not quiet:
                        sys.stderr.write('{}\n'.format(str_name))
                    file_ = open(str_name,'a+')
                    numeric_name = numeric_name + 1
                else:
                    if not quiet:
                        sys.stderr.write('{}\n'.format(save_name))
                    file_ = open(save_name,'a+')
                    save_name=''
                file_.writelines(batch)
                file_.close()
                batch = []
            if include:
                batch.append(line)
        else:
            batch.append(line)
        if not line:
            break
        
main()

