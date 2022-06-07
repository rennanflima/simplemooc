from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class HomeViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_template_used(self):
        response = self.client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'home.html')
