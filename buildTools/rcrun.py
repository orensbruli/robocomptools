#!/usr/bin/python

from __future__ import print_function
import argparse
import os
import string
from workspace import workspace as WS

def find_script(action,component):
    paths = WS.find_component_exec(component)
    pathsrc = WS.find_component_src(component)
    pathsrc = [ os.path.join(x,'bin') for x in pathsrc]
    pathsrc.append(paths)
    for path in pathsrc:
        for file in os.listdir(path):
            if file[-3:] == '.sh' or file[-5:] == '.bash':
                if string.lower(file[:len(action)])==string.lower(action):
                    return os.path.join(path,file)
    return False

def main():
    parser = argparse.ArgumentParser(description="Tool for locating and running a robocomp component")
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('component', nargs='?', help='start a component')
    group.add_argument('-s', '--start', nargs = 1, help="start a component")
    group.add_argument('-st', '--stop', nargs = 1, help="stop a component")
    group.add_argument('-fst', '--fstop', nargs = 1, help=" force start a component")
    parser.add_argument('-d', '--debug', action = 'store_true' , help="start a component")
    parser.add_argument('-cf', '--cfile', nargs = 1 , help="use custom ice config file (absolute path)")
    parser.add_argument('-c', '--config', nargs = 1 , help="ice config file to choose from default config directory")
    args = parser.parse_args()

    #if stop command no need for searching and all
    if args.stop:
        stpath = find_script("stop",args.stop[0]);
        if stpath:
            #print("using script {0}".format(stpath))
            command = stpath
        else:
            command = "killall " + str(args.stop[0])
        os.system(command)
        return
    elif args.fstop:
        sfpath = find_script("forcestop",args.stop[0]);
        if sfpath:
            #print("using script {0}".format(sfpath))
            command = sfpath
        else:
            command = "killall -9 " + str(args.fstop[0])
        os.system(command)
        return
    
    #get component name
    if args.start:
        component = str(args.start[0])
    elif args.component:
        component = args.component
    else:
        parser.error("No component specified")

    #search for the component
    componentPath = WS.find_component_exec(component)
    componentPathetc = componentPath[:-4]

    if not componentPath:
        print("couldnt find the component %s in any of the workspaces" % (component))
        return
    
    #find the config file
    '''
        if only one file is present in the etc directory then it will be used
        else if it has file named config the it will be used 
        if it has file named generic_config it will be used
        else we will use a random file
        used defined config file will override all the above
    '''
    configFiles = []
    configPath = componentPathetc + '/etc'
    for root, dirs, files in os.walk(configPath): configFiles = files
    if len(configFiles) == 1:
        ice_config = configPath + "/" + configFiles[0]
    else:
        if "config" in configFiles:
            ice_config = configPath + "/config"
        elif 'generic_config' in  configFiles:
            ice_config = configPath + "/generic_config"
        else:
            ice_config = configPath + "/" + configFiles[0]
    
    if args.config:
        if args.config[0] in configFiles:
            ice_config = configPath + "/" + args.config[0]
    elif args.cfile:
        ice_config = args.config[0]

    #execute the command
    spath = find_script("start",component);
    sdpath = find_script("startdebug",component);
    print(spath)
    if args.start:
        if spath and not (args.config or args.cfile or args.debug):
            command = spath
        elif sdpath and args.debug:
            command = sdpath
        else:
            command = componentPath + "/" + string.lower(component) + " --Ice.Config=" + ice_config
    else:
        if spath and not (args.config or args.cfile or args.debug):
            command = spath
        elif sdpath and args.debug:
            command = sdpath
        else:
            command = componentPath + "/" + string.lower(component) + " --Ice.Config=" + ice_config
    
    print("executing : "+command)
    os.system(command)

if __name__ == '__main__':
    main()

