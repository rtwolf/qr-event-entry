# PULP entry thing

import pprint, os, re, sys, time, zbar, StringIO
from os import walk
from sys import argv
from subprocess import Popen, PIPE

user_input = ""
undo_list = []

def undo():
	pass

def load_guests(file_name):
	'''Loads csv into memory as a string'''
	f = open(file_name, 'r')
	guest_list = f.read()
	f.close()
	return guest_list

# def search(needle):
# 	results = re.findall(".*" + needle + ".*", guest_list, flags=re.IGNORECASE)
# 	return results
# 	'''
# 	# old system for multiple files
# 	f = os.listdir("lists")
# 	results = []
# 	for f in f:
# 		file_it = open("lists/" + f, 'r')
# 		results.append(re.findall(".*" + needle + ".*", file_it.read(), flags=re.IGNORECASE))
# 		file_it.close()
# 	return results
# 	'''

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
	p = Popen(["/cygdrive/c/Program Files (x86)/ZBar/bin/zbarcam", "--raw"], stdout = PIPE)

	while user_input != "exit":
		guest_list = load_guests(list_to_use)
		# print p.stdout.readline()
		# user_input = p.readline()
		user_input = raw_input("\nScan a QR code or enter name/email address: ")
		print user_input
		if user_input == "exit":
			out.write("\nGood bye!")
			pass
		elif user_input == "undo":
			undo()
		else:
			results = re.findall(".*" + user_input + ".*", guest_list, flags=re.IGNORECASE)
			# pp.pprint(results)
			if len(results) == 0:
				out.write("\nNo ticket found. Try again!")
			elif len(results) == 1:
				pp.pprint(results[0].split(","))
				get_response = raw_input("\nPress enter to accept it or type anything else to search again: ")
				if get_response == "":
					out.write("\nyou're in!")
					entry(results[0])
				elif get_response == "exit":
					out.write("\nGood bye!")
					user_input = "exit"
				else:
					out.write("OK try again!")
			else:
				counter = 1
				for result in results:
					out.write(str(counter) + ": ")
					pp.pprint(result.split(","))
					counter += 1
				selection = "0"
				while selection.isdigit():
					selection = raw_input("\nHit enter to select the first one, enter a ticket number, or enter any letter to exit: ")
					if selection == "":
						out.write("\nyou're in!\n")
						pp.pprint(results[0])
						entry(results[0])
					if not selection.isdigit():
						break
					if int(selection) >= 1 and int(selection) <= len(results):
						out.write("\nyou're in!\n")
						pp.pprint(results[int(selection) - 1])
						entry(results[int(selection) - 1])
					else:
						out.write("\nPlease enter a valid selection or press any letter to exit.")
	

if __name__ == '__main__':
    main("lists/guests.csv")