from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from simplemooc.courses.models import Course


# Create your tests here.
class ContactCourseViewTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name='Django', slug='django')
        self.url = reverse('courses:details', args=(self.course.slug,))

    def tearDown(self):
        self.course.delete()

    def test_contact_form_error(self):
        data = {'name': 'Fulano de Tal', 'email': '', 'message': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    def test_contact_form_success(self):
        data = {'name': 'Fulano de Tal', 'email': 'admin@admin.com', 'message': 'Oi'}
        response = self.client.post(self.url, data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].to, [settings.CONTACT_EMAIL])
        self.assertEquals(mail.outbox[0].subject, '[Django] Contato')
