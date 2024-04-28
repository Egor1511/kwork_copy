from django.db import models
from django.db.models import DecimalField


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
        on_delete=models.CASCADE,
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
