#!/usr/bin/env python2.7-32
"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Support         :www.asymptopia.org/forum

    Author          :Charles B. Cosse

    Email           :ccosse@asymptopia.org

    Copyright       :(C) 2006-2015 Asymptopia Software

    License         :GPLv3

***********************************************************/
"""
import os,sys,string,time
sys.path.append('/usr/share/games/tuxmathscrabble/lib')
from TuxMathScrabble.tms import *

def usage():
	msg="""
Usage: tuxmathscrabble [OPTION]
	Available options are:
	-help				Show this help
	-wx				Enable the wx admin interface
	"""
	print msg
	

if __name__ == "__main__":
	appdir='TuxMathScrabble'
	if len(sys.argv)==1:
		x=TuxMathScrabbleApp()
	elif sys.argv[1]=='-help':
		usage()
	elif sys.argv.count('-wx')>0:
		from TuxMathScrabble.tms_wx import *
		x=TuxMathScrabbleAppWX()
	else:
		x=TuxMathScrabbleApp()
	
