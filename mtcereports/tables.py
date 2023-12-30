import django_tables2 as tables
from .models import Job
from django_tables2.utils import A

class JobTable(tables.Table):
    class Meta:
        model = Job
        template_name = "django_tables2/bootstrap5.html"
        fields = ("date", "title", "region", "substation", "job_category", "job_description", "job_status", "personnel",  "author")
        orderable = False

    title = tables.LinkColumn("job-detail", args=[A("pk")], attrs={"class": "no-underline"})

    def render_personnel(self, value):
        return ', '.join([person.first_name for person in value.all()]) if value.exists() else ''

