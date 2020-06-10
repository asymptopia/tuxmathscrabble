#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :ccosse.github.io

    Author          :Charlie Cosse

    Email           :ccosse@gmail.com

    Copyright       :(C) 1999-2020 Asymptopia Software

    License         :GPLv3

***********************************************************/
"""
import wx
from .wxadmin import *
from .tms import *

class TuxMathScrabbleAppWX(wx.App):

	def __init__(self):
		wx.App.__init__(self, 0)

		mode=0
		level=4
		use_default_level=True
		while True:
			prog=TuxMathScrabble(mode,level,use_default_level,True)
			mode,level=prog.run()


			if mode<0:prog.on_exit()
			elif mode==0:pass#prog.update_highscores()
			elif mode==1:prog.update_highscores()
			elif mode==2:
				rval=prog.admin.ShowModal()
				mode=0

			use_default_level=0
