#
#Class TMS_Localizer only used to access the board
#	
class TMS_Localizer_TURBO:
	"""TMS_Localizer has game model.
	"""
	def __init__(self,board,game):
		self.board=board
		self.game=game#only used to update score
		self.board_map=None
		self.state_map=None
		self.counts=None
		self.M=self.board.M
		self.N=self.board.N
		

	def update_board_map(self):
		#returns a 2D array of str_vals
		self.board_map,self.counts=self.board.get_map()
		self.board.update_state()
		self.state_map=self.board.state	
