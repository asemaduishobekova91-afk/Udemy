from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'student'),
        ('teacher', 'teacher'),
        ('admin', 'admin'),
    )

    full_name = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=60, choices=ROLE_CHOICES, default='client')
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.username}'

class Category(models.Model):
    category_name = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=500)

    def __str__(self):
        return self.sub_category_name


class Course(models.Model):
    course_name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name='subcategory_courses')
    LevelChoices = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    )

    level = MultiSelectField(choices=LevelChoices, max_choices=3, max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='course_users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course_image = models.ImageField(upload_to='course_image/', blank=True, null=True)
    def str(self):
        return f'{self.course_name}'


    def get_avg_rating(self):
        reviews = self.reviews_course.all()
        if reviews.exists():
            return round(sum([i.rating for i in reviews]) / reviews.count(),1)
        return 0

    def get_count_people(self):
        return self.reviews_course.count()
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons_course')
    title = models.CharField(max_length=250)
    video_url = models.URLField(null=True, blank=True)
    content = models.TextField()
    def __str__(self):
        return f'{self.course.course_name}, {self.title}'



class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments_course')
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.title}'



class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams_course')
    title = models.CharField(max_length=250)
    duration = models.DurationField(help_text="Duration in minutes")
    def __str__(self):
        return f'{self.course.course_name}, {self.title}'



class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,related_name='questions_exam')
    question_name = models.CharField(max_length=400)
    passing_score = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    def __str__(self):
        return f'{self.question_name}'


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options_question')
    option_name = models.CharField(max_length=400)
    option_type = models.BooleanField()
    def __str__(self):
        return f'{self.option_name}'


class Certificate(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate = models.URLField()
    def __str__(self):
        return f'{self.course.course_name}, {self.student.username}'



class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='reviews_course')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.course.course_name}, {self.user.username}'