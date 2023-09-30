import pytest
from django.conf import settings

from .lazy_constants import ANON_CLIENT, AUTHOR_CLIENT
from ..forms import CommentForm


@pytest.mark.django_db
class TestContent:

    def test_news_count(self, client, bulk_news, home_url):
        response = client.get(home_url)
        news_feed = response.context['object_list']
        news_count = len(news_feed)
        assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE

    def test_news_order(self, client, bulk_news, home_url):
        response = client.get(home_url)
        news_feed = response.context['object_list']
        all_dates = [news.date for news in news_feed]
        sorted_dates = sorted(all_dates, reverse=True)
        assert all_dates == sorted_dates

    @pytest.mark.parametrize(
        'param_client, form_availability',
        (
            (AUTHOR_CLIENT, True),
            (ANON_CLIENT, False)
        )
    )
    def test_form_availability(
        self,
        param_client,
        form_availability,
        detail_url
    ):
        response = param_client.get(detail_url)
        form_in_context = 'form' in response.context
        assert form_in_context == form_availability
        if form_in_context:
            assert isinstance(response.context['form'], CommentForm)

    def test_comment_order(self, detail_url, comments, client):
        response = client.get(detail_url)
        news = response.context['news']
        comment_dates = [comment.created for comment in news.comment_set.all()]
        sorted_comment_dates = sorted(comment_dates)
        assert comment_dates == sorted_comment_dates
