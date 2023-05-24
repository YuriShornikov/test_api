import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from model_bakery import baker

from demo.models import Message

@pytest.fixture#фикстура для замены повторяемого кода
def client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user('admin')

@pytest.fixture
def message_factory():
    def factory(*args, **kwargs):
        return baker.make(Message, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_api(client, user, message_factory):
    #Arrange - то, что мы достаем из бд и помещаем
    # client = APIClient()
    # User.objects.create_user('admin')
    messages = message_factory(_quantity=10)#создание 10 сообщений

    # Message.objects.create(user_id=user.id, text='text')#user_id=1

    #Act - наши действия с параметрами
    response = client.get('/messages/')

    #Assert  - проверка действий
    assert response.status_code == 200
    data = response.json()
    # assert len(data) == 1
    assert len(data) == len(messages)
    # assert data[0]['text'] == 'text'
    for i, m in enumerate(data):
        assert m['text'] == messages[i].text

# test_api()

@pytest.mark.django_db
def test_create_message(client, user):#подставляем клиента и пользователя

    count = Message.objects.count()
    response = client.post('/messages/', data={'user': user.id, 'text': 'test text'})#, format='json'
    assert response.status_code == 201
    assert Message.objects.count() == count + 1#увеличение количества сообщени после каждого запроса



