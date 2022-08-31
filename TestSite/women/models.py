from django.db import models
from django.urls import reverse

class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории") # Category передано как строка. потому что модель(класс) Category обозначен после этого класса и интерпретатор не знает ещё о нём - будет ошибка not found
    
    def __str__(self) -> str:
        return f'{self.title}, {self.pk}'
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['time_create', 'title']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


# # Полезности
# сформировал стркутуры БД для эприложения women
# python manage.py makemigrations создал миграцию
# python manage.py sqlmigrate women 0001 посмотрел, какой sql-запрос будет происходить для создания БД данного вида
# python manage.py migrate произвожу миграцию, что б запрос произошёл и таблица создалась в БД (и там дополительно создаются дополнительные таблицы, вспомогательные, "файлы миграции для них заранее заготовлены фреймворком)

# Добавление записи в БД: (через консоль)
# Сначала зайти в интерактивный режим чего-то там:
# python manage.py shell
# from women.models import Women
# Women(title='Анджелина Джоли', content='Биография Анджелины Джоли'), создание объекта. Вернётся объект и его можно потом присвоить переменной через element = _ (В _ хранится последний вернувшийся элемент, как я понял)
# element.save() после этого элемент отправится в БД
# после этого можно снова написать element и там уже в конце покажет id этого элемента. До добавления в БД там будет находиться None
# Что б посмотреть sql-запрос, который был выполнен для добавления этой записи надо:
# from django.db import connection
# Далее обратимся к специальной коллекции queries:
# connection.queries
# Подобный метод называется ленивыми запросами
# Можно подобным образом сохранять
# w3 = Women()
# w3.title = 'Джулия Робертс'
# w3.content = 'Биография Джулии Робертс'
# w3.save()

# Можно сразу формировать данные и записывать их через статический объект класса модели, н-р Women.objects
# w4 = Women.objects.create(title='Ума Турман', content='Биография Ума Турман') # Можно и без присвоения данного кода какой-либо переменной