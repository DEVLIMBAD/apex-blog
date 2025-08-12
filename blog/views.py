from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from .models import Post
from .forms import PostForm, ContactForm
from django.urls import reverse_lazy
from .forms import ContactForm
from .models import ContactFormSubmission, AboutPage
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import ContactMessage


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(published=True)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_superuser  # Update with your logic if custom roles exist

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser
    
class AboutView(TemplateView):
    template_name = 'blog/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_page'] = AboutPage.objects.first()
        return context

class ContactView(FormView):  # Renamed from ContactMessage to follow Django conventions
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        message = form.save(commit=False)  # Save the form data to database
        message.save()  # This will save the form data to database

        # Send email notification to admin
        send_mail(
            subject=f'New Contact message from {message.name}',
            message=f"""
Name: {message.name}
Email: {message.email}
Message: {message.message}

View in admin: {self.request.build_absolute_uri(f'/admin/blog/contactmessage/{message.id}/change/')}
            """.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        return super().form_valid(form)

class ThanksView(TemplateView):
    template_name = 'blog/thanks.html'  

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'published']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_authenticated



@login_required
def toggle_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author or request.user.is_superuser:
        post.published = True
        post.save()
        return redirect('post_detail', pk=post.pk)
    return redirect('post_list')

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.user.is_superuser)
        if form.is_valid():
            # Set the author to current user before saving
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Needed if you have many-to-many relations
            return redirect('post_detail', pk=post.pk)  # Redirect to new post
    else:
        form = PostForm()
    
    return render(request, 'post_create.html', {'form': form})

def home(request):
    return render(request, 'blog/home.html')


