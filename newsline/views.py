from django.shortcuts import render, redirect, get_object_or_404
from .models import Articles, Category
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
import requests

def news_home(request):
    news = Articles.objects.order_by('-date')
    return render(request, 'news/news_home.html', {'news': news})

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article'

class NewsUpdateView(UpdateView):
    form_class = ArticlesForm
    model = Articles
    template_name = 'news/create.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

def is_admin(user):
    return user.is_authenticated and user.is_superuser


class NewsDeleteView(DeleteView):
    model = Articles
    success_url = '/news/'
    template_name = 'news/news-delete.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

@login_required
@user_passes_test(is_admin)
def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/news')
        else:
            error = 'Ошибка. Проверьте, правильны ли ваши данные.'

    form = ArticlesForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'news/create.html', data)

def category_articles(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    articles = Articles.objects.filter(category=category)
    context = {'category': category, 'articles': articles}
    return render(request, 'news/category_articles.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/news')
    else:
        form = UserCreationForm()
    return render(request, 'news/register.html', {'form': form})

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/news')
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль.')
    return render(request, 'news/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/news')

def like_article(request, article_id):
    article = get_object_or_404(Articles, pk=article_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'like':
            article.increase_likes()
        elif action == 'dislike':
            article.increase_dislikes()

    return redirect('/news')

def fetch_vk_text(request):
    # URL запроса к API Вконтакте
    url = 'https://api.vk.com/method/wall.get'

    # Параметры запроса
    params = {
        'domain': 'kei_ulstu',
        'owner_id': '-66721941',
        'count': 5,
        'access_token': 'vk1.a.nPPCykdbQkeOGx92LoMCW4fR48b31mSc_FA2C7rmwLzu3JvI6dXGKNH5NZYBqaAykJsbCcmIPmuPdwkQPEzAK1B1ZSriFtDl3bkUypJySWBsDSMYVgYXK8og-P9JGo1uqJdNyhwLeRjWUQ5-8lpc2RtZS05r60u2m9GYpiHjRPVJtcosWS8dLFP2KmMGgblxXgUpSeTHHVMsGaA_72IKjg',
        'filter': 'all',
        'v': '5.131',
    }

    # Выполнение HTTP-запроса к API Вконтакте
    response = requests.get(url, params=params)
    data = response.json()

    # Обработка полученных данных
    if 'response' in data:
        for post in data['response']['items']:
            if 'text' in post:
                text = post['text']
                title_end_index = text.find('.')  # Индекс первой точки
                if title_end_index == -1:
                    title_end_index = text.find('!')  # Индекс первого восклицательного знака
                if title_end_index != -1:
                    title = text[:title_end_index + 1]
                else:
                    title = post['text'][:140]
                anons = post['text'][:250]
                text_in_box = post['text']
                date = datetime.fromtimestamp(post['date'])

                # Создайте новую статью и сохраните ее в базе данных
                article = Articles.objects.create(
                    title=title,
                    anons=anons,
                    text_in_box=text_in_box,
                    date=date,
                    category=None  # Укажите категорию статьи, если требуется
                )
                article.save()

    return render(request, 'news/import.html')
