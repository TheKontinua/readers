import json
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase

from mentapp.models import Chapter, Chapter_Loc, Question, Quiz, Quiz_Question, User, Volume


class TestEditQuizView(TestCase):

    # Sets up data that will be the same for each test method, need to be logged in as admin
    def setUp(self):
        self.credentials = {
            'email': 'a@a.com',
            'password': 'a',
        }
        User.objects.create_superuser(**self.credentials)
        self.client.post('/login/', self.credentials)
        return super().setUp()
    
    # Creates a quiz in the database with a a new Volume and Chapter.
    # Books, computer, internet and calculator all allowed or 
    # not allowed as signified by allowTools. All other
    # values are set to 1 with the exception of chapter_id
    # of the new chapter ("This is a makeQuiz test chapter").
    def makeQuiz(self, allowTools):
        volume = Volume.objects.create()

        chapter = Chapter.objects.create(
            chapter_id = "This is a makeQuiz test chapter",
            volume = volume,
            ordering = 1
        )

        return Quiz.objects.create(
            conceptual_difficulty = 1,
            book_allowed = allowTools,
            computer_allowed = allowTools,
            internet_allowed = allowTools,
            calculator_allowed = allowTools, 
            time_required_mins = 1, 
            volume = chapter.volume,
            chapter = chapter
        )
    
    # Posts data to edit given a quiz id and the data to post
    def postData(self, quizId, jsonData):
        return self.client.post("/edit_quiz/"+ str(quizId), jsonData, 
                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
    
    # Sets up data that is not expected to change across test methods
    @classmethod
    def setUpTestData(cls):
        pass

    def testViewUrl(self):
        quiz = self.makeQuiz(False)
        print("Test view")
        print(str(quiz.quiz_id))
        print("Test view")
        response = self.client.get("/edit_quiz/" + str(quiz.quiz_id))
        self.assertEqual(response.status_code, 200)

    def initializeJsonSave(self, allow_tools, question_ids, conceptual_difficulty, 
                           volume_id, chapter_id, time_required_minutes):
        jsonDict = dict()

        allow_tools_str = "true"
        if(allow_tools == False):
            allow_tools_str = ""
        
        jsonDict["command"] = "save"
        jsonDict["ids"] = json.dumps(question_ids)
        jsonDict["time_required_mins"] = str(time_required_minutes)
        jsonDict["label"] = "the name"
        jsonDict["conceptual_difficulty"] = str(conceptual_difficulty)
        jsonDict["calculator_allowed"] = allow_tools_str
        jsonDict["computer_allowed"] = allow_tools_str
        jsonDict["internet_allowed"] = allow_tools_str
        jsonDict["book_allowed"] = allow_tools_str
        jsonDict["volume"] = volume_id
        jsonDict["chapter"] = chapter_id

        data = dict()
        data["data"] = jsonDict
        return jsonDict

    def testViewSaveSetToolsTrue(self):
        quiz = self.makeQuiz(False)
        jsonData = self.initializeJsonSave(True, list(), 0, 
                                           Chapter.objects.all().first().volume.volume_id, 
                                           Chapter.objects.all().first().chapter_id, 0)       
        quiz_id = quiz.quiz_id
        self.postData(quiz_id, jsonData)
        response = self.postData(quiz_id, jsonData)
        self.assertEqual(response.status_code, 200)
        quiz = get_object_or_404(Quiz, quiz_id = quiz_id)
        self.assertEqual(quiz.calculator_allowed, True)
        self.assertEqual(quiz.book_allowed, True)
        self.assertEqual(quiz.computer_allowed, True)
        self.assertEqual(quiz.internet_allowed, True)

    def testViewSaveSetToolsFalse(self):
        quiz = self.makeQuiz(True)
        jsonData = self.initializeJsonSave(False, list(), 0, 
                                           Chapter.objects.all().first().volume.volume_id, 
                                           Chapter.objects.all().first().chapter_id, 0)
        quiz_id = quiz.quiz_id
        self.postData(quiz_id, jsonData)
        quiz = get_object_or_404(Quiz, quiz_id = quiz_id)
        self.assertEqual(quiz.calculator_allowed, False)
        self.assertEqual(quiz.book_allowed, False)
        self.assertEqual(quiz.computer_allowed, False)
        self.assertEqual(quiz.internet_allowed, False)

    def testViewSaveDifficulty(self):
        quiz = self.makeQuiz(True)
        
        previousDifficulty = quiz.conceptual_difficulty
        arbitraryDifficulty = 1000 + previousDifficulty
        jsonData = self.initializeJsonSave(False, list(), arbitraryDifficulty, 
                                           Chapter.objects.all().first().volume.volume_id, 
                                           Chapter.objects.all().first().chapter_id, 0)
        quiz_id = quiz.quiz_id
        self.postData(quiz_id, jsonData)
        quiz = get_object_or_404(Quiz, quiz_id = quiz_id)
        self.assertTrue(previousDifficulty != arbitraryDifficulty)
        self.assertTrue(arbitraryDifficulty == quiz.conceptual_difficulty)
    
    def testViewSaveTime(self):
        quiz = self.makeQuiz(True)
        
        previousTime = quiz.time_required_mins
        arbitraryTime = 1000 + previousTime
        jsonData = self.initializeJsonSave(False, list(), 0, 
                                           Chapter.objects.all().first().volume.volume_id, 
                                           Chapter.objects.all().first().chapter_id, arbitraryTime)
        quiz_id = quiz.quiz_id
        self.postData(quiz_id, jsonData)
        quiz = get_object_or_404(Quiz, quiz_id = quiz_id)
        self.assertTrue(previousTime != arbitraryTime)
        self.assertTrue(arbitraryTime == quiz.time_required_mins)
    
    def testViewSaveVolumeChapter(self):
        quiz = self.makeQuiz(True)
        newVolume = Volume.objects.create()
        newChapter = Chapter.objects.create(
            chapter_id = "This is a testViewSaveVolumeChapter test chapter",
            volume = newVolume,
            ordering = Chapter.objects.all().order_by('-ordering').first().ordering + 1
        )
        previousChapter = quiz.chapter
        previousVolume = quiz.volume
        jsonData = self.initializeJsonSave(False, list(), 0, 
                                           newVolume.volume_id, newChapter.chapter_id, 0)
        quiz_id = quiz.quiz_id
        self.postData(quiz_id, jsonData)
        quiz = get_object_or_404(Quiz, quiz_id = quiz_id)
        self.assertTrue(previousChapter != newChapter)
        self.assertTrue(previousVolume != newVolume)
        self.assertTrue(quiz.volume == newVolume)
        self.assertTrue(quiz.chapter == newChapter)

    def testViewRemoveQuestion(self):
        quiz = self.makeQuiz(True)
        user = User.objects.create()
        question = Question.objects.create(
            creator = user,
            chapter = Chapter.objects.all().first()
        )
        quizQuestion = Quiz_Question.objects.create(
            quiz = quiz,
            question = question,
            ordering = 0
        )

        jsonData = self.initializeJsonSave(False, list(), 0, 
                                        Chapter.objects.all().first().volume.volume_id, 
                                        Chapter.objects.all().first().chapter_id, 0)
        self.postData(quiz.quiz_id, jsonData)
        with self.assertRaises(Quiz_Question.DoesNotExist):
            Quiz_Question.objects.get(quiz = quizQuestion.quiz, question = quizQuestion.question)

    def testViewRemoveQuestionMiddle(self):
        quiz = self.makeQuiz(True)
        user = User.objects.create()
        quizQuestions = list()
        for i in range(3):
            question = Question.objects.create(
                creator = user,
                chapter = Chapter.objects.all().first()
            )
            quizQuestion = Quiz_Question.objects.create(
                quiz = quiz,
                question = question,
                ordering = i
            )
            quizQuestions.append(quizQuestion)
        ids = [quizQuestions[0].question.question_id, quizQuestions[2].question.question_id]
        jsonData = self.initializeJsonSave(False, ids, 0, 
                                        Chapter.objects.all().first().volume.volume_id, 
                                        Chapter.objects.all().first().chapter_id, 0)
        self.postData(quiz.quiz_id, jsonData)
        with self.assertRaises(Quiz_Question.DoesNotExist):
            Quiz_Question.objects.get(quiz = quizQuestions[1].quiz, question = quizQuestions[1].question)

        dbQuestion0 = get_object_or_404(Quiz_Question, quiz = quiz,
                                        question = quizQuestions[0].question_id)
        self.assertEqual(dbQuestion0.question, quizQuestions[0].question)

        dbQuestion2 = get_object_or_404(Quiz_Question, quiz = quiz,
                                        question = quizQuestions[2].question_id)
        
        self.assertEqual(dbQuestion2.question, quizQuestions[2].question)
        self.assertEqual(dbQuestion0.ordering, 0)
        self.assertEqual(dbQuestion2.ordering, 1)