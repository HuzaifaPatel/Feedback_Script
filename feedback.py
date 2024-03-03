import os
import csv
import shutil
DIR_PATH = "/home/huzi/Downloads/brightspace_submissions"
CSV_PATH = "/home/huzi/Downloads/a2.csv"
# OrgDefinedId means student number. example #123456789. Must include hashtag
# username means student name (#firstnamelastname) order matters, no spaces, hashtag must be included
# Third header is assignment title (get it from brightspace)
# Fourth Header is where the feedback will go
# Fifth Header denotes the EOL
#only header that should EVER change is the third one (assignment name)
headers = ['OrgDefinedId', 'Last_Name', 'First_Name', 'Username', 'A2: Rookit Points Grade', 'Participation Text Grade', 'End-of-Line Indicator']

#this is where we write all the data to
filename = 'data.csv'


data = {} # key is student name without commas. value is as follows: [student number, name (with commas), grade, feedback]
def remove_contents_from_directories():
	os.chdir(DIR_PATH)
	for file_path in os.listdir(DIR_PATH):
		if os.path.isdir(file_path):
			os.chdir(DIR_PATH + "/" + file_path)
			print(DIR_PATH + "/" + file_path)
			for file in os.listdir():
				if os.path.isdir(file):
					shutil.rmtree(file)
				else:
					os.remove(file)
		os.chdir(DIR_PATH)

# we get the student number from the directory names given by brightspace
def get_student_number(file):
	lis = file.split(" ")
	lis = lis[2:-5]
	return "#"+lis[-1][:-1]


def get_student_name(file):
	lis = file.split(" ")
	lis = lis[2:-6]
	name = " ".join(lis)
	data[name] = []
	data[name].append(get_student_number(file))

def get_feedback_data():
	with open(CSV_PATH, 'r', newline='') as file:
		reader = csv.DictReader(file)
		for row in reader:
			name = row['Student_Name'].replace(", ", " ")
			if name in data:
				data[name].append(row['Student_Name'].split(", ")[0])
				data[name].append(row['Student_Name'].split(", ")[1])
				data[name].append("#" + " ".join(row['Student_Name'].split(", ")[::-1]).lower().replace(" ", ""))
				if float(row['Mark']) < 0:
					data[name].append(0)
				data[name].append(round(float(row['Mark']), 2))
				data[name].append((row['Comment2']))
				data[name].append("#") # add EOL


#make sure only brightspace folders are in folder
def construct_prereq_data():
	os.chdir(DIR_PATH)
	for file_path in os.listdir(DIR_PATH):
		if os.path.isdir(file_path):
			get_student_name(file_path)
	get_feedback_data()


def construct_feedback_file():
	os.chdir(DIR_PATH)
	for student in data:
		for file_path in os.listdir(DIR_PATH):
			if os.path.isdir(file_path):
				if student in file_path:
					os.chdir(DIR_PATH + "/" + file_path)
					file = open(DIR_PATH + "/" + file_path + "/feedback.txt", 'a+')
					file.write(str(data[student][5]))
					file.close()
					os.chdir(DIR_PATH)

def create_csv_file():
	os.chdir(DIR_PATH)
	with open(filename, mode='w', newline='') as file:
		writer = csv.writer(file)
    	# Write the header row
		writer.writerow(headers)

		for student_name in data:
			writer.writerows([data[student_name]])


#run this first
remove_contents_from_directories()

# #run this second. Here, we get student number, student name, and feedback
construct_prereq_data()

# # run this last
construct_feedback_file()

create_csv_file()