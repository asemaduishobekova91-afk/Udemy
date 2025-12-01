from rest_framework.permissions import BasePermission

class StudentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'student':
            return True
        else:
            return False

class TeacherPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'teacher':
            return True
        else:
            return False
