# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script Starter
#   Marina Osiechko, 3/8/2026, Modified Script from Starter
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.


# TODO Create a Person Class (Done)
# This newly created Person class inherits code from Python's object class.
class Person:
    """
    A class representing person data.

    Properties:
    - first_name (str): The student's first name.
    - last_name (str): The student's last name.

    ChangeLog:
    - MOsiechko, 3.8.2026: Created class Person.
    """

    # TODO Add first_name and last_name properties to the constructor (Done)
    def __init__(self, first_name: str = '', last_name: str = ''):
        self.first_name = first_name
        self.last_name = last_name

    # TODO Create a getter and setter for the first_name property (Done)
    @property   #(Use this decorator for the getter or accessor)
    def first_name(self):
        return self.__first_name.title()    # formatting code

    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha() or value == "":   # is character or empty string
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    # TODO Create a getter and setter for the last_name property (Done)
    @property  # (Use this decorator for the getter or accessor)
    def last_name(self):
        return self.__last_name.title()  # formatting code

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha() or value == "":  # is character or empty string
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    # TODO Override the __str__() method to return Person data (Done)
    def __str__(self):
        return f'{self.first_name},{self.last_name}'

# TODO Create a Student class that inherits from the Person class (Done)
class Student(Person):
    """
        A collection data about students

        ChangeLog: (Who, When, What)
        Marina Osiechko, 3/8/2026,Created Class
        Marina Osiechko, 3/8/2026,Added properties and private attributes
        """

    # TODO call to the Person constructor and pass it the first_name and last_name data (Done)
    # super method connects first and last name to the Person class
    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        super().__init__(first_name=first_name,
                         last_name=last_name)

        # TODO add an assignment to the course_name property using the course_name parameter (Done)
        self.course_name = course_name

    # TODO add the getter for course_name (Done)
    @property
    def course_name(self):
        return self.__course_name

    # TODO add the setter for course_name (Done)
    @course_name.setter
    def course_name(self, value: str):
        self.__course_name = value

    # TODO Override the __str__() method to return the Student data (Done)
    def __str__(self):
        return f'{self.first_name},{self.last_name},{self.course_name}'


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with JSON files

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    Marina Osiechko,3.8.2026,Modified Code
    """
    @staticmethod
    def read_data_from_file(file_name: str, students: list):
        """ This function reads data from a JSON file and loads it into a list of dictionary rows
        then returns the list filled with student data.

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Marina Osiechko,3.8.2026,Converted dictionary data to Student data
        Marina Osiechko,3.9.2026,Converted Student objects into dictionaries

        :param file_name: string data with name of file to read from
        :return: list
        """
        file = None

        try:
            # Get a list of dictionary rows from the data file
            file = open(file_name, "r")
            json_students = json.load(file)  # the load function returns a list of dictionary rows.

            # Convert the list of dictionary rows into a list of Student objects
            # TODO replace this line of code to convert dictionary data to Student data (Done)
            # student_objects = json_students
            for row in json_students:    # Convert the list of dictionary rows into Student objects
                students.append(Student(first_name=row["FirstName"],
                                        last_name=row["LastName"],
                                        course_name=row["CourseName"]))
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)

        except json.JSONDecodeError as e:
            IO.output_error_messages(message="Error: The file contains invalid JSON.", error=e)

        finally:
            if file is not None and file.closed == False:
                file.close()

        return students

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a JSON file with data from a list of dictionary rows

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Marina Osiechko,3.8.2026, Added code converting student objects to dictionaries

        :param file_name: string data with name of file to write to
        :param student_data: list of dictionary rows to be writen to the file

        :return: None
        """
        file = None
        json_students = []

        try:
            # TODO Add code to convert Student objects into dictionaries (Done)
            for student in student_data:   # Convert List of Student objects to list of dictionary rows.
                student_json: dict \
                = {"FirstName": student.first_name, "LastName": student.last_name, "CourseName": student.course_name}
                json_students.append(student_json)

            file = open(file_name, "w")
            json.dump(json_students, file, indent=2)

            IO.output_student_courses(student_data=student_data)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message,error=e)
        finally:
            if file is not None and file.closed == False:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    RRoot,1.2.2030,Added menu output and input functions
    RRoot,1.3.2030,Added a function to display the data
    RRoot,1.4.2030,Added a function to display custom error messages
    Marina Osiehcko,3.7.2026,Modified Code
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays the custom error messages to the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Marina Osiechko,3.8.2026,Added code to access Student object data instead of dictionary data

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1","2","3","4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays the student and course names to the user as coma-separated
        values.

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Marina Osiechko, 3.8.2026, Changed code to access Student object instead of dict data

        :param student_data: list of dictionary rows to be displayed
        :return: None
        """

        print("-" * 50)
        for student in student_data:

            # TODO Add code to access Student object data instead of dictionary data (Done)
            #print(f'Student {student["FirstName"]} '
            #      f'{student["LastName"]} is enrolled in {student["CourseName"]}')
            # print(f"{student.first_name},{student.last_name},{student.course_name}")   # Coma-separated view
            print(student)
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name and last name, with a course name from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Marina Osiechko,3.8.2026, Replaced code to use Student object instead of dict objects

        :param student_data: list of dictionary rows to be filled with input data
        :return: list
        """

        try:
            first_name = input("Enter the student's first name: ")
            if not first_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            last_name = input("Enter the student's last name: ")
            if not last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ")

            # TODO Replace this code to use a Student objects instead of a dictionary objects (Done)
            #student = {"FirstName": student_first_name,
            #           "LastName": student_last_name,
            #           "CourseName": course_name}

            student= Student(first_name, last_name, course_name)

            student_data.append(student)
            print()
            print(f"You have registered {student.first_name} {student.last_name} for {student.course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Start of main body

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = []
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, students = students)
#FileProcessor.read_data_from_file(FILE_NAME, students)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
