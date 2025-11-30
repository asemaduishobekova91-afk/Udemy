from django.urls import path,include
from .views import (UserProfileViewSet, LessonViewSet, AssignmentListAPIView,AssignmentDetailAPIView, ExamListAPIView,ExamDetailAPIView,
                    QuestionViewSet, OptionViewSet, CertificateViewSet,ReviewViewSet, CategoryListAPIView,
                    CategoryDetailAPIView,SubCategoryListAPIView,SubCategoryDetailAPIView,CourseListAPIView,
                    CourseDetailAPIView,ExamCreateAPIView)

from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register(r'userprofile',UserProfileViewSet)
router.register(r'lesson',LessonViewSet)
router.register(r'question',QuestionViewSet)
router.register(r'option',OptionViewSet)
router.register(r'certificate',CertificateViewSet)
router.register(r'review',ReviewViewSet)




urlpatterns = [
    path('',include(router.urls)),
    path('category/',CategoryListAPIView.as_view(),name='category-list'),
    path('category/<int:pk>/',CategoryDetailAPIView.as_view(),name='category-detail'),
    path('subcategory/',SubCategoryListAPIView.as_view(),name='subcategory-list'),
    path('subcategory/<int:pk>/',SubCategoryDetailAPIView.as_view(),name='subcategory-detail'),
    path('course/',CourseListAPIView.as_view(),name='course-list'),
    path('course/<int:pk>/',CourseDetailAPIView.as_view(),name='course-detail'),
    path('assignment/',AssignmentListAPIView.as_view(),name='assignment-list'),
    path('assignment/<int:pk>/',AssignmentDetailAPIView.as_view(),name='assignment-detail'),
    path('exam/',ExamListAPIView.as_view(),name='exam-list'),
    path('exam/<int:pk>/',ExamDetailAPIView.as_view(),name='exam-detail'),
    path('exam/create/',ExamCreateAPIView.as_view(),name='exam-create'),

]