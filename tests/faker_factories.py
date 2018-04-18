import factory
from factory import django
from faker import Factory as FakerFactory

from django.conf import settings
from django.contrib.auth import get_user_model

faker = FakerFactory.create(
    getattr(settings, 'FAKER_SETTINGS_LOCALE', 'en_GB'))


class FakeUserFactory(django.DjangoModelFactory):

    class Meta:
        model = get_user_model()

    username = factory.LazyAttribute(lambda x: faker.name())
