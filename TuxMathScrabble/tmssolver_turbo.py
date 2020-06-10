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
import time, random
from .calc import parse
from .tmslocalizer_turbo import *

#
# a simple recursive permutation function
# the number of permutations of a sequence of n unique items is given by n! (n factorial)
# more details at http://mathworld.wolfram.com/Permutation.html
# tested with Python24 vegaseat 16feb2006
#
def permutate(l):
	sz = len(l)
	if sz <= 1:
		return [l]
	return [p[:i]+[l[0]]+p[i:] for i in xrange(sz) for p in permutate(l[1:])]

def comb(data,n):
	if n == 0:
		yield []
	elif n==1:
		for i in xrange(len(data)-n+1):
			yield [data[i]]
	else:
		for i in xrange(len(data)-n+1):
			for cc in comb(data[i+1:],n-1):
				yield [data[i]]+cc

#
#funtion to complete the set of permutation with doublet/triplet
#perm = initial permutation
#x = list of doublet/tripplet to 'add'
#... all this to avoid duplicate inside the permutation list
#
def permutate_norepeat(perm,x,nbtoadd):

	if nbtoadd==0: # nothing to do
		return perm
	elif nbtoadd==1: # one value to add, easy
		return [lperm[:i]+[lidx]+lperm[i:] for lperm in perm for lidx in x[0] for i in range(0,firstidx(lperm,lidx)+1) ]
	else:
		newperm=[]
		lx=[x[0][:],x[1][:]]
		sz = len(x)

		for lidx in x[0]:
			test=[lperm[:i]+[lidx]+lperm[i:] for lperm in perm for i in range(0,firstidx(lperm,lidx)+1) ]
			if test!=[]:
				#then find if this value is a tripplet or doublet,
				#and remove it, to avoid duplicate
				if sz>1 and len(lx[1])>0 and lx[1].count(lidx)>0:
					lx[1].remove(lidx)
				else:
					lx[0].remove(lidx)
				#recursive call with the new vector
				newperm+=permutate_norepeat(test,lx,nbtoadd-1)
		return newperm


#to get the first index of this value inside the list, else -1
def firstidx(list,lidx):
	 return ( list.index(lidx) if list.count(lidx)>0 else -1)

#
#a modified permutate function to avoid duplicate
#and to allow as input a vector of "forced value" to be included
#
def gpermutate(x,nn,forcedvalue=None):
	#init
	ll=x[:]
	ll.sort(reverse=True)
	newll=[]
	idx=0

	#build 3 pools:
	#newll[0] = unique occurrence in x
	#newll[1] = doublet in x
	#newll[2] = triplet and more....
	while idx<2:
		newll.append(list(set(ll)))
		newll[idx].sort(reverse=True)
		for lx in newll[idx]:
			ll.remove(lx)
		idx+=1

	newll.append(ll)

	gperm=[]
	shift=len(forcedvalue) if forcedvalue!=None else 0

	#main loop
	#classic permutation / combination are computed on
	#the set of unique occurence (permutate(lcomb)) on newll[0]
	#and doublet/triplet are then added in permutate_norepeat
	for idx in range(1+min(nn-shift,len(newll[1])+len(newll[2]))):
		if len(newll[0])>=nn-idx-shift:
			for lcomb in comb(newll[0],nn-idx-shift):

					#add forcedvalue
					if forcedvalue!=None:
						for val in forcedvalue: lcomb.append(val)

					if idx==0: gperm+=permutate(lcomb)
					else: gperm+=permutate_norepeat(permutate(lcomb),newll[1:],idx)

	return gperm


#
#Class TMS_Solver to gernerate an equation
#
class TMSSolver_TURBO:
	def __init__(self,mode,level,parent):

		self.global_config=parent.global_config
		self.parent=parent

		self.env=self.parent.env
		self.admin=self.parent.admin
		self.players=self.parent.players
		self.MODE=mode
		self.LEVEL=level
		self.NNUMBERS=self.parent.NNUMBERS
		self.NTRAYSPOTS=parent.NTRAYSPOTS
		self.STOP_RUNNING=0

		self.game=self.parent
		self.tray=None
		self.str2pt=None

	def getstr2pt(self):
		self.global_config=self.parent.global_config
		if self.str2pt==None:
			self.str2pt={
					'=':self.global_config['VALUE_EQUAL_SIGN']['value'],
					'+':self.global_config['VALUE_PLUS_SIGN']['value'],
					'-':self.global_config['VALUE_MINUS_SIGN']['value'],
					'*':self.global_config['VALUE_MULTIPLICATION_SIGN']['value'],
					'/':self.global_config['VALUE_DIVISION_SIGN']['value'],
			}
			for idx in range(0,6):
				nstr=str(idx)+'.0'
				self.str2pt[nstr]=self.global_config['VALUE_NUMBERS_0_THROUGH_5']['value']
			for idx in range(6,11):
				nstr=str(idx)+'.0'
				self.str2pt[nstr]=self.global_config['VALUE_NUMBERS_6_THROUGH_10']['value']
			for idx in range(11,16):
				nstr=str(idx)+'.0'
				self.str2pt[nstr]=self.global_config['VALUE_NUMBERS_11_THROUGH_15']['value']
			for idx in range(16,100):
				nstr=str(idx)+'.0'
				self.str2pt[nstr]=self.global_config['VALUE_NUMBERS_16_THROUGH_99']['value']


	def getStringValues(self):
		return [spot.guest.str_val for spot in self.tray.get_spots()]

#
#Look inside candidate, and use signs property to find
#tiles that could be switch "without effect"
#
#this function is wrong, will prevent some solutions to be found
#to modify is the AI is not good enough
#
	def get_switchable_pairs(self,expr, holenblist):
		lcom=[]
		last_hidx=-100
		last_idx=-100

		for hidx in range(len(holenblist)):
			idx=holenblist[hidx]

			nextsign=( expr[idx+1] if idx<len(expr)-1 else None	)
			cursign=( expr[idx-1] if idx>1 else None)
			previoussign=( expr[idx-3] if idx>3 else None )

			if last_idx==idx-2:
				if cursign=='/' and (not previoussign or previoussign=='/'):
					lcom.append([last_hidx,hidx])
				elif cursign=='*' and previoussign!='/':
					lcom.append([last_hidx,hidx])
				elif cursign=='+' and (not previoussign or previoussign=='+') \
					and nextsign not in ['*','/']:
					lcom.append([last_hidx,hidx])
				elif cursign=='-' and (not previoussign or previoussign=='-') \
					and nextsign not in ['*','/']:
					lcom.append([last_hidx,hidx])

			#this part is wrong, cancel more cases than necessary
			if last_idx==idx-4:
				if (expr[idx-1]=='+' and expr[idx-3]=='+') \
				or (expr[idx-1]=='*' and expr[idx-3]=='*'):
					lcom.append([last_hidx,hidx])
				if last_idx>0:
					if (expr[idx-1]=='-' and expr[idx-3]=='-'
						and expr[idx-5]=='-') \
					or (expr[idx-1]=='/' and expr[idx-3]=='/'
						and expr[idx-5]=='/'):
						lcom.append([last_hidx,hidx])

			last_idx=idx
			last_hidx=hidx

		return lcom

#test the tile type: true for number, false for sign
	def tiletype(self, mplusn):
		return ((mplusn)%2==1-self.game.localizer.board.signtag)
#
#Function to screen the board and determine if a set of empty
#tiles is a playable place (or potential place pplace)
#
	def generate_potential_expr(self,lentraysign,lentraynb):

		#update of board:
		self.game.localizer.update_board_map()

		#find tiles that are 'dead' for rows and/or columns
		state=self.game.localizer.state_map

		#state code for tiles
		#0=empty playable,
		#1=full (so playable too),
		#2=dead/unvailable for play (due to neighbourhood)

		pplace=[]
		lM=self.game.localizer.M
		lN=self.game.localizer.N
		lmap=self.game.localizer.board_map

		if self.game.localizer.board.num_commited>0:

		#Loop on row and col to find some place on the board ("potential place")
		#where an Equation could be filled:
			for midx in range(lM):
				for nidx in range(lN):
					#look for potential place inside rows:
					#find a start for a new expr, must start with a valid number tile
					#initialisation
					if state['row'][midx][nidx]!=2 and self.tiletype(midx+nidx) \
						and not (nidx>0 and state['row'][midx][nidx-1]==1):

						holenb=fillednb=withequal=holesign=0
						start_idx=nidx2=nidx

						#given current case state filled informations:
						while nidx2 < lN and state['row'][midx][nidx2]!=2:
							end_idx=nidx2
							is_a_nb=self.tiletype(midx+nidx2)

							if state['row'][midx][nidx2]==0:
								if is_a_nb: holenb+=1
								else: holesign+=1
							elif state['row'][midx][nidx2]==1:
								fillednb+=1
								if lmap[midx][nidx2]=='=': withequal=1

							if holenb>lentraynb or \
								holesign>1+lentraysign-withequal:
								break

							#A expr criteria: lenght>=2, end with a number tile, with at least one filled and one valid unfilled tile
							#with 0 or 1 equal sign (to be changed, for a more general case)...
							#In case followed by a sign: cannot be the end, skip
							#...in that case cannot be a start, so force the next loop to end
							if end_idx-start_idx>1 and  is_a_nb and holenb+holesign>0 \
							and fillednb>0 and ( (withequal==0 and holesign>0) or withequal==1 ) \
							and not (nidx2 < lN-1 and state['row'][midx][nidx2+1]==1):
								#ADD THIS POTENTIAL expr in the pplace list
								pplace.append(['row',						#0 type: row
															midx,							#1 row index
															start_idx, 					#2 column index of the start
															end_idx-start_idx+1,	#3 length of this expr
															[lmap[midx][lidx] for lidx in range(start_idx,end_idx+1)],#4 vector filled with borad values
															withequal,				#5 tag @1 if there is already an '=' on the board for this expr, else 0
															holenb,						#6 number of unfilled 'number' tiles
															holesign,						#7 number of unfilled 'sign' tiles
															fillednb])						#8 number of filled tiles
							nidx2+=1

					#same conditions on columns

					if state['col'][midx][nidx]!=2 and self.tiletype(midx+nidx) \
						and not (midx>0 and state['col'][midx-1][nidx]==1):

						holenb=fillednb=withequal=holesign=0
						start_idx=midx2=midx

						#given current case state filled informations:
						while midx2 < lM and state['col'][midx2][nidx]!=2:
							end_idx=midx2
							is_a_nb=self.tiletype(nidx+midx2)

							if state['col'][midx2][nidx]==0:
								if is_a_nb: holenb+=1
								else: holesign+=1
							elif state['col'][midx2][nidx]==1:
								fillednb+=1
								if lmap[midx2][nidx]=='=': withequal=1

							if holenb>lentraynb or \
								holesign>1+lentraysign-withequal:
								break

							#A expr criteria: lenght>=2, end with a number tile, with at least one filled and one valid unfilled tile
							#with 0 or 1 equal sign (to be changed, for a more general case).
							if end_idx-start_idx>1 and  is_a_nb and holenb+holesign>0 \
							and fillednb>0 and ( (withequal==0 and holesign>0) or withequal==1 ) \
							and not (midx2 < lM-1 and state['col'][midx2+1][nidx]==1):
									#ADD THIS POTENTIAL expr in the pplace list
									pplace.append(['col',					#0 type column
															nidx,							#1 column index
															start_idx, 					#2 ... (see previous)
															end_idx-start_idx+1,	#3
															[lmap[lidx][nidx] for lidx in range(start_idx,end_idx+1)],
															withequal,				#5
															holenb,						#6
															holesign,						#7
															fillednb])						#8
							midx2+=1
		else:
			#It's the FIRST TURN, play the max length equation
			#at the centre of the board.
			maxlen=min(2*lentraynb-1,2*(lentraysign+1)+1)

			if lN>=lM: #more columns than rows, place it in the centre columns
				start_idx=max(0, int((lM-maxlen))/2)
				end_idx=start_idx+2
				while end_idx-start_idx+1<=maxlen and end_idx<lM:
					curlen=end_idx-start_idx+1
					pplace.append(['col',								#0
												int(lN/2),#1
												start_idx, 							#2
												end_idx-start_idx+1,			#3
												['' for lidx in range(start_idx,end_idx+1)],
												0,											#5
												int((curlen+1)/2),					#6
												int((curlen-1)/2),					#7
												0])										#8
					end_idx+=2
			else: #more rows than columns, place it in the centre rows
				start_idx=max(0, int((lN-maxlen))/2)
				end_idx=start_idx+2
				while end_idx-start_idx+1<=maxlen and end_idx<lN:
					curlen=end_idx-start_idx+1
					pplace.append(['row',								#0
												int(lM/2),#1
												start_idx, 							#2
												end_idx-start_idx+1,			#3
												['' for lidx in range(start_idx,end_idx+1)],
												0,											#5
												int((curlen+1)/2),					#6
												int((curlen-1)/2),					#7
												0])										#8
					end_idx+=2
		#a comparaison funtion based on pplace vector:
		#criteria = max number of unfilled tile
		def pplace_comp_len(pplace1,pplace2):
			diff21=(pplace2[3]-pplace2[8])-(pplace1[3]-pplace1[8])
			if diff21>0: return 1
			elif diff21<0: return -1
			else: return random.choice((-1,1))

		#sort the potential place list and return
		pplace.sort(pplace_comp_len)

		return pplace


	def generate_expressions(self):

		#main init=tray, board state, max param of potential place
		#score
		self.getstr2pt()
		score=0

		#tray:
		self.tray=self.players[self.player_idx].tray
		traylist=self.getStringValues()
		traylist.sort(reverse=True)
		traynb=traylist[1:self.NNUMBERS+1]
		traysign=traylist[self.NNUMBERS+1:]

		#expr param init
		holesign=holenb=fillednb=-1
		filledvalue=[]
		withequal=-1

		#List to store permutation of numbers / signs
		ptraynb=[]
		ptraysign=[]

		#generate the vector of potential place (pplace)
		pplace=self.generate_potential_expr(len(traysign),len(traynb))

		#MAIN LOOP, to sum up:
		#for each expr place, build permutations of numbers and signs,
		# loop on permutations, fill equation and evaluate
		for pp in pplace:

			lastfilledvalue=filledvalue[:]
			lastfillednb=fillednb
			fillednb=pp[8]
			expr=pp[4][:]

			#build list of permutations of signs and numbers
			if holesign!=pp[7] or withequal!= pp[5]:
				holesign=pp[7]
				withequal= pp[5]
				ptraysign=( gpermutate(traysign,holesign) if withequal==1 else gpermutate(traysign,holesign,['=']) )

			if holenb!=pp[6]:
				holenb=pp[6]
				ptraynb=gpermutate(traynb, holenb)

			#experimental=to enter the loop in any case
			if len(ptraynb)==0:ptraynb=[None]
			if len(ptraysign)==0:ptraysign=[None]

			#build vector of position of numbers and signs to be filled
			rgexpr=range(len(expr))
			holenblist=[x for x in rgexpr if expr[x]=='' and x%2==0]
			holesignlist=[x for x in rgexpr if expr[x]=='' and x%2==1]
			filledvalue=[expr[x] for x in rgexpr if expr[x]!='']

			#store those range, since will be called many times
			rgholesignlist=range(len(holesignlist))
			rgholenblist=range(len(holenblist))

			# a condition to skip time-consuming computation at the beginning of the game
			if fillednb==1 and lastfillednb==1 \
				and filledvalue[0]==lastfilledvalue[0] \
				and len(ptraynb)*len(ptraysign)>20000:
				pass
			else:
				#loop on permutation of tray signs / numbers to build expr:
				#LOOP on permutation of SIGNS
				for ltraysign in ptraysign:

					for lidx in rgholesignlist:
						expr[holesignlist[lidx]]=ltraysign[lidx]

					#find the equal sign and pairs that can be switched without effect
					idx_equal=expr.index('=')
					lcom=self.get_switchable_pairs(expr,holenblist)

					#LOOP on permutation of NUMBERS
					for ltraynb in ptraynb:

						#use this sign function to skip some expr
						if not [True for lc in lcom if ltraynb[lc[0]]>ltraynb[lc[1]]]:

							#fill values in expr list
							for lidx in rgholenblist:
								expr[holenblist[lidx]]=ltraynb[lidx]

							#check value of each equation's side equation
							#only 1 equal operator allowed
							valleft=self.evaluate(expr[:idx_equal])
							valright=self.evaluate(expr[idx_equal+1:])

							#SOLUTION TEST:
							#if equality>>ok, format results, and score data
							#last test to prevent case where each side failed to evaluate
							if valleft==valright and valleft!=None:

								score=sum([self.str2pt[expr[x]] for x in rgexpr])
								self.game.players[self.player_idx].score+=score
								self.game.last_points=score

								if pp[0]=='row':
									return [ [ expr[x],pp[1],pp[2]+x ] for x in rgexpr if pp[4][x]=='' ]
								else:
									return [ [ expr[x],pp[2]+x,pp[1] ] for x in rgexpr if pp[4][x]=='' ]


		return (None)

	def evaluate(self,expr):
		#try:val=eval(''.join(expr))
		try:
			return parse(expr)
		except:
			return(None)


	def handle_events(self):
		print('override me')

	def load_config(self,intermediate_path,fname):
		print('override me')

	def reload_configs(self):
		print('override me')

	def on_exit(self):
		print('override me')

	def mktstamp(self):
		#tstamp which increases monotonically with time
		t=time.localtime()
		YYYY="%d"%t[0]
		MM="%02d"%t[1]
		DD="%02d"%t[2]
		hh="%02d"%t[3]
		mm="%02d"%t[4]
		ss="%02d"%t[5]
		tstamp="%s%s%s%s%s%s"%(YYYY,MM,DD,hh,mm,ss)
		return tstamp
