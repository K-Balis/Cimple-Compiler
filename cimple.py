# Name(1) : Konstantinos Balis, AM(1) : 4117, Username(1) : cse74117
# Name(2) : Stefanos Gkanos, AM(2) : 4043, Username(2) : cse74043

import sys																# For argv and exit

input_program = open(sys.argv[1], 'r')

# ------------------------------------  Globals  ----------------------------------------

lineNo = 1																# Program starts at line number 1
flag = 0																# Is used to keep information about comments in program	
quadnum = 1
QuadsOutputFiles = []													# List of quads used for .int and .c files
QuadsCodeGenerator = []													# List of quads used in code generator
listoftemps = []
listofidentifiers = []
i = 1
FunctionAndProcedureFlag = 0											# Flag for .c file
optionalsign = ''

keywords = [ 'program', 'declare', 'if', 'else', 'while', 'switchcase', 'forcase', 'incase', 'default', 'case', 'not', 'and', 'or', 'function', 'procedure', 'call', 'return', 'in', 'inout', 'input', 'print']
																																												
transition_diagram = [['start_state', 'addition', 'subtraction', 'multiplication', 'division', 'opencurlybracket', 'closecurlybracket', 'openbracket', 'closebracket', 'opensquarebracket', 'closesquarebracket', 'comma', 'semicolon', 'asgn_state', 'equals', 'smaller_state', 'larger_state', 'dot', 'rem_state', 'eof', 'idk_state', 'dig_state', 'wrong_input_error'],						# Transition table for start state
					['number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'dig_state_error', 'dig_state', 'wrong_input_error'],																												# Transition table for digit state
					['identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'identifier', 'idk_state', 'idk_state', 'wrong_input_error'],									# Transition table for letter state
					['assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assignment', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error', 'assingment_state_error'],		# Transition table for letter state
					['smaller', 'smaller', 'smaller', 'smaller', 'smaller', 'smaller', 'smaller', 'smaller', 'smaller', 'smaller', 'smaller', 'smaller', 'smaller', 'smaller', 'smallerorequal', 'smaller', 'notequal', 'smaller', 'smaller', 'smaller', 'smaller', 'smaller', 'wrong_input_error'],																							# Transition table for smaller state
					['larger', 'larger', 'larger', 'larger', 'larger', 'larger', 'larger', 'larger', 'larger', 'larger', 'larger', 'larger', 'larger', 'larger', 'largerorequal', 'larger', 'larger', 'larger', 'larger', 'larger', 'larger', 'larger', 'wrong_input_error'],																													# Transition table for larger state
					['rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'rem_state', 'start_state', 'eof', 'rem_state', 'rem_state', 'rem_state']]																	# Transition table for comments state

rel_op = ['=', '<=', '>=', '>', '<', '<>']								# Relational operators
ari_op = ['+', '-', '*', '/']											# Arithmetic operators

# --------------------------------  Lexical Analysis  -----------------------------------

def lexical_analysis():
	tokenString = ''										# Empty String
	global lineNo											# Load global variables
	global flag
	cur_state = 'start_state'								# state = state0 from lecture
	while(cur_state == 'start_state' or cur_state == 'dig_state' or cur_state == 'idk_state' or cur_state == 'asgn_state' or cur_state == 'smaller_state' or cur_state == 'larger_state' or cur_state == 'rem_state'):	# While ok and no errors
		char = input_program.read(1)						# Read next character
		if (char == ' ' or char == '\t' or char == '\n'):	# All white characters change the current state in the same way (in '\n' we have to also update the line counter)
			if (char == '\n'):
				lineNo = lineNo + 1							# If character is new line update the line counter
			t_char = 0										# We give t_char "codes" we can use to navigate in the transition table. Here 0 means that we seek the next state by looking in 1st column (transition_diagram[:][0])
		elif (char == '+'):									# Same for all the characters of Cimples' alphabet
			t_char = 1
		elif (char == '-'):
			t_char = 2
		elif (char == '*'):
			t_char = 3
		elif (char == '/'):
			t_char = 4
		elif (char == '{'):
			t_char = 5
		elif (char == '}'):
			t_char = 6
		elif (char == '('):
			t_char = 7
		elif (char == ')'):
			t_char = 8
		elif (char == '['):
			t_char = 9
		elif (char == ']'):
			t_char = 10
		elif (char == ','):
			t_char = 11
		elif (char == ';'):
			t_char = 12
		elif (char == ':'):
			t_char = 13
		elif (char == '='):
			t_char = 14
		elif (char == '<'):
			t_char = 15
		elif (char == '>'):
			t_char = 16
		elif (char == '.'):
			t_char = 17
		elif (char == '#'):
			t_char = 18	
			flag = flag + 1										# Count number of '#'. If odd number at the end of the program there is an unclosed comment section.
		elif (char == ''):										# End of File
			t_char = 19
		elif ('a' <= char <= 'z' or 'A' <= char <= 'Z'):		# Character is a English letter
			t_char = 20
		elif (char.isdigit()):									# Character is a digit
			t_char = 21
		else :													# If nothing from above => Wrong Input
			t_char = 22
		while(1):												# Find next state using the transition table for each state
			if (cur_state == 'start_state'):
				cur_state = transition_diagram[0][t_char]		# First row of transition table and depending on the t_char value we can find which is the next state. Same for the other 6
				break
			elif (cur_state == 'dig_state'):
				cur_state = transition_diagram[1][t_char]
				break
			elif (cur_state == 'idk_state'):
				cur_state = transition_diagram[2][t_char]
				break
			elif (cur_state == 'asgn_state'):	
				cur_state = transition_diagram[3][t_char]
				break
			elif (cur_state == 'smaller_state'):
				cur_state = transition_diagram[4][t_char]
				break
			elif (cur_state == 'larger_state'):
				cur_state = transition_diagram[5][t_char]
				break
			elif (cur_state == 'rem_state'):
				cur_state = transition_diagram[6][t_char]
				break
		if (len(tokenString) != 30):																																	# If string hasn't reach its length limit we can add token
			if(cur_state != 'start_state' and cur_state != 'rem_state'):																								# If no white characters or comments that means there is a useful token
					tokenString += char																																	# If char isn't new line add token
		else :
			print("Error! There is a string in line : ({}) that's at least 30 characters long (the maximum length).".format(lineNo))									# If string's length exceeds 30 characters end programm and print the error and end the program
			sys.exit()
		if (cur_state == 'assingment_state_error'):																														# Lines from #109 to #118 check for syntax errors
			print("Error! Not a equals (=) symbol after colon (:) in line ({}).".format(lineNo))
			sys.exit()
		if (cur_state == 'dig_state_error'):
			print("Error! In line : ({}). There is a letter in a numerical expression.".format(lineNo))
			sys.exit()
		if (cur_state == 'wrong_input_error'):
			print("Error! There is a character in line : ({}) that doesn't belong in the alphabet of this language.".format(lineNo))
			sys.exit()
		if ((flag % 2) != 0 and cur_state == 'eof'):																													# If flag is odd and eof then there is an open comment section
			print("Error! End of File but there is an unclosed comment section near the line : ({}).".format(lineNo))
			sys.exit()
	if (cur_state == 'number' or cur_state == 'identifier' or cur_state == 'smaller' or cur_state == 'larger'):
		if (char == '\n'):																																				# If new line -1 so the tokenString is returned with the right number line
			lineNo -= 1
		char = input_program.seek((input_program.tell() - 1), 0)																										# If we have completed a number, an identifier, the smaller and the lager state we exit that state which means that a character that doesn't belong the in the respective word unit has triggered that change. So go back one character in file to read it the next time
		tokenString = tokenString[:(len(tokenString) - 1)]																												# Cut that character from the string
	if(tokenString.isdigit()):
		if (int(tokenString) >= 2**32):																																	# Check for valid number
			print("Error! Number in line : ({}) is out of limits [-2^32 + 1, 2^32 - 1].".format(lineNo))
			sys.exit()
	if (tokenString.isalpha()):
		if tokenString in keywords:																																		# Check if it belongs in keywords table
			cur_state = 'keyword'
	#print(cur_state.ljust(22), tokenString.ljust(22), lineNo)
	return [cur_state, tokenString, lineNo]																																# Return cur_state which works as the tokenType, the tokenString and the line where was found	

# ---------------------------------  Syntax Analysis -----------------------------------

def syntax_analysis():
	def program(output):
		global programName
		templine = output[2]
		if (output[1] == 'program'):										# First string in file should be 'program'
			output = lexical_analysis()
			tempprogramName = output[1]
			if (output[0] == 'identifier'):									# Second should be programs' 'name' 
				output = lexical_analysis()
				output.append(tempprogramName)
				output.append('True')
				output = block(output)
				if (output[1] == '.'):										# Program ends with '.'
					return
				else :
					print("Error! Program doesn't end with '.' in line ({}).".format(output[2]))
					sys.exit()
			else:
				print("Error! With programs' name in line ({}).".format(templine))
				sys.exit()
		else :
			print("Error! Program does not start with 'program'. Line ({}).".format(output[2]))
			sys.exit()	

	def block(output):
		name = output[3]
		calledfromprogram = output[4]
		New_Scope(name)
		if (calledfromprogram == 'False'):
			addParameters()
		output = declarations(output)									    # First check for variable declarations
		output = subprograms(output)										# Check for functions and procedures
		genquad( "begin_block", name, "_", "_")
		if (calledfromprogram == 'False'):
			startQuad()
		output = statements(output)										    # Commands of main program
		if (calledfromprogram == 'True'):
			genquad( "halt", "_", "_", "_")
		else:
			framelength()
		genquad( "end_block", name, "_", "_")
		Symbol_Table()
		codegenerator()		
		delete_Scope()
		return output

	def declarations(output):
		while (output[1] == 'declare'):
			output = lexical_analysis()
			output = varlist(output)
			if (output[1] != ';'):											# Must see ';' at the end of declarations
				print("Error! Declarations section does not end with ';' in line ({}).".format(output[2]))
				sys.exit()
			else:
				output = lexical_analysis()
		return output

	def varlist(output):
		global listofidentifiers
		if (output[0] == 'identifier'):
			listofidentifiers.append(output[1])
			entity = Record_Entity()
			entity.name = output[1]
			entity.type = 'Variable'
			entity.variable.offset = offset()
			New_Entity(entity)
			output = lexical_analysis()
			while (output[1] == ',') :										# Variables are separated with commas
				output = lexical_analysis()
				if(output[0] == 'identifier'):
					listofidentifiers.append(output[1])
					entity = Record_Entity()
					entity.name = output[1]
					entity.type = 'Variable'
					entity.variable.offset = offset()
					New_Entity(entity)
					output = lexical_analysis()
				else :
					print("Error! Not an identifier after comma! Line : ({})".format(output[2]))
					sys.exit()
		else:
			print("Error! Not an identifier after 'declare' statement! Line : ({})".format(output[2]))
			sys.exit()
		return output

	def subprograms(output):
		global FunctionAndProcedureFlag
		while (output[1] == 'procedure' or output[1] == 'function'):
			FunctionAndProcedureFlag = 1
			if (output[1] == 'procedure'):
				isProcedure = 'True'
			else:
				isProcedure = 'False'				
			output = lexical_analysis()										# Subprogram
			tempsubprogramname = output[1]
			if (output[0] == 'identifier'):									# Functions' or procedures' name
				entity = Record_Entity()
				entity.type = 'Subprogram'
				entity.name = tempsubprogramname
				if (isProcedure == 'True'):
					entity.subprogram.type = 'Procedure'
				else :
					entity.subprogram.type = 'Function'
				New_Entity(entity)
				output = lexical_analysis()
				if (output[1] == '('):										# Parameters list in ( )
					output = lexical_analysis()
					output = formalparlist(output)
					if (output[1] == ')'):
						output = lexical_analysis()
						output.append(tempsubprogramname)
						output.append('False')
						output = block(output)
					else :
						print("Error! Bracket doesn't close after subprograms' list of formal parameters! Line : ({})".format(output[2]) )
						sys.exit()
				else :
					print("Error! Not a open bracket after subprogram ID! Line : ({})".format(output[2]) )	
					sys.exit()
			else :
				print("Error! Expected a subprogram ID! Line : ({})".format(output[2]) )
				sys.exit()
		return output

	def formalparlist(output):
		output = formalparitem(output)
		while (output[1] == ','):											# Parameters separated with commas
			output = lexical_analysis()
			output = formalparitem(output)
		return output

	def formalparitem(output):											    # A formal parameter
		if (output[1] == 'in'):
			output = lexical_analysis()
			if (output[0] == 'identifier'):
				argument = Record_Argument()
				argument.name = output[1]
				argument.parMode = 'CV'
				New_Argument(argument)
				output = lexical_analysis()
			else :
				print("Error! Not an identifier after 'in' statement! Line : ({})".format(output[2]) )
				sys.exit()
		elif (output[1] == 'inout'):
			output = lexical_analysis()
			if (output[0] == 'identifier'):
				argument = Record_Argument()
				argument.name = output[1]
				argument.parMode = 'REF'
				New_Argument(argument)
				output = lexical_analysis()
			else :
				print("Error! Not an identifier after 'inout' statement! Line : ({})".format(output[2]) )
				sys.exit()
		return output

	def statements(output):
		if (output[1] == '{'):												# If multiple statements we need {};
			output = lexical_analysis()
			output = statement(output)
			while (output[1] == ';'):
				output = lexical_analysis()
				output = statement(output)
			if (output[1] != '}'):
				print("Error! Syntax error at statement in line ({}).".format(output[2] - 1))
				sys.exit()
			else :
				output = lexical_analysis()
				return output
		else :
			output = statement(output)
			if (output[1] == ';'):
				output = lexical_analysis()
				return output
			else :
				print("Error! Statement in line ({}) doesn't end with ';'.".format(output[2]))
				sys.exit()

	def statement(output):
		if (output[0] == 'identifier'):									    # Assignment Statement
			idname = output[1]
			templine = output[2]
			output = lexical_analysis()
			if (output[1] == ':='):
				output = lexical_analysis()
				output = expression(output)
				genquad( ':=', output[3], '_', idname)
				return output
			else :
				print("Error! After 'identifier' an ':=' symbol is expected for assignment statement in line ({}).".format(templine))
				sys.exit()
		elif (output[1] == 'if'):										    # If Statement
			output = lexical_analysis()
			if (output[1] == '('):
				output = lexical_analysis()
				output = condition(output)
				backpatch(output[3], nextquad())
				bfalse = output[4]
				if (output[1] == ')'):
					output = lexical_analysis()
					output = statements(output)
					ifList = makelist(nextquad())
					genquad('jump', '_', '_', '_')
					backpatch(bfalse, nextquad())
					if (output[1] == 'else'):								# Else Part
						output = lexical_analysis()
						output = statements(output)
					backpatch(ifList, nextquad())
					return output
				else :
					print("Error! Closing bracket for whileStat condition was expected in line ({}).".format(output[2]))
					sys.exit()
			else:
				print("Error! Opening bracket for whileStat condition was expected in line ({}).".format(output[2]))
				sys.exit()
		elif (output[1] == 'while'):									    # While Statement
			output = lexical_analysis()
			if (output[1] == '(') :
				output = lexical_analysis()
				Bquad = nextquad()
				output = condition(output)
				backpatch(output[3], nextquad())
				bfalse = output[4]
				if (output[1] == ')') :
					output = lexical_analysis()
					output = statements(output)
					genquad('jump', '_', '_', Bquad)
					backpatch(bfalse, nextquad())
					return output
				else :
					print("Error! Closing bracket for whileStat condition was expected in line ({}).".format(output[2]))
					sys.exit()
			else:
				print("Error! Opening bracket for whileStat condition was expected in line ({}).".format(output[2]))
				sys.exit()
		elif (output[1] == 'switchcase'):								    # Switch Statement
			templine = output[2]
			output = lexical_analysis()
			exitlist = emptylist()
			while (output[1] == 'case'):
				output = lexical_analysis()
				if (output[1] == '('):
					output = lexical_analysis()
					output = condition(output)
					backpatch(output[3], nextquad())
					condFalse = output[4]
					if (output[1] == ')'):
						output = lexical_analysis()
						output = statements(output)
						e = makelist(nextquad())
						genquad( 'jump', '_', '_', '_')
						exitlist = merge(exitlist, e)
						backpatch(condFalse, nextquad())
					else :
						print("Error! Condtitions in switchcase section haven't closed properly. Line : ({}).".format(templine))
						sys.exit()		
				else :
					print("Error! An '(' is expected after case. Line : ({}).".format(templine))
					sys.exit()
			if (output[1] == 'default'):
				output = lexical_analysis()
				output = statements(output)
				backpatch(exitlist, nextquad())
			else :
				print("Error! Default statement is expected in switchcase. Line : ({}).".format(templine))
				sys.exit()
		elif (output[1] == 'forcase'):									    # Forcase Statement
			templine = output[2]
			output = lexical_analysis()
			quadcounter = nextquad()
			while (output[1] == 'case'):
				output = lexical_analysis()
				if (output[1] == '('):
					output = lexical_analysis()
					output = condition(output)
					backpatch(output[3], nextquad())
					condFalse = output[4]
					if (output[1] == ')'):
						output = lexical_analysis()
						output = statements(output)
						genquad( 'jump', '_', '_', quadcounter)
						backpatch(condFalse, nextquad())
					else :
						print("Error! Condtitions in forcase section haven't closed properly. Line : ({}).".format(templine))
						sys.exit()		
				else :
					print("Error! An '(' is expected after case. Line : ({}).".format(templine))
					sys.exit()
			if (output[1] == 'default'):
				output = lexical_analysis()
				output = statements(output)
			else :
				print("Error! Default statement is expected in forcase. Line : ({}).".format(templine))
				sys.exit()
		elif (output[1] == 'incase'):									    # Incase Statement
			templine = output[2]
			output = lexical_analysis()
			quadcounter = nextquad()
			w = newtemp()
			genquad( ':=', '1', '_', w)
			while (output[1] == 'case'):
				output = lexical_analysis()
				if (output[1] == '('):
					output = lexical_analysis()
					output = condition(output)
					backpatch(output[3], nextquad())
					condFalse = output[4]
					if (output[1] == ')'):
						output = lexical_analysis()
						output = statements(output)
						genquad( ':=', '0', '_', w)
						backpatch( condFalse, nextquad())
					else :
						print("Error! Condtitions section in incase haven't closed properly. Line : ({}).".format(templine))
						sys.exit()
				else :
					print("Error! An '(' is expected after case. Line : ({}).".format(templine))
					sys.exit()
			genquad( '=', w, '1', quadcounter)
		elif (output[1] == 'call'):										    # Call Statement
			templine = output[2]
			output = lexical_analysis()
			if (output[0] == 'identifier'):
				idname = output[1]
				output = lexical_analysis()
				if (output[1] == '('):
					output = lexical_analysis()
					output = actualparlist(output)
					genquad( 'call', idname, '_', '_')
					if (output[1] == ')'):
						output = lexical_analysis()
						return output
					else :
						print("Error! List of actual parameters in call statement hasn't closed properly. Line : ({}).".format(templine))
						sys.exit()
				else :
					print("Error! An '(' is expected after identifier in call statement. Line : ({}).".format(templine))
					sys.exit()
			else :
				print("Error! An identifier is expected after 'call'. Line : ({}).".format(templine))
				sys.exit()
		elif (output[1] == 'return' or output[1] == 'print'):			    # Return and Print Statement
			funcname = output[1]
			output = lexical_analysis()
			if (output[1] == '('):
				output = lexical_analysis()
				output = expression(output)
				if (funcname == 'print'):
					genquad( 'out', output[3], '_', '_')
				elif (funcname == 'return'):
					genquad( 'retv', output[3], '_', '_')
				if (output[1] == ')') :
					output = lexical_analysis()
					return output
				else :
					if (output[1] == 'return'):
						print("Error! Return statement hasn't close after expression in line ({}).".format(output[2]))
						sys.exit()
					else :
						print("Error! Print statement hasn't close after expression in line ({}).".format(output[2]))
						sys.exit()						
			else :
				if (output[1] == 'return'):
					print("Error! '(' was expected after return statement in line ({}).".format(output[2]))
					sys.exit()
				else :
					print("Error! '(' was expected after print statement in line ({}).".format(output[2]))
					sys.exit()
		elif (output[1] == 'input'):									    # Input Statement
			output = lexical_analysis()
			if (output[1] == '('):
				output = lexical_analysis()
				if (output[0] == 'identifier'):
					genquad('inp', output[1], '_', '_')
					output = lexical_analysis()
					if (output[1] == ')'):
						output = lexical_analysis()
						return output
					else :
						print("Error! Input statement hasn't close. Line ({}).".format(output[2]))
						sys.exit()
				else :
					print("Error! An identifier was expected after '(' in input statement. Line ({}).".format(output[2]))
					sys.exit()					
			else :
				print("Error! '(' was expected after input statement in line ({}).".format(output[2]))
				sys.exit()
		return output

	def actualparlist(output):												# Actual Parameters List
		if (output[1] == 'in'):
			output = lexical_analysis()
			output = expression(output)
			genquad( 'par', output[3], 'CV', '_')
		elif (output[1] == 'inout'):
			output = lexical_analysis()
			if (output[0] != 'identifier'):
				print("Error! Not an identifier after inout in line ({}).".format(output[2]))
				sys.exit()
			else :
				genquad( 'par', output[1], 'REF', '_')
				output = lexical_analysis()
		while (output[1] == ','):
			output = lexical_analysis()
			if (output[1] == 'in'):
				output = lexical_analysis()
				output = expression(output)
				genquad( 'par', output[3], 'CV', '_')
			elif (output[1] == 'inout'):
				output = lexical_analysis()
				if (output[0] != 'identifier'):
					print("Error! Not an identifier after inout in line ({}).".format(output[2]))
					sys.exit()
				else :
					genquad( 'par', output[1], 'REF', '_')
					output = lexical_analysis()		
		return output

	def condition(output):												    # Boolean Exression
		conditionTrue = []
		conditionFalse = []
		output = boolterm(output)
		conditionTrue = output[3]
		conditionFalse = output[4]
		while (output[1] == 'or') :
			output = lexical_analysis()
			backpatch(conditionFalse, nextquad())
			output = boolterm(output)
			conditionTrue = merge(conditionTrue, output[3])
			conditionFalse = output[4]
		if (len(output) == 3):
			output.append(conditionTrue)
			output.append(conditionFalse)
		elif (len(output) == 4):
			output[3] = conditionTrue
			output.append(conditionFalse)
		elif (len(output) == 5):
			output[3] = conditionTrue
			output[4] = conditionFalse
		return output

	def boolterm(output):												    # Term in Boolean Expression
		booltermTrue = []
		booltermFalse = []
		output = boolfactor(output)
		booltermTrue = output[3]
		booltermFalse = output[4]
		while (output[1] == 'and'):
			output = lexical_analysis()
			backpatch(booltermTrue, nextquad())
			output = boolfactor(output)
			booltermFalse = merge(booltermFalse, output[4])
			booltermTrue = output[3]
		if (len(output) == 3):
			output.append(booltermTrue)
			output.append(booltermFalse)
		elif (len(output) == 4):
			output[3] = booltermTrue
			output.append(booltermFalse)
		elif (len(output) == 5):
			output[3] = booltermTrue
			output[4] = booltermFalse
		return output

	def boolfactor(output):
		boolfactorTrue = []
		boolfactorFalse = []
		reloperator = '_'	                   								# Just initialization (Should NOT be printed)
		if (output[1] == 'not'):				                			# Not condition
			output = lexical_analysis()
			if (output[1] == '['):
				output = lexical_analysis()
				output = condition(output)
				tempcondition = output.copy()				                # Temporary copy cause we have to use output to close bracket
				if (output[1] == ']'):
					output = lexical_analysis()
					boolfactorTrue = tempcondition[3]
					boolfactorFalse = tempcondition[4]
				else :
					print("Error! Closing bracket after condition was expected in line ({}).".format(output[2]))
					sys.exit()
			else : 
				print("Error! Opening bracket after 'not' statement was expected in line ({}).".format(output[2]))
				sys.exit()
		elif (output[1] == '['):											# Condition
			output = lexical_analysis()
			output = condition(output)
			tempcondition = output.copy()									# Temporary copy cause we have to use output to close bracket
			if (output[1] == ']'):
				output = lexical_analysis()
				boolfactorTrue = tempcondition[3]
				boolfactorFalse = tempcondition[4]
			else :
				print("Error! ']' after condition was expected in line ({}).".format(output[2]))
				sys.exit()
		else :																# Expression rel_op expression
			e1place = output[1]
			output = expression(output)
			if (output[1] not in rel_op):
				print("Error! A relational operator was expected in the expression. Line ({}).".format(output[2]))
				sys.exit()
			else:
				for x in range(len(rel_op)):
					if (output[1] == rel_op[x]):
						reloperator = rel_op[x]
				output = lexical_analysis()
				e2place = output[1]
				output = expression(output)
				boolfactorTrue = makelist(nextquad())
				genquad(reloperator, e1place, e2place, '_')
				boolfactorFalse = makelist(nextquad())
				genquad('jump', '_', '_', '_')
		if (len(output) == 3):
			output.append(boolfactorTrue)
			output.append(boolfactorFalse)
		elif (len(output) == 4):
			output[3] = boolfactorTrue
			output.append(boolfactorFalse)
		elif (len(output) == 5):
			output[3] = boolfactorTrue
			output[4] = boolfactorFalse
		return output		

	def expression(output):
		global optionalsign
		if (output[1] == '+' or output[1] == '-'):							# symbols "+" and "-" are optional
			optionalsign = output[1]
			output = lexical_analysis()
		output = term(output)
		T1place = output[3]
		while (output[1] == '+' or output[1] == '-'):
			arithmeticsymbol = output[1]
			output = lexical_analysis()
			output = term(output)
			T2place = output[3]
			w = newtemp()
			genquad( arithmeticsymbol, T1place, T2place, w)
			T1place = w
		if (len(output) == 4):
			output[3] = T1place
		else:
			output.append(T1place)
		return output
	
	def term(output):
		output = factor(output)
		F1place = output[3]
		while (output[1] == '*' or output[1] == '/'):
			multiplicationsymbol = output[1]
			output = lexical_analysis()
			output = factor(output)
			F2place = output[3]
			w = newtemp()
			genquad( multiplicationsymbol, F1place, F2place, w)
			F1place = w
		if (len(output) == 4):
			output[3] = F1place
		else:
			output.append(F1place)
		return output

	def factor(output):
		global optionalsign
		factorflag = 0													# If we find identifier we should return id.place or (w for us) from idtail() else we should return Eplace
		if (output[1].isdigit()):										# Integer
			if (optionalsign != ''):
				temp = output[1]
				out = optionalsign + temp
				output[1] = out
				optionalsign = ''
			Eplace = str(output[1])
			output = lexical_analysis()
		elif (output[1] == '('):										# Expression
			output = lexical_analysis()
			output = expression(output)
			Eplace = output[3]
			if (output[1] == ')'):
				output = lexical_analysis()
			else :
				print("Error! Closing bracket after expression was expected in line ({}).".format(output[2]))
				sys.exit()
		elif (output[0] == 'identifier'):								# ID idtail
			factorflag = 1												# If flag equals 1 then it means we have to return what idtail() returns
			Eplace = output[1]
			output = lexical_analysis()
			output.append(Eplace)
			output = idtail(output)
		else :
			print("Error! Wrong factor syntax in line ({}).".format(output[2]))
			sys.exit()
		if (len(output) == 4 and factorflag == 0):						# Flag check
			output[3] = Eplace
		elif (len(output) == 3 and factorflag == 0):
			output.append(Eplace)
		return output

	def idtail(output):
		assign_v = output[3]
		if (output[1] == '('):
			output = lexical_analysis()
			output = actualparlist(output)
			w = newtemp()
			genquad( 'par', w, 'RET', '_')
			genquad( 'call', assign_v, '_', '_')
			if (output[1] == ')'):
				output = lexical_analysis()
				output.append(w)
				return output
			else:
				print("Error! Closing bracket after expression was expected in line ({}).".format(output[2]))
		return output
	output = lexical_analysis()
	program(output)														# Call program() to run syntax analyzer
	return

# ----------------------------  Intermediate Code Generator -----------------------------

def nextquad():															# Number of next Quad
	global quadnum
	
	return quadnum

def genquad(op, x, y, z):												# Generate Next Quad
	global QuadsCodeGenerator
	global QuadsOutputFiles
	global quadnum
	quadlist = [nextquad(), op, x, y, z]
	quadnum = quadnum + 1
	QuadsOutputFiles.append(quadlist)
	QuadsCodeGenerator.append(quadlist)
	return quadlist

def newtemp(): 															# Create new temporary variable
	global i
	global listoftemps
	temp = 'T_' + str(i)												# Create unique temporary variable
	i = i + 1
	listoftemps.append(temp)
	entity = Record_Entity()
	entity.type = 'Temporary Variable'
	entity.name = temp
	entity.tempvar.offset = offset()
	New_Entity(entity)
	return temp

def emptylist():														# Create an empty list
	emptylist = []
	return emptylist

def makelist(x):														# Create quad label list
	labellist = [x]
	return labellist

def merge(list1, list2):												# Merges two lists to create quad label list
	mergelist = []
	mergelist.extend(list1)
	mergelist.extend(list2)
	return mergelist

def backpatch(list, z):													# Fill QuadsOutputFiles[][4] with z if empty
	global QuadsOutputFiles
	for i in range(len(list)):
		for j in range(len(QuadsOutputFiles)):
			if (list[i] == QuadsOutputFiles[j][0] and QuadsOutputFiles[j][4] == '_'):
				QuadsOutputFiles[j][4] = z
				break													# Break because only one quad at time fills QuadsOutputFiles[][4] with z if empty
	return

# ---------------------------------- Symbol Table ---------------------------------------

class Record_Entity():
	def __init__(self):
		self.name = ''
		self.type = ''
		self.variable = self.Variable()
		self.subprogram = self.Subprogram()
		self.parameter = self.Parameter()
		self.tempvar = self.TempVar()
	class Variable:
		def __init__(self):
			self.type = 'Integer'
			self.offset = 0
	class Subprogram:
		def __init__(self):
			self.type = ''
			self.startQuad = 0
			self.argument = []
			self.framelength = 0
	class Parameter:
		def __init__(self):
			self.mode = ''
			self.offset = 0
	class TempVar:
		def __init__(self):
			self.type = 'Integer'
			self.offset = 0

class Record_Scope():
	def __init__(self):
		self.name = ''
		self.List_Entity = []
		self.nestinglevel = 0
		self.enclosingScope = None

class Record_Argument():
	def __init__(self):
		self.name = ''
		self.parMode = ''
		self.type = 'Integer'

Top_Scope = None

def New_Scope(name):
	global Top_Scope
	newscope = Record_Scope()
	newscope.name = name
	newscope.enclosingScope = Top_Scope
	if(Top_Scope == None):
		newscope.nestinglevel = 0
	else:
		newscope.nestinglevel = Top_Scope.nestinglevel + 1
	Top_Scope = newscope

def New_Entity(object):
	global Top_Scope
	Top_Scope.List_Entity.append(object)

def New_Argument(object):
	global Top_Scope
	Top_Scope.List_Entity[-1].subprogram.argument.append(object)

def delete_Scope():
	global Top_Scope
	delscope = Top_Scope
	Top_Scope = Top_Scope.enclosingScope
	del delscope

def offset():
	global Top_Scope
	offset_count = 0
	
	if(len(Top_Scope.List_Entity) != 0):
		for entity in Top_Scope.List_Entity:
			if (entity.type == 'Variable' or entity.type == 'Temporary Variable' or entity.type == 'Parameter') :
				offset_count = offset_count + 1
	offset = 12 + (offset_count * 4)
	return offset

def startQuad():
	global Top_Scope
	Top_Scope.enclosingScope.List_Entity[-1].subprogram.startQuad = nextquad()

def framelength():
	global Top_Scope
	Top_Scope.enclosingScope.List_Entity[-1].subprogram.framelength = offset()

def addParameters():
	global Top_Scope
	for argument in Top_Scope.enclosingScope.List_Entity[-1].subprogram.argument:
		entity = Record_Entity()
		entity.name = argument.name
		entity.type = 'Parameter'
		entity.parameter.mode = argument.parMode
		entity.parameter.offset = offset()
		New_Entity(entity)

def Symbol_Table():
	global Top_Scope
	global Symboltablefile

	scope = Top_Scope
	while scope != None:
		print("Nesting Level: "+str(scope.nestinglevel), file = Symboltablefile)
		print("\t" + "Scope: "+scope.name, file = Symboltablefile) 
		print("\t\tEntities:", file = Symboltablefile)
		for entity in scope.List_Entity:
			if(entity.type == 'Variable'):
				print("\t\t\t" + entity.name + " " + entity.type + " " + entity.variable.type + " " + str(entity.variable.offset), file = Symboltablefile)
			elif(entity.type == 'Temporary Variable'):
				print("\t\t\t" + entity.name + " " + entity.type + " " + entity.tempvar.type + " " + str(entity.variable.offset), file = Symboltablefile)
			elif(entity.type == 'Subprogram'):
				if(entity.subprogram.type == 'Function'):
					print("\t\t\t" + entity.name + " " + entity.type + " " + entity.subprogram.type + " " + str(entity.subprogram.startQuad) + " " + str(entity.subprogram.framelength), file = Symboltablefile)
					print("\t\t\t\t" + "Arguments:", file = Symboltablefile)
					if(len(entity.subprogram.argument) != 0):
						for argument in entity.subprogram.argument:
							print("\t\t\t\t\t" + argument.name + " " + argument.type + " " + argument.parMode, file = Symboltablefile)
					else:
						print("\t\t\t\t\t" + "Function has no Arguments", file = Symboltablefile)
				elif(entity.subprogram.type == 'Procedure'):
					print("\t\t\t" + entity.name + " " + entity.type + " " + entity.subprogram.type + " " + str(entity.subprogram.startQuad) + " " + str(entity.subprogram.framelength), file = Symboltablefile)
					print("\t\t\t\t" + "Arguments:", file = Symboltablefile)
					if(len(entity.subprogram.argument) != 0):
						for argument in entity.subprogram.argument:
							print("\t\t\t\t\t" + argument.name + " " + argument.type + " " + argument.parMode, file = Symboltablefile)
					else:
						print("\t\t\t\t\t" + "Procedure has no Arguments", file = Symboltablefile)
			elif(entity.type == 'Parameter'):
				print("\t\t\t" + entity.name + " " + entity.type + " " + entity.parameter.mode + " " + str(entity.parameter.offset), file = Symboltablefile)
		scope = scope.enclosingScope


# ------------------------------  ASC and Symbol Table File  ----------------------------

ASCFile = open('ascFile.asm', 'w')
Symboltablefile = open('SymbolTable.txt', 'w')

# ----------------------------------  Code Generator  -----------------------------------

def ancestor_stack(variable):
	global Top_Scope
	scope = Top_Scope
	while(scope != None):
		for entity in scope.List_Entity:
			if(entity.name == variable):
				return [Top_Scope, entity]
		scope = scope.enclosingScope
	print('Could not find scope with {} variable!'.format(variable))
	sys.exit()

def gnvlcode(variable):
	global Top_Scope
	global ASCFile

	print('lw $t0,-4($sp)', file = ASCFile)
	variableinfo = ancestor_stack(variable)
	for i in range(1,(Top_Scope.nestinglevel - variableinfo[0],nestinglevel)):
		print('lw $t0,-4($t0)', file = ASCFile)
	if(variableinfo[1].type == 'Variable'):
		print('add $t0,$t0,-{}'.format(variableinfo[1].variable.offset), file = ASCFile)
	if(variableinfo[1].type == 'Parameter'):
		print('add $t0,$t0,-{}'.format(variableinfo[1].parameter.offset), file = ASCFile)

def loadvr(v, r):
	global Top_Scope
	global ASCFile

	if(v.lstrip("-").isdigit()):							# Strip so we we can check for negative numbers
		print('li $t{},{}'.format(r, v), file = ASCFile)
	else:
		variableinfo = ancestor_stack(v)
		if(variableinfo[0].nestinglevel == 0):
			if(variableinfo[1].type == 'Variable'):
				print('lw $t{},-{}($s0)'.format(r, variableinfo[1].variable.offset), file = ASCFile)
			elif(variableinfo[1].type == 'Parameter'):
				print('lw $t{},-{}($s0)'.format(r, variableinfo[1].parameter.offset), file = ASCFile)
		elif(variableinfo[0].nestinglevel == Top_Scope.nestinglevel):
			if(variableinfo[1].type == 'Variable'):
				print('lw $t{},-{}($sp)'.format(r, variableinfo[1].variable.offset), file = ASCFile)
			elif(variableinfo[1].type == 'Parameter'):
				if(variableinfo[1].parameter.mode == 'CV'):
					print('lw $t{},-{}($sp)'.format(r, variableinfo[1].parameter.offset), file = ASCFile)
				elif(variableinfo[1].parameter.mode == 'REF'):
					print('lw $t0,-{}($sp)'.format(r, variableinfo[1].parameter.offset), file = ASCFile)
					print('lw $tr,($t0)'.format(r), file = ASCFile)
			elif(variableinfo[1].type == 'Temporary Variable'):
				print('lw $t{},-{}($sp)'.format(r, variableinfo[1].tempvar.offset), file = ASCFile)
		elif(variableinfo[0].nestinglevel < Top_Scope.nestinglevel):
			if(variableinfo[1].type == 'Variable'):
				gnvlcode(v)
				print('lw $t{},($t0)'.format(r), file = ASCFile)
			elif(variableinfo[1].type == 'Parameter'):
				if(variableinfo[1].parameter.mode == 'CV'):
					gnvlcode(v)
					print('sw $t{},($t0)'.format(r), file = ASCFile)
				elif(variableinfo[1].parameter.mode == 'REF'):
					gnvlcode(v)
					print('lw $t0,($t0)', file = ASCFile)
					print('sw $t{},($t0)'.format(r), file = ASCFile)

def storerv(r, v):
	global Top_Scope
	global ASCFile
	variableinfo = ancestor_stack(v)
	if(variableinfo[0].nestinglevel == 0):
		if(variableinfo[1].type == 'Variable'):
			print('sw $t{},-{}($s0)'.format(r, variableinfo[1].variable.offset), file = ASCFile)
		elif(variableinfo[1].type == 'Parameter'):
			print('sw $t{},-{}($s0)'.format(r, variableinfo[1].parameter.offset), file = ASCFile)
	elif(variableinfo[0].nestinglevel == Top_Scope.nestinglevel):
		if(variableinfo[1].type == 'Variable'):
			print('sw $t{},-{}($sp)'.format(r, variableinfo[1].variable.offset), file = ASCFile)
		elif(variableinfo[1].type == 'Parameter'):
			if(variableinfo[1].parameter.mode == 'CV'):
				print('sw $t{},-{}($sp)'.format(r, variableinfo[1].parameter.offset), file = ASCFile)
			elif(variableinfo[1].parameter.mode == 'REF'):	
				print('lw $t0,-{}($sp)'.format(r, variableinfo[1].parameter.offset), file = ASCFile)
				print('sw $tr,($t0)'.format(r), file = ASCFile)
		elif(variableinfo[1].type == 'Temporary Variable'):
			print('sw $t{},-{}($sp)'.format(r, variableinfo[1].tempvar.offset), file = ASCFile)
	elif(variableinfo[0].nestinglevel < Top_Scope.nestinglevel):
		if(variableinfo[1].type == 'Variable'):
			gnvlcode(v)
			print('sw $t{},($t0)'.format(r), file = ASCFile)
		elif(variableinfo[1].type == 'Parameter'):
			if(variableinfo[1].parameter.mode == 'CV'):
				gnvlcode(v)
				print('sw $t{},($t0)'.format(r), file = ASCFile)
			elif(variableinfo[1].parameter.mode == 'REF'):
				gnvlcode(v)
				print('lw $t0,($t0)', file = ASCFile)
				print('sw $t{},($t0)'.format(r), file = ASCFile)

def codegenerator():
	global Top_Scope
	global QuadsCodeGenerator
	global ASCFile
	global FunctionAndProcedureFlag
	for j in range(len(QuadsCodeGenerator)):
		if(QuadsCodeGenerator[j][1] == 'begin_block' and Top_Scope.nestinglevel == 0):
			print('j L{}'.format(QuadsCodeGenerator[j][0]), file = ASCFile)
	for i in range(len(QuadsCodeGenerator)):
		if(QuadsCodeGenerator[i][1] == 'end_block' and Top_Scope.nestinglevel == 0): 		# Do nothing for end block in program
			pass
		elif(QuadsCodeGenerator[i][1] == 'halt'):											# Do nothing
			pass
		elif(QuadsCodeGenerator[i][1] == 'par' or QuadsCodeGenerator[i][3] == 'CV' or QuadsCodeGenerator[i][3] == 'REF' or QuadsCodeGenerator[i][1] == 'call'):
			pass
		else:	
			print('L{}:'.format(QuadsCodeGenerator[i][0]), file = ASCFile)
			if(QuadsCodeGenerator[i][1] == 'jump'):
			if(QuadsCodeGenerator[i][1] in rel_op):
				print('b L{}'.format(QuadsCodeGenerator[i][4]), file = ASCFile)
				loadvr(QuadsCodeGenerator[i][2], 1)
				loadvr(QuadsCodeGenerator[i][3], 2)
				if(QuadsCodeGenerator[i][1] == '='):
					print('beq,$t1,$t2,L{}'.format(QuadsCodeGenerator[i][4]), file = ASCFile)
				if(QuadsCodeGenerator[i][1] == '<>'):
					print('bne,$t1,$t2,L{}'.format(QuadsCodeGenerator[i][4]), file = ASCFile)
				if(QuadsCodeGenerator[i][1] == '>'):
					print('bgt,$t1,$t2,L{}'.format(QuadsCodeGenerator[i][4]), file = ASCFile)
				if(QuadsCodeGenerator[i][1] == '<'):
					print('blt,$t1,$t2,L{}'.format(QuadsCodeGenerator[i][4]), file = ASCFile)
				if(QuadsCodeGenerator[i][1] == '<='):
					print('ble,$t1,$t2,L{}'.format(QuadsCodeGenerator[i][4]), file = ASCFile)
				if(QuadsCodeGenerator[i][1] == '>='):
					print('bge,$t1,$t2,L{}'.format(QuadsCodeGenerator[i][4]), file = ASCFile)
			elif(QuadsCodeGenerator[i][1] == ':='):
				loadvr(QuadsCodeGenerator[i][2], 1)
				storerv(1, QuadsCodeGenerator[i][4])
			elif(QuadsCodeGenerator[i][1] in ari_op):
				loadvr(QuadsCodeGenerator[i][2], 1)
				loadvr(QuadsCodeGenerator[i][3], 2)
				if(QuadsCodeGenerator[i][1] == '+'):
					print('add,$t1,$t1,$t2', file = ASCFile)
				if(QuadsCodeGenerator[i][1] == '-'):
					print('sub,$t1,$t1,$t2', file = ASCFile)
				if(QuadsCodeGenerator[i][1] == '*'):
					print('mul,$t1,$t1,$t2', file = ASCFile)
				if(QuadsCodeGenerator[i][1] == '/'):
					print('div,$t1,$t1,$t2', file = ASCFile)
				storerv(1, QuadsCodeGenerator[i][4])
			elif(QuadsCodeGenerator[i][1] == 'out'):
				print('li $v0,1', file = ASCFile)
				loadvr(QuadsCodeGenerator[i][2], 1)
				print('move $a0,$t1', file = ASCFile)
				print('syscall', file = ASCFile)
			elif(QuadsCodeGenerator[i][1] == 'inp'):
				print('li $v0,5', file = ASCFile)
				print('syscall', file = ASCFile)
				print('move $t1,$v0', file = ASCFile)
				storerv(1, QuadsCodeGenerator[i][2])
			elif(QuadsCodeGenerator[i][1] == 'retv'):
				loadvr(QuadsCodeGenerator[i][2], 1)
				print('lw $t0,-8($sp)', file = ASCFile)
				print('sw $t1,($t0)', file = ASCFile)
			elif(QuadsCodeGenerator[i][1] == 'begin_block'):
				if(Top_Scope.nestinglevel == 0):
					print('add $sp,$sp,{}'.format(offset()), file = ASCFile)
					print('move $s0,$sp', file = ASCFile)
				else:
					print('sw $ra,($sp)', file = ASCFile)
			elif(QuadsCodeGenerator[i][1] == 'end_block'):							# End block in function/procedure
				print('lw $ra,($sp)', file = ASCFile)
				print('jr $ra', file = ASCFile)
	QuadsCodeGenerator = []

syntax_analysis()

#if(FunctionAndProcedureFlag == 1):
	#print("Program ends but .asm file doesn't work properly because function(s) and/or procedure(s) exist! Every other file in output works.")
# ---------------------------------  Quad and C# Files  ---------------------------------

quadfile = open('test.int', 'w')									# If everything is ok from syntax and lexical analysis open file to save the quads
#for i in range(len(QuadsOutputFiles)):
#	print(str(QuadsOutputFiles[i][0]).ljust(8), str(QuadsOutputFiles[i][1]).ljust(24), str(QuadsOutputFiles[i][2]).ljust(32), str(QuadsOutputFiles[i][3]).ljust(32), str(QuadsOutputFiles[i][4]))	# Print quad in file
quadfile.close()

if (FunctionAndProcedureFlag == 0):									# If function(s) or/and procudure(s) exists in program we won't create C# file
	CFile = open('test.c', 'w')
	print("#include <stdio.h>", file = CFile)
	print("int main(void){", file = CFile)
	if (len(listofidentifiers) != 0):
		print("\tint ", end = '', file = CFile)
	for i in range(len(listofidentifiers)):
		if ((i + 1) != len(listofidentifiers)):							# If i not the last ([i + 1] if last will break the loop) print identifiers separated with (,)
			print(listofidentifiers[i], end = '', file = CFile)
			print(",", end = ' ', file = CFile)
		else:															# If last print the identifier with (;)
			print(listofidentifiers[i], end = '', file = CFile)
			print(";", file = CFile)
	if (len(listoftemps) != 0):											# Same for temporary variables
		print("\tint ", end = '', file = CFile)
	for i in range(len(listoftemps)):
		if ((i + 1) != len(listoftemps)):
			print(listoftemps[i], end = '', file = CFile)
			print(",", end = ' ', file = CFile)
		else:
			print(listoftemps[i], end = '', file = CFile)
			print(";\n", file = CFile)
	for i in range(len(QuadsOutputFiles)):										# No check for return cause means there is a function that returns value and as we have stated functions cannot exist in this C program
		if (QuadsOutputFiles[i][1] == 'begin_block'):
			print("\t" + "L_" + str(i+1) + " :" + "\t\t", end = ' ', file = CFile)
		elif (QuadsOutputFiles[i][1] in rel_op):
			print("\t" + "L_" + str(i+1) + " : " + "if (" + str(QuadsOutputFiles[i][2]) + " " + str(QuadsOutputFiles[i][1]) + " " + str(QuadsOutputFiles[i][3]) +") goto L_" + str(QuadsOutputFiles[i][4]) + ";" + "\t\t", end = ' ', file = CFile)		# If we find relational operator write expression and "goto" to let program know where to jump
		elif (QuadsOutputFiles[i][1] in ari_op):
			print("\t" + "L_" + str(i+1) + " : " + str(QuadsOutputFiles[i][4]) + " = " + str(QuadsOutputFiles[i][2]) + " " + str(QuadsOutputFiles[i][1]) + " " + str(QuadsOutputFiles[i][3]) + ";" + "\t\t", end = ' ', file = CFile)
		elif (QuadsOutputFiles[i][1] == ':='):
			print("\t" + "L_" + str(i+1) + " : " + str(QuadsOutputFiles[i][4]) + " = " + str(QuadsOutputFiles[i][2]) + ";" + "\t\t", end = ' ', file = CFile)
		elif (QuadsOutputFiles[i][1] == 'jump'):
			print("\t" + "L_" + str(i+1) + " : " + "goto L_" + str(QuadsOutputFiles[i][4]) + ";" + "\t\t", end = ' ', file = CFile)														# If we find jump.. "goto" where to go
		elif (QuadsOutputFiles[i][1] == 'out'):
			print("\t" + "L_" + str(i+1) + " : " + "printf(\"" +  str(QuadsOutputFiles[i][2]) + " = %d\", " + QuadsOutputFiles[i][2] +");" + "\t\t", end = ' ', file = CFile)
		elif (QuadsOutputFiles[i][1] == 'inp'):
			print("\t" + "L_" + str(i+1) + " : " + "scanf(\"%d\", " + "&" + QuadsOutputFiles[i][2] +");" + "\t\t", end = ' ', file = CFile)
		elif (QuadsOutputFiles[i][1] == 'halt'):
			print("\t" + "L_" + str(i+1) + " : {};" + "\t\t", end = ' ', file = CFile)
		print("/*" + ' ' + "( " + str(QuadsOutputFiles[i][1]) + ' ' + str(QuadsOutputFiles[i][2]) +  ' ' + str(QuadsOutputFiles[i][3]) + ' ' + str(QuadsOutputFiles[i][4]) + " )" + ' ' + "*/", file = CFile)			# Print quad in comment
	print("}", end = '', file = CFile)
	CFile.close()