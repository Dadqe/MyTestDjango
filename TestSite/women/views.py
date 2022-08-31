from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # Если используем стандартную форму регистрации от Django и Авторизации
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from typing import Any, Dict, Optional
from .forms import *
from .models import *
from .utils import *


class WomenHome(DataMixin, ListView):
    # "Фактически эта строчка выбирает все записи из таблицы и пытается отобразить их в виде списка. При этом класс ListView по умолчанию использует следующий шаблон <имя приложения>/<имя модели>_list.html. Он будет искать по этому маршруту в нашем случае это women/women_list.html мы пока не прописываем, оставляем так"
    model = Women 
    template_name: str = "women/index.html"
    context_object_name = 'posts'
    
    # Функция которая формирует и динамический и статический контент, что б передать в шаблон template (В нашем случае мы это передаём из-за menu). т.к. в extra_context передавать можно только статические неизменяемые данные (списки нельзя) только неизменяемые значения
    def get_context_data(self, *, object_list=None, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))
    
    # Данным методом регулирую посты. Прошу показать только те посты, которые опубликованы.
    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')

def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'}) # Используется, когда сделан tag для меню

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name: str = 'women/addpage.html'
    success_url = reverse_lazy('home') # Что б после удачного добавления статьи нас перенаправляло на домашнюю страницу
    # login_url = '/admin/'
    login_url = reverse_lazy('home') # если не залогинен, будет отправлять на домашнюю страницу. Что б избавить от путанницы себя, пускай на админку перенаправляет
    raise_exception = True # Будет выдавать ошибку 403 незарегистрированным пользователям. И отррабатывает поверх переадресации
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name: str = 'women/post.html'
    slug_url_kwarg: str = 'post_slug'
    context_object_name: Optional[str] = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'], cat_selected=context['post'].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty: bool = False
    
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name: str = 'women/register.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self):
        '''Метод срабатывает при удачной авторизации и перенапрявляет нас по указанной ссылке'''
        # Используем или этот метод или объявляем глобальную переменную в <Name_site>/settings.py LOGIN_REDIRECT_URL = '/'
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')