from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, View
from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Category, Subscription
from .filters import NewsFilter
from .forms import NewsForm, SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.contrib import messages
from allauth.account.views import LoginView, SignupView
from datetime import datetime
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.http.response import HttpResponse
from django.utils import timezone
from rest_framework import viewsets
from .serializers import NewsSerializer, CategorySerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def signup(request):
    print("User is already registered.")
    if request.user.is_authenticated:

        messages.info(request, "You are already registered.")
        return redirect('/news')

    else:
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

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('news_list')    # Redirect back to the news list page


class NewsDetail(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj


class NewsByCategory(ListView):
    template_name = 'news_by_category.html'
    context_object_name = 'news_items'

    def get_queryset(self):
        # Retrieve the category by slug instead of name
        self.category = get_object_or_404(Category, name=self.kwargs['category_name'])
        return News.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the category object to the context
        context['category'] = self.category
        return context


@permission_required('app.add_news', raise_exception=True)
def create_news(request):
    today = timezone.now().date()
    start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_of_day = timezone.make_aware(datetime.combine(today, datetime.max.time()))

    user_posts_today = News.objects.filter(
        author=request.user,
        published_date__range=(start_of_day, end_of_day)
    ).count()

    max_posts_per_day = 5   # Restrict users from posting news larger than this number

    if user_posts_today >= max_posts_per_day:
        messages.error(request, 'You have reached your daily limit for creating news posts.')
        return redirect('/news')

    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)  # Save the new post
            new_post.author = request.user  # Automatically set the author to the current logged-in user
            new_post.save()
            messages.success(request, 'News post created and subscribers notified.')

            return redirect('/news')
    else:
        form = NewsForm

    return render(request, 'news_form.html', {'form': form})


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('app.change_news',)
    form_class = NewsForm
    model = News
    template_name = 'news_form.html'
    success_url = reverse_lazy('news_list')
    login_url = '/login/'  # URL to redirect to for login
    redirect_field_name = 'next'  # Field name for redirecting back to the original page after login


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('app.change_news',)
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    login_url = '/login/'  # URL to redirect to for login


@login_required
def get_author(request):

    premium_group = Group.objects.get(name='authors')

    if premium_group in request.user.groups.all():
        messages.info(request, "You are already an author!")
    else:
        request.user.groups.add(premium_group)
        messages.success(request, "Congratulations! You are now an author!")

    return redirect('/news')    # main page URL pattern


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already signed in!")
            return redirect('/news')
        return super().dispatch(request, *args, **kwargs)


class CustomSignupView(SignupView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already signed up!")
            return redirect('/news')  # Replace 'home' with the URL of your main page
        return super().dispatch(request, *args, **kwargs)


@login_required
def subscribe_to_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    subscription, created = Subscription.objects.get_or_create(user=request.user, category=category)
    if created:
        messages.success(request, f'You have successfully subscribed to the {category.name} category!')

    else:
        messages.info(request, f'You are already subscribed to the {category.name} category.')
    return redirect('news_by_category', category_name=category.name)  # Redirect to the category detail page


class Index(View):
    def get(self, request):
        string = _('Hello world! This is the index page!')

        return HttpResponse(string)
