from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField('Название', max_length=50)
    slug = models.SlugField(max_length=60, unique=True)
    description = models.TextField('Описание', blank=True, default='')

    def __str__(self):
        return self.name

    def get_num_products(self):
        return self.products.count()
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = 'Категории'


class Manufacturer(models.Model):
    name = models.CharField('Название', max_length=60)
    slug = models.SlugField(max_length=60, unique=True)
    description = models.TextField('Описание', blank=True, default='')

    def __str__(self):
        return self.name

    def get_num_products(self):
        return self.products.count()

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Product(models.Model):
    name = models.CharField('Наименование', max_length=200)
    slug = models.SlugField('URL', max_length=200, default='')
    cost = models.PositiveIntegerField('Стоимость (руб.)', default=0)
    description = models.TextField('Краткое описание товара', blank=True)
    details = RichTextField('Полное описание товара', default='')
    in_stock = models.BooleanField('Наличие товара')
    quantity = models.PositiveIntegerField('Кол-во в наличии', default=0)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.SET_NULL,
        verbose_name='Производитель',
        null=True,
        related_name='products'
    )
    date = models.DateTimeField('Дата поступления на продажу', default=timezone.now)
    orders_count = models.PositiveIntegerField('Кол-во заказов', default=0)
    on_sale = models.BooleanField('Выставлено на продажу', default=False)

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_primary_photo(self):
        return self.photos.get(primary=True)
    
    def get_all_photos(self):
        return self.photos.all()

    def get_num_reviews(self):
        return self.review.count()
        
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class ProductPhoto(models.Model):
    photo = models.ImageField('Изображение', upload_to='shop/')
    primary = models.BooleanField(default=False)
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE,
        related_name='photos'
    )

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