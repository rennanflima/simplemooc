from django.test import TestCase

from model_mommy import mommy

from simplemooc.courses.models import Course


class CourseManagerTest(TestCase):

    def setUp(self):
        self.courses_django = mommy.make(Course, name='Python na Web com Django', _quantity=5)
        self.courses_dev = mommy.make(Course, name='Python para Devs', _quantity=10)

    def tearDown(self):
        Course.objects.all().delete()

    def test_course_search(self):
        self.assertEqual(Course.objects.search('django').count(), 5)
        self.assertEqual(Course.objects.search('devs').count(), 10)
        self.assertEqual(Course.objects.search('python').count(), 15)
