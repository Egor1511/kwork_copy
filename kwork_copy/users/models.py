from users.base_model import BaseProfile


class FreelancerProfile(BaseProfile):

    class Meta:
        verbose_name = 'Фрилансер'
        verbose_name_plural = 'Фрилансеры'
        ordering = ['name']


class CustomerProfile(BaseProfile):

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'
        ordering = ['name']
