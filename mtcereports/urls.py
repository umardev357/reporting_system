
from django.urls import path
from .views import CombinedMonthJobsView, CombinedMonthJobsExportView

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('myjobs/', views.MyJobsView.as_view(), name = 'my-jobs'),
    path('alljobs/', views.AllJobsView.as_view(), name = 'all-jobs'),
    #path('alljobs', views.JobTableView.as_view(), name = 'all-jobs'),
    path('jobstable/', views.JobTableView.as_view(), name = 'jobs-table'),
    path('job/<int:pk>', views.JobDetailView.as_view(), name = 'job-detail'),
    path('job/create/', views.JobCreate.as_view(), name='job-create'),
    path('job/<int:pk>/update/', views.JobUpdate.as_view(), name='job-update'),
    #path('job/<int:pk>/update/', views.JobUpdateView.as_view(), name='job-update'),
    path('job/<int:pk>/delete/', views.JobDelete.as_view(), name='job-delete'),
    path('monthcontainerlist/', views.MonthContainerListView.as_view(), name = 'monthcontainer-list'),
    path('allmonthcontainerlist/', views.AllMonthContainerListView.as_view(), name = 'all-monthcontainer-list'),
    path('combinedmonthcontainerlist/', views.CombinedMonthContainerListView.as_view(), name = 'combined-monthcontainer-list'),
    path('monthcontainer/create/', views.MonthContainerCreate.as_view(), name='monthcontainer-create'),
    path('monthcontainer/<int:pk>/', views.MonthContainerDetailView.as_view(), name = 'month-container'),
    path('mymonthcontainerlist/', views.MyMonthContainerListView.as_view(), name = 'my-monthcontainer-list'),
    #path('jobs/<int:year>/<int:month>/', views.MonthlyJobsView.as_view(), name='monthly-jobs'),
    path('combinedmonthjobs/<int:year>/<int:month>/', views.CombinedMonthJobsView.as_view(), name='combined-month-jobs'),
    #path('combined-month-jobs/export/<int:year>/<str:month>/', CombinedMonthJobsExportView.as_view(), name='combined-month-jobs-export'),
    path('combined-month-jobs/export/<int:year>/<month>/', CombinedMonthJobsExportView.as_view(), name='combined-month-jobs-export'),
    path('allmonthjobs/<int:year>/<int:month>/<str:author>/', views.AllMonthJobsView.as_view(), name='all-month-jobs'),
    path('mymonthjobs/<int:year>/<int:month>/', views.MyMonthJobsView.as_view(), name='my-month-jobs'),
    path('monthcontainer/<int:pk>/delete/', views.MonthContainerDelete.as_view(), name='monthcontainer-delete'),
]


