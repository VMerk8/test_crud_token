import binascii
from os import urandom

from django.contrib.auth.models import User
from django.db import models


class AuthToken(models.Model):

    key = models.CharField("Ключ", max_length=40, primary_key=True)

    user = models.OneToOneField(
        User, related_name='Токен_аутентификации',
        on_delete=models.CASCADE, verbose_name="Пользователи"
    )
    created = models.DateTimeField("Created", auto_now_add=True)

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токены"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(AuthToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(urandom(20)).decode()

    def __str__(self):
        return self.key
