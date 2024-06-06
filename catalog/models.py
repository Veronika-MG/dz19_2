from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    """ Модель для категории """
    name = models.CharField(max_length=100, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    """
    Модель для продукта относящегося к категории по ключу ForeignKey.
    """
    name = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='product/', **NULLABLE)
    # category = models.CharField(max_length=100, verbose_name='Категория')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', help_text='Выберите категорию')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    date_of_creation = models.DateField(auto_now_add=False, verbose_name='Дата изготовления', **NULLABLE, help_text='В формате "дд.мм.гггг"')
    last_modified_date = models.DateField(**NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    is_published = models.BooleanField(default=False, verbose_name='опубликовано')

    def __str__(self):
        return f'{self.name}: {self.price}  ({self.category})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('category',)
        permissions = [
            ('can_publish', 'Право доступа для публикации')
        ]

class Version(models.Model):
    """ Модель для версии продукта """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    number = models.PositiveIntegerField(verbose_name='номер версии')
    name = models.CharField(max_length=150, verbose_name='название версии')
    current_version = models.BooleanField(default=True, verbose_name='признак текущей версии')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
