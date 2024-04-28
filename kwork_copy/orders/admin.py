from django.contrib import admin

from orders import permissions
from orders.models import Order


class CustomOrderAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        user = request.user

        if hasattr(user, 'freelancerprofile'):
            return [field.name for field in self.model._meta.fields if
                    field.name != 'freelancer']
        if hasattr(user, 'customerprofile'):
            return ['freelancer']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if hasattr(user, 'customerprofile'):
            profile = user.customerprofile
            return qs.filter(customer=profile)
        elif hasattr(user, 'freelancerprofile'):
            return qs.filter(freelancer__isnull=True)

        return qs.none()

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            user = request.user

            if hasattr(user, 'customerprofile'):
                if permissions.IsOwnerOrReadOnly.has_object_permission(
                        self, request, self, obj):

                    return obj.customer == user.customerprofile
            elif hasattr(user, 'freelancerprofile'):
                if permissions.IsOwnerOrReadOnly.has_object_permission(
                        self, request, self, obj):
                    return True

        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            user = request.user

            if hasattr(user, 'customerprofile'):
                return obj.customer == user.customerprofile
            return False

        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if hasattr(request.user, 'customerprofile'):
            return True
        return False

    def has_view_permission(self, request, obj=None):
        user = request.user

        if hasattr(user, 'customerprofile'):
            return obj.customer == user.customerprofile
        elif hasattr(user, 'freelancerprofile'):
            return True

    def has_module_permission(self, request):
        return request.user.is_staff


admin.site.register(
    Order,
    CustomOrderAdmin
)
