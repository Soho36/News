from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
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
from django.core.mail import send_mail
from django.db.models.signals import post_save
from bs4 import BeautifulSoup


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


@permission_required('app.add_news', raise_exception=True)
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            new_post = form.save()      # Save the new post
            category = new_post.category    # Get the category of the new post
            subscriptions = Subscription.objects.filter(category=category)
            recipient_list = [subscription.user.email for subscription in subscriptions]
            soup = BeautifulSoup(new_post.description, 'html.parser')
            plain_text = soup.get_text()
            post_excerpt = ' '.join(plain_text.split()[:5]) + '...'

            send_mail(
                subject=f'New post in {category.name}',
                message=f'A new post has been added to the {category.name} category!\n{post_excerpt}',
                from_email='viskey7@yandex.com',
                recipient_list=recipient_list,
            )
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
    # latest_post = News.objects.filter(category=category).latest('created_at')
    subscription, created = Subscription.objects.get_or_create(user=request.user, category=category)
    if created:
        messages.success(request, f'You have successfully subscribed to the {category.name} category!')

    else:
        messages.info(request, f'You are already subscribed to the {category.name} category.')
    return redirect('news_by_category', category_name=category.name)  # Redirect to the category detail page
