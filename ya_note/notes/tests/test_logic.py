from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note


User = get_user_model()


class TestCaseMixin(TestCase):
    TITLE = 'New title'
    TEXT = 'New text'
    SLUG = 'new_slug'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.url = reverse('notes:add')
        cls.redirect_url = reverse('notes:success')
        cls.login_url = reverse('users:login')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.form_data = {
            'title': cls.TITLE,
            'text': cls.TEXT,
            'slug': cls.SLUG
        }


class TestNoteCreation(TestCaseMixin):

    def test_user_can_create_note(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.redirect_url)
        self.assertEqual(Note.objects.count(), 1)
        self.form_data.update(author=self.author.id)
        new_note = Note.objects.last()
        self.assertDictContainsSubset(self.form_data, model_to_dict(new_note))

    def test_anonymous_user_cant_create_note(self):
        response = self.client.post(self.url, data=self.form_data)
        expected_url = f'{self.login_url}?next={self.url}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), 0)

    def test_not_unique_slug(self):
        note = Note.objects.create(
            title='Title',
            text='Text',
            slug='note-slug',
            author=self.author
        )
        self.form_data['slug'] = note.slug
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_empty_slug(self):
        self.form_data.pop('slug')
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.redirect_url)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.last()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)


class TestNoteEditAndDelete(TestCaseMixin):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.nonauthor = User.objects.create(username='Nonauthor')
        cls.nonauthor_auth_client = Client()
        cls.nonauthor_auth_client.force_login(cls.nonauthor)
        cls.note = Note.objects.create(
            title='Title',
            text='Text',
            slug='note-slug',
            author=cls.author
        )
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.del_url = reverse('notes:delete', args=(cls.note.slug,))

    def test_author_can_edit_note(self):
        response = self.auth_client.post(self.edit_url, self.form_data)
        self.assertRedirects(response, self.redirect_url)
        self.note.refresh_from_db()
        self.form_data.update(author=self.author.id)
        self.assertDictContainsSubset(self.form_data, model_to_dict(self.note))

    def test_other_user_cant_edit_note(self):
        response = self.nonauthor_auth_client.post(
            self.edit_url,
            self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertDictEqual(
            model_to_dict(self.note),
            model_to_dict(note_from_db)
        )

    def test_author_can_delete_note(self):
        response = self.auth_client.post(self.del_url)
        self.assertRedirects(response, self.redirect_url)
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cant_delete_note(self):
        response = self.nonauthor_auth_client.post(self.del_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
