from django_filters import FilterSet
from .models import Course

class CourseFilter(FilterSet):
    class Meta:
        model = Course
        fields = {'course_name': ['exact'],
                  'price': ['gt', 'lt', 'gte', 'lte'],
                  'description': ["exact"],
                  }

