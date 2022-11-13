from django.db import models
from django.core import validators 
from django.core.exceptions import ValidationError


class Bb(models.Model):
    KINDS = (
        ('Купля-продажа',(
            ('b', 'Куплю'),
            ('s','Продам'),
            )),
    ('Обмен',(
        ('с','Обменяю'),
    ))
)
    kind = models.CharField(max_length=1, choices=KINDS, default='s', verbose_name='Продам/Куплю')
    title = models.CharField(max_length=50, verbose_name='Товар',
                              validators=[validators.RegexValidator(regex='^.{4,}$')],
                              error_messages={'invalid': 'Неправильное название товара'}
                            )
    content = models.TextField(null=True, blank=True, verbose_name='Описание') 
    price = models.FloatField(null=True, blank=True, verbose_name='Цена') 
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models. PROTECT, verbose_name=' Рубрика')
    #Дополпнительное вычисляемое поле ( функциональное поле).
    def title_and_price(self):
        
        if self.price:
            return '%s (%.2f)' % (self.title, self.price)
        else:
            return self.title
    # Название для функционального поля
    title_and_price.short_description = 'Название и цена'

    """сделаем так, чтобы занесение описания продаваемого товара было 
    обязательным, и предотвратим ввод отрицательного значения цены. Вот код метода 
    clean (), который реализует всё это"""
    def clean(self):
        errors = {}
        if not self.content:
           errors['content'] = ValidationError('Укажите описание ' +\
                                                'продаваемого товара')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите ' +\
            'неотрицательное значение цены')
        if errors:
            raise ValidationError(errors)



    class Meta:
        verbose_name_plural = 'Объявления' 
        verbose_name = 'Объявление' 
        ordering = ['-published']


class Rubric (models .Model) :
    name = models. CharField (max_length=20, db_index=True, verbose_name='Название')
    def __str__ (self):
        return self.name 
    class Meta:
        verbose_name_plural = 'Рубрики' 
        verbose_name = 'Рубрика' 
        ordering = ['name']


