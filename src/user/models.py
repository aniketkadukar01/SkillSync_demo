from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.models import BaseModel, Choice
from django.core.validators import MinLengthValidator
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.

class User(AbstractUser, BaseModel):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        blank=True,
        null=True,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)
    type = models.ForeignKey(
        Choice,
        on_delete=models.DO_NOTHING,
        related_name='users',
        limit_choices_to={'choice_type': 'user'},
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        unique=True,
        validators=[MinLengthValidator(10)],
        error_messages={
            'min_length': 'Phone number must be exactly 10 characters.',
            'max_length': 'Phone number must be exactly 10 characters.',
            'unique': 'A user with that phone number already exists.',
        },
    )
    status = models.ForeignKey(
        Choice,
        on_delete=models.DO_NOTHING,
        related_name='users_status',
        limit_choices_to={'choice_type': 'status'},
        blank=True,
        null=True,
    )
    image = models.ImageField(blank=True, null=True, upload_to='media/user_pictures',)
    gender = models.ForeignKey(
        Choice,
        on_delete=models.DO_NOTHING,
        related_name='users_gender',
        limit_choices_to={'choice_type': 'gender'},
        blank=True,
        null=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.email}"

    class Meta:
        db_table = 'users'
