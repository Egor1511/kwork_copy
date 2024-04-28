from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if hasattr(user, 'customerprofile'):
                if request.method in ['PATCH', 'PUT']:
                    if request.method == 'PATCH':
                        return obj.customer == user
                    return 'freelancer' not in request.data
                return True
            elif hasattr(user, 'freelancerprofile'):
                if request.method in ['PATCH', 'PUT']:
                    if not obj.freelancer:
                        return 'freelancer' in request.data and len(
                            request.data) == 1
                    return False
                return True
        return False
