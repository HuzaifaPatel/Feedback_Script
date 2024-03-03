import os
import csv

DIR_PATH = "C:\\Users\\huzai\\Downloads\\A1 Race conditions and access control Download Feb 16, 2024 835 PM"
CSV_PATH = "C:\\Users\\huzai\\Desktop\\A1.csv"
name = []
feedback = []

def remove_contents():
	for file_path in os.listdir(DIR_PATH):
		os.chdir(DIR_PATH)
		if os.path.isdir(file_path):
			os.chdir(DIR_PATH + "\\" + file_path)
			for file in os.listdir():
				os.remove(file)

def get_student_number():
	for file in os.listdir(DIR_PATH):
		if os.path.isdir(file):
			lis = file.split(" ")
			lis = lis[2:-5]
			student_number = lis[-1][:-1]
			lis = lis[:-1]
			name = " ".join(lis)
			print(name)
			print(student_number)
			
def get_feedback_data():
	with open(CSV_PATH, 'r', newline='') as file:
		reader = csv.reader(file)
		header = next(reader)
		for row in reader:
			if len(row[0]) != 0:
				name.append(row[0])
				feedback.append(row[27])


def construct_feedback_file():
	os.chdir(DIR_PATH)
	for student in range(len(name)):
		for file_path in os.listdir(DIR_PATH):
			if os.path.isdir(file_path):
				new_name = name[student].replace(",","")
				if new_name in file_path:
					os.chdir(DIR_PATH + "\\" + file_path)
					file = open(DIR_PATH + "\\" + file_path + "\\feedback.txt", 'a+')
					file.write(feedback[student])
					file.close()
					os.chdir(DIR_PATH)


get_feedback_data()
remove_contents()
construct_feedback_file()
# get_student_number()