from django.db import models


class BaseProfile(models.Model):
    class Role(models.TextChoices):
        """List of available values for 'role' field."""
        CUSTOMER = 'CS', 'Заказчик'
        FREELANCER = 'FL', 'Фрилансер'

    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Пользователь',
        unique=True,
    )
    name = models.CharField(
        verbose_name='Имя',
        help_text='Имя пользователя',
        max_length=50,
    )
    contact_info = models.TextField(
        verbose_name='Контактная информация',
        help_text='Контактная информация пользователя',
        blank=True,
        null=True,
    )
    experience = models.TextField(
        verbose_name='Опыт работы',
        help_text='Опыт работы пользователя',
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        help_text='Роль пользователя',
        max_length=9,
        blank=True,
        choices=Role.choices,
        default=Role.FREELANCER,
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['name']

    def get_absolute_url(self):
        return f'/{self.__name__.lower()}/{self.pk}/'

    def get_edit_url(self):
        return f'/{self.__name__.lower()}/{self.pk}/edit/'

    def get_delete_url(self):
        return f'/{self.__name__.lower()}/{self.pk}/delete/'

    def get_list_url(self):
        return f'/{self.__name__.lower()}/'

    def get_create_url(self):
        return f'/{self.__name__.lower()}/create/'

    def get_update_url(self):
        return f'/{self.__name__.lower()}/{self.pk}/update/'

    @property
    def is_freelancer(self):
        return self.role == self.Role.FREELANCER
