from faker import Factory as FakerFactory
from rest_framework.test import APITestCase
from rest_framework import status

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
from django.contrib.auth import get_user_model

from exo_messages.models import Message
from exo_messages.conf import settings

from .faker_factories import FakeUserFactory

faker = FakerFactory.create(
    getattr(settings, 'FAKER_SETTINGS_LOCALE', 'en_GB'))
User = get_user_model()


class ExoMessageTest(APITestCase):

    def test_user_messages_marked_as_read_after_login(self):
        # PREPARE DATA
        user = FakeUserFactory.create()
        user.set_password('123456')
        user.save()
        Message.objects.create_message(
            user=user,
            code=settings.EXO_MESSAGES_CH_CODE_VALIDATED_EMAIL,
            level=settings.EXO_MESSAGES_CH_SUCCESS,
            read_when_login=True,
        )
        self.assertEqual(Message.objects.filter_by_user(
            user).not_read().count(), 1)

        # DO ACTION
        self.client.login(username=user.uuid, password='123456')

        # ASSERTS
        self.assertFalse(Message.objects.filter_by_user(
            user).not_read().exists())

    def test_user_messages_not_marked_as_read_after_login(self):
        # PREPARE DATA
        user = FakeUserFactory.create()
        user.set_password('123456')
        user.save()
        Message.objects.create_message(
            user=user,
            code=settings.EXO_MESSAGES_CH_CODE_VALIDATED_EMAIL,
            level=settings.EXO_MESSAGES_CH_SUCCESS,
            read_when_login=False,
        )
        self.assertEqual(Message.objects.filter_by_user(
            user).not_read().count(), 1)

        # DO ACTION
        self.client.login(username=user.uuid, password='123456')

        # ASSERTS
        self.assertEqual(Message.objects.filter_by_user(
            user).not_read().count(), 1)

    def test_messages_api_close_message(self):
        # PREPARE DATA
        user = FakeUserFactory.create()
        user.set_password('123456')
        user.save()
        Message.objects.create_message(
            user=user,
            code=settings.EXO_MESSAGES_CH_CODE_VALIDATED_EMAIL,
            level=settings.EXO_MESSAGES_CH_SUCCESS,
            can_be_closed=True,
        )

        self.client.login(username=user.uuid, password='123456')
        pk = Message.objects.filter_by_user(user).last().pk
        url = reverse('internal-messages:message-close', kwargs={'pk': pk})

        # DO ACTION
        self.client.post(url)

        # ASSERTS
        self.assertFalse(Message.objects.filter_by_user(
            user).not_read().exists())

    def test_messages_api_create_message(self):
        # PREPARE DATA
        user = FakeUserFactory.create()
        user.set_password('123456')
        user.save()
        variables = {
            'counter': 10
        }
        data = {
            'user': str(user.uuid),
            'code': settings.EXO_MESSAGES_CH_CODE_VALIDATED_EMAIL,
            'level': settings.EXO_MESSAGES_CH_SUCCESS,
            'can_be_closed': True,
            'read_when_login': True,
            'variables': variables
        }

        self.client.login(username=user.uuid, password='123456')
        url = reverse('internal-messages:message-list')

        # DO ACTION
        response = self.client.post(url, data=data)

        # ASSERTS
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(Message.objects.all().count(), 1)

    def test_messages_api_do_not_close_message(self):
        # PREPARE DATA
        user = FakeUserFactory.create()
        user.set_password('123456')
        user.save()
        Message.objects.create_message(
            user=user,
            code=settings.EXO_MESSAGES_CH_CODE_VALIDATED_EMAIL,
            level=settings.EXO_MESSAGES_CH_SUCCESS,
            can_be_closed=False,
        )
        self.client.login(username=user.uuid, password='123456')
        pk = Message.objects.filter_by_user(user).last().pk
        url = reverse('internal-messages:message-close', kwargs={'pk': pk})

        # DO ACTION
        self.client.post(url)

        # ASSERTS
        self.assertEqual(Message.objects.filter_by_user(
            user).not_read().count(), 1)

    def test_create_updatable_message_without_existing_message(self):
        # PREPARE DATA
        user = FakeUserFactory.create()
        user.set_password('123456')
        user.save()

        # DO ACTION
        message, created = Message.objects.update_or_create_message(
            user=user,
            code=settings.EXO_MESSAGES_CH_CODE_VALIDATED_EMAIL,
            level=settings.EXO_MESSAGES_CH_SUCCESS,
        )

        # aSSERTIONS
        self.assertTrue(created)
        self.assertIsNotNone(message)

    def test_create_updatable_message_with_counter(self):
        # PREPARE DATA
        user = FakeUserFactory.create()
        user.set_password('123456')
        user.save()
        Message.objects.update_or_create_message(
            user=user,
            code=settings.EXO_MESSAGES_CH_CODE_VALIDATED_EMAIL,
            level=settings.EXO_MESSAGES_CH_SUCCESS,
            variables={'counter': 5},
        )

        # DO ACTION
        message, created = Message.objects.update_or_create_message(
            user=user,
            code=settings.EXO_MESSAGES_CH_CODE_VALIDATED_EMAIL,
            level=settings.EXO_MESSAGES_CH_SUCCESS,
            variables={'counter': 10},
        )

        # ASSERTIONS
        self.assertFalse(created)
        self.assertEqual(message.variables.get('counter'), 15)

    def test_update_message_with_multiple_readed_messages(self):
        # PREPARE DATA
        user = FakeUserFactory.create()
        user.set_password('123456')
        user.save()
        for _ in range(3):
            Message.objects.create_message(
                user=user,
                code=settings.EXO_MESSAGES_CH_CODE_VALIDATED_EMAIL,
                level=settings.EXO_MESSAGES_CH_SUCCESS,
                read_when_login=True,
                variables={'counter': faker.random_int()}
            )
        self.client.login(username=user.uuid, password='123456')

        Message.objects.update_or_create_message(
            user=user,
            code=settings.EXO_MESSAGES_CH_CODE_VALIDATED_EMAIL,
            level=settings.EXO_MESSAGES_CH_SUCCESS,
            variables={'counter': 5},
        )

        # DO ACTION
        message, created = Message.objects.update_or_create_message(
            user=user,
            code=settings.EXO_MESSAGES_CH_CODE_VALIDATED_EMAIL,
            level=settings.EXO_MESSAGES_CH_SUCCESS,
            variables={'counter': 10},
        )

        # ASSERTIONS
        self.assertFalse(created)
        self.assertEqual(message.variables.get('counter'), 15)
