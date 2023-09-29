from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.reader = User.objects.create(username='Reader')
        cls.note = Note.objects.create(
            title='Title',
            text='Text',
            slug='note-slug',
            author=cls.author
        )

    def test_notes_list_for_different_users(self):
        users_note_in_list = (
            (self.author, True),
            (self.reader, False)
        )
        url = reverse('notes:list')
        for user, note_in_list in users_note_in_list:
            with self.subTest(user=user, note_in_list=note_in_list):
                self.client.force_login(user)
                response = self.client.get(url)
                object_list = response.context['object_list']
                self.assertEqual(note_in_list, self.note in object_list)

    def test_pages_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                self.client.force_login(self.author)
                response = self.client.get(url)
                self.assertIn('form', response.context)
