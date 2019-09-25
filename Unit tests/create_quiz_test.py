#Known bug is that instructorStorage.dat must be deleted inbetween each
#iteratio of tests

import unittest
import os
from create_quiz import *

class TestCreate_Quiz(unittest.TestCase):

    def setUp(self):
        
        self.question1 = Question("a","Most expensive MTG card", ["Black Lotus" , "Underground Sea", "lightning Bolt"], 0)
        self.question2 = Question("b","Best color in MTG", ["White", "Red", "Black", "Blue", "Green"], 3)
        self.quizName = "Chuck"
        self.startTime = datetime.datetime(2019, 3,10)
        self.endTime = datetime.datetime(2019, 3, 19)
        self.attempts = 3
        self.choices =["a","b"]
        self.weight = 10
        self.students = {"Troy": "", "Nick": "", "Riley": "", "Steven": "", "Tinguri": ""}
        self.instructor =  "Dr.Brown"
        self.goodQuiz = Quiz("Chuck", datetime.datetime(2019, 3, 10), datetime.datetime(2019, 3, 19), 3, [self.question1, self.question2], 10, {"Troy": "", "Nick": "", "Riley": "", "Steven": "", "Tinguri": ""}, "Dr.Brown")
        self.testQuiz = Create_Quiz

        

    def test_createQuiz(self):
        storage = IStore("instructorStorage.dat")
        storage.addToBank(self.instructor, self.question1)
        storage.addToBank(self.instructor, self.question2)
        storage.close()
        newQuiz = self.testQuiz.createQuiz(self.quizName, self.startTime, self.endTime, self.attempts, self.choices, self.weight, self.students, self.instructor)
        self.assertEqual(newQuiz.getName(), self.goodQuiz.getName())
        self.assertEqual(newQuiz.getStartTime(), self.goodQuiz.getStartTime())
        self.assertEqual(newQuiz.getEndTime(), self.goodQuiz.getEndTime())
        self.assertEqual(newQuiz.getAttempts(), self.goodQuiz.getAttempts())
        self.assertEqual(newQuiz.getWeight(), self.goodQuiz.getWeight())
        self.assertEqual(newQuiz.getStudents(), self.goodQuiz.getStudents())
        self.assertEqual(newQuiz.getInstructor(), self.goodQuiz.getInstructor())

    def test_createQuizBad(self):
        with self.assertRaises(QuizLookupError):
            self.testQuiz.createQuiz(self.quizName, self.startTime, self.endTime, self.attempts, self.choices, self.weight, self.students, self.instructor)

    def test_modifyAttempts(self):
        self.testQuiz.modifyQuiz("Chuck", "A", "4",self.instructor)
        self.assertTrue(self.goodQuiz.getAttempts(), 4)

    def test_modifyWeight(self):
        self.testQuiz.modifyQuiz("Chuck", "W", "50",self.instructor)
        self.assertTrue(self.goodQuiz.getWeight(), 50)

    def test_loadQuiz(self):
        currentQuiz = self.testQuiz.loadQuiz("Chuck",self.instructor)
        self.assertEqual(currentQuiz.getName(), self.goodQuiz.getName())
        self.assertEqual(currentQuiz.getStartTime(), self.goodQuiz.getStartTime())
        self.assertEqual(currentQuiz.getEndTime(), self.goodQuiz.getEndTime())
        self.assertEqual(currentQuiz.getAttempts(), self.goodQuiz.getAttempts())
        self.assertEqual(currentQuiz.getWeight(), self.goodQuiz.getWeight())
        self.assertEqual(currentQuiz.getStudents(), self.goodQuiz.getStudents())
        self.assertEqual(currentQuiz.getInstructor(), self.goodQuiz.getInstructor())

    def test_loadQuizBad(self):
        with self.assertRaises(QuizLookupError):
            self.testQuiz.loadQuiz("Chunk",self.instructor)

    def test_modifyEndBad(self):
        with self.assertRaises(ValueError):
            self.testQuiz.modifyQuiz("Chuck", "E", "(2018,1,1)",self.instructor)

    def test_modifyEnd(self):
        self.testQuiz.modifyQuiz("Chuck", "E","2019 ,12 , 14",self.instructor)
        self.assertTrue(self.goodQuiz.getEndTime(), datetime.datetime(2019,12,14))

    def test_modifyAttemptsBad(self):
        with self.assertRaises(ValueError):
            self.testQuiz.modifyQuiz("Chuck", "A", "-3",self.instructor)

    def test_modifyWeightBad(self):
        with self.assertRaises(ValueError):
            self.testQuiz.modifyQuiz("Chuck", "W", "-10", self.instructor)

    def test_addToBank(self):
        try:
            self.testQuiz.addToBank("Question 1","How long have I spent on this assignment", ["4 hours", "10 hours", "15 hours"], 1, self.instructor)
            pass
        except:
            self.fail("The test failed")

    def test_addToBankError(self):
        with self.assertRaises(QuestionLookupError):
            self.testQuiz.addToBank("Question 1", "How long have I spent on this assignment", ["4 hours", "10 hours", "15 hours"], 1,self.instructor)

if __name__ == "__main__":
    storage = IStore("instructorStorage.dat")
    x = User("Dr.Brown", "13245", "instructor")
    if not storage.lookupUser("Dr.Brown"): 
        storage.addUser(x)
    
    storage.close()
    unittest.main()
    
