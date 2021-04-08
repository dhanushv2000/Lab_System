import django_filters
from django_filters import *
from .models import *

class studentfilter(django_filters.FilterSet):
    emails = CharFilter(field_name = 'email', lookup_expr = 'icontains')
    roll_number = CharFilter(field_name = 'roll_number', lookup_expr = 'icontains')
    class Meta:
        model = Student_link
        fields = ['section']
