#!/usr/bin/env python3
import shelve
from OtherClasses import *

"""A module for decoupling Shelve from Group M's Quiz Project.

    Data structure:
    Shelve stores data within a dictionary. IStore makes a shelve file
    to store instructor user info and the quizes they make and allows
    you to add, remove, and alter quizes. SStore makes a shelve file to
    store student user info and the results of quizes they take and allows
    for results to be updated. Any IStore or SStore object must be closed
    by using the close() method when finished with the object.

    Note that shelve is not a practical interface for commercial storage
    in projects of this nature. This is merely for crudely functional,
    school-based purposes. A database should be used for larger scale
    projects.   
"""

class ItemLookupError(Exception):
    """Raised upon failure to add or retrieve an object from storage."""
    def __init__(self, message = ""):
        self.msg = message

class UserLookupError(ItemLookupError):
    """Raised upon failure to add or retrieve a user from storage."""
    pass

class QuizLookupError(ItemLookupError):
    """Raised upon failure to add or retrieve a quiz from storage."""
    pass

class QuestionLookupError(ItemLookupError):
    """Raised upon failure to add or retrieve a question from storage."""
    pass

class ResultLookupError(ItemLookupError):
    """Raised upon failure to add or retrieve a quiz result from
        storage.
    """
    pass

class UserStore:
    """Acts as a base class for instructor and student storage. Contains a
        main shelve file for users, and allows for lookup, addition, and
        removal of users. Any subclass will have a username for a key, and
        a tuple as the associated value, with a User object as the first
        item in the tuple, with anything else required for storage as
        other tuple values. Must be closed to save any changes. Doing so
        renders this object useless.
        
        Shelve dictionary structure:
        {username:(User, ?, ...), ...}
    """
    def __init__(self, filename):
        """Creates a Shelve file for user storage.

            Parameters:
            filename (str): The name of the file that data will be stored
                in
        """
        self._Users = shelve.open(filename, writeback=True)

    def lookupUser(self, username):
        """Returns True if the user exists in storage, False if not.

            Parameters:
            username (str): The name of the user being searched for
        """
        return username in self._Users
    
    def getUser(self, username):
        """Returns the User object associated with the given username from
            storage. If the user does not exist, raises UserLookupError.

            Parameters:
            username (str): The name of the user being searched for
        """
        if not self.lookupUser(username):
            raise UserLookupError("User not found.")
        else: return self._Users[username][0]

    def delUser(self, username):
        """Removes the user from persistent storage. If a user with the
            given name does not exist, does nothing.
            
            Parameters:
            username (str): The name of the user being removed
        """
        if username in self._Users: del self._Users[username]

    def close(self):
        """Commits any changes made to storage and closes the storage."""
        self._Users.close()

    def __contains__(self, user):
        return user in self._Users

class IStore(UserStore):
    """Contains a shelve file where the key is an instructor username, and
        the associated value is a tuple containing the instructor's User
        object, followed by another dictionary to store quizes, followed by
        another dictionary to store the instructor's questions.
    """
        
    def addUser(self, user):
        """Adds given instructor User to storage. If username is taken,
            raises UserLookupError
            
            Parameters:
            user (User): The User object being stored
        """
        if user.name in self._Users: raise UserLookupError("Duplicate username.")
        self._Users[user.name] = (user, {}, {})

    def addQuiz(self, instructorname, quiz, replace = False):
        """Adds a quiz to the instructor's quiz dictionary. If a quiz with
            the given name already exists, raise QuizLookupError if replace
            is False, otherwise replace the old quiz with the current quiz.
            If instructor not found, raises UserLookupError.

            Parameters:
            instructorname (str): The name of the instructor who the quiz
                will be stored for
            quiz (Quiz): The quiz object being stored
            replace (bool): If a quiz of the given name exists, this value
                decides if it is replaced (True) or an error is raised
                (False)
        """
        if self.lookupUser(instructorname):
            if quiz.name in self._Users[instructorname][1]:
                if replace:
                    self._Users[instructorname][1][quiz.name] = quiz
                else: raise QuizLookupError("Duplicate quiz name. Quiz not added.")
            else: self._Users[instructorname][1][quiz.name] = quiz
        else: raise UserLookupError("Instructor not found.")          

    def delQuiz(self, instructorname, quizname):
        """Removes the quiz from the instructor's quiz dictionary. If a
            quiz with the given name does not exist, does nothing. If
            instructor doesn't exist, raise UserLookupError.

            Parameters:
            instructorname (str): The name of the instructor who will have
                their quiz removed
            quizname (str): The name of the quiz to be removed
        """
        if self.lookupUser(instructorname):
            if quizname in self._Users[instructorname][1]:
                del self._Users[instructorname][1][quizname]
        else: raise UserLookupError("Instructor not found.")

    def getQuiz(self, instructorname, quizname):
        """Returns the quiz of the given name by the given instructor. If
            there is no quiz by the given name, raises QuizLookupError.
            If instructor doesn't exist, raise UserLookupError.

            Parameters:
            instructorname (str): The name of the instructor who owns the
                quiz
            quizname (str): The name of the quiz to be returned
        """
        if self.lookupUser(instructorname):
            if quizname in self._Users[instructorname][1]:
                return self._Users[instructorname][1][quizname]
            else: raise QuizLookupError("Quiz not found.")
        else: raise UserLookupError("Instructor not found.")

    def allQuizes(self, instructor = None, student = None):
        """Returns a list of all quizes for all instructors. If an
            instructor is specified, only quizes from the given instructor
            will be in the list. If a student is specified, only quizes for
            which the student is eligible will be in the list. If an
            instructor is given and said instructor is not found in
            storage, raises UserLookupError.

            Parameters:
            instructor (str): If given, the output will be limited to
                quizes created by this instructor.
            student (str): If given, the output will be limited to quizes
                eligible to this student.
        """
        def _instructorquizdive(thisInstructor):
            extension = []
            for quizname in self._Users[thisInstructor][1]:
                quiz = self._Users[thisInstructor][1][quizname]
                if student == None or student in quiz.getStudents():
                    extension.append(quiz)
            return extension
        outlist = []
        if instructor != None:
            if not self.lookupUser(instructor):
                raise UserLookupError("Instructor not found.")
            outlist.extend(_instructorquizdive(instructor))
        else:
            for i in self._Users:
                outlist.extend(_instructorquizdive(i))
        return outlist

    def addToBank(self, instructorname, question):
        """Adds given Question to the instructor's question bank. If a
            question with the same name as the given question exists, raises
            QuestionLookupError. If instructor doesn't exist, raises
            UserLookupError.

            Parameters:
            instructorname (str): The name of the instructor who will have
                a question added to their bank
            question (Question): The Question object to be added
        """
        if self.lookupUser(instructorname):
            if question.name not in self._Users[instructorname][2]:
                self._Users[instructorname][2][question.name] = question
            else: raise QuestionLookupError("Duplicate question name")
        else: raise UserLookupError("Instructor not found.")

    def delFromBank(self, instructorname, questionname):
        """Removes question with given name from instructor's question
            bank. If no such question exists, does nothing. If instructor
            is not found, raises UserLookupError.

            Parameters:
            instructorname (str): The name of the instructor who will have
                a question removed from their bank
            questionname (str): The name of the question to be removed
        """
        if self.lookupUser(instructorname):
            if questionname in self._Users[instructorname][2]:
                del self._Users[instructorname][2][questionname]
        else: raise UserLookupError("Instructor not found.")

    def getFromBank(self, instructorname, questionname):
        """Returns question with given name from instructor's question
            bank. If no such question exists, raises QuestionLookupError.
            If instructor doesn't exist, raise UserLookupError.

            Parameters:
            instructorname (str): The name of the instructor who will have
                a question returned from their bank
            questionname (str): The name of the question to be returned
        """
        if self.lookupUser(instructorname):
            if questionname in self._Users[instructorname][2]:
                return self._Users[instructorname][2][questionname]
            else: raise QuestionLookupError("Question not found.")
        else: raise UserLookupError("Instructor not found.")

class SStore(UserStore):
    """Contains a shelve file where the key is a student username, and the
        associated value is a tuple containing the student's User object
        followed by another dictionary. This second level dictionary
        has an instructor username as a key, and yet another dictionary as a
        value. This third level dictionary has a quiz name as a key, and a
        list of Attempts as a value.

        Shelve Dictionary structure:
        {studentname:(User, {instructorname:{quizname:[Attempt,...]}})}
    """
    
    def addUser(self, user):
        """Adds a new student User to storage. If username is taken, raises
            UserLookupError.

            Parameters:
            user (User): The User object being stored
        """
        if user.name in self._Users:
            raise UserLookupError("Duplicate username.")
        self._Users[user.name] = (user, {})

    def addResult(self, username, instructorname, attempt):
        """Adds an Attempt object to the shelve entry for the student with
            the given username under the given instructor's name. If the
            student user doesn't exist, raises UserLookupError.

            Parameters:
            username (str): The name of the student who made the attempt
                being added
            instructorname (str): The name of the instructor who posted
                the quiz that was attempted
            attempt (Attempt): The Attempt object being added
        """
        if self.lookupUser(username):
            if instructorname in self._Users[username][1]:
                if attempt.quiz_name in \
                   self._Users[username][1][instructorname]:
                    self._Users[username][1][instructorname]\
                    [quizname].append(attempt)
                else:
                    self._Users[username][1][instructorname][quizname] = \
                    [attempt]
            else:
                self._Users[username][1][instructorname] = \
                  {attempt.quiz_name:[attempt]}
        else: raise UserLookupError("Student not found.")        

    def delResult(self, username, instructorname, quizname):
        """Removes all quiz attempts associated with the student with the
            given username and the given instructor username for the
            given quiz name. If there is no existing result, does nothing.
            If given student doesn't exist in storage, raise
            UserLookupError.

            Parameters:
            username (str): The name of the student who made the attempt(s)
                being removed
            instructorname (str): The name of the instructor who posted
                the quiz that is having its results removed
            quizname (str): The name of the quiz that is having its results
                removed
        """
        if self.lookupUser(username):
            if instructorname in self._Users[username][1]:
                if quizname in self._Users[username][1][instructorname]:
                    del self._Users[username][1][instructorname][quizname]
        else: raise UserLookupError("Student not found.")

    def getResult(self, username, instructorname, quizname, attemptindex):
        """Returns the Attempt object submitted by the student with the given
            username. The Attempt returned is determined by the attemptindex,
            with the list in which attempts are stored being sorted by time
            of attempt. Raises a UserLookupError if student is not found,
            raises ResultLookupError if there is no Attempt found.

            Parameters:
            username (str): The name of the student who made the Attempt
                being returned
            instructorname (str): The name of the instructor who posted
                the quiz associated with the returned Attempt
            quizname (str): The name of the quiz associated with the
                returned Attempt.
            attemptindex (int): The index of the Attempt being returned.
        """
        if self.lookupUser(username):
            if instructorname in self._Users[username][1]:
                if quizname in self._Users[username][1][instructorname]:
                    if len(self._Users[username][1][instructorname][quizname])\
                       >= (attemptindex + 1):
                        return self._Users[username][1][instructorname][quizname]\
                                [attemptindex]
                    else: raise ResultLookupError("Result not found: invalid index")
                else: raise ResultLookupError("Result not found: invalid quiz")
            else: raise ResultLookupError("Result Not Found: invalid instructor")
        else: raise UserLookupError("Student not found.")

    def updateResult(self, username, instructorname, attempt, attemptindex):
        """Replaces the Attempt at the given index with a new one. This
            method should be used to update an existing Attempt with a
            grade. Raises UserLookupError if student user is not found.
            Raises QuizLookupError if student has no results stored by the
            given instructor with the given quiz name. Raises
            ResultLookupError if there is no Attempt object at the given
            index.

            Parameters:
            username (str): The name of the student who made the attempt
                being updated
            instructorname (str): The name of the instructor who posted
                the quiz associated with the Attempt being updated
            attempt (Attempt): The attempt that is replacing the old one
            attemptindex (int): The index of the Attempt being replaced
        """
        if self.lookupUser(username):
            if instructorname in self._Users[username][1]:
                if attempt.quiz_name in self._Users[username][1][instructorname]:
                    if len(self._Users[username][1][instructorname]\
                           [attempt.quiz_name]) >= (attemptindex + 1):
                        self._Users[username][1]\
                            [instructorname][attempt.quiz_name]\
                                [attemptindex] = attempt
                    else: raise ResultLookupError("Result not found: invalid index")
                else: raise ResultLookupError("Result not found: invalid quiz")
            else: raise ResultLookupError("Result Not Found: invalid instructor")
        else: raise UserLookupError("Student not found.")

        


        
