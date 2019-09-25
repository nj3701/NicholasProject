#!/usr/bin/env python3
import datetime

"""
This is a module of classes that Team M's Group Project's persistence
module requires for storage. Note that some of these were made by group
members OTHER than the person responsible for Module 1; although they are
the responsibility of other members, the persistence layer needs to know
the class definitions.
"""

#---
#---Module 1 Classes
#---

class User:
    """Class with fields to store user account information.

        Fields:
        name: Account username
        pswd: Account password
        level: Account's access level.
    """
    
    def __init__(self, username, password, accessLevel = "student"):
        """Create a User object.

            Parameters:
            username (str): Assigned to the object's name field.
            password (str): Assigned to the object's pswd field.
            accessLevel (str): Assigned to the object's level field.
        """
        self.name = username
        self.pswd = password
        self.level = accessLevel

    def getName(self):
        """Return the string in the user's name field."""
        return self.name

    def setName(self, newName):
        """Change user's name field to given string.

            Parameter:
            newName (str): User's name field will be set to this.
        """
        self.name = newName

    def getPass(self):
        """Return the string in the user's pswd field."""
        return self.pswd

    def setPass(self, newPswd):
        """Change user's pswd field to the given string.

            Parameter:
            newPswd (str): User's pswd field will be set to this.
        """
        self.pswd = newPswd

    def getLevel(self):
        """Return the string in the user's level field."""
        return self.level

    def setLevel(self, newLevel):
        """Change user's access level to given string.

            Parameters:
            newLevel (str): User's level field will be set to this.
        """
        self.level = newLevel

#---
#---Module 2 Classes
#---

class Quiz:
    def __init__ (self, name = "", startTime = datetime.datetime.now(), endTime = datetime.datetime(2040,1,1), attempts = 1, multipleAnswers = [], weight = 10, studentList = {}, instructor = ""):
        self.name = name
        self.startTime = startTime
        self.endTime = endTime
        self.attempts = attempts
        self.question = multipleAnswers
        self.weight = weight
        self.students = studentList
        self.instructor = instructor

#Gettor methods

    def __str__(self):
        """ A newly defined quiz str statement in order to print the quiz in
                a readable format
        """
        print(self.name + "Instructor: " +str(self.instructor))
        print("Start time: " + str(self.startTime) + "   End time: " + str(self.endTime))
        print("number of attempts: " + str(self.attempts))
        for questions in self.question:
            print(questions.getName())
            for choices in questions.getChoices():
                print(choices)
        print("Weight of the quiz: " + str(self.weight))
        return ""
    def getName(self):
        return self.name
    def getStartTime(self):
        """ A method to return the start time of the quiz """
        return self.startTime

    def getEndTime(self):
        """ A method to return the end time of the quiz """
        return self.endTime

    def getAttempts(self):
        """ A method to return the number of attempts of the quiz """
        return self.attempts

    def getQuestions(self):
        """ A method to return the questions of the quiz """
        return self.question

    def getWeight(self):
        """ A method to return the weight of the quiz """
        return self.weight

    def getStudents(self):
        """ A method to return students that can take the quiz """
        return self.students.keys()

    def getInstructor(self):
        """A method to return the instructor that created the quiz"""
        return self.instructor

    

#Mutator methods
    def changeStudents(self, student, addOrRemove = True):
        """ A method to add or remove a student from the student list
                Checks to see if the student value is valid"""
        if isinstance (student, str):
            if addOrRemove == True:
                self.students.append(student)
            else:
                for students in self.students:
                    if students == student:
                        self.students.pop(student)
        else:
            while not isinstance (student, str):
                student = input("Please enter a valid student name ")
            if addOrRemove == True:
                self.students.append(student)
            else:
                for students in self.students:
                    if students == student:
                        self.students.pop(student) 
            

    def changeStart(self, newTime):
        """ A method to change the start time of the quiz. Checks to see if
                given time is a datetime.datetime object"""
        if isinstance(newTime, datetime.datetime):
            self.startTime = newTime
        else:
            while not isinstance(newTime, datetime.datetime):
                newTime = datetime.datetime(input("Please enter a valid start time "))
            self.startTime = newTime

    def changeEnd(self, newTime):
        """ A method to change the end time of the quiz  Checks to see if
                given time is a datetime.datetime object"""
        if isinstance(newTime, datetime.datetime):
            self.endTime = newTime
        else:
            while not isinstance(newTime, datetime.datetime):
                newTime = datetime.datetime(input("Please enter a valid endtime "))
            self.endTime = newTime

    def changeWeight(self, newWeight):
        """A method to change the weight of a quiz, checks to see if the input
                is a valid int"""
        if isinstance(newWeight, int):
            self.weight = newWeight
        else:
            while not isinstance(newWeight, int):
                newWeight = input("Please enter a valid weight ")
                if newWeight.isdigit():
                    newWeight = int(newWeight)
            self.weight = newWeight
        
        
    def changeAttempts(self, newLimit):
        """A method to change the number of attempts a student can have at a quiz
            Checks to see if newLimit is a valid int"""
        if isinstance(newLimit, int):
            self.attempts = newLimit
        else:
            while not isinstance (newLimit, int):
                newLimit = input("Please enter a valid number for attempts")
                if newLimit.isdigit():
                    newLimit = int(newLimit)
            self.attempts = newLimit

    def addQuestion(self, question):
        """A method to add a question to the quiz

            Raises:
                TypeError - if something besides a question is passed
    """
        if isinstance (question, Question):
            self.question.append(question)
        else:
            raise TypeError (question + "Must be of type Question")

    def removeQuestion(self, position):
        """A method to remove a question from the quiz

            Raises:
            IndexError - if out of range of list
        """
        self.question.remove(position)



class Question:
    """
        A class to hold the attributes of a Question

        Attributes:
            name - The name/ body of the question
            choices - The mutiple choices that could be the answer
            answer - The single, or multiple answers to the question
    """

    def __init__(self, questionName, content = "", choices = [], answer = []):
        self.name = questionName
        self.content = content
        self.choices = choices
        self.answer = answer
        if isinstance (self.answer, int):
            holder = self.answer
            self.answer = []
            self.answer.append(holder)

    def __str__(self):
        """Overwritten string method, used to print question name and the choices"""
        print (self.getName())
        holder = ""
        for i in self.getChoices():
            holder += ("   " + i + "\n")
        return (self.name + "\n" +holder)
        
    def getName(self):
        """A method to return the question name"""
        return self.name

    def getChoices(self):
        """A method to return the mutiple choice questions"""
        return self.choices

    def getAnswer(self):
        """A method to return the answer for a question """
        return self.answer


    def changeName(self, newName):
        """A method to change the name of a question """
        if isinstance(newName, str):
            self.name = newName

    def addAnswer(self, newAnswer):
        """A method to add an answer for a given multiple choice, checks to
                see if newAnswer is a valid index.

            Rasies:
                IndexError - if given answer is out of range
        """
        if isinstance (newAnswer, int):
            if newAnswer > 0 and newAnswer < len(self. choices):
                self.answer.append(newAnswer)
            else:
                raise IndexError("newAnswer is out of range")
        else:
            while isinstance (newAnswer, int) != True:
                newAnswer = input("Please enter a valid integar ")
                if newAnswer.isdigit():
                    newAnswer = int(newAnswer)
            self.answer.append(newAnswer)

    def addChoice(self, newChoice):
        """A method to add a question choice to the question"""
        self.choices.append(newChoice)

    
    def removeChoice(self, indexNum):
        """A method to remove a choice by index number

            Raises:
            IndexError - if given number is out of range
        """
        if isinstance (indexNum, int):
            if indexNum > 0 and indexNum < len(self.choices):
                self.choices.remove(indexNum)
            else:
                raise IndexError("Key is out of range")
        else:
            while isinstance (indexNum, int) != True:
                indexNum = input("Please enter a valid integar ")
            if indexNum > 0 and indexNum < len(self.choices):
                self.choices.remove(indexNum)
            else:
                raise IndexError("Key is out of range")

#---
#---Module 3 Classes
#---
            
class Attempt:
    def __init__(self, student_name=None, quiz_name=None, answer=None, submit_time=None):
        """
            args:
                name: the student's name       | type: str
                quiz_name: the quiz's name     | type: str
                result: answer for the quiz    | type: dict
                submit_time: submit time       | type: datetime
        """
        self._student_name = student_name
        self._quiz_name = quiz_name
        self._answer = answer
        self._submit_time = submit_time
        self._grade = None

    # getters #####################################################################################
    @property
    def student_name(self):
        """    do: return student's name    """
        return self._student_name

    @property
    def quiz_name(self):
        """    do: return quiz's name    """
        return self._quiz_name

    @property
    def answer(self):
        """    do: return answer written by student    """
        return self._answer

    @property
    def submit_time(self):
        """    do: return the submit time of this attempt    """
        return self._submit_time

    @property
    def grade(self):
        """    do: return grade    """
        return self._grade

    # setters #####################################################################################
    @student_name.setter
    def student_name(self, student_name):
        """    do: set student's name    """
        self._student_name = student_name

    @quiz_name.setter
    def quiz_name(self, quiz_name):
        """    do: set quiz's name    """
        self._quiz_name = quiz_name

    @answer.setter
    def answer(self, answer):
        """    do: set answer written by student    """
        self._answer = answer

    @submit_time.setter
    def submit_time(self, submit_time):
        """    do: set the submit time of this attempt    """
        self._submit_time = submit_time

    @grade.setter
    def grade(self, grade):
        """    do: set grade    """
        self._grade = grade















#
