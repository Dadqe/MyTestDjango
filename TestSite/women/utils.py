from .models import *
from django.db.models import Count

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]

class DataMixin:
    paginate_by: int = 3    # Указываем, сколько постов отображать на каждой странцие этот атрибут будет применён ко всем дочерним классам отображения..которые наследуются от этого миксина
    
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('women'))
        # сделаю отображение ссылки на "добавить статью" только для зарегистрированных пользователей" Регистрация в админке позваоляет видеть всё.
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:  # type: ignore
            user_menu.pop(1)
        
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context