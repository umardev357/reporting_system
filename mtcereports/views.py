

from django.db.models import Max
from django_tables2.export.views import ExportMixin

from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.messages import get_messages

from django.db import IntegrityError

from datetime import datetime
from calendar import month_name
from django import forms
from django_tables2 import SingleTableView

from .tables import JobTable

from django.views import generic, View
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .models import Job, Personnel, Equipment, JobCategory, Substation, MonthContainer
# Create your views here.

@login_required
def index(request):
    """View function for the home page of the P&C maintenance report site"""

    # Generate count of some of the main objects
    num_jobs = Job.objects.all().count()

    # Pending jobs (job_status = 'p')
    num_jobs_pending = Job.objects.filter(job_status__exact='p').count()

    # Completed jobs (job_status = 'c')
    num_jobs_completed = Job.objects.filter(job_status__exact='c').count()

    # Generate count of some other objects such as substations
    num_substations = Substation.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_jobs': num_jobs,
        'num_jobs_pending': num_jobs_pending,
        'num_jobs_completed': num_jobs_completed,
        'num_substations': num_substations,
        'num_visits': num_visits,
    }
    #Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


#@permission_required('mtcereports.can_extract')
class AllJobsView(LoginRequiredMixin, SingleTableView, generic.ListView):
    permission_required = 'mtcereports.can_extract'
    # Or multiple permissions
    # *******permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!

    model = Job
    template_name = 'mtcereports/all_jobs.html'
    #paginate_by = 10

    def get_queryset(self):
        return (
            Job.objects.filter()
            #.filter(status__exact='o')
            .order_by('date')
        )
    
    table_class = JobTable
    
class MyJobsView(LoginRequiredMixin, SingleTableView, generic.ListView):

    model = Job
    template_name = 'mtcereports/my_jobs.html'
    #paginate_by = 10

    def get_queryset(self):
        return (
            Job.objects.filter(author = self.request.user)
            #.filter(status__exact='o')
            .order_by('date')
        )
    
    table_class = JobTable


class JobTableView(SingleTableView):
    model = Job
    table_class = JobTable
    template_name = 'mtcereports/jobs_table.html'

class JobDetailView(generic.DetailView):
    model = Job

class JobCreateForm(forms.ModelForm):
    personnel = forms.ModelMultipleChoiceField(
        queryset=Personnel.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    
    class Meta:
        model = Job
        exclude = ['author']
        widgets = {
                'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            }

'''class JobCreate(LoginRequiredMixin, CreateView):
    """View function for creating a new job"""
    #permission_required = 'catalog.can_mark_returned'

    model = Job
    form_class = JobCreateForm
    #fields = '__all__'
#PermissionRequiredMixin,
    
    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author to the logged-in user
        return super().form_valid(form)'''
    
class JobCreate(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobCreateForm
    template_name = 'mtcereports/job_form.html'  # Replace with your actual template name
    success_url = reverse_lazy('my-jobs')  # Replace with your actual job list view name

    def form_valid(self, form):
        form.instance.author = self.request.user

        # Check if the "Save and Add Another Entry" button was clicked
        if 'save_and_add_another' in self.request.POST:
            # Save the current entry and redirect the user back to the form for a new entry
            self.object = form.save()
            return redirect('job-create')
        else:
            # Save the current entry and redirect the user to the job list page
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['save_and_add_another'] = True  # This variable can be used in the template
        return context

class JobUpdate(LoginRequiredMixin, UpdateView):
    """View to allow a user update or edit a job already added"""
    #permission_required = 'catalog.can_mark_returned'
    model = Job
   # fields = '__all__'

    form_class = JobCreateForm
    template_name = 'mtcereports/job_update.html'  # Replace with your actual template name
    
    def get_success_url(self):
        return reverse('job-detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Job updated successfully!')
        return super().form_valid(form)



class JobDelete(LoginRequiredMixin, DeleteView):
    """View to allow a user delete a job already added"""
    #permission_required = 'catalog.can_mark_returned'
    model = Job
    #success_url = reverse_lazy('my-jobs')

    def get_success_url(self):
        return reverse('my-jobs')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Job successfully deleted.')
        return super().delete(request, *args, **kwargs)


class MonthContainerListView(LoginRequiredMixin, generic.ListView):

    model = MonthContainer
    template_name = 'mtcereports/monthcontainer_list.html'
    paginate_by = 12

    def get_queryset(self):
        return (
            MonthContainer.objects.filter()
            #.filter(status__exact='o')
            #.order_by('date')
        )
    
    #table_class = JobTable

class MyMonthContainerListView(LoginRequiredMixin, generic.ListView):

    model = MonthContainer
    template_name = 'mtcereports/my_monthcontainer_list.html'
    paginate_by = 12

    def get_queryset(self):
        return (
            MonthContainer.objects.filter(author = self.request.user)
            #.filter(status__exact='o')
            #.order_by('-month_name', '-year_name')
        )
    
class AllMonthContainerListView(LoginRequiredMixin, generic.ListView):

    model = MonthContainer
    template_name = 'mtcereports/all_monthcontainer_list.html'
    paginate_by = 12

    def get_queryset(self):
        return (
            MonthContainer.objects.filter()
            #.filter(status__exact='o')
            #.order_by('-month_name', '-year_name')
        )
    
'''class CombinedMonthContainerListView(LoginRequiredMixin, generic.ListView):

    model = MonthContainer
    template_name = 'mtcereports/combined_monthcontainer_list.html'
    paginate_by = 12

    def get_queryset(self):
        return (
            MonthContainer.objects.filter()
            #.filter(status__exact='o')
            #.order_by('-month_name', '-year_name')
        )'''



class CombinedMonthContainerListView(LoginRequiredMixin, generic.ListView):

    model = MonthContainer
    template_name = 'mtcereports/combined_monthcontainer_list.html'
    paginate_by = 12

    def get_queryset(self):
        # Get distinct month and year combinations without considering the author
        distinct_monthcontainers = (
            MonthContainer.objects
            .values('year_name', 'month_name')
            .annotate(max_id=Max('id'))
            .order_by()
        )

        # Retrieve the MonthContainer objects
        monthcontainer_list = MonthContainer.objects.filter(
            id__in=[container['max_id'] for container in distinct_monthcontainers]
        )

        return monthcontainer_list


class MonthContainerCreateForm(forms.ModelForm):
    class Meta:
        model = MonthContainer
        exclude = ['author']

class MonthContainerCreate(LoginRequiredMixin, CreateView):
    """View function for creating a new month job container"""
    #permission_required = 'mtcereports.can_add_monthjob'

    model = MonthContainer
    form_class = MonthContainerCreateForm
    success_url = reverse_lazy('my-monthcontainer-list')  # Redirect URL after successful form submission
    #template_name = 'monthcontainer_form.html'
    #fields = '__all__'
#PermissionRequiredMixin,
    
    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author to the logged-in user

        year = form.cleaned_data['year_name']
        month = form.cleaned_data['month_name']
        author = self.request.user

        try:
            # Check if a container already exists for the given month and year
            container = MonthContainer.objects.get(year_name=year, month_name=month, author=author)
            messages.error(self.request, 'A container for this month and year already exists. Please click the Monthly Reports to see folders that exist.')
            return self.form_invalid(form)
        except MonthContainer.DoesNotExist:
            # No existing container, proceed to create a new one
            messages.success(self.request, 'Container created successfully!')
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my-monthcontainer-list')


class MonthContainerDetailView(generic.DetailView):
    model = MonthContainer
#This is where you were. You were working on getting the month container jobs to behave like my jobs

class CombinedMonthJobsView(LoginRequiredMixin, ExportMixin, SingleTableView, generic.ListView):
    model = Job
    template_name = 'mtcereports/combined_month_jobs.html'
    context_object_name = 'job_list'
    paginate_by = 10
    table_class = JobTable
    export_name = 'combined_month_jobs'

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Job.objects.filter(date__year=year, date__month=month)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs['year']
        month = self.kwargs['month']
        name_of_month = month_name[int(month)]
        context['year'] = year
        context['month'] = name_of_month
        return context


import tablib

'''MONTH_MAPPING = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
    
}'''

class CombinedMonthJobsExportView(View):
    def get(self, request, year, month):
        jobs = Job.objects.filter(date__year=year, date__month=month)

        dataset = tablib.Dataset()
        dataset.headers = ['Title', 'Author', 'Date', 'Region', '...']

        for job in jobs:
            dataset.append([job.title, job.author.username, job.date, job.region, '...'])

        response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=combined_month_jobs_{year}_{month}.xlsx'

        return response




from django.shortcuts import get_object_or_404
    
class AllMonthJobsView(LoginRequiredMixin, SingleTableView, generic.ListView):
    model = Job
    template_name = 'mtcereports/all_month_jobs.html'
    context_object_name = 'job_list'
    paginate_by = 10
    table_class = JobTable

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        author_username = self.kwargs['author']
        monthcontainer = get_object_or_404(MonthContainer, year_name=year, month_name=month, author__username=author_username)
        return Job.objects.filter(date__year=year, date__month=month, author=monthcontainer.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs['year']
        month = self.kwargs['month']
        author_username = self.kwargs['author']
        monthcontainer = get_object_or_404(MonthContainer, year_name=year, month_name=month, author__username=author_username)
        name_of_month = month_name[int(month)]
        context['year'] = year
        context['month'] = name_of_month
        context['author'] = author_username
        context['monthcontainer'] = monthcontainer
        return context
 
    
class MyMonthJobsView(LoginRequiredMixin, SingleTableView, generic.ListView):
    model = Job
    template_name = 'mtcereports/my_month_jobs.html'
    context_object_name = 'job_list'
    paginate_by = 10
    

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Job.objects.filter(date__year=year, date__month=month, author = self.request.user)
    
    '''author = self.request.user'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs['year']
        month = self.kwargs['month']
        name_of_month = month_name[int(month)]
        context['year'] = year
        context['month'] = name_of_month
        return context    
    
    table_class = JobTable

class MonthContainerDelete(LoginRequiredMixin, DeleteView):
    """View to allow a user delete a job already added"""
    #permission_required = 'catalog.can_mark_returned'
    model = MonthContainer
    success_url = reverse_lazy('my-monthcontainer-list') 



