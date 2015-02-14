#!/usr/bin/env python
#-*- coding: utf-8 -*-
#fetch DSLEditor from external server
import sys,os,urllib

url32 = "--output-document DSLEditor.tar.gz 'https://robocloud.unex.es/public.php?service=files&t=59b9b4214d0de5e056184b93428d44fc&download'"
url64 = "--output-document DSLEditor.tar.gz 'https://robocloud.unex.es/public.php?service=files&t=ac16d5368704df20a691f8b496236378&download'"


def yesNoInput(message):
  answer = ''
  while answer != 'yes' and answer != 'no':
    if message[-1] != ' ': message = message + ' '
    answer = raw_input(message)
  return answer



def selectVersion():
  print 'Which version do you want to download?'
  print '   1. 32 bits'
  print '   2. 64 bits'
  version = raw_input('Version: ')
  if version == '1':
    url = url32
    name = 'DSLEditor_32_newPaths'
  elif version == '2':
    url = url64
    name = 'DSLEditor_64_newPaths'
  else:
    print 'No available version'
    sys.exit(0)
  return url,name

def checkExistence():
  path = os.environ['ROBOCOMP'] + '/tools/roboCompDSL/'
  print path
  if os.path.exists(path):
    if yesNoInput('You already have a RCDslEditor version. Delete it? (yes/no)') == 'yes':
      os.system('rm -r '+path)
    else:
      if yesNoInput('Try to download anyway? (yes/no)') == 'no':
        sys.exit(0)

def download(url,name):
  ret = os.system('wget -c ' + url)
  if ret == 0:
    ret = os.system('tar -xzf DSLEditor.tar.gz')
    
    os.system('mv '+name+'/roboCompDSL roboCompDSL')
    #os.system('rm DSLEditor.tar.gz')
    #os.system('rm -r '+name)
  else:
    print 'Error downloading, please try again'
    sys.exit(0)


if __name__ == '__main__':
  checkExistence()
  url,name = selectVersion()
  download(url,name)
