from django.db import models
from django.db.models import DecimalField

from users.base_model import BaseProfile


class FreelancerProfile(BaseProfile):
    pass


class CustomerProfile(BaseProfile):
    pass


class Order(models.Model):
    title = models.CharField(
        verbose_name='Заголовок',
        help_text='Заголовок заказа',
        max_length=100,
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание заказа',
    )
    created_at = models.DateTimeField(
        verbose_name='Создан',
        help_text='Дата создания заказа',
        auto_now_add=True,
    )
    price = DecimalField(
        verbose_name='Цена',
        help_text='Цена заказа',
        decimal_places=2,
        max_digits=10,
        default=0,
    )
    customer = models.ForeignKey(
        'users.CustomerProfile',
        on_delete=models.CASCADE,
        verbose_name='Заказчик',
        help_text='Заказчик',
    )
    freelancer = models.ForeignKey(
        'users.FreelancerProfile',
        on_delete=models.SET_NULL,
        verbose_name='Фрилансер',
        help_text='Фрилансер',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

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
