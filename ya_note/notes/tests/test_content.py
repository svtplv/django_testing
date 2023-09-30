from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Reader')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Title',
            text='Text',
            slug='note-slug',
            author=cls.author
        )

    def test_notes_list_for_different_users(self):
        users_note_in_list = (
            (self.author_client, self.author, True),
            (self.reader_client, self.reader, False)
        )
        url = reverse('notes:list')
        for user_client, username, note_in_list in users_note_in_list:
            with self.subTest(username=username, note_in_list=note_in_list):
                response = user_client.get(url)
                notes = response.context['object_list']
                self.assertEqual(note_in_list, self.note in notes)

    def test_pages_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
