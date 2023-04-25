from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField('Название', max_length=50)
    slug = models.SlugField(max_length=60, unique=True)
    description = models.TextField('Описание', blank=True, default='')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = 'Категории'

class Manufacturer(models.Model):
    name = models.CharField('Название', max_length=60)
    slug = models.SlugField(max_length=60, unique=True)
    description = models.TextField('Описание', blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Product(models.Model):
    name = models.CharField('Наименование', max_length=200)
    cost = models.PositiveIntegerField('Стоимость', default=0)
    description = models.TextField('Описание')
    in_stock = models.BooleanField('Наличие товара')
    quantity = models.PositiveIntegerField('Кол-во в наличии', default=0)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.SET_NULL,
        verbose_name='Производитель',
        null=True
    )
    date = models.DateTimeField('Дата поступления на продажу', default=timezone.now)
    orders_count = models.PositiveIntegerField('Кол-во заказов', default=0)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class ProductPhoto(models.Model):
    title = models.CharField('Название', max_length=50)
    photo = models.ImageField('Изображение', upload_to='shop/')
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE,
        related_name='photos'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фото товаров'
        verbose_name_plural = 'Фото товаров'

class RatingStar(models.Model):
    value = models.PositiveIntegerField('Значение', default=0)
    
    def __str__(self):
        return f'{self.value}'
    
    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звёзды рейтинга'

class Rating(models.Model):
    ip = models.CharField('IP-адрес', max_length=15)
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='rating',
        verbose_name='Товар'
    )
    star = models.ForeignKey(
        RatingStar,
        on_delete=models.CASCADE,
        verbose_name='Звезда', 
    )
    
    def __str__(self):
        return f'{self.star} - {self.product}'
    
    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

class Review(models.Model):
    nickname = models.CharField('Имя пользователя', max_length=100)
    email = models.EmailField()
    text = models.TextField('Отзыв')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='review',
    )
    quality_star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, related_name='quality')
    price_star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, related_name='price')

    def __str__(self):
        return f'{self.email} - {self.product}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'