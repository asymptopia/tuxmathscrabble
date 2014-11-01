import sys
import re

# Variation on exemple from Fredrik Lundh
# see http://effbot.org/zone/simple-top-down-parsing.htm
# token_pat = re.compile("\s*(?:(\d+)|(\*|.))")

class symbol_base(object):

	id = None # node/token type name
	value = None # used by literals

	def nud(self):
		raise SyntaxError(
			"Syntax error (%r)." % self.id
		)

	def led(self, left):
		raise SyntaxError(
			"Unknown operator (%r)." % self.id
		)
		
symbol_table = {}

def symbol(id, bp=0):
	try:
		s = symbol_table[id]
	except KeyError:
		class s(symbol_base):
			pass
		s.id = id
		s.lbp = bp
		symbol_table[id] = s
	else:
		s.lbp = max(bp, s.lbp)
	return s
	
symbol("(literal)")
symbol("+", 10); symbol("-", 10)
symbol("*", 20); symbol("/", 20)
symbol("(end)")

def led(self, left):
	return left+expression(10)
symbol("+").led = led

def led(self, left):
	return left-expression(10)
symbol("-").led = led

def led(self, left):
	return left*expression(20)
symbol("*").led = led

def led(self, left):
	return left/expression(20)
symbol("/").led = led

def nud(self):
	return self.value
symbol("(literal)").nud = nud

#alternative syntax, seems slightly slower ...
#~ symbol("+").led = lambda self,left: left+expression(10)	
#~ symbol("-").led = lambda self,left: left-expression(10)	
#~ symbol("*").led = lambda self,left: left*expression(20)	
#~ symbol("/").led = lambda self,left: left/expression(20)
#~ symbol("(literal)").nud = lambda self: self.value

def prefix(id, bp):
	def nud(self):
		return expression(bp)
	symbol(id).nud = nud

prefix("+", 100); prefix("-", 100)

#no check on the equation,
#should be an alternance of number and operator
def tokenize(program):
	number=True
	for item in program:
		if number:
			symbol = symbol_table["(literal)"]
			s = symbol()
			s.value = float(item)
			number=False
			yield s
		else:
			symbol = symbol_table.get(item)
			number=True	
			yield symbol()
	number=not number	
	symbol = symbol_table["(end)"]
	yield symbol()


def expression(rbp=0):
	global token
	t = token
	token = next()
	left = t.nud()
	while rbp < token.lbp:
		t = token
		token = next()
		left = t.led(left)
	return left

def parse(program):
	global token, next
	next = tokenize(program).next
	token = next()
	return expression()
