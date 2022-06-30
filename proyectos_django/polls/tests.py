import datetime

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Question
# Create your tests here.

class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns false with questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quien es el mejor profesor?", pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)


    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns False with questions whose pub_date is in the past"""
        time2 = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(question_text="¿Que otros leguajes quieres estudiar?", pub_date=time2)
        self.assertIs(past_question.was_published_recently(),False)

    def test_was_published_recently_with_present_questions(self):
        """was_published_recently returns true with questions whose pub_date is in the present"""
        time3 = timezone.now()
        present_question = Question(question_text="¿Quien va ganando?", pub_date=time3)
        self.assertIs(present_question.was_published_recently(),True)

    def test_question_without_choises(self):
        """If a quiestion is created without choises is deleted"""

        question = Question.objects.create(
            question_text="¿Quien es el mejor CD de Platzi?",
            pub_date=timezone.now(),
            choices=0)

        if question.choices <= 1:
            question.delete()

        questions_count = len(Question.objects.all())

        self.assertEqual(questions_count, 0)



def create_question(question_text, days):
    """
    Create question with the given question_text and the given number of days
    offset to now (negative for questions published  in the past and positive if questions are
    yet to be published
    :param question_text: given question text
    :param days: number of days offset to now, negative number if published in the past and positive if
    questions are yet to be published
    :return:
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)



class QuestionIndexView(TestCase):
    def test_no_questions(self):
        """If no question exist, an apropiated message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_future_questions(self):
        """Questions published in the future aren't displayed in the index page"""
        create_question("Future question",days=30)
        response= self.client.get(reverse("polls:index"))
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
    def test_past_questions(self):
        """Questions published in the past aren displayed in the index page"""
        question=create_question("Past question",days=-30)
        response= self.client.get(reverse("polls:index"))

        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions are displayed
        """
        past_question=create_question("Past question",days=-30)
        future_question = create_question("Future question", days=30)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )


    def test_two_past_questions(self):
        """The question index page may display multiple quiestions"""
        past_question1 = create_question("Past question1", days=-30)
        past_question2 = create_question("Past question2", days=-10)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question2,past_question1]
        )

    def test_two_future_questions(self):
        """The question index page won't display multiple quiestions from the future"""
        future_question1 = create_question("Future question1", days=30)
        future_question2 = create_question("Future question2", days=10)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        will return a 404 error not found
        """
        future_question1 = create_question("Future question1", days=30)
        url=reverse("polls:detail",args=(future_question1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        will display the question's text

        """
        past_question1 = create_question("Past question1", days=-30)
        url = reverse("polls:detail", args=(past_question1.id,))
        response = self.client.get(url)
        self.assertContains(response,past_question1.question_text)


class QuestionResultViewTest(TestCase):
    def test_result_no_questions(self):

        """If no question exist, a 404 not found message is displayed"""

        #response = self.client.get(reverse("polls:results",kwargs={'pk':1}))
        response = self.client.get(reverse("polls:results", args=(1,)))
        self.assertEqual(response.status_code,404)

    #toca corregir este tema porque esta fallando video 8 del curso intermedio de python
    def test_result_question_from_the_future(self):

        """If results from a question from the future is asked, a 404 not found message is displayed"""
        future_question=create_question("Future question",days=30)
        #response = self.client.get(reverse("polls:results",kwargs={'pk':future_question.id}))

        response = self.client.get(reverse("polls:results", args=(future_question.id,)))
        self.assertEqual(response.status_code,404)





    def test_result_question_from_the_past(self):

        """If results from a question from the past is asked,it will be displayed"""

        past_question=create_question("Past question",days=-30)
        #response = self.client.get(reverse("polls:results",kwargs={'pk':past_question.id}))
        response = self.client.get(reverse("polls:results", args=(past_question.id,)))
        self.assertContains(response,past_question.question_text)
