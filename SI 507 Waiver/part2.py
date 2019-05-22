import sys
import sqlite3

progparams = sys.argv
if len(progparams) == 2:
	progparams.append('')
db = sqlite3.connect('Northwind_small.sqlite')
c = db.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablelist = sorted([x[0] for x in c.fetchall()])
# print(tablelist)

def lname_to_ID(lastname):
	c.execute("SELECT Id FROM Employee WHERE LastName='{}'".format(lastname))
	empid = c.fetchall()
	try:
		return empid[0][0]
	except Exception:
		return None

expected_input = ['customers', 'employees', 'orders']

if len(progparams) == 1 or progparams[1] not in expected_input:
	print('Please include the proper parameters to make this work, try something in these:\n{}'.format(expected_input))

elif progparams[1] == 'customers':
	# customerparam = ('Id','CompanyName')
	c.execute("SELECT Id, CompanyName FROM Customer")
	customerl = c.fetchall()
	print("ID\t\tCustomer Name")
	for x in customerl:
		print('{}\t\t{}'.format(*x), sep='')

elif progparams[1] == 'employees':
	# empparam = ('Id','FirstName', 'LastName')
	c.execute("SELECT Id, FirstName, LastName FROM Employee")
	employeel = c.fetchall()
	print("ID\t\tEmployee Name")
	for x in employeel:
		print('{}\t\t{} {}'.format(*x), sep='')

elif progparams[1] == 'orders':
	if progparams[2].find('cust') == 0:
		ordercustparam = progparams[2][progparams[2].find('=')+1:].upper()
		c.execute("SELECT OrderDate FROM 'Order' WHERE CustomerId='{}'".format(ordercustparam))
		custorderl = c.fetchall()
		print('Order date by ID {}'.format(ordercustparam))
		for x in custorderl:
			print(*x)
	elif progparams[2].find('emp') == 0:
		lastnamegiven = progparams[2][progparams[2].find('=')+1:].capitalize()
		IDconvert = lname_to_ID(lastnamegiven)
		if IDconvert == None:
			print('No such employee: {}'.format(lastnamegiven))
		else:
			c.execute("SELECT OrderDate FROM 'Order' WHERE EmployeeId='{}'".format(IDconvert))
			emporderl = c.fetchall()
			print('Order dates processed by Employee {}, ID {}'.format(lastnamegiven, IDconvert))
			for x in emporderl:
				print(*x)
	else:
		print('Please add an additional parameter after orders, options are:\n "cust=<customer code>"\n "emp=<employee last name>"')

db.close()
