from django.db.models import Manager

from .conf import settings
from .exceptions import ExoMessagesException
from .queryset import MessageQuerySet


class MessageManager(Manager):
    use_for_related_fields = True
    use_in_migrations = True
    queryset_class = MessageQuerySet

    def get_queryset(self):
        return self.queryset_class(
            self.model,
            using=self._db).filter(
                deleted=False).filter_by_user_active()

    def filter_by_user(self, user):
        return self.queryset_class(self.model, using=self._db).filter(
            deleted=False, user=user,
        )

    def create_message(self, user, code, level, *args, **kwargs):
        if code not in [_[0] for _ in settings.EXO_MESSAGES_CH_CODE]:
            raise ExoMessagesException('Invalid code')
        if level not in [_[0] for _ in settings.EXO_MESSAGES_CH_LEVEL]:
            raise ExoMessagesException('Invalid level')

        return self.create(
            user=user,
            code=code,
            level=level,
            can_be_closed=kwargs.get('can_be_closed', False),
            read_when_login=kwargs.get('read_when_login', False),
            variables=kwargs.get('variables', {}))

    def clear_messages(self, user, code, pk=None):
        messages = self.filter_by_user(user).filter_by_code(code)
        if pk:
            messages = messages.filter(variables__user_pk=pk)

        messages.delete()


class MessageAllManager(Manager):
    queryset_class = MessageQuerySet

    def get_queryset(self):
        return self.queryset_class(
            self.model,
            using=self._db,
        ).filter(deleted=False)

    def filter_by_user(self, user):
        return self.get_queryset().filter(user=user)
