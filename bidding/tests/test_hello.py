import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_hello():
    url = reverse('hello')  # Replace 'hello' with your actual URL name
    response = client.get(url)
    assert response.status_code == 200
    assert b'Hello, World!' in response.content