import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from demo.models import Message


@pytest.mark.django_db
def test_api():
    #Arrange - то, что мы достаем из бд и помещаем
    client = APIClient()
    User.objects.create_user('admin')
    Message.objects.create(user_id=1, text='text')

    #Act - наши действия с параметрами
    response = client.get('/messages/')

    #Assert  - проверка действий
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['text'] == 'text'

test_api()