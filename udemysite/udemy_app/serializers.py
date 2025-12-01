from django.contrib.auth import authenticate

from .models import (UserProfile,Category,SubCategory,Course,Lesson,
                     Assignment,Exam,Question,Option,Certificate,Review)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class UserProfileRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'role',]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

class UserProfileLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role']



class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']



class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id','sub_category_name']



class   CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','course_name','price','description', 'course_image']



class SubCategoryDetailSerializer(serializers.ModelSerializer):
    subcategory_courses = CourseListSerializer(many=True, read_only=True)
    class Meta:
        model = SubCategory
        fields = ['sub_category_name','subcategory_courses']



class CategoryDetailSerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['category_name','sub_categories']



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id','title','video_url','content']




class AssignmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id','title',]




class AssignmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id','title','description','due_date']




class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option_name','option_type']



class QuestionSerializer(serializers.ModelSerializer):
    options_question = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['question_name','passing_score','options_question']


class CourseExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name',]



class ExamListSerializer(serializers.ModelSerializer):
    exams_course = CourseExamSerializer(many=True, read_only=True)
    class Meta:
        model = Exam
        fields = ['id','title','exams_course']

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'




class ExamDetailSerializer(serializers.ModelSerializer):
    course = CourseExamSerializer(read_only=True)
    questions_exam = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = [ 'title', 'duration', 'course', 'questions_exam']


class CertificateSerializer(serializers.ModelSerializer):
    student = UserProfileSerializer()

    class Meta:
        model = Certificate
        fields = ['course','student','issued_at','certificate']



class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Review
        fields = ['user','rating','comment','created_date']


class CourseDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y')
    updated_at = serializers.DateTimeField(format='%d-%m-%Y')
    reviews_course = ReviewSerializer(many=True, read_only=True)
    lessons_course = LessonSerializer(many=True, read_only=True)
    created_by = UserProfileSerializer()
    get_avg_rating = serializers.SerializerMethodField()      # имя поля совпадает с полем в fields
    get_count_people = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'course_name', 'description', 'level', 'price', 'created_at', 'updated_at', 'course_image',
            'lessons_course', 'created_by', 'reviews_course', 'get_avg_rating', 'get_count_people'
        ]

    def get_get_avg_rating(self, obj):       # метод должен называться get_<field_name>
        return obj.get_avg_rating()

    def get_get_count_people(self, obj):
        return obj.get_count_people()
