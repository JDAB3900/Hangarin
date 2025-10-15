
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from Application.models import Task, Category, Priority, SubTask, Note
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

# Home page view (Task List)
class HomePageView(ListView):
    model = Task
    context_object_name = 'home'
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Totals across your domain models
        context['total_categories'] = Category.objects.count()
        context['total_priorities'] = Priority.objects.count()
        context['total_tasks'] = Task.objects.count()
        context['total_subtasks'] = SubTask.objects.count()
        context['total_notes'] = Note.objects.count()

        # Provide counts under names expected by the template
        context['categories_count'] = context['total_categories']
        context['priorities_count'] = context['total_priorities']
        context['tasks_count'] = context['total_tasks']
        context['subtasks_count'] = context['total_subtasks']

        # Year-to-date counts for models with created_at
        today = timezone.now().date()
        year = today.year
        context['tasks_created_this_year'] = Task.objects.filter(created_at__year=year).count()
        context['subtasks_created_this_year'] = SubTask.objects.filter(created_at__year=year).count()
        context['notes_created_this_year'] = Note.objects.filter(created_at__year=year).count()

        return context

# Category Views
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_ordering(self):
        allowed = ['name']
        sort_by = self.request.GET.get('sort_by')
        if sort_by in allowed:
            return sort_by
        return 'name'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        # Use effective ordering so dropdown selection reflects current state
        context['sort_by'] = self.get_ordering()
        return context

class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

# Priority Views
class PriorityListView(ListView):
    model = Priority
    template_name = 'priority_list.html'
    context_object_name = 'priorities'

    def get_ordering(self):
        allowed = ['name']
        sort_by = self.request.GET.get('sort_by')
        if sort_by in allowed:
            return sort_by
        return 'name'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        # Use effective ordering so dropdown selection reflects current state
        context['sort_by'] = self.get_ordering()
        return context


class PriorityCreateView(CreateView):
    model = Priority
    fields = ['name']
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')

class PriorityUpdateView(UpdateView):
    model = Priority
    fields = ['name']
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')

class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = 'priority_confirm_delete.html'
    success_url = reverse_lazy('priority-list')

# Task Views
class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_ordering(self):
        allowed = [
            'title',
            'status',
            'deadline',
            'priority__name',
            'category__name',
            'created_at',
            '-created_at',
        ]
        sort_by = self.request.GET.get('sort_by')
        if sort_by in allowed:
            return sort_by
        return 'category__name'

    def get_queryset(self):
        qs = super().get_queryset().select_related('priority', 'category')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(description__icontains=q)
                | Q(status__icontains=q)
                | Q(priority__name__icontains=q)
                | Q(category__name__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        # Use effective ordering so dropdown selection reflects current state
        context['sort_by'] = self.get_ordering()
        return context

class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description', 'status', 'deadline', 'priority', 'category']
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title', 'description', 'status', 'deadline', 'priority', 'category']
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

# SubTask Views
class SubTaskListView(ListView):
    model = SubTask
    template_name = 'subtask_list.html'
    context_object_name = 'subtasks'

    def get_ordering(self):
        allowed = [
            'task__title',
            'title',
            'status',
            'created_at',
            '-created_at',
        ]
        sort_by = self.request.GET.get('sort_by')
        if sort_by in allowed:
            return sort_by
        return '-created_at'

    def get_queryset(self):
        qs = super().get_queryset().select_related('task')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(status__icontains=q) | Q(task__title__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        # Use effective ordering so dropdown selection reflects current state
        context['sort_by'] = self.get_ordering()
        return context


class SubTaskCreateView(CreateView):
    model = SubTask
    fields = ['task', 'title', 'status']
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')

class SubTaskUpdateView(UpdateView):
    model = SubTask
    fields = ['task', 'title', 'status']
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')

class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = 'subtask_confirm_delete.html'
    success_url = reverse_lazy('subtask-list')

# Note Views
class NoteListView(ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'

    def get_ordering(self):
        allowed = [
            'task__title',
            'content',
            'created_at',
            '-created_at',
        ]
        sort_by = self.request.GET.get('sort_by')
        if sort_by in allowed:
            return sort_by
        return '-created_at'

    def get_queryset(self):
        qs = super().get_queryset().select_related('task')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(content__icontains=q) | Q(task__title__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        # Use effective ordering so dropdown selection reflects current state
        context['sort_by'] = self.get_ordering()
        return context


class NoteCreateView(CreateView):
    model = Note
    fields = ['task', 'content']
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')

class NoteUpdateView(UpdateView):
    model = Note
    fields = ['task', 'content']
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    success_url = reverse_lazy('note-list')