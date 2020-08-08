from tkinter import *
from tkinter import ttk
import tkinter.font as font
import numpy as np
from datetime import date
import tkinter.messagebox as MessageBox
from PIL import ImageTk, Image
from mongoDB import *

current_window = None
width = 1000
height = 800
issue_limit = 3
bullet = "\u2022"
fields = {}
logged_as = ""
user_id = ""

def to_home():

	root.update()
	root.deiconify()
	logged_as = ""
	user_id = ""
	current_window.destroy()

def to_homepage():

	if(logged_as == "admin"):
		admin_window()
	elif(logged_as == "student"):
		student_window()

def add_book_check():
	
	records = db.books_list
	
	ID = fields['ID'].get()
	name = fields['name'].get()
	author = fields['author'].get()
	publisher = fields['publisher'].get()
	price = fields['price'].get()
	copies = fields['copies'].get()

	if(ID == "" or name == "" or author == "" or publisher == "" or price == "" or copies == ""):
		MessageBox.showinfo("Status", "All fields are required !")
		return
	
	if(records.count_documents({'ID': ID}) != 0):
		MessageBox.showinfo("Status", "This Book Id is already used !")
		return
	
	n = 0
	try:
		n = int(price)
	except ValueError:
		try:
			n = float(price)
		except ValueError:
			MessageBox.showinfo("Status", "Enter Price properly")
			return
	
	if(n <= 0):
		MessageBox.showinfo("Status", "Price should be positive")
		return
	
	copy = 0
	try:
		copy = int(copies)
	except ValueError:
		MessageBox.showinfo("Status", "Copies should be an integer")
		return
	
	if(copy <= 0):
		MessageBox.showinfo("Status", "Copies should be a positive integer")
		return

	new_book = {
		'ID': ID,
		'name': name,
		'author': author,
		'publisher': publisher,
		'price': price,
		'copies': copy
	}

	records.insert_one(new_book)
	MessageBox.showinfo("Status", "Book added successfully.")
	to_homepage()

def add_book():
	
	fields.clear()
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Add Book")
	win.geometry(string)
	win.configure(bg="#6CBB3C")
	current_window = win

	logout = Button(win, text="Log out", command=to_home)
	logout.pack()
	logout.configure(activebackground="#786D5F")
	logout.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.configure(activebackground="#786D5F")
	exit.place(x=925, y=20)

	cour = font.Font(family="Courier", size=30, weight='bold')
	tag = Label(win, text="*All fields are required*", bg="#6CBB3C", fg="#990012")
	tag.pack()
	tag.place(x=185, y=100)
	tag['font']=cour

	book_id = Label(win, text="Book ID", font=("times new roman", 20))
	book_id.pack()
	book_id.configure(bg="#6CBB3C")
	book_id.place(x=250, y=250)

	e_book_id = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_book_id.pack()
	e_book_id.place(x=525, y=250)

	fields['ID'] = e_book_id

	name = Label(win, text="Book Name", font=("times new roman", 20))
	name.pack()
	name.configure(bg="#6CBB3C")
	name.place(x=250, y=300)

	e_name = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_name.pack()
	e_name.place(x=525, y=300)

	fields['name'] = e_name

	author = Label(win, text="Book Author", font=("times new roman", 20))
	author.pack()
	author.configure(bg="#6CBB3C")
	author.place(x=250, y=350)

	e_author = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_author.pack()
	e_author.place(x=525, y=350)

	fields['author'] = e_author

	publisher = Label(win, text="Publisher", font=("times new roman", 20))
	publisher.pack()
	publisher.configure(bg="#6CBB3C")
	publisher.place(x=250, y=400)

	e_publisher = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_publisher.pack()
	e_publisher.place(x=525, y=400)

	fields['publisher'] = e_publisher

	price = Label(win, text="Price", font=("times new roman", 20))
	price.pack()
	price.configure(bg="#6CBB3C")
	price.place(x=250, y=450)

	e_price = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_price.pack()
	e_price.place(x=525, y=450)

	fields['price'] = e_price

	copies = Label(win, text="Copies to add", font=("times new roman", 20))
	copies.pack()
	copies.configure(bg="#6CBB3C")
	copies.place(x=250, y=500)

	e_copies = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_copies.pack()
	e_copies.place(x=525, y=500)

	fields['copies'] = e_copies

	cancel = Button(win, text="Cancel", command=to_homepage)
	cancel.pack()
	cancel.configure(width=10, height=2)
	cancel.place(x=300, y=650)

	add = Button(win, text="Add Book", command=add_book_check)
	add.pack()
	add.configure(width=10, height=2)
	add.place(x=575, y=650)

def book_list():
	
	fields.clear()
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Books List")
	win.geometry(string)
	win.configure(bg="#6CBB3C")
	current_window = win

	back = Button(win, text="Back", command=to_homepage)
	back.pack()
	back.configure(activebackground="#786D5F")
	back.place(x=20, y=20)

	logout = Button(win, text="Log out", command=to_home)
	logout.pack()
	logout.configure(activebackground="#786D5F")
	logout.place(x=825, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.configure(activebackground="#786D5F")
	exit.place(x=925, y=20)

	records = db.books_list
	li = list(records.find({}))
	books = sorted(li, key = lambda i: i['name'])

	frame = Frame(win)
	frame.configure(bg='lightblue', width=925)
	frame.place(x=40, y=115)

	tree = ttk.Treeview(frame)
	tree.configure(height=30)
	tree.pack(side=LEFT)

	scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
	scroll.pack(side=RIGHT)
	
	tree.configure(yscroll=scroll.set)

	tree["columns"] = ("1", "2", "3", "4", "5", "6")
	tree['show'] = 'headings'

	tree.column("1", width=75, anchor='c')
	tree.column("2", width=225, anchor='c')
	tree.column("3", width=225, anchor='c')
	tree.column("4", width=225, anchor='c')
	tree.column("5", width=75, anchor='c')
	tree.column("6", width=75, anchor='c')

	tree.heading("1", text="Book Id")
	tree.heading("2", text="Book Name")
	tree.heading("3", text="Author")
	tree.heading("4", text="Publisher")
	tree.heading("5", text="Price")
	tree.heading("6", text="Available")

	for bk in books:
		tree.insert("", 'end', values=(bk['ID'], bk['name'], bk['author'], bk['publisher'], bk['price'], bk['copies']))

def student_list():
	
	fields.clear()
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Students List")
	win.geometry(string)
	win.configure(bg="#6CBB3C")
	current_window = win

	back = Button(win, text="Back", command=to_homepage)
	back.pack()
	back.configure(activebackground="#786D5F")
	back.place(x=20, y=20)

	logout = Button(win, text="Log out", command=to_home)
	logout.pack()
	logout.configure(activebackground="#786D5F")
	logout.place(x=825, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.configure(activebackground="#786D5F")
	exit.place(x=925, y=20)

	records = db.students_list
	li = list(records.find({}))
	students = sorted(li, key = lambda i: i['name'])

	frame = Frame(win)
	frame.configure(bg='lightblue', width=925)
	frame.place(x=40, y=115)

	tree = ttk.Treeview(frame)
	tree.configure(height=30)
	tree.pack(side=LEFT)

	scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
	scroll.pack(side=RIGHT)
	
	tree.configure(yscroll=scroll.set)

	tree["columns"] = ("1", "2", "3", "4")
	tree['show'] = 'headings'

	tree.column("1", width=125, anchor='c')
	tree.column("2", width=275, anchor='c')
	tree.column("3", width=375, anchor='c')
	tree.column("4", width=125, anchor='c')

	tree.heading("1", text="Student Id")
	tree.heading("2", text="Name")
	tree.heading("3", text="Department")
	tree.heading("4", text="Issued book")

	for st in students:
		tree.insert("", 'end', values=(st['ID'], st['name'], st['dept'], st['issued']))

def issue_book_check():
	
	st_id = fields['student'].get()
	bk_id = fields['book'].get()

	if(st_id == "" or bk_id == ""):
		MessageBox.showinfo("Status", "Fill details properly !")
		return
	
	records = db.students_list
	if(records.count_documents({'ID': st_id}) == 0):
		MessageBox.showinfo("Status", "Student not found !")
		return
	
	records = db.books_list
	if(records.count_documents({'ID': bk_id}) == 0):
		MessageBox.showinfo("Status", "Book not found !")
		return

	records = db.records_list
	if(records.count_documents({'student_id': st_id, 'book_id': bk_id}) != 0):
		rec = list(records.find({'student_id': st_id, 'book_id': bk_id}))[0]
		if(rec['return_date'] == "Not returned"):
			MessageBox.showinfo("Status", "This book is already issued to this student !")
			return

	records = db.students_list
	student = list(records.find({'ID': st_id}))[0]
	if(student['issued'] == issue_limit):
		MessageBox.showinfo("Status", "Student reached max limit !")
		return

	records = db.books_list
	book = list(records.find({'ID': bk_id}))[0]
	if(book['copies'] == 0):
		MessageBox.showinfo("Status", "This book is not available at this moment !")
		return

	u = (student['issued']+1)
	v = (book['copies']-1)

	st = {
		'issued': u
	}

	bk = {
		'copies': v
	}

	records = db.students_list
	records.update_one({'ID': st_id}, {'$set': st})

	records = db.books_list
	records.update_one({'ID': bk_id}, {'$set': bk})

	record = {
		'student_id': st_id,
		'student_name': student['name'],
		'book_id': bk_id,
		'book_name': book['name'],
		'issue_date': str(date.today()),
		'return_date': "Not returned"
	}

	records = db.records_list
	records.insert_one(record)
	MessageBox.showinfo("Status", "Book issued successfully !")
	to_homepage()

def issue_book():
	
	fields.clear()
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Issue Book")
	win.geometry(string)
	win.configure(bg='#6CBB3C')
	current_window = win

	logout = Button(win, text="Log out", command=to_home)
	logout.pack()
	logout.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.place(x=925, y=20)

	st = Label(win, text="Student Id", font=("times new roman", 20))
	st.pack()
	st.configure(bg="#6CBB3C")
	st.place(x=275, y=275)

	e_st = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_st.pack()
	e_st.place(x=500, y=275)

	fields['student'] = e_st

	bk = Label(win, text="Book Id", font=("times new roman", 20))
	bk.pack()
	bk.configure(bg="#6CBB3C")
	bk.place(x=275, y=325)

	e_bk = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_bk.pack()
	e_bk.place(x=500, y=325)

	fields['book'] = e_bk

	cancel = Button(win, text="Cancel", command=to_homepage)
	cancel.pack()
	cancel.place(x=345, y=450)

	submit = Button(win, text="Submit", command=issue_book_check)
	submit.pack()
	submit.place(x=570, y=450)

def return_book_check():
	
	st_id = fields['student'].get()
	bk_id = fields['book'].get()

	if(st_id == "" or bk_id == ""):
		MessageBox.showinfo("Status", "Fill details properly !")
		return
	
	records = db.students_list
	if(records.count_documents({'ID': st_id}) == 0):
		MessageBox.showinfo("Status", "Student not found !")
		return
	
	records = db.books_list
	if(records.count_documents({'ID': bk_id}) == 0):
		MessageBox.showinfo("Status", "Book not found !")
		return

	records = db.records_list
	if(records.count_documents({'student_id': st_id, 'book_id': bk_id}) == 0):
		MessageBox.showinfo("Status", "No such active record found !")
		return
	else:
		rec = list(records.find({'student_id': st_id, 'book_id': bk_id}))[0]
		if(rec['return_date'] != "Not returned"):
			MessageBox.showinfo("Status", "No such active record found !")
			return

	records = db.students_list
	student = list(records.find({'ID': st_id}))[0]
	
	records = db.books_list
	book = list(records.find({'ID': bk_id}))[0]
	
	u = (student['issued']-1)
	v = (book['copies']+1)

	st = {
		'issued': u
	}

	bk = {
		'copies': v
	}

	records = db.students_list
	records.update_one({'ID': st_id}, {'$set': st})

	records = db.books_list
	records.update_one({'ID': bk_id}, {'$set': bk})

	record = {
		'return_date': str(date.today())
	}

	records = db.records_list
	records.update_one({'student_id': st_id, 'book_id': bk_id}, {'$set': record})
	MessageBox.showinfo("Status", "Book returned successfully !")
	to_homepage()

def return_book():
	
	fields.clear()
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Return Book")
	win.geometry(string)
	win.configure(bg='#6CBB3C')
	current_window = win

	logout = Button(win, text="Log out", command=to_home)
	logout.pack()
	logout.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.place(x=925, y=20)

	st = Label(win, text="Student Id", font=("times new roman", 20))
	st.pack()
	st.configure(bg="#6CBB3C")
	st.place(x=275, y=275)

	e_st = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_st.pack()
	e_st.place(x=500, y=275)

	fields['student'] = e_st

	bk = Label(win, text="Book Id", font=("times new roman", 20))
	bk.pack()
	bk.configure(bg="#6CBB3C")
	bk.place(x=275, y=325)

	e_bk = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_bk.pack()
	e_bk.place(x=500, y=325)

	fields['book'] = e_bk

	cancel = Button(win, text="Cancel", command=to_homepage)
	cancel.pack()
	cancel.place(x=345, y=450)

	submit = Button(win, text="Submit", command=return_book_check)
	submit.pack()
	submit.place(x=570, y=450)

def show_records():
	
	fields.clear()
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Records")
	win.geometry(string)
	win.configure(bg="#6CBB3C")
	current_window = win

	back = Button(win, text="Back", command=to_homepage)
	back.pack()
	back.configure(activebackground="#786D5F")
	back.place(x=20, y=20)

	logout = Button(win, text="Log out", command=to_home)
	logout.pack()
	logout.configure(activebackground="#786D5F")
	logout.place(x=825, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.configure(activebackground="#786D5F")
	exit.place(x=925, y=20)

	records = db.records_list
	li = list(records.find({}))
	
	frame = Frame(win)
	frame.configure(bg='lightblue', width=925)
	frame.place(x=40, y=115)

	tree = ttk.Treeview(frame)
	tree.configure(height=30)
	tree.pack(side=LEFT)

	scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
	scroll.pack(side=RIGHT)
	
	tree.configure(yscroll=scroll.set)

	tree["columns"] = ("1", "2", "3", "4", "5", "6")
	tree['show'] = 'headings'

	tree.column("1", width=100, anchor='c')
	tree.column("2", width=200, anchor='c')
	tree.column("3", width=100, anchor='c')
	tree.column("4", width=250, anchor='c')
	tree.column("5", width=125, anchor='c')
	tree.column("6", width=125, anchor='c')

	tree.heading("1", text="Student Id")
	tree.heading("2", text="Student Name")
	tree.heading("3", text="Book Id")
	tree.heading("4", text="Book Name")
	tree.heading("5", text="Issue Date")
	tree.heading("6", text="Return Date")

	for rec in li:
		tree.insert("", 'end', values=(rec['student_id'], rec['student_name'], rec['book_id'], rec['book_name'], rec['issue_date'], rec['return_date']))

def admin_window():

	global logged_as
	logged_as = "admin"
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Homepage")
	win.geometry(string)
	win.configure(bg="#6CBB3C")
	current_window = win

	myFont = font.Font(size=30)

	books = Button(win, text="Books List", command=book_list, width=12, height=2)
	books.pack()
	books.configure(activebackground="#786D5F")
	books.place(x=100, y=175)
	books['font'] = myFont

	students = Button(win, text="Students List", command=student_list, width=12, height=2)
	students.pack()
	students.configure(activebackground="#786D5F")
	students.place(x=570, y=175)
	students['font'] = myFont

	book_add = Button(win, text="Add Book", command=add_book, width=12, height=2)
	book_add.pack()
	book_add.configure(activebackground="#786D5F")
	book_add.place(x=100, y=375)
	book_add['font'] = myFont

	book_issue = Button(win, text="Issue Book", command=issue_book, width=12, height=2)
	book_issue.pack()
	book_issue.configure(activebackground="#786D5F")
	book_issue.place(x=570, y=375)
	book_issue['font'] = myFont

	book_return = Button(win, text="Return Book", command=return_book, width=12, height=2)
	book_return.pack()
	book_return.configure(activebackground="#786D5F")
	book_return.place(x=100, y=575)
	book_return['font'] = myFont

	records = Button(win, text="All Records", command=show_records, width=12, height=2)
	records.pack()
	records.configure(activebackground="#786D5F")
	records.place(x=570, y=575)
	records['font'] = myFont

	logout = Button(win, text="Log out", command=to_home)
	logout.pack()
	logout.configure(activebackground="#786D5F")
	logout.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.configure(activebackground="#786D5F")
	exit.place(x=925, y=20)

def admin_reset_password_check():

	passwd = fields['passwd'].get()
	confirm = fields['confirm'].get()
	records = db.admins_list
	
	if(len(passwd) < 8):
		MessageBox.showinfo("Status", "Password should have a minimum length of 8 !")
		return
		
	if(passwd != confirm):
		MessageBox.showinfo("Status", "Password and confirm password should be same !")
		return
	
	admin_update = {
		'password': passwd
	}

	records.update_one({'ID': user_id}, {'$set': admin_update})
	MessageBox.showinfo("Status", "Password changed successfully.")

	admin_login()

def admin_reset_password():

	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Forgot Password")
	win.geometry(string)
	win.configure(bg='#6CBB3C')
	current_window = win

	cancel = Button(win, text="Cancel", command=admin_login)
	cancel.pack()
	cancel.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.place(x=925, y=20)

	passwd = Label(win, text="New Password", font=("times new roman", 20))
	passwd.pack()
	passwd.configure(bg="#6CBB3C")
	passwd.place(x=250, y=275)

	e_passwd = Entry(win, show=bullet, font=("times new roman", 15), bg="#E5E4E2")
	e_passwd.pack()
	e_passwd.place(x=525, y=275)

	fields['passwd'] = e_passwd

	conf = Label(win, text="Confirm Password", font=("times new roman", 20))
	conf.pack()
	conf.configure(bg="#6CBB3C")
	conf.place(x=250, y=325)

	e_conf = Entry(win, show=bullet, font=("times new roman", 15), bg="#E5E4E2")
	e_conf.pack()
	e_conf.place(x=525, y=325)

	fields['confirm'] = e_conf

	submit = Button(win, text="Submit", command=admin_reset_password_check)
	submit.pack()
	submit.place(x=450, y=400)

def admin_forget_details_check():
	
	answer = fields['answer'].get()
	records = db.admins_list
	admin = list(records.find({'ID': user_id}))[0]

	if(admin['answer'].lower() != answer.lower()):
		MessageBox.showinfo("Status", "Incorrect ! Try Again !")
		return

	admin_reset_password()

def admin_forget_details():
	
	ID = fields['ID'].get()
	global user_id
	user_id = ID
	records = db.admins_list
	admin = list(records.find({'ID': ID}))[0]
	
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Forgot Password")
	win.geometry(string)
	win.configure(bg='#6CBB3C')
	current_window = win

	cancel = Button(win, text="Cancel", command=admin_login)
	cancel.pack()
	cancel.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.place(x=925, y=20)
	
	mem_id = Label(win, text=admin['question'], font=("times new roman", 20))
	mem_id.pack()
	mem_id.configure(bg="#6CBB3C")
	mem_id.place(x=200, y=275)

	e_ans = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_ans.pack()
	e_ans.place(x=575, y=275)
	
	fields['answer'] = e_ans

	submit = Button(win, text="Submit", command=admin_forget_details_check)
	submit.pack()
	submit.place(x=450, y=400)

def admin_forget_check():
	
	ID = fields['ID'].get()

	if(ID == ""):
		MessageBox.showinfo("Error !", "Enter an ID to search")
		return

	records = db.admins_list

	if(records.count_documents({'ID': ID}) == 0):
		MessageBox.showinfo("Search Status", "This ID is not registered !")
		return

	admin_forget_details()

def admin_forget():
	
	global fields
	fields.clear()
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Forgot Password")
	win.geometry(string)
	win.configure(bg='#6CBB3C')
	current_window = win

	mem_id = Label(win, text="Member ID", font=("times new roman", 20))
	mem_id.pack()
	mem_id.configure(bg="#6CBB3C")
	mem_id.place(x=250, y=225)

	e_mem_id = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_mem_id.pack()
	e_mem_id.place(x=425, y=225)

	fields['ID'] = e_mem_id

	search = Button(win, text="Search", command=admin_forget_check)
	search.pack()
	search.place(x=650, y=225)

	cancel = Button(win, text="Cancel", command=admin_login)
	cancel.pack()
	cancel.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.place(x=925, y=20)

def admin_signup_check():

	ID = fields['ID'].get()
	name = fields['name'].get()
	secret = fields['secret'].get()
	question = fields['question'].get()
	answer = fields['answer'].get()
	passwd = fields['passwd'].get()
	confirm = fields['confirm'].get()

	if(ID == "" or name == "" or answer == ""):
		MessageBox.showinfo("Filling Status", "All fields are required")
		return

	if(secret == ""):
		MessageBox.showinfo("Filling Status", "Secret Code must be entered for Admin login")
		return

	if(question == '-select-'):
		MessageBox.showinfo("Filling Status", "Please Choose a Security Question")
		return

	if(len(passwd) < 8):
		MessageBox.showinfo("Filling Status", "Password should have a minimum length of 8")
		return

	if(passwd != confirm):
		MessageBox.showinfo("Filling Status", "Password and Confirm Password must be same")
		return

	records = db.admins_list
	if(records.count_documents({'ID': ID}) != 0):
		MessageBox.showinfo("Filling status", "Member is already registered")
		return

	records = db.secret_codes
	if(records.count_documents({'secret': secret}) == 0):
		MessageBox.showinfo("Filling status", "Secret code doesn't match")
		return

	fields.clear()

	new_admin = {
		'ID': ID,
		'name': name,
		'question': question,
		'answer': answer,
		'password': passwd
	}

	records = db.admins_list
	records.insert_one(new_admin)
	MessageBox.showinfo("Filling Status", "Created account successfully")
	admin_login()

def admin_signup():
	
	global fields
	fields.clear()
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Admin signup")
	win.geometry(string)
	win.configure(bg='#6CBB3C')
	current_window = win

	cour = font.Font(family="Courier", size=30, weight='bold')
	tag = Label(win, text="*All fields are required*", bg="#6CBB3C", fg="#990012")
	tag.pack()
	tag.place(x=185, y=100)
	tag['font']=cour

	mem_id = Label(win, text="Member ID", font=("times new roman", 20))
	mem_id.pack()
	mem_id.configure(bg="#6CBB3C")
	mem_id.place(x=250, y=225)

	e_mem_id = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_mem_id.pack()
	e_mem_id.place(x=525, y=225)

	fields['ID'] = e_mem_id

	name = Label(win, text="Member Name", font=("times new roman", 20))
	name.pack()
	name.configure(bg="#6CBB3C")
	name.place(x=250, y=275)

	e_name = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_name.pack()
	e_name.place(x=525, y=275)

	fields['name'] = e_name

	code = Label(win, text="Secret Code", font=("times new roman", 20))
	code.pack()
	code.configure(bg="#6CBB3C")
	code.place(x=250, y=325)

	e_code = Entry(win, show=bullet, font=("times new roman", 15), bg="#E5E4E2")
	e_code.pack()
	e_code.place(x=525, y=325)

	fields['secret'] = e_code

	question = Label(win, text="Security Question", font=("times new roman", 20))
	question.pack()
	question.configure(bg="#6CBB3C")
	question.place(x=250, y=375)

	OPTIONS = [
    	"First pet name ?",
    	"Dream City ?",
    	"Favourite Food ?",
    	"Most awkward nickname ?"
	]

	variable = StringVar(win)
	variable.set('-select-')

	e_question = OptionMenu(win, variable, *OPTIONS)
	e_question.pack()
	e_question.configure(width=20)
	e_question.place(x=525, y=375)

	fields['question'] = variable

	answer = Label(win, text="Security Answer", font=("times new roman", 20))
	answer.pack()
	answer.configure(bg="#6CBB3C")
	answer.place(x=250, y=425)

	e_answer = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_answer.pack()
	e_answer.place(x=525, y=425)

	fields['answer'] = e_answer

	passwd = Label(win, text="Enter Password", font=("times new roman", 20))
	passwd.pack()
	passwd.configure(bg="#6CBB3C")
	passwd.place(x=250, y=475)

	e_passwd = Entry(win, show=bullet, font=("times new roman", 15), bg="#E5E4E2")
	e_passwd.pack()
	e_passwd.place(x=525, y=475)

	fields['passwd'] = e_passwd

	conf = Label(win, text="Confirm Password", font=("times new roman", 20))
	conf.pack()
	conf.configure(bg="#6CBB3C")
	conf.place(x=250, y=525)

	e_conf = Entry(win, show=bullet, font=("times new roman", 15), bg="#E5E4E2")
	e_conf.pack()
	e_conf.place(x=525, y=525)

	fields['confirm'] = e_conf

	login = Button(win, text="Login", command=admin_login)
	login.pack()
	login.configure(width=10, height=2)
	login.place(x=300, y=650)

	signup = Button(win, text="Sign Up", command=admin_signup_check)
	signup.pack()
	signup.configure(width=10, height=2)
	signup.place(x=575, y=650)

	cancel = Button(win, text="Home", command=to_home)
	cancel.pack()
	cancel.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.place(x=925, y=20)	

def admin_login_check():

	ID = fields['ID'].get()
	passwd = fields['passwd'].get()

	if(ID == "" or passwd == ""):
		MessageBox.showinfo("Status", "All fields are required !")
		return
	
	records = db.admins_list

	if(records.count_documents({'ID': ID}) == 0):
		MessageBox.showinfo("Status", "This Id is not registered yet !")
		return
	
	admin = list(records.find({'ID': ID}))[0]

	if(admin['password'] != passwd):
		MessageBox.showinfo("Status", "Password doesn't match !")
		return
	
	admin_window()

def admin_login():

	global fields
	fields.clear()
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Admin login")
	win.geometry(string)
	win.configure(bg='#6CBB3C')
	current_window = win

	cour = font.Font(family="Courier", size=50, weight='bold')
	tag = Label(win, text="Admin Login", bg="#6CBB3C", fg="#990012")
	tag.pack()
	tag.place(x=275, y=100)
	tag['font']=cour

	mem_id = Label(win, text="Member ID : ", font=("times new roman", 30))
	mem_id.pack()
	mem_id.configure(bg="#6CBB3C")
	mem_id.place(x=200, y=275)

	e_mem_id = Entry(win, font=("times new roman", 25), bg="#E5E4E2")
	e_mem_id.pack()
	e_mem_id.place(x=425, y=275)

	fields['ID'] = e_mem_id

	passwd = Label(win, text="Password    : ", font=("times new roman", 30))
	passwd.pack()
	passwd.configure(bg="#6CBB3C")
	passwd.place(x=200, y=375)

	e_passwd = Entry(win, show=bullet, font=("times new roman", 25), bg="#E5E4E2")
	e_passwd.pack()
	e_passwd.place(x=425, y=375)
	
	fields['passwd'] = e_passwd

	login = Button(win, text="Login", command=admin_login_check)
	login.pack()
	login.configure(width=15, height=2)
	login.place(x=250, y=550)

	signup = Button(win, text="Sign Up", command=admin_signup)
	signup.pack()
	signup.configure(width=15, height=2)
	signup.place(x=575, y=550)

	forget = Button(win, text="Forgot Password?", command=admin_forget)
	forget.pack()
	forget.place(x=640, y=425)

	cancel = Button(win, text="Home", command=to_home)
	cancel.pack()
	cancel.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.place(x=925, y=20)

def student_window():

	global logged_as
	logged_as = "student"
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Homepage")
	win.geometry(string)
	win.configure(bg="#6CBB3C")
	current_window = win

	myFont = font.Font(size=30)

	books = Button(win, text="Books List", command=book_list, width=12, height=2)
	books.pack()
	books.configure(activebackground="#786D5F")
	books.place(x=100, y=175)
	books['font'] = myFont

	students = Button(win, text="Students List", command=student_list, width=12, height=2)
	students.pack()
	students.configure(activebackground="#786D5F")
	students.place(x=335, y=375)
	students['font'] = myFont

	records = Button(win, text="All Records", command=show_records, width=12, height=2)
	records.pack()
	records.configure(activebackground="#786D5F")
	records.place(x=570, y=575)
	records['font'] = myFont

	logout = Button(win, text="Log out", command=to_home)
	logout.pack()
	logout.configure(activebackground="#786D5F")
	logout.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.configure(activebackground="#786D5F")
	exit.place(x=925, y=20)

def student_reset_password_check():

	passwd = fields['passwd'].get()
	confirm = fields['confirm'].get()
	records = db.students_list
	
	if(len(passwd) < 8):
		MessageBox.showinfo("Status", "Password should have a minimum length of 8 !")
		return
		
	if(passwd != confirm):
		MessageBox.showinfo("Status", "Password and confirm password should be same !")
		return
	
	student_update = {
		'password': passwd
	}

	records.update_one({'ID': user_id}, {'$set': student_update})
	MessageBox.showinfo("Status", "Password changed successfully.")

	student_login()

def student_reset_password():

	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Forgot Password")
	win.geometry(string)
	win.configure(bg='#6CBB3C')
	current_window = win

	cancel = Button(win, text="Cancel", command=student_login)
	cancel.pack()
	cancel.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.place(x=925, y=20)

	passwd = Label(win, text="New Password", font=("times new roman", 20))
	passwd.pack()
	passwd.configure(bg="#6CBB3C")
	passwd.place(x=250, y=275)

	e_passwd = Entry(win, show=bullet, font=("times new roman", 15), bg="#E5E4E2")
	e_passwd.pack()
	e_passwd.place(x=525, y=275)

	fields['passwd'] = e_passwd

	conf = Label(win, text="Confirm Password", font=("times new roman", 20))
	conf.pack()
	conf.configure(bg="#6CBB3C")
	conf.place(x=250, y=325)

	e_conf = Entry(win, show=bullet, font=("times new roman", 15), bg="#E5E4E2")
	e_conf.pack()
	e_conf.place(x=525, y=325)

	fields['confirm'] = e_conf

	submit = Button(win, text="Submit", command=student_reset_password_check)
	submit.pack()
	submit.place(x=450, y=400)

def student_forget_details_check():
	
	answer = fields['answer'].get()
	records = db.students_list
	student = list(records.find({'ID': user_id}))[0]

	if(student['answer'].lower() != answer.lower()):
		MessageBox.showinfo("Status", "Incorrect ! Try Again !")
		return

	student_reset_password()

def student_forget_details():
	
	ID = fields['ID'].get()
	global user_id
	user_id = ID
	records = db.students_list
	student = list(records.find({'ID': ID}))[0]
	
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Forgot Password")
	win.geometry(string)
	win.configure(bg='#6CBB3C')
	current_window = win

	cancel = Button(win, text="Cancel", command=student_login)
	cancel.pack()
	cancel.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.place(x=925, y=20)
	
	mem_id = Label(win, text=student['question'], font=("times new roman", 20))
	mem_id.pack()
	mem_id.configure(bg="#6CBB3C")
	mem_id.place(x=200, y=275)

	e_ans = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_ans.pack()
	e_ans.place(x=575, y=275)
	
	fields['answer'] = e_ans

	submit = Button(win, text="Submit", command=student_forget_details_check)
	submit.pack()
	submit.place(x=450, y=400)
		
def student_forget_check():
	
	ID = fields['ID'].get()

	if(ID == ""):
		MessageBox.showinfo("Error !", "Enter an ID to search")
		return

	records = db.students_list

	if(records.count_documents({'ID': ID}) == 0):
		MessageBox.showinfo("Search Status", "This ID is not registered !")
		return

	student_forget_details()

def student_forget():
	
	fields.clear()
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Forgot Password")
	win.geometry(string)
	win.configure(bg='#6CBB3C')
	current_window = win

	mem_id = Label(win, text="Member ID", font=("times new roman", 20))
	mem_id.pack()
	mem_id.configure(bg="#6CBB3C")
	mem_id.place(x=250, y=225)

	e_mem_id = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_mem_id.pack()
	e_mem_id.place(x=425, y=225)

	fields['ID'] = e_mem_id

	search = Button(win, text="Search", command=student_forget_check)
	search.pack()
	search.place(x=650, y=225)

	cancel = Button(win, text="Cancel", command=student_login)
	cancel.pack()
	cancel.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.place(x=925, y=20)

def student_signup_check():

	ID = fields['ID'].get()
	name = fields['name'].get()
	dept = fields['dept'].get()
	question = fields['question'].get()
	answer = fields['answer'].get()
	passwd = fields['passwd'].get()
	confirm = fields['confirm'].get()

	if(ID == "" or name == "" or answer == "" or dept == ""):
		MessageBox.showinfo("Filling Status", "All fields are required")
		return

	if(question == '-select-'):
		MessageBox.showinfo("Filling Status", "Please Choose a Security Question")
		return

	if(len(passwd) < 8):
		MessageBox.showinfo("Filling Status", "Password should have a minimum length of 8")
		return

	if(passwd != confirm):
		MessageBox.showinfo("Filling Status", "Password and Confirm Password must be same")
		return

	records = db.students_list
	if(records.count_documents({'ID': ID}) != 0):
		MessageBox.showinfo("Filling status", "Member is already registered")
		return

	issued_book = 0
	fields.clear()

	new_student = {
		'ID': ID,
		'name': name,
        'dept': dept,
		'question': question,
		'answer': answer,
		'password': passwd,
        'issued': issued_book
	}

	records = db.students_list
	records.insert_one(new_student)
	MessageBox.showinfo("Filling Status", "Created account successfully")
	student_login()

def student_signup():
	
	fields.clear()
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Student signup")
	win.geometry(string)
	win.configure(bg='#6CBB3C')
	current_window = win

	cour = font.Font(family="Courier", size=30, weight='bold')
	tag = Label(win, text="*All fields are required*", bg="#6CBB3C", fg="#990012")
	tag.pack()
	tag.place(x=185, y=100)
	tag['font']=cour


	mem_id = Label(win, text="Member ID", font=("times new roman", 20))
	mem_id.pack()
	mem_id.configure(bg="#6CBB3C")
	mem_id.place(x=250, y=225)

	e_mem_id = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_mem_id.pack()
	e_mem_id.place(x=525, y=225)

	fields['ID'] = e_mem_id

	name = Label(win, text="Member Name", font=("times new roman", 20))
	name.pack()
	name.configure(bg="#6CBB3C")
	name.place(x=250, y=275)

	e_name = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_name.pack()
	e_name.place(x=525, y=275)

	fields['name'] = e_name

	dept = Label(win, text="Department", font=("times new roman", 20))
	dept.pack()
	dept.configure(bg="#6CBB3C")
	dept.place(x=250, y=325)

	e_dept = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_dept.pack()
	e_dept.place(x=525, y=325)

	fields['dept'] = e_dept

	question = Label(win, text="Security Question", font=("times new roman", 20))
	question.pack()
	question.configure(bg="#6CBB3C")
	question.place(x=250, y=375)

	OPTIONS = [
    	"First pet name ?",
    	"Dream City ?",
    	"Favourite Food ?",
    	"Most awkward nickname ?"
	]

	variable = StringVar(win)
	variable.set('-select-')

	e_question = OptionMenu(win, variable, *OPTIONS)
	e_question.pack()
	e_question.configure(width=20)
	e_question.place(x=525, y=375)

	fields['question'] = variable

	answer = Label(win, text="Security Answer", font=("times new roman", 20))
	answer.pack()
	answer.configure(bg="#6CBB3C")
	answer.place(x=250, y=425)

	e_answer = Entry(win, font=("times new roman", 15), bg="#E5E4E2")
	e_answer.pack()
	e_answer.place(x=525, y=425)

	fields['answer'] = e_answer

	passwd = Label(win, text="Enter Password", font=("times new roman", 20))
	passwd.pack()
	passwd.configure(bg="#6CBB3C")
	passwd.place(x=250, y=475)

	e_passwd = Entry(win, show=bullet, font=("times new roman", 15), bg="#E5E4E2")
	e_passwd.pack()
	e_passwd.place(x=525, y=475)

	fields['passwd'] = e_passwd

	conf = Label(win, text="Confirm Password", font=("times new roman", 20))
	conf.pack()
	conf.configure(bg="#6CBB3C")
	conf.place(x=250, y=525)

	e_conf = Entry(win, show=bullet, font=("times new roman", 15), bg="#E5E4E2")
	e_conf.pack()
	e_conf.place(x=525, y=525)

	fields['confirm'] = e_conf

	login = Button(win, text="Login", command=student_login)
	login.pack()
	login.configure(width=10, height=2)
	login.place(x=300, y=650)

	signup = Button(win, text="Sign Up", command=student_signup_check)
	signup.pack()
	signup.configure(width=10, height=2)
	signup.place(x=575, y=650)

	cancel = Button(win, text="Home", command=to_home)
	cancel.pack()
	cancel.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.place(x=925, y=20)	

def student_login_check():

	ID = fields['ID'].get()
	passwd = fields['passwd'].get()

	if(ID == "" or passwd == ""):
		MessageBox.showinfo("Status", "All fields are required !")
		return
	
	records = db.students_list

	if(records.count_documents({'ID': ID}) == 0):
		MessageBox.showinfo("Status", "This Id is not registered yet !")
		return
	
	student = list(records.find({'ID': ID}))[0]

	if(student['password'] != passwd):
		MessageBox.showinfo("Status", "Password doesn't match !")
		return
	
	logged_as = "student"
	student_window()

def student_login():

	fields.clear()
	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("Student login")
	win.geometry(string)
	win.configure(bg='#6CBB3C')
	current_window = win

	cour = font.Font(family="Courier", size=50, weight='bold')
	tag = Label(win, text="Student Login", bg="#6CBB3C", fg="#990012")
	tag.pack()
	tag.place(x=225, y=100)
	tag['font']=cour

	mem_id = Label(win, text="Member ID : ", font=("times new roman", 30))
	mem_id.pack()
	mem_id.configure(bg="#6CBB3C")
	mem_id.place(x=200, y=275)

	e_mem_id = Entry(win, font=("times new roman", 25), bg="#E5E4E2")
	e_mem_id.pack()
	e_mem_id.place(x=425, y=275)

	fields['ID'] = e_mem_id

	passwd = Label(win, text="Password    : ", font=("times new roman", 30))
	passwd.pack()
	passwd.configure(bg="#6CBB3C")
	passwd.place(x=200, y=375)

	e_passwd = Entry(win, show=bullet, font=("times new roman", 25), bg="#E5E4E2")
	e_passwd.pack()
	e_passwd.place(x=425, y=375)
	
	fields['passwd'] = e_passwd

	login = Button(win, text="Login", command=student_login_check)
	login.pack()
	login.configure(width=15, height=2)
	login.place(x=250, y=550)

	signup = Button(win, text="Sign Up", command=student_signup)
	signup.pack()
	signup.configure(width=15, height=2)
	signup.place(x=575, y=550)

	forget = Button(win, text="Forgot Password?", command=student_forget)
	forget.pack()
	forget.place(x=640, y=425)

	cancel = Button(win, text="Home", command=to_home)
	cancel.pack()
	cancel.place(x=20, y=20)

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.place(x=925, y=20)

def about():

	root.withdraw()
	global current_window
	if(current_window is not None):
		current_window.destroy()

	win = Toplevel()
	win.title("About")
	win.geometry(string)
	win.configure(bg="#6CBB3C")
	current_window = win

	myFont = font.Font(size=30)
	
	back = Button(win, text="Back", command=to_home)
	back.pack()
	back.place(x=40, y=35)
	back['font'] = myFont

	exit = Button(win, text="Exit", command=quit)
	exit.pack()
	exit.place(x=850, y=35)
	exit['font'] = myFont
		
	abt_txt = Label(win, text="This project is developed by\nShoif Md Mia.\nMain aim for this project is\nto use database in a project.\nFor user interface tkinter is\nused and for database MongoDB\nis used here in this project.\n\nFeel free to contact. E-mail:\nshoifmohammad@gmail.com", bg='#6CBB3C', fg="#2B1B17")
	abt_txt.config(font=("Courier", 40))
	abt_txt.pack()
	abt_txt.place(x=40, y=150)

records = db.admins_list
a = records.count_documents({})

root = Tk()
root.title("Library Management System")
right = int(root.winfo_screenwidth()/2 - width/2)
down = int(root.winfo_screenheight()/2 - height/2)
string = str(width) + "x" + str(height) + "+" + str(right) + "+" + str(down)

root.geometry(string)
root.configure(bg='#6CBB3C')

label = Label(root, text="Welcome to\nLibrary Management System", bg='#6CBB3C', fg="#2B1B17")
label.config(font=("Courier", 45))
label.pack()
label.place(x=50, y=125)

img = ImageTk.PhotoImage(Image.open("flower.png"))
panel_left = Label(root, image=img)
panel_left.pack(side="left")
panel_left.place(y=0)

panel_right = Label(root, image=img)
panel_right.pack()
panel_right.place(x = 870, y=0)

myFont = font.Font(size=30)

button_admin = Button(root, text="Admin login", command=admin_login, width=12, height=2)
button_admin.pack()
button_admin.configure(activebackground="#786D5F")
button_admin.place(x=100, y=375)
button_admin['font'] = myFont

button_student = Button(root, text="Student login", command=student_login, width=12, height=2)
button_student.pack()
button_student.configure(activebackground="#786D5F")
button_student.place(x=570, y=375)
button_student['font'] = myFont

button_exit = Button(root, text="Exit", command=quit, width=12, height=2)
button_exit.pack()
button_exit.configure(activebackground="#786D5F")
button_exit.place(x=100, y=575)
button_exit['font'] = myFont

button_about = Button(root, text="About", command=about, width=12, height=2)
button_about.pack()
button_about.configure(activebackground="#786D5F")
button_about.place(x=570, y=575)
button_about['font'] = myFont

root.mainloop()