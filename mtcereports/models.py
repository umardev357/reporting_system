from django.core.validators import MinValueValidator, MaxValueValidator

from django.urls import reverse
from django.db import models
from datetime import date

from django.contrib.auth.models import User

#permission definition
class CanExtractPermission(models.Model):
    class Meta:
        permissions = [
            ('can_extract', 'Can extract data'),
        ]
        
# Create your models here.

class Job(models.Model):
    """This is the Job model for a job that has been done."""
    title = models.TextField(max_length = 200)
    

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, null=True
        )

    date = models.DateField(null=True)

    REGIONS = (
        ('ae', 'Accra East'),
        ('aw', 'Accra West'),
        ('v', 'Volta'),
        ('ase', 'Ashanti East'),
        ('asw', 'Ashanti West'),
        ('ass', 'Ashanti South'),
        ('e', 'Eastern'),
        ('w', 'Western'),
        ('t', 'Tema'),
        ('c', 'Central'),
        ('po', 'Projects Office'),
        ('sta', 'Subtransmission Accra'),
        ('stk', 'Subtransmission Ashanti'),
    )

    region = models.CharField(
        max_length = 3,
        choices = REGIONS,
        #blank = True,
        help_text = 'Select region where job was done',
    )

    substation = models.ForeignKey(
        'Substation',
        on_delete = models.SET_NULL, null = True,
        help_text='Select substation where work was done'
        )

    job_description = models.TextField(
        max_length=500,
        help_text = 'Describe the work done in detail',
        )
    
    equipment = models.ForeignKey(
        'Equipment',
        on_delete = models.SET_NULL, null = True,
        help_text='Select equipment on which was done'
        )
    
    job_category = models.ForeignKey(
        'JobCategory',
        on_delete = models.SET_NULL, null = True,
        help_text='Select the category of job'
        )

    JOBSTATUS = (
        ('P', 'Pending'),
        ('C', 'Completed'),
    )
    
    job_status = models.CharField(
        max_length = 1,
        choices = JOBSTATUS,
        help_text = 'Select the status of the job'
    )

    personnel = models.ManyToManyField(
        'Personnel',
        #on_delete = models.SET_NULL, null = True,
        help_text='Select personnel involved in the job'
        )
    
    remarks = models.CharField(max_length = 500)

    def get_absolute_url(self):
        """Returns the url to access a detail record for a job."""
        return reverse('job-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object"""
        return self.title

class Substation(models.Model):
    """Model representing a substation"""
    name = models.CharField(max_length = 200,)
    
    station_code = models.CharField(max_length = 10,)

    region = models.CharField(
        max_length = 3,
        choices = Job.REGIONS,
        help_text = "Select region where station is found",
    )

    def __str__(self):
        """String for representing the Model object"""
        return self.name
    

class Equipment(models.Model):
    """Model representing the equipment worked on in the substation"""
    name = models.CharField(max_length = 200,)

    class Meta:
        verbose_name_plural = "Equipment"

    def __str__(self):
        """String for representing the Equipment object"""
        return self.name
        

class JobCategory(models.Model):
    """Model for representing the job category"""
    name = models.CharField(max_length = 100 )

    description = models.TextField(
        max_length = 500,
        help_text = 'Describe what this job category is about',
        )
    
    class Meta:
        verbose_name_plural = "Job Categories"

    def __str__(self):
        """String for representing the Job category object"""
        return self.name


class Personnel(models.Model):
    """Model representing a personnel."""
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    staff_number = models.PositiveIntegerField(validators=[MaxValueValidator(999999)])
   

    POSTS = (
        ('DIR', 'Director'),
        ('GM', 'General Manager'),
        ('MGR', 'Manager'),
        ('SUP', 'Supervisor'),
        ('ENG', 'Engineer'),
    )

    position = models.CharField(
        max_length = 3,
        choices = POSTS,
        help_text = "Select your position",
    )

    class Meta:
        ordering = ['last_name', 'first_name']

    class Meta:
        verbose_name_plural = "Personnel"

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('personnel-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name}, {self.position}'

class MonthContainer(models.Model):
    """Model representing a conatainer with jobs in a perticular month"""
    year_name = models.PositiveIntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2100)
        ],
        help_text = "Select year",
    )
    
    '''MONTH = (
        ('jan', 'January'),
        ('feb', 'February'),
        ('mar', 'March'),
        ('apr', 'April'),
        ('may', 'May'),
        ('jun', 'June'),
        ('jul', 'July'),
        ('aug', 'August'),
        ('sep', 'September'),
        ('oct', 'October'),
        ('nov', 'November'),
        ('dec', 'December'),
    )'''

    MONTH = (
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    )

    

    month_name = models.CharField(
        max_length = 15,
        choices = MONTH,
        help_text = "Select month",
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, null=True
        )
    
    class Meta:
        unique_together = ('year_name', 'month_name', 'author')
    
    class Meta:
        ordering = ['month_name', 'year_name']

    def __str__(self):
        """String for representing the Month Container object."""
        return f'{self.year_name}, {self.month_name}'
    
    '''def get_absolute_url(self):
       """Returns the url to access a particular container instance."""
       return reverse('month-container', args=[str(self.id)])'''
    
    def get_absolute_url(self):
        return reverse('all-month-jobs', args=[self.year_name, self.month_name, ])
