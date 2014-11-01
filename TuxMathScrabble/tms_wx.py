#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@asymptopia.org

    Copyright       :(C) 2006-2009 Asymptopia Software

    License         :GPLv3

***********************************************************/
"""
import wx
from wxadmin import *
from tms import *

class TuxMathScrabbleAppWX(wx.App):
	
	def __init__(self):
		wx.App.__init__(self, 0)
		
		mode=0
		level=4
		use_default_level=True
		print "okay"
		while True:
			print "calling prog"
			prog=TuxMathScrabble(mode,level,use_default_level,True)
			print "calling prog.run"
			mode,level=prog.run()
			
			
			if mode<0:prog.on_exit()
			elif mode==0:pass#prog.update_highscores()
			elif mode==1:prog.update_highscores()
			elif mode==2:
				rval=prog.admin.ShowModal()
				mode=0
			
			use_default_level=0
