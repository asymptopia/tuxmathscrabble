"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@gmail.com

    Copyright       :(C) 2006-2008 Asymptopia Software

    License         :GPL2

***********************************************************/
"""

import pygame
from pygame.locals import *
import unicodedata

class Tile(pygame.sprite.Sprite):
	
	def __init__(self,image,int_val,str_val,uchar,ptval):
		pygame.sprite.Sprite.__init__(self)
		
		self.image=image
		self.rect=self.image.get_rect()
		
		self.saved_center=None
		self.int_val=int_val
		self.str_val=str_val
		self.uchar=uchar
		self.ptval=ptval
		#self.imagefname=imagefname
		
	def update(self):
		self.rect.center = pygame.mouse.get_pos()
	
	def reset(self):
		self.rect.center=self.saved_center
	
