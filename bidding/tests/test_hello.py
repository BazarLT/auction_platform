from http import client
import pytest
from django.urls import reverse

@pytest.mark.django_db
@pytest.mark.django_db
def test_hello_view():
    url = reverse('hello')  # Replace 'hello' with your actual URL name
    response = client.get(url)
    assert response.status_code == 200
    assert b'Hello, World!' in response.content

@pytest.mark.django_db
def test_hello_view_not_found():
    url = reverse('non_existent_url')  # Replace with a non-existent URL name
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_hello_view_post_method():
    url = reverse('hello')  # Replace 'hello' with your actual URL name
    response = client.post(url)
    assert response.status_code == 405  # Method Not Allowed

@pytest.mark.django_db
def test_hello_view_with_query_params():
    url = reverse('hello')  # Replace 'hello' with your actual URL name
    response = client.get(url, {'name': 'Natali'})
    assert response.status_code == 200
    assert b'Hello, Natali!' in response.content