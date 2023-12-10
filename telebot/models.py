from django.db import models


class Store(models.Model):
    store_name = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.store_name


class User(models.Model):
    user_name = models.CharField(max_length=100, unique=True)
    telegram_id = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.user_name


class Trek(models.Model):
    start = models.ForeignKey(to=Store, related_name='start', on_delete=models.CASCADE)
    finish = models.ForeignKey(to=Store, related_name='finish', on_delete=models.CASCADE)
    trek = models.FloatField()

    class Meta:
        verbose_name = 'Путь'
        verbose_name_plural = 'Пути'

    def __str__(self):
        return f'{self.start} - {self.finish} = {self.trek} km'


class Order(models.Model):
    store = models.OneToOneField(to=Store, related_name='store', on_delete=models.CASCADE, unique=True)
    user = models.ForeignKey(to=User, related_name='user', on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    massa = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.store}  {self.data}'


class CompletedOrder(models.Model):
    store = models.OneToOneField(to=Store, related_name='completed_store', on_delete=models.CASCADE, unique=True)
    user = models.ForeignKey(to=User, related_name='order_user', on_delete=models.CASCADE)
    data = models.DateTimeField()
    massa = models.PositiveIntegerField(default=0)
    completed_user = models.ForeignKey(to=User, related_name='completed_user', on_delete=models.CASCADE)
    completed_data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Выполненый заказ'
        verbose_name_plural = 'Выполненые заказы'

    def __str__(self):
        return f'{self.store}  {self.data} {self.completed_user}'
