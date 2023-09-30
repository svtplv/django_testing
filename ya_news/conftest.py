import pytest
from datetime import timedelta

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from news.constants import COMMENT_TEXT, NEW_COMMENT_TEXT
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Title',
        text='Text',
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Comment text'
    )
    return comment


@pytest.fixture
def comments(news, author):
    now = timezone.now()
    for index in range(5):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Comment text {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return Comment.objects.all()


@pytest.fixture
def bulk_news():
    today = timezone.now()
    all_news = [
        News(
            title=f'News {index}',
            text='Text.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    bulk_news = News.objects.bulk_create(all_news)
    return bulk_news


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def edit_url(news):
    return reverse('news:edit', args=(news.id, ))


@pytest.fixture
def delete_url(news):
    return reverse('news:delete', args=(news.id, ))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def comment_form_data():
    form_data = {'text': COMMENT_TEXT}
    return form_data


@pytest.fixture
def upd_comment_form_data():
    form_data = {'text': NEW_COMMENT_TEXT}
    return form_data
