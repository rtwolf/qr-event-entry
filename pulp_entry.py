# PULP entry thing - pulpartparty.ca

import pprint, os, re, sys, time, zbar, StringIO, pyglet
from os import walk
from sys import argv
from subprocess import Popen, PIPE
# termcolor from here: https://pypi.python.org/pypi/termcolor
from termcolor import colored, cprint

user_input = ""
undo_list = []

def undo(out=sys.stdout):
	'''Undoes last entry. Yay!
	'''
	pp = pprint.PrettyPrinter(indent=4)
	entered = ""
	entered = load_guests("lists/entered.csv")
	if entered == "":
		out.write("No people here yet!")
	else:
		entered = entered.split("\r")
		if entered[-1] != "":
			print "The following person has been unadmitted: "
			pp.pprint(entered[-1])
			f = open ("lists/guests.csv", "a")
			f.write(entered[-1] + "\r\n")
			f.close()
			del entered[-1]
		elif entered[-2] != "":
			print "The following person has been unadmitted: "
			pp.pprint(entered[-2])
			f = open ("lists/guests.csv", "a")
			f.write(entered[-2] + "\r\n")
			f.close()
			del entered[-2]
		write_file("lists/entered.csv", "\r".join(entered))


def load_guests(file_name):
	'''Loads csv into memory as a string'''
	f = open(file_name, 'r')
	guest_list = f.read()
	f.close()
	return guest_list

def write_file(file_name, text):
	f = open(file_name, "w")
	f.write(text)
	f.close()

def entry(ticket):
	'''Handles the work of a guest being registered as entered:
	- alters guest_list and writes the updated version to a files
	- adds guest entry to other csv of people in
	- Adds to undo list to make that a possibility
	'''
	file_name = "lists/guests.csv"
	guest_list = load_guests(file_name)
	# backup
	write_file("lists/guests" + time.strftime("%d%H%M%S") + ".csv", guest_list)
	guest_list = guest_list.replace(ticket, "")
	# write new file
	write_file(file_name, guest_list)

	f = open ("lists/entered.csv", "a")
	f.write(ticket)
	f.close()

def main(list_to_use, out=sys.stdout):
	pp = pprint.PrettyPrinter(indent=4)
	user_input = ""
	# inspired by this: http://lateral.netmanagers.com.ar/weblog/posts/BB913.html then updated with subprocess
	# p = Popen(["zbarcam", "--raw"], stdout = PIPE)
	entry_success = colored("\nYou're in!", 'blue')
	song = pyglet.media.load('Windows Exclamation.wav')
	song.play()
	pyglet.app.run()
	while user_input != "exit":
		guest_list = load_guests(list_to_use)
		# print p.stdout.readline()
		# user_input = p.readline()
		user_input = raw_input(colored("\nScan a QR code or enter name/email address: ", 'red'))
		user_input = user_input.strip()
		if user_input == "exit": # typed exit
			out.write("\nGood bye!")
			pass
		elif user_input == "undo": # typed undo
			undo()
		else: # entered a search term or tickethash
			results = re.findall(".*" + user_input + ".*", guest_list, flags=re.IGNORECASE)
			# pp.pprint(results)
			if len(results) == 0: # no match - could be already in
				out.write("\nNo ticket found. Try again!")
			elif len(results) == 1: # one match found, just hit enter
				pp.pprint(results[0].split(","))
				if user_input == results[0].split(",")[0]:
					out.write(entry_success)
					entry(results[0])
				else:
					get_response = raw_input(colored("\nPress enter to accept it or type 'x' to search again: ", 'green'))
					if get_response == "":
						out.write(entry_success)
						entry(results[0])
					elif get_response == "exit":
						out.write("\nGood bye!")
						user_input = "exit"
					else:
						out.write("OK try again!")
			else: # multiple matches found
				counter = 1
				for result in results:
					out.write(str(counter) + ": ")
					pp.pprint(result.split(","))
					counter += 1
				selection = "0"
				while selection.isdigit():
					selection = raw_input("\nHit enter to select the first one, enter a ticket number, or enter any letter to exit: ")
					if selection == "":
						out.write(entry_success)
						pp.pprint(results[0])
						entry(results[0])
						# selection = "0"
					if not selection.isdigit():
						break
					if int(selection) >= 1 and int(selection) <= len(results):
						out.write(entry_success)
						pp.pprint(results[int(selection) - 1])
						entry(results[int(selection) - 1])
					else:
						out.write("\nPlease enter a valid selection or press any letter to exit.")
	

if __name__ == '__main__':
    main("lists/guests.csv")