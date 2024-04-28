from django.contrib import admin

from orders.models import Order
from users.models import CustomerProfile, FreelancerProfile


class CustomerUserAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if hasattr(user, 'customerprofile'):
            return qs.filter(user=user)
        elif hasattr(user, 'freelancerprofile'):
            orders = Order.objects.filter(freelancer=user.freelancerprofile)
            customers = CustomerProfile.objects.filter(
                order__in=orders).distinct()
            return customers

        return qs.none()

    def has_change_permission(self, request, obj=None):
        user = request.user

        if hasattr(user, 'customerprofile'):
            return user.customerprofile == obj
        return False

    def has_delete_permission(self, request, obj=None):
        user = request.user

        if hasattr(user, 'customerprofile'):
            return user.customerprofile == obj
        return False

    def has_add_permission(self, request):
        return False

    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True


admin.site.register(CustomerProfile, CustomerUserAdmin)


class FreelancerUserAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    def has_change_permission(self, request, obj=None):
        user = request.user

        if hasattr(user, 'freelancerprofile'):
            return user.freelancerprofile == obj
        return False

    def has_delete_permission(self, request, obj=None):
        user = request.user

        if hasattr(user, 'freelancerprofile'):
            return request.user.freelancerprofile == obj
        return False

    def has_add_permission(self, request):
        return False

    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True


admin.site.register(FreelancerProfile, FreelancerUserAdmin)