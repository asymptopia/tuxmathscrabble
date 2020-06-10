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
import time
import pygame
from pygame.locals import *
from .spot import Spot


class Board(pygame.sprite.Group):

	def __init__(self,M,N,XC,YC,background_image,default_spot_image):
		pygame.sprite.Group.__init__(self)
		self.M=M
		self.N=N
		self.XC=XC
		self.YC=YC

		self.YTOP=None
		self.YBOT=None
		self.XLHS=None
		self.XRHS=None

		self.default_spot_image=default_spot_image
		self.map=None
		self.num_commited=0

		if background_image and not default_spot_image:self.make_background_spots(background_image)
		else:self.make_default_spots(default_spot_image)

		self.representation2D=[ [ self.get_spotMN(m,n) for n in range(self.N)] for m in range(self.M) ]

		#Tables of states for resolution
		#Just used for the main board
		self.state={'row':[ [0 for n in range(self.N)] for m in range(self.M) ],
							'col':[ [0 for n in range(self.N)] for m in range(self.M) ]}
		self.signtag=-1

	def get_idx_map(self,letters):
		test = lambda spot: ("%2d"%letters.index(spot.guest.uchar) if spot.guest else '--' )
		return [ [ test(self.representation2D[m][n]) for n in range(self.N)] for m in range(self.M) ]

	def print_idx_map(self,letters):
		idx_map=self.get_idx_map(letters)
		#print [ [idx_map[ridx][cidx] for cidx in range(len(idx_map[0]))] for ridx in range(len(idx_map)) ],''

	def get_map(self):#return meta info as well...

		counts={}
		for idx in ['+','-','*','/','=']:counts[idx]={'count':0,'mn':[]}
		for idx in range(21):counts[str(float(idx))]={'count':0,'mn':[]}

		m=[[ '' for nidx in range(self.N)] for midx in range(self.M)]
		for midx in range(self.M):
			for nidx in range(self.N):
				spot=self.representation2D[midx][nidx]
				if spot.guest:
					str_val=spot.guest.str_val
					m[midx][nidx]=str_val
					counts[str_val]['count']+=1
					counts[str_val]['mn'].append((midx,nidx))

		#tag for tiletype to be set once after the first equation:
		if self.signtag<0 and counts['=']['count'] >0:
			self.signtag= ( counts['=']['mn'][0][0]+counts['=']['mn'][0][1] )% 2

		return(m,counts)

#test the tile type: true for number, false for sign
	def tiletype(self, mplusn): return ((mplusn)%2==1-self.signtag)

	def update_state(self):

		#2 board map to state the tile potential for a row
		#or column resolution
		#update with filled tiles
		test = lambda spot: (1 if spot.guest else 0)
		for itype in ('row','col') :
			self.state[itype]=[[ test(self.representation2D[m][n]) for n in range(self.N)] for m in range(self.M)]

		#state: 0=playable, 1=full, 2=dead
		#if there is not a list an equal sign on the board
		#the board is empty 		#find if signs are on odd or even cases
		state_chg=1
		while state_chg==1: #a short recursion, for propagation of "dead" tiles
			#tag to check a map change:
			state_chg=0

			for m in range(self.M):
				for n in range(self.N):
					for itype in ('row','col'):
						#we are working on number only, and unfilled tiles
						if self.tiletype(m+n) and self.state[itype][m][n]!=1:
							#to use symetry row/col and avoid code duplication, maybe not a good idea...
							if itype=='row': nsym=1; msym=0
							elif itype=='col': nsym=0; msym=1
							ok_change=0

							#a dead sign tile can kill some number tiles on borders
							if nsym*n+msym*m==0:
								if self.state[itype][m+msym][n+nsym]==2 :ok_change=1

							if nsym*n+msym*m==nsym*(self.N-1)+msym*(self.M-1):
								if self.state[itype][m-msym][n-nsym]==2:ok_change=1

							#cornered by 2 dead sign tile = 1 dead number tile
							if nsym*n+msym*m>0 and  nsym*n+msym*m<nsym*(self.N-1)+msym*(self.M-1):
								if self.state[itype][m-msym][n-nsym]==2\
								and self.state[itype][m+msym][n+nsym]==2:
									ok_change=1

							#impossible with a filled adjacent down tile
							if nsym*m+msym*n>0:
								if self.state[itype][m-nsym][n-msym]==1: ok_change=1
							#impossible with a filled adjacent up tile
							if nsym*m+msym*n<nsym*(self.M-1)+msym*(self.N-1):
								if self.state[itype][m+nsym][n+msym]==1: ok_change=1

							#(dead number tile or border) >> filled sign tile >> a new dead number tile on this row/col
							if nsym*n+msym*m>0:
								if self.state[itype][m-msym][n-nsym]==1:
									if nsym*n+msym*m>1:
										if self.state[itype][m-2*msym][n-2*nsym]==2: ok_change=1
									elif 	nsym*n+msym*m==1: ok_change=1

							if nsym*n+msym*m<nsym*(self.N-1)+msym*(self.M-1):
								if self.state[itype][m+msym][n+nsym]==1:
									if nsym*n+msym*m<nsym*(self.N-2)+msym*(self.M-2):
										if self.state[itype][m+2*msym][n+2*nsym]==2: ok_change=1
									elif nsym*n+msym*m==nsym*(self.N-2)+msym*(self.M-2): ok_change=1

							#between 2 dead number tiles >> a new dead number tile for this row/col
							if nsym*n+msym*m>1 and nsym*n+msym*m<nsym*(self.N-2)+msym*(self.M-2):
								if (self.state[itype][m-2*msym][n-2*nsym]==2
								and self.state[itype][m+2*msym][n+2*nsym]==2 ): ok_change=1

							if ok_change==1:
								if self.state[itype][m][n]!=2: state_chg=1
								self.state[itype][m][n]=2

			for m in range(self.M):
				for n in range(self.N):
					for itype in ('row','col'):
						#we are working on sign only, and unfilled tiles
						if not self.tiletype(m+n)  and self.state[itype][m][n]!=1:

							#to use symetry row/col
							if itype=='row':nsym=1; msym=0
							elif itype=='col':nsym=0; msym=1
							ok_change=0

							#impossible to put a sign a the beginning/end of the row/col
							if nsym*n+msym*m==0 or nsym*n+msym*m==nsym*(self.N-1)+msym*(self.M-1):
								ok_change=1
							#impossible next to a dead tile on the current row/col
							elif self.state[itype][m-msym][n-nsym]==2 or self.state[itype][m+msym][n+nsym]==2:
								ok_change=1
							#really difficult if the adjacent tiles are filled
							elif self.state[itype][m][n]==0:# Following conditions are too strong
								if nsym*m+msym*n>0:
									if self.state[itype][m-nsym][n-msym]==1 : ok_change=1
								if nsym*m+msym*n<nsym*(self.M-1)+msym*(self.N-1):
									if self.state[itype][m+nsym][n+msym]==1: ok_change=1

							if ok_change==1:
								if self.state[itype][m][n]!=2: state_chg=1
								self.state[itype][m][n]=2

	def get_listofheads(self): return [spot for spot in self.sprites() if spot.guest and spot.AMHEAD]
	def get_num_commited(self): return(self.num_commited)
	def get_spots(self): return(self.sprites())
	def increment_num_commited(self): self.num_commited+=1

	def check4guest(self,m,n):
		if m<0 or m>self.M-1 or n<0 or n>self.N-1:return(0)
		spot=self.get_spotMN(m,n)
		if spot.guest==None:return(0)
		else:return(1)

	def clear_spots(self):
		for spot in self.sprites():
			spot.remove(self)

	def get_spotMN(self,m,n):
		for spot in self.sprites():
			if spot.getMN()==(m,n): return(spot)

	def take_guestMN(self,tile,m,n):
		spot=self.get_spotMN(m,n)
		spot.take_guest(tile,1)
		return(spot)

	def get_guest_by_str(self,str_val):
		for spot in self.sprites():
			if spot.guest and spot.guest.str_val==str_val:
				return spot.pop_guest()

	#SPOT MAKERS:				-print 'need to break-up background image!'
	def make_background_spots(self,background_image):
		for m in range(self.M):
			for n in range(self.N):
				self.add(Spot(default_spot_image,m,n))#change to background_tile

	def make_default_spots(self,default_spot_image):
		XC=self.XC
		YC=self.YC
		M=self.M
		N=self.N

		h=default_spot_image.get_height()
		w=default_spot_image.get_width()

		self.YTOP=YC-int((M/2.)*h)
		self.YBOT=YC+int((M/2.)*h)
		self.XLHS=XC-int((N/2.)*w)
		self.XRHS=XC+int((N/2.)*w)

		for m in range(M):
			for n in range(N):
				spot=Spot(default_spot_image,m,n,'REG')
				spot.rect.center=(	self.XLHS+int((n+.5)*w), self.YTOP+int((m+.5)*h)	)
				self.add(spot)
