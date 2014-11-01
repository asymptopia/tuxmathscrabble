#!/usr/bin/env python
"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@asymptopia.org

    Copyright       :(C) 2006-2010 Asymptopia Software

    License         :GPLv3

***********************************************************/
"""
import os,sys
APPNAME='TuxMathScrabble'

for sitepkgdir in sys.path:
	if sitepkgdir[-13:]=='site-packages':break

rm_path=os.path.join('/var/games/',APPNAME)
if os.path.exists(rm_path):
	cmd="rm -rf %s"%rm_path
	os.system(cmd)

rm_path=os.path.join(sitepkgdir,APPNAME)
if os.path.exists(rm_path):
	cmd="rm -rf %s"%rm_path
	print cmd
	os.system(cmd)

if len(sys.argv)>1 and sys.argv[1]=='uninstall':
	print 'application sucessfully removed.'
	sys.exit()
	
#Added 1/6/08 b/c Macs don't (apparantly) have /var/games by default (some linux distros may not, either)
if not os.path.exists('/var'):os.mkdir('/var')
if not os.path.exists('/var/games'):os.mkdir('/var/games')
if not os.path.exists('/var/games/TuxMathScrabble'):os.mkdir('/var/games/TuxMathScrabble')

path='/var/games/TuxMathScrabble'

cmd="cp -r  Font %s"%(path)
print cmd
os.system(cmd)

cmd="chmod -R 755 /var/games/%s"%(APPNAME)
print cmd
os.system(cmd)

cmd="cp .tms_config_master %s"%(path)
print cmd
os.system(cmd)

path=os.path.join(sitepkgdir,APPNAME)
if not os.path.exists(path):os.mkdir(path)

cmd="cp -r %s %s"%(APPNAME,sitepkgdir)
print cmd
os.system(cmd)

cmd="cp tuxmathscrabble.py /usr/local/bin/tuxmathscrabble"
print cmd
os.system(cmd)

cmd="chmod -R 755 %s/%s"%(sitepkgdir,APPNAME)
print cmd
os.system(cmd)


##########################################################	
print '**********************************************'
print '*                                            *'
print '*           Setup Complete                   *'
print '*                                            *'
print '* Run: /usr/local/bin/tuxmathscrabble  -help *'
print '*                                            *'
print '*      Checkout more software at:            *'
print '*      http://www.asymptopia.org             *'
print '*                                            *'
print '**********************************************'

