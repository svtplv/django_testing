from random import choice

import pytest
from pytest_django.asserts import assertFormError

from ..constants import COMMENT_TEXT, NEW_COMMENT_TEXT
from ..forms import BAD_WORDS, WARNING
from ..models import Comment
from .lazy_constants import ANON_CLIENT, AUTHOR_CLIENT, READER_CLIENT


@pytest.mark.django_db
class TestLogic:
    @pytest.mark.parametrize(
        'param_client, exp_increase',
        (
            (ANON_CLIENT, 0),
            (AUTHOR_CLIENT, 1)
        )
    )
    def test_creating_comment(
        self,
        param_client,
        exp_increase,
        detail_url,
        comment_form_data,
        author,
        news
    ):
        comment_start_count = Comment.objects.count()
        param_client.post(detail_url, comment_form_data)
        exp_comment_count = comment_start_count + exp_increase
        comment_count = Comment.objects.count()
        assert comment_count == exp_comment_count
        if exp_increase:
            comment = Comment.objects.all().last()
            assert comment.text == comment_form_data['text']
            assert comment.author == author
            assert comment.news == news

    def test_user_cant_use_bad_words(self, author_client, detail_url):
        comments_start_count = Comment.objects.count()
        bad_words_data = {
            'text': f'Какой-то текст, {choice(BAD_WORDS)}, еще текст'
        }
        response = author_client.post(detail_url, data=bad_words_data)
        assertFormError(
            response,
            form='form',
            field='text',
            errors=WARNING
        )
        comments_count = Comment.objects.count()
        assert comments_count == comments_start_count

    @pytest.mark.parametrize(
        'param_client, exp_decrease',
        (
            (READER_CLIENT, 0),
            (AUTHOR_CLIENT, 1)
        )
    )
    def test_deleting_comment(
        self,
        param_client,
        comment,
        delete_url,
        exp_decrease
    ):
        comment_start_count = Comment.objects.count()
        param_client.delete(delete_url)
        exp_comment_count = comment_start_count - exp_decrease
        comment_count = Comment.objects.count()
        assert comment_count == exp_comment_count

    @pytest.mark.parametrize(
        'param_client, exp_comment_text',
        (
            (READER_CLIENT, COMMENT_TEXT),
            (AUTHOR_CLIENT, NEW_COMMENT_TEXT)
        )
    )
    def test_editing_comment(
        self,
        param_client,
        comment,
        edit_url,
        upd_comment_form_data,
        exp_comment_text,
        news,
        author
    ):
        param_client.post(edit_url, data=upd_comment_form_data)
        comment.refresh_from_db()
        assert comment.text == exp_comment_text
        assert comment.author == author
        assert comment.news == news
