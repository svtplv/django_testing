import pytest
from django.conf import settings

from .lazy_constants import ANON_CLIENT, AUTHOR_CLIENT


@pytest.mark.django_db
class TestContent:

    def test_news_count(self, home_object_list):
        news_count = len(home_object_list)
        assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE

    def test_news_order(self, home_object_list):
        all_dates = [news.date for news in home_object_list]
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

    def test_comment_order(self, detail_url, comments, client):
        response = client.get(detail_url)
        news = response.context['news']
        all_comments = news.comment_set.all()
        assert all_comments[0].created < all_comments[1].created
