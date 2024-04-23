from django.db import models

NULLABLE = {'blank': True, 'null': True}

class Address(models.Model):
    title = models.CharField(max_length=150, verbose_name='название магазина')
    location = models.TextField(verbose_name='местоположение')
    image = models.ImageField(upload_to='address/', **NULLABLE)
    date_of_creation = models.DateField(auto_now_add=False, verbose_name='Дата создания', **NULLABLE, help_text='В формате "дд.мм.гггг"')

    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)



    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'адрес'
        verbose_name_plural = 'адреса'
        ordering = ['-date_of_creation', 'title']
