from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Category
from .filters import NewsFilter
from .forms import NewsForm, SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('news_list')
        else:
            return render(request, 'signup.html', {'form': form})  # Handle invalid form submission
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class NewsList(ListView):
    model = News
    ordering = ['-published_date']
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10     # number of entries per page

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'


class NewsByCategory(ListView):
    template_name = 'news_by_category.html'
    context_object_name = 'news_items'

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category_name'])
        return News.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/news')
    else:
        form = NewsForm

    return render(request, 'news_form.html', {'form': form})


class NewsUpdate(LoginRequiredMixin, UpdateView):
    form_class = NewsForm
    model = News
    template_name = 'news_form.html'
    success_url = reverse_lazy('news_list')
    login_url = '/login/'  # URL to redirect to for login
    redirect_field_name = 'next'  # Field name for redirecting back to the original page after login


class NewsDelete(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    login_url = '/login/'  # URL to redirect to for login
