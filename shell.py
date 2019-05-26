import os
import sys
import stat
import subprocess

# Global text variables
ascii_art = """
$$$$$$$\             $$$$$$\  $$\                 $$\ $$\ 
$$  __$$\           $$  __$$\ $$ |                $$ |$$ |
$$ |  $$ |$$\   $$\ $$ /  \__|$$$$$$$\   $$$$$$\  $$ |$$ |
$$$$$$$  |$$ |  $$ |\$$$$$$\  $$  __$$\ $$  __$$\ $$ |$$ |
$$  ____/ $$ |  $$ | \____$$\ $$ |  $$ |$$$$$$$$ |$$ |$$ |
$$ |      $$ |  $$ |$$\   $$ |$$ |  $$ |$$   ____|$$ |$$ |
$$ |      \$$$$$$$ |\$$$$$$  |$$ |  $$ |\$$$$$$$\ $$ |$$ |
\__|       \____$$ | \______/ \__|  \__| \_______|\__|\__|
          $$\   $$ |                                      
          \$$$$$$  |                                      
           \______/ 
		   
[ascii art from http://patorjk.com/software/taag/]

"""

version_text = """
PyShell Version 1.0
%s
This shell allows users to run basic bash commands
Supported functions include:
	- cd
	- pwd
	- command chaining [&&]
	- commands accessible by the $PATH

Functions that I hope to support include:
	- input/output redirection with '<' and '>'
	- piping
	- nowaiting by adding '&' after commands
""" % (ascii_art)

working_directory = str(os.getcwd())

"""
Main method handles basic bash loop
and handles user input
"""
def main():
	
	global working_directory	
	while(True):
		try:
			command = input("PyShell::%s$ " % (working_directory.replace(os.getenv("HOME"), "~")))
		except EOFError:
			print("exit")
			break
		if command == "":
			continue
		if command == "exit":
			break

		# split up command elements by successive cases
		list_of_commands = command.split("&&")
		# Run each command
		for action in list_of_commands:
			execute_command(action.split(), action[len(action)-1] == '&')


"""
Function that executes a program
currently does not handle for piping
"""
def execute_command(args, nowait):

	# Built-In Commands
	if args[0] == "version":
		version()
	
	elif args[0] == "pwd":
		print(os.getcwd())
	
	elif args[0] == "cd":
		change_directory(args)
	
	else:
		child_process = os.fork()
		
		# Error
		if(child_process < 0):
			print("Error handling 'fork()' action", file=sys.stderr)
		
		# Child
		elif(child_process == 0):
			run_program(args)
		
		# Parent
		else:
			os.waitpid(child_process, 0)


"""
Function that runs binary executable files
- Assumes that "args" is the user's command split by spaces
Execution handles for two cases:
	1) User has specified absolute path to the executable
	2) Executable specified may be defined in the $PATH
"""
def run_program(args):
	
	# User gave an absolute path
	if args[0][0] == '/' or args[0][0] == '.':
		try:
			os.execve(args[0], args, os.environ)
		except FileNotFoundError:
			print("No program: '%s' found" % (args[0]), file=sys.stderr)

	# Must search envionment path
	else:
		environment_path = os.getenv("PATH")
		executable_paths = environment_path.split(":")
		for path in executable_paths:
			current_path = "%s/%s" % (path, args[0])
			try:
				os.execve(current_path, args, os.environ)
			except:
				continue
		print("No program: '%s' found" % (args[0]), file=sys.stderr)
		sys.exit()

"""
Function that takes a 'cd' command and tries to 
change the current directory to what the user has specified
"""
def change_directory(args):

	global working_directory
	
	if len(args) == 1 or args[1] == "~":
		os.chdir(os.getenv("HOME"))
	
	else:
		try:
			home_text = os.getenv("HOME") + "/"
			os.chdir(args[1].replace("~", home_text))
		except FileNotFoundError as err:
			print(err)
	
	check_dir = str(os.getcwd())
	if check_dir != working_directory:
		working_directory = check_dir

"""
Return basic info about the shell
[Not much relevant information here right now]
"""
def version():
	global version_text
	print(version_text)

main()
