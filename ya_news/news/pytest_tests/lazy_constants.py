import pytest

HOME_URL = pytest.lazy_fixture('home_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
EDIT_COMMENT_URL = pytest.lazy_fixture('edit_url')
DELETE_COMMENT_URL = pytest.lazy_fixture('delete_url')
ANON_CLIENT = pytest.lazy_fixture('client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
READER_CLIENT = pytest.lazy_fixture('admin_client')
