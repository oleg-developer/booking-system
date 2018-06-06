import hashlib
import unicodedata

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

__all__ = [
    'User'
]


class UserManager(BaseUserManager):
    use_in_migrations = True

    @staticmethod
    def normalize_username(username):
        return unicodedata.normalize('NFKC', force_text(username))

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        username = self.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User
    """
    username = models.CharField(verbose_name=_('username'), unique=True,
                                max_length=32)
    email = models.EmailField(verbose_name=_('email'), null=True, blank=True)
    is_staff = models.BooleanField(_('is staff'), default=False, help_text=_(
        'Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(verbose_name=_('date joined'),
                                       auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """
        Get full name
        :return: full name or username
        """
        try:
            return self.chief.full_name
        except ObjectDoesNotExist:
            pass

        try:
            return self.staff.full_name
        except ObjectDoesNotExist:
            pass

        return self.username

    def get_short_name(self):
        """
        Get short name
        :return: first name or email
        """
        # return self.first_name if self.first_name else self.email
        return self.username

    def get_registration_token(self):
        """
        Generating a registration token
        :return: 
        """
        token_str = 'SaltString{id}{username}{date}'.format(
            id=self.id,
            username=self.username,
            date=self.date_joined.timestamp()
        )
        hash_obj = hashlib.sha256(token_str.encode('utf-8'))
        return hash_obj.hexdigest()

    def get_recovery_token(self):
        """
        Generating a token for password recovery
        :return: 
        """
        token_str = 'recoverSalt{username}{date}{id}'.format(
            id=self.id,
            username=self.username,
            date=self.date_joined.timestamp()
        )
        hash_obj = hashlib.sha256(token_str.encode('utf-8'))
        return hash_obj.hexdigest()

    def get_hotel(self):
        """
        Geting hotel owner / employee
        :return: 
        """
        try:
            # if chief
            return self.chief.hotel
        except ObjectDoesNotExist:
            pass
        try:
            # if staff
            return self.staff.chief.hotel
        except ObjectDoesNotExist:
            pass
        return None
