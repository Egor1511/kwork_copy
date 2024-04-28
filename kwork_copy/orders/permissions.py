from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if user.role == 'customer':
                if request.method in ['PATCH', 'PUT']:
                    if request.method == 'PATCH':
                        return obj.customer == user
                    return 'freelancer' not in request.data
                return True
            elif user.role == 'freelancer':
                if request.method in ['PATCH', 'PUT']:
                    return 'freelancer' in request.data
                return False
        return False
