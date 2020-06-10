"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charlie Cosse

    Email           :ccosse@gmail.com

    Copyright       :(C) 1999-2020 Asymptopia Software

    License         :GPLv3

***********************************************************/
"""
import sys,time,os,string
from random import random

DEBUG=0

class TMSSolver_ORIG:
	def __init__(self,mode,level,parent):
		if DEBUG:print('TMSSolver')

		self.parent=parent
		self.global_config=parent.global_config

		self.env=None
		self.global_config=None
		self.admin=None
		self.players=parent.players
		self.MODE=mode
		self.LEVEL=level
		self.NNUMBERS=parent.NNUMBERS
		self.NTRAYSPOTS=parent.NTRAYSPOTS
		self.STOP_RUNNING=0

		self.game=parent
		self.tray=None


		self.plets={
			'triplets':[],
			'doublets':[],
			'singlets':[],
			'operator_doublets':self.get_operator_plets(2),
			'operator_singlets':self.get_operator_plets(1),
		}

		self.expressions={
		   'triplet_expressions':[],
		   'doublet_expressions':[],
		   'singlet_expressions':[],
		   'wc_triplet_expressions':[],
		   'wc_doublet_expressions':[],
		   'wc_singlet_expressions':[],
		   'wc_wc_doublet_expressions':[],
		}
		self.str2pt=None


	#This needs modified to handle mult/div:
	def get_operator_plets(self,N):

		plets=[]
		ops=[
			['+'],
			['+','-'],
			['+','-','*'],
			['+','-','*','/'],
		]
		available_ops=ops[self.LEVEL-1]

		if(N==1):
			for oidx in range(len(available_ops)):
				plets.append([available_ops[oidx]])

		elif(N==2):
			if available_ops.count('-') and available_ops.count('/'):
				plets.append(['-','/'])
				plets.append(['/','-'])
			if available_ops.count('*') and available_ops.count('/'):
				plets.append(['*','/'])
				plets.append(['/','*'])
			if available_ops.count('+') and available_ops.count('/'):
				plets.append(['+','/'])
				plets.append(['/','+'])
			if available_ops.count('+') and available_ops.count('*'):
				plets.append(['+','*'])
				plets.append(['*','+'])
			if available_ops.count('-') and available_ops.count('*'):
				plets.append(['-','*'])
				plets.append(['*','-'])
			if available_ops.count('+') and available_ops.count('-'):
				plets.append(['+','-'])
				plets.append(['-','+'])
			if available_ops.count('/'):
				plets.append(['/','/'])
			if available_ops.count('*'):
				plets.append(['*','*'])
			if available_ops.count('-'):
				plets.append(['-','-'])
			if available_ops.count('+'):
				plets.append(['+','+'])

		return(plets)

	def getStringValues(self):
		str_values=[]
		spots=self.tray.get_spots()#not sorted 1-10,so sort:
		nnumbers=self.NNUMBERS
		newspots=[]
		for spotidx in range(nnumbers):
			newspots.append(0)#=[0,0,0,0,0,0]

		ntrayspots=self.NTRAYSPOTS
		while len(spots)>ntrayspots-nnumbers:
			for spot in spots:
				if spot.getMN()[1]<nnumbers:
					newspots[spot.getMN()[1]]=spot
					spots.remove(spot)

		for dummy in range(len(newspots)):
			str_values.append(newspots[dummy].guest.str_val)

		print(str_values)
		return(str_values)

	def cycle_vals(self,vals):
		tmp=vals.pop()
		vals.insert(int(random()*len(vals)),tmp)
		return(vals)

	def get3x2x1x(self,N):
		#N=1,2,3 ~ singlets,doublets,tripplets
		#all unique index-triplets in set of 6 Tiles:
		#if 2 "5"'s in tiles, two "5"-singlets returned, etc..
		plets=[]
		num_times_cycled=0
		str_vals=self.getStringValues()
		#print str_vals
		NumNumbers=6
		while(num_times_cycled<1000):#print ratio when added vs idx on this before v2.0 release
			for idx in range(0,NumNumbers-N):
				i_plet=[]
				s_plet=[]
				for jdx in range(N):
					i_plet.append(float(str_vals[idx+jdx]))#changed to "float" v2.0
				i_plet.sort()
				for jdx in range(N):
					s_plet.append(str(i_plet[jdx]))

				if plets.count(s_plet)==0:plets.append(s_plet)
				elif(N==1 and plets.count(s_plet)<str_vals.count(s_plet[0])):
					plets.append(s_plet)

			str_vals=self.cycle_vals(str_vals)
			num_times_cycled=num_times_cycled+1
		return(plets)

	def generate_expressions(self,performance_factor):

		available_plets=[
			'triplets',
			'doublets',
			'singlets'
		]
		self.global_config=self.parent.global_config
		self.tray=self.players[self.player_idx].tray

		while len(self.plets['triplets']):self.plets['triplets'].pop()
		while len(self.plets['doublets']):self.plets['doublets'].pop()
		while len(self.plets['singlets']):self.plets['singlets'].pop()

		if available_plets.count('triplets'):self.plets['triplets']=self.get3x2x1x(3)
		if available_plets.count('doublets'):self.plets['doublets']=self.get3x2x1x(2)
		if available_plets.count('singlets'):self.plets['singlets']=self.get3x2x1x(1)

		while len(self.expressions['triplet_expressions']):x=self.expressions['triplet_expressions'].pop();del x
		while len(self.expressions['doublet_expressions']):x=self.expressions['doublet_expressions'].pop();del x
		while len(self.expressions['singlet_expressions']):x=self.expressions['singlet_expressions'].pop();del x
		while len(self.expressions['wc_triplet_expressions']):x=self.expressions['wc_triplet_expressions'].pop();del x
		while len(self.expressions['wc_doublet_expressions']):x=self.expressions['wc_doublet_expressions'].pop();del x
		while len(self.expressions['wc_singlet_expressions']):x=self.expressions['wc_singlet_expressions'].pop();del x
		while len(self.expressions['wc_wc_doublet_expressions']):x=self.expressions['wc_wc_doublet_expressions'].pop();del x

		#MAX_REPLACEMENTS=[2,3,3,3]

		MAX_REPLACEMENTS=[
			self.global_config['MAX_REPLACEMENTS_L1']['value'],
			self.global_config['MAX_REPLACEMENTS_L2']['value'],
			self.global_config['MAX_REPLACEMENTS_L3']['value'],
			self.global_config['MAX_REPLACEMENTS_L4']['value']
		]


		if MAX_REPLACEMENTS[self.LEVEL-1]>=0 and available_plets.count('triplets'):
			for pdx in range(len(self.plets['triplets'])):
				permutations=self.get3xPermutations(self.plets['triplets'][pdx])#permutations of idx+1 (i.e. 1,2,3 rather than 0,1,2)
				for perm in permutations:
					for odx in range(len(self.plets['operator_doublets'])):
						expr=[perm[0],self.plets['operator_doublets'][odx][0],perm[1],self.plets['operator_doublets'][odx][1],perm[2]]#save these
						value=self.evaluate(expr)
						if not value:continue
						self.expressions['triplet_expressions'].append([pdx,odx,expr,value])


		if MAX_REPLACEMENTS[self.LEVEL-1]>=1 and self.global_config['ALLOW_WC3X3']['value']:
			#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
			#"""deactivating: this works, but takes too long (testing, not generating (here)) by brute force.
			#wc_idx=0
			for pdx in range(0,len(self.plets['triplets'])):
				permutations=self.get3xPermutations(self.plets['triplets'][pdx])#permutations of idx+1 (i.e. 1,2,3 rather than 0,1,2)
				for perm in permutations:
					for odx in range(len(self.plets['operator_doublets'])):
						for val in range(16):
							expr=[str(val),self.plets['operator_doublets'][odx][0],perm[1],self.plets['operator_doublets'][odx][1],perm[2]]
							value=self.evaluate(expr)
							if not value:continue
							expr=['WC:'+str(val)+'.0',self.plets['operator_doublets'][odx][0],perm[1],self.plets['operator_doublets'][odx][1],perm[2]]
							self.expressions['wc_triplet_expressions'].append([pdx,odx,expr,value])
			#wc_idx=1
			for pdx in range(0,len(self.plets['triplets'])):
				permutations=self.get3xPermutations(self.plets['triplets'][pdx])#permutations of idx+1 (i.e. 1,2,3 rather than 0,1,2)
				for perm in permutations:
					for odx in range(len(self.plets['operator_doublets'])):
						for val in range(16):
							expr=[perm[0],self.plets['operator_doublets'][odx][0],str(val),self.plets['operator_doublets'][odx][1],perm[2]]
							value=self.evaluate(expr)
							if not value:continue
							expr=[perm[0],self.plets['operator_doublets'][odx][0],'WC:'+str(val)+'.0',self.plets['operator_doublets'][odx][1],perm[2]]
							self.expressions['wc_triplet_expressions'].append([pdx,odx,expr,value])
			#wc_idx=2
			for pdx in range(0,len(self.plets['triplets'])):
				permutations=self.get3xPermutations(self.plets['triplets'][pdx])#permutations of idx+1 (i.e. 1,2,3 rather than 0,1,2)
				for perm in permutations:
					for odx in range(len(self.plets['operator_doublets'])):
						for val in range(16):
							expr=[perm[0],self.plets['operator_doublets'][odx][0],perm[1],self.plets['operator_doublets'][odx][1],str(val)]
							value=self.evaluate(expr)
							if not value:continue
							expr=[perm[0],self.plets['operator_doublets'][odx][0],perm[1],self.plets['operator_doublets'][odx][1],'WC:'+str(val)+'.0']
							self.expressions['wc_triplet_expressions'].append([pdx,odx,expr,value])
			#wc_idx~operator[0]
			for pdx in range(0,len(self.plets['triplets'])):
				permutations=self.get3xPermutations(self.plets['triplets'][pdx])#permutations of idx+1 (i.e. 1,2,3 rather than 0,1,2)
				for perm in permutations:
					for odx in range(len(self.plets['operator_doublets'])):
						expr=[perm[0],self.plets['operator_doublets'][odx][0],perm[1],self.plets['operator_doublets'][odx][1],perm[2]]
						value=self.evaluate(expr)
						if not value:continue
						expr=[perm[0],'WC:'+self.plets['operator_doublets'][odx][0],perm[1],self.plets['operator_doublets'][odx][1],perm[2]]
						self.expressions['wc_triplet_expressions'].append([pdx,odx,expr,value])
			#wc_idx~operator[1]
			for pdx in range(0,len(self.plets['triplets'])):
				permutations=self.get3xPermutations(self.plets['triplets'][pdx])#permutations of idx+1 (i.e. 1,2,3 rather than 0,1,2)
				for perm in permutations:
					for odx in range(len(self.plets['operator_doublets'])):
						expr=[perm[0],self.plets['operator_doublets'][odx][0],perm[1],self.plets['operator_doublets'][odx][1],perm[2]]
						value=self.evaluate(expr)
						if not value:continue
						expr=[perm[0],self.plets['operator_doublets'][odx][0],perm[1],'WC:'+self.plets['operator_doublets'][odx][1],perm[2]]
						self.expressions['wc_triplet_expressions'].append([pdx,odx,expr,value])

			if DEBUG:print('finished wc_triplet_expressions generation:',len(self.expressions['wc_triplet_expressions']))
			#"""
			#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		if MAX_REPLACEMENTS[self.LEVEL-1]>=0:
			for pdx in range(0,len(self.plets['doublets'])):
				permutations=self.get2xPermutations(self.plets['doublets'][pdx])#permutations of idx+1 (i.e. 1,2,3 rather than 0,1,2)
				for perm in permutations:
					for odx in range(len(self.plets['operator_singlets'])):
						expr=[perm[0],self.plets['operator_singlets'][odx][0],perm[1]]
						value=self.evaluate(expr)
						if not value:continue
						self.expressions['doublet_expressions'].append([pdx,odx,expr,value])

			#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		if MAX_REPLACEMENTS[self.LEVEL-1]>=1:
			#wc_idx=0
			for pdx in range(0,len(self.plets['singlets'])):
				for odx in range(len(self.plets['operator_singlets'])):
					key="MAXNUM_LEVEL_%d"%(self.LEVEL)
					for val in range(self.global_config[key]['value']):
						expr=[str(val)+'.0',self.plets['operator_singlets'][odx][0],self.plets['singlets'][pdx][0]]
						value=self.evaluate(expr)
						if not value:continue
						expr=['WC:'+str(val)+'.0',self.plets['operator_singlets'][odx][0],self.plets['singlets'][pdx][0]]
						self.expressions['wc_doublet_expressions'].append([pdx,odx,expr,value])


			#wc_idx=1
			for pdx in range(0,len(self.plets['singlets'])):
				for odx in range(len(self.plets['operator_singlets'])):
					key="MAXNUM_LEVEL_%d"%(self.LEVEL)
					for val in range(self.global_config[key]['value']):
						expr=[self.plets['singlets'][pdx][0],self.plets['operator_singlets'][odx][0],str(val)+'.0']
						value=self.evaluate(expr)
						if not value:continue
						expr=[self.plets['singlets'][pdx][0],self.plets['operator_singlets'][odx][0],'WC:'+str(val)+'.0']
						self.expressions['wc_doublet_expressions'].append([pdx,odx,expr,value])


			#wc~operator:
			for pdx in range(0,len(self.plets['doublets'])):
				permutations=self.get2xPermutations(self.plets['doublets'][pdx])#permutations of idx+1 (i.e. 1,2,3 rather than 0,1,2)
				for perm in permutations:
					for odx in range(len(self.plets['operator_singlets'])):
						expr=[perm[0],self.plets['operator_singlets'][odx][0],perm[1]]
						value=self.evaluate(expr)
						if not value:continue
						expr=[perm[0],'WC:'+self.plets['operator_singlets'][odx][0],perm[1]]
						self.expressions['wc_doublet_expressions'].append([pdx,odx,expr,value])


			#SHUFFLE EXPRESSIONS TO GET EVEN REPRESENTATION
			for dummy in range(len(self.expressions['wc_doublet_expressions'])):
				insert_idx=int( (  len(self.expressions['wc_doublet_expressions'])  -2  ) *random() )
				expr2insert=self.expressions['wc_doublet_expressions'].pop()
				self.expressions['wc_doublet_expressions'].insert(insert_idx,expr2insert)

			#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		if MAX_REPLACEMENTS[self.LEVEL-1]>=2:
			#wc_idx=1 AND wc_idx=2
			key="MAXNUM_LEVEL_%d"%(self.LEVEL)
			for v1 in range(self.global_config[key]['value']):
				for v2 in range(self.global_config[key]['value']):

					for odx in range(len(self.plets['operator_singlets'])):

						expr=[str(v1)+'.0',self.plets['operator_singlets'][odx][0],str(v2)+'.0']
						value=self.evaluate(expr)
						if not value:continue
						expr=['WC:'+str(v1)+'.0',self.plets['operator_singlets'][odx][0],'WC:'+str(v2)+'.0']
						self.expressions['wc_wc_doublet_expressions'].append([0,odx,expr,value])#what did "pdx"(now "0") do?

			#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		if MAX_REPLACEMENTS[self.LEVEL-1]>=0:
			for pdx in range(len(self.plets['singlets'])):
				expr=[self.plets['singlets'][pdx][0]]
				value=self.evaluate(expr[0])
				if not value:continue
				self.expressions['singlet_expressions'].append([pdx,None,expr,value])

			#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		if MAX_REPLACEMENTS[self.LEVEL-1]>=1:
			#wc_idx=0
			key="MAXNUM_LEVEL_%d"%(self.LEVEL)
			for pdx in range(self.global_config[key]['value']):
				expr=['WC:'+str(pdx)+'.0']
				value=pdx
				if not value:continue
				self.expressions['wc_singlet_expressions'].append([pdx,None,expr,value])

			#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

		for key in self.expressions.keys():
			if DEBUG:print("%s: %d"%(key,len(self.expressions[key])))


		if not self.STOP_RUNNING:return None

	def evaluate(self,expr):
		#print expr
		str=''
		for idx in range(len(expr)):
			str=str+expr[idx]

		try:
			val=eval(str)
			#print str,val
		except:return(None)
		return(val)

	def get3xPermutations(self,tripplet):#receives single triplet list of len=3
		#print 'tripplet:',tripplet
		p=[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
		px3=[]#list of permuted "t"riplets
		for pidx in range(len(p)):
			tx3=[]#a permuted "t"riplet
			for tidx in range(3):
				#print 'pidx:',pidx,'  tidx:',tidx,'  p[pidx][tidx]-1=',p[pidx][tidx]-1,'  tripplet[p[pidx][tidx]-1]=',tripplet[p[pidx][tidx]-1]
				tx3.append(tripplet[p[pidx][tidx]-1])
			if px3.count(tx3)==0:px3.append(tx3)
			#print 'px3:',px3
		return(px3)

	def get2xPermutations(self,doublet):
		p=[[1,2],[2,1]]
		px2=[]#list of permuted doublets
		for pidx in range(len(p)):
			dx2=[]#permuted doublet
			for tidx in range(2):
				dx2.append(doublet[p[pidx][tidx]-1])
			if px2.count(dx2)==0:px2.append(dx2)
		return(px2)


	def construct_submission(self,lhs_expressions,rhs_expressions):

		for key in self.expressions.keys():
			if lhs_expressions==self.expressions[key]:lhs=key
			if rhs_expressions==self.expressions[key]:rhs=key

		if DEBUG:print("%s(%d) * %s(%d) = %e"%(lhs,len(lhs_expressions),rhs,len(rhs_expressions),len(lhs_expressions)*len(rhs_expressions)))

		stringValues=self.getAllStringValues()

		#str2pt=self.global_config['SCORING']
		if not self.str2pt:
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

		str2pt=self.str2pt

		score=0
		if self.game.STOP_RUNNING!=0:return None

		self.game.queue_thinking_maneuver()

		if DEBUG:print("%d * %d = %d"%(len(lhs_expressions),len(rhs_expressions),len(lhs_expressions)*len(rhs_expressions)))
		for idx1 in range(len(lhs_expressions)):
			for idx2 in range(len(rhs_expressions)):

				self.handle_events()
				if self.STOP_RUNNING:return None

				if lhs_expressions[idx1][3]==rhs_expressions[idx2][3]:#check equality of expressions before equating

					num_replacements=0
					addition_used=0
					subtraction_used=0
					multiplication_used=0
					division_used=0

					#print 'combining:',lhs_expressions[idx1],rhs_expressions[idx2]
					combinedList=[]
					for idx in range(len(lhs_expressions[idx1][2])):
						#print 'idx1=',idx1,' idx=',idx
						combinedList.append(lhs_expressions[idx1][2][idx])
					combinedList.append('=')
					for idx in range(len(rhs_expressions[idx2][2])):
						combinedList.append(rhs_expressions[idx2][2][idx])

					ok=1
					for elem in combinedList:
						count=combinedList.count(elem)
						if elem.count('WC:'):#Then we don't want to check for it in stringValues!!
							pass
						elif stringValues.count(elem)<count:
							#print combinedList,elem,count,stringValues.count(elem)
							ok=0

					if ok==1:
						rlist=self.game.localizer.localize(combinedList)
						if rlist:

							print('')
							print(lhs_expressions[idx1])
							print(rhs_expressions[idx2])
							print(rlist)
							print('')

							score=0
							for cidx in range(len(combinedList)):

								if combinedList[cidx][:3]=='WC:':
									score+=str2pt[combinedList[cidx][3:]]
									num_replacements+=1

									if 0:pass
									elif combinedList[cidx][3:]=='+':addition_used+=1
									elif combinedList[cidx][3:]=='-':subtraction_used+=1
									elif combinedList[cidx][3:]=='*':multiplication_used+=1
									elif combinedList[cidx][3:]=='/':division_used+=1

								else:
									score+=str2pt[combinedList[cidx]]

									if 0:pass
									elif combinedList[cidx]=='+':addition_used+=1
									elif combinedList[cidx]=='-':subtraction_used+=1
									elif combinedList[cidx]=='*':multiplication_used+=1
									elif combinedList[cidx]=='/':division_used+=1

							pidx=self.game.player_idx
							self.game.players[pidx].score+=score
							self.game.last_points=score
							self.game.num_replacements=num_replacements
							self.game.addition_used=addition_used
							self.game.subtraction_used=subtraction_used
							self.game.multiplication_used=multiplication_used
							self.game.division_used=division_used
							return(rlist)

					else:del combinedList

		self.game.last_points=score
		return(None)

	def getAllStringValues(self):
		str_values=[]
		spots=self.tray.get_spots()#not sorted 1-10,so sort:
		ntrayspots=self.game.NTRAYSPOTS
		newspots=[]
		for spotidx in range(ntrayspots):
			newspots.append(0)#=[0,0,0,0,0,0,0,0,0,0]
		while len(spots)>0:
			for spot in spots:
				newspots[spot.getMN()[1]]=spot
				spots.remove(spot)
		for dummy in range(len(newspots)):
			str_values.append(newspots[dummy].guest.str_val)
		return(str_values)

	def generate_options(self):

		triplet_expressions			=self.expressions['triplet_expressions']
		doublet_expressions			=self.expressions['doublet_expressions']
		singlet_expressions			=self.expressions['singlet_expressions']
		wc_triplet_expressions		=self.expressions['wc_triplet_expressions']
		wc_doublet_expressions		=self.expressions['wc_doublet_expressions']
		wc_wc_doublet_expressions	=self.expressions['wc_wc_doublet_expressions']
		wc_singlet_expressions		=self.expressions['wc_singlet_expressions']
		operator_doublets			=self.plets['operator_doublets']
		operator_singlets			=self.plets['operator_singlets']

		LEVEL=self.game.LEVEL
		if DEBUG:print('tux generating options')

		self.options=[]#the result of this function
		tray=self.tray
		spots=self.tray.get_spots()

		#board get 1 copy 1x str_val array in preparation of numerous brute-force localization attempts:
		self.game.localizer.update_board_map()

		num_commited=self.game.board.get_num_commited()

		MAX_REPLACEMENTS=[
			self.global_config['MAX_REPLACEMENTS_L1']['value'],
			self.global_config['MAX_REPLACEMENTS_L2']['value'],
			self.global_config['MAX_REPLACEMENTS_L3']['value'],
			self.global_config['MAX_REPLACEMENTS_L4']['value']
		]

		ALLOW_WC3X3=self.game.global_config['ALLOW_WC3X3']['value']
		t0=time.time()

		rlist=None

		if num_commited>=7 and MAX_REPLACEMENTS[self.LEVEL-1]>=4:
			if DEBUG:print('5')
			rlist=self.construct_submission(wc_wc_doublet_expressions,wc_wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)

		if self.STOP_RUNNING:return None
		if num_commited>=7 and MAX_REPLACEMENTS[self.LEVEL-1]>=3:
			if DEBUG:print('4')
			rlist=None
			if ALLOW_WC3X3:rlist=self.construct_submission(wc_triplet_expressions,wc_wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if ALLOW_WC3X3:rlist=self.construct_submission(wc_wc_doublet_expressions,wc_triplet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(wc_doublet_expressions,wc_wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(wc_wc_doublet_expressions,wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(wc_wc_doublet_expressions,wc_singlet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(wc_singlet_expressions,wc_wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if DEBUG:print('done MAX_REPLACEMENTS=3')

		if self.STOP_RUNNING:return None
		if num_commited>=4 and MAX_REPLACEMENTS[self.LEVEL-1]>=2:
			if DEBUG:print('3')
			rlist=None
			if ALLOW_WC3X3:rlist=self.construct_submission(wc_triplet_expressions,wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(wc_doublet_expressions,wc_triplet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(triplet_expressions,wc_wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(wc_wc_doublet_expressions,triplet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			if ALLOW_WC3X3:rlist=self.construct_submission(wc_triplet_expressions,wc_singlet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(wc_singlet_expressions,wc_triplet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(wc_doublet_expressions,wc_singlet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(wc_singlet_expressions,wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(doublet_expressions,wc_wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(wc_wc_doublet_expressions,doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(wc_wc_doublet_expressions,singlet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(singlet_expressions,wc_wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(wc_doublet_expressions,wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)

		if self.STOP_RUNNING:return None
		if num_commited>=1 and MAX_REPLACEMENTS[self.LEVEL-1]>=1:
			if DEBUG:print('2')
			rlist=self.construct_submission(triplet_expressions,wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(wc_doublet_expressions,triplet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			if ALLOW_WC3X3:rlist=self.construct_submission(wc_triplet_expressions,doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if ALLOW_WC3X3:rlist=self.construct_submission(doublet_expressions,wc_triplet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(doublet_expressions,wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(wc_doublet_expressions,doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)

			rlist=self.construct_submission(doublet_expressions,wc_singlet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(wc_singlet_expressions,doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(singlet_expressions,wc_doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(wc_doublet_expressions,singlet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(wc_singlet_expressions,singlet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(singlet_expressions,wc_singlet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if DEBUG:print('done MAX_REPLACEMENTS=1')

		if self.STOP_RUNNING:return None
		if MAX_REPLACEMENTS[self.LEVEL-1]>=0 and  num_commited==0:
			if DEBUG:print('1')
			rlist=self.construct_submission(triplet_expressions,doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(doublet_expressions,triplet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(triplet_expressions,singlet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(singlet_expressions,triplet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(doublet_expressions,doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(singlet_expressions,doublet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			rlist=self.construct_submission(doublet_expressions,singlet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)
			if self.STOP_RUNNING:return None

			rlist=self.construct_submission(singlet_expressions,singlet_expressions)
			if rlist:return(rlist)
			if DEBUG:print(time.time()-t0)

		return None


	def handle_events(self):
		if DEBUG:print('override me')

	def load_config(self,intermediate_path,fname):
		if DEBUG:print('override me')

	def reload_configs(self):
		if DEBUG:print('override me')

	def on_exit(self):
		if DEBUG:print('override me')

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
