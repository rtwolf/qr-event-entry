# test PULP entry thing

import nose
from nose.tools import eq_, assert_raises, with_setup

from StringIO import StringIO

import pulp_entry
from pulp_entry import *

def setup_func():
	f = open("test/test.csv", "w")
	f.write(
		'hash,Sold Time,Package Type,Coupon,Name,Email\r' + 
		'5d7e5943ef4d09ee058097f8a92a09f6,"04/23/2013 00:03:32","1 Early Bird Ticket. LIMITED TIME!","","Adam Golding","adamgolding@adamgolding.com"\r' +
		'b0d07f9f6553caa3ff6a241d05e6dfcb,"03/31/2013 20:53:32","5 Early Bird Tickets","","","matthewcharleshenning@gmail.com"\r' +
		'a8a4d0f721f633be85fbdc5936cd5a17,"03/31/2013 20:53:32","5 Early Bird Tickets","","","matthewcharleshenning@gmail.com"\r' +
		'11803190bf7c6fe8559da852cdcf7b92,"03/31/2013 20:53:32","5 Early Bird Tickets","","","matthewcharleshenning@gmail.com"\r' +
		'7f38ff8b51a8f53983283eefca24e06a,"03/20/2013 00:21:39","Early Bird! LIMITED TIME!","","Alistair Forsyth","alistair.forsyth@gmail.com"\r' +
		'c88f942b47ec8fa53caf1880cd73c201,"03/26/2013 14:36:14","1 Early Bird Ticket. LIMITED TIME!","","","siva.vijenthira@gmail.com"\r'
		)
	f.close()
	# load_guests("test/test.csv")

def teardown_func():
	pass


def test_exit():
	# redirect input
	pulp_entry.raw_input = lambda _: "exit"
	# redirect output
	outo = StringIO()
	# actual call
	pulp_entry.main("test/test.csv", out=outo)
	# get the output for reals yo
	output = outo.getvalue().strip()

	eq_(output, "Good bye!", "uh oh! '" + output + "'")

@with_setup(setup_func, teardown_func)
def test_no_match():
	# simulate input
	pulp_entry.raw_input = lambda _: "black"
	pulp_entry.raw_input = lambda _: "exit"
	# redirect output
	outo = StringIO()
	# actual cal
	pulp_entry.main("test/test.csv", out=outo)
	# get the output for reals yo
	output = outo.getvalue().strip()

	eq_(
		output, 
		"Good bye!",
		"uh oh! '" + output + "'"
		)

@with_setup(setup_func, teardown_func)
def test_one_match():
	results = search("adam")
	expected_results = ["5d7e5943ef4d09ee058097f8a92a09f6,\"04/23/2013 00:03:32\",\"1 Early Bird Ticket. LIMITED TIME!\",\"\",\"Adam Golding\",\"adamgolding@adamgolding.com\"\r"]

	eq_(results, expected_results, "uh oh! Expected:<\n" + str(expected_results) + ">\ngot:<\n" + str(results) + ">")

@with_setup(setup_func, teardown_func)
def test_multiple_matches():
	results = search("matt")
	expected_results = ['b0d07f9f6553caa3ff6a241d05e6dfcb,"03/31/2013 20:53:32","5 Early Bird Tickets","","","matthewcharleshenning@gmail.com"\r',
		'a8a4d0f721f633be85fbdc5936cd5a17,"03/31/2013 20:53:32","5 Early Bird Tickets","","","matthewcharleshenning@gmail.com"\r',
		'11803190bf7c6fe8559da852cdcf7b92,"03/31/2013 20:53:32","5 Early Bird Tickets","","","matthewcharleshenning@gmail.com"\r']

	eq_(results, expected_results, "uh oh! Expected:<\n" + str(expected_results) + ">\ngot:<\n" + str(results) + ">")

# def test_single_entry():
# 	entry('5d7e5943ef4d09ee058097f8a92a09f6,"04/23/2013 00:03:32","1 Early Bird Ticket. LIMITED TIME!","","Adam Golding","adamgolding@adamgolding.com"\r')


# 	eq_(results, expected_results, "uh oh! Expected:<\n" + str(expected_results) + ">\ngot:<\n" + str(results) + ">")

if __name__ == "__main__":
    nose.runmodule()