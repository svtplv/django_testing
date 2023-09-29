from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from .lazy_constants import (
    AUTHOR_CLIENT,
    DELETE_COMMENT_URL,
    DETAIL_URL,
    EDIT_COMMENT_URL,
    HOME_URL,
    LOGIN_URL,
    LOGOUT_URL,
    READER_CLIENT,
    SIGNUP_URL
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    (HOME_URL, DETAIL_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL)
)
def test_pages_availability(client, url):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'url',
    (EDIT_COMMENT_URL, DELETE_COMMENT_URL)
)
class TestEditAndDeleteCommentAvailability:
    @pytest.mark.parametrize(
        'param_client, exp_status',
        (
            (AUTHOR_CLIENT, HTTPStatus.OK),
            (READER_CLIENT, HTTPStatus.NOT_FOUND)
        )
    )
    def test_availability_for_auth_client(
        self,
        param_client,
        url,
        exp_status,
        comment
    ):
        response = param_client.get(url)
        assert response.status_code == exp_status

    @pytest.mark.django_db
    def test_redirect_for_anonymous_client(self, url, client, login_url):
        expected_url = f'{login_url}?next={url}'
        response = client.get(url)
        assertRedirects(response, expected_url)
