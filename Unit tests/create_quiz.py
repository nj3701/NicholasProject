from QuizShelve import *

"""Create quiz module

    Classes:
        Create_Quiz - A module for create and modify quiz objects
"""


class Create_Quiz:
    """Allows instructors to create a quiz from scratch, or modify an existing quiz

    Methods:
        createQuiz - Creates a quiz from start to finish based on user input
        modifyQuiz - Loads a quiz by name, and using a key value allows the user
                        to modify aspects of the quiz
        loadQuiz - Loads a quiz by name, for viewing only
        addToBank - Used to create a question and put it in the question Bank

    Raises:

    """

    #Public methods

    def createQuiz(quizName, startTime, endTime, attempts, choices, weight, students, currentUser):
        
        """Creates a quiz from start to finish

            Parameters:
                quizName - A string which denotes the name of the quiz
                startTime - The datetime.datetime denoting the start of the quiz
                endTime - The datetime.datetime denoting the end of the quiz
                attempts - The int denoting the number of attempts the students get
                choices - A list of the questions to be included in the quiz
                weight - The int denoting the weight of the quiz
                students - A list of students who can take the quiz
            Raises:
                ValueError - if endTime is before startTime
                             if weight and attempts are not positive integars
                             if the quiz name is already in use

            Returns a quiz object
        """
        storage = IStore("instructorStorage.dat")
        questions = []
        for elements in choices:
            questions.append(storage.getFromBank(currentUser, elements))
        newQuiz = Quiz(quizName, startTime, endTime, attempts, choices, weight, students, currentUser)
        storage.addQuiz(currentUser, newQuiz)
        storage.close()
        return Quiz(quizName,startTime, endTime, attempts, choices, weight, students, currentUser)


    def modifyQuiz(quizName, key, val, user):
        """Allows the user to modify an exisiting quiz

            Parameters:
                quizName - The string of the quiz name which is being modified
                key - The string that is used as a key to change a given value
                val - The value of the attribute being changed, can be a str or int
            Keys:
                N - Modify quizName
                S - Modify startTime
                E - Modify endTime
                A - Modify attempts
                AC - add a choice to choices
                RC - remove a choice from choices
                W - Modify the weight attribute
                AS - Add a student to the students
                RS - Remove a student from the students

            Raises:
                ValueError - If key k is not a valid key
                QuizLookupError - If the quiz is not in the instructor's quizzes

            Returns:
                A quiz object with modified attributes
        """
        storage = IStore("instructorStorage.dat")
        currentQuiz = storage.getQuiz(user, quizName)
        if key == "N":
            currentQuiz.changeName(val)
        elif key == "S":
            val = val.split(",")
            sYear = int(val[0])
            sMon = int(val[1])
            sDay = int(val[2])
            val = datetime.datetime(sYear, sMon, sDay)
            currentQuiz.changeStart(val)
        elif key == "E":
            val = val.split(",")
            eYear = int(val[0])
            eMon = int(val[1])
            eDay = int(val[2])
            val = datetime.datetime(eYear, eMon, eDay)
            currentQuiz.changeEnd(val)
        elif key == "A":
            val = int(val)
            if val < 0:
                raise ValueError("Attempts must be positive int")
            
            currentQuiz.changeAttempts(val)
        elif key == "AC":
            val = storage.getFromBank(currentLogin, val)
            currentQuiz.addQuestion(val)
        elif key == "RC":
            val = int(val)
            currentQuiz.removeQuestion(val)
        elif key =="W":
            val = int(val)
            if val < 0:
                raise ValueError("Weight must be positive int")
            
            currentQuiz.changeWeight(val)
        elif key =="AS":
            currentQuiz.changeStudents(val)
        elif key =="RS":
            currentQuiz.changeStudents(val, False)
        else:
            raise KeyError("Key entered is not valid")
        storage.close()
        return Quiz(currentQuiz.getName(),currentQuiz.getStartTime(),currentQuiz.getEndTime(),currentQuiz.getAttempts(), currentQuiz.getQuestions(), currentQuiz.getWeight(), currentQuiz.getStudents(),currentQuiz.getInstructor())

    def loadQuiz(quizName, instructorName):
        """Loads the quiz by name for viewing only

            Raises:
                QuizLookupError - If the quiz name was not found

            Returns:
                A quiz object specified by name
        """
        storage = IStore("instructorStorage.dat")
        currentQuiz = storage.getQuiz(instructorName, quizName)
        storage.close()
        return currentQuiz

    def addToBank(questionName, content, choices, answer, user):
        """Used to add a single question to the question bank

            Parameters:
                questionName - String input denoting the name of the question
                choices - A list of the multiple choices that are available
                answer = Int number denoting the index of the list that is correct
    
            Raises:
               QuestionLoopupError - if name has been used before
               IndexError - If answer index is out of index range

            Returns:
                A object of Question type with name, choices, and an answer
        """
        storage = IStore("instructorStorage.dat")
        newQuestion = Question(questionName, content, choices, answer)
        storage.addToBank(user, newQuestion)
        storage.close()
        return newQuestion
