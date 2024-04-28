from users.models import FreelancerProfile, CustomerProfile
from users.serializers import FreelancerProfileSerializer, \
    CustomerProfileSerializer


def get_user_profile(user):
    """
    Get user profile from user model

    :param user: User model
    :return: User profile
    """
    profile = None
    if hasattr(user, 'freelancerprofile'):
        profile = user.freelancerprofile
    elif hasattr(user, 'customerprofile'):
        profile = user.customerprofile
    return profile


def get_profile_serializer(profile):
    """
    Get serializer for user profile
    :param profile: User profile
    :return: User profile serializer
    """
    if isinstance(profile, FreelancerProfile):
        return FreelancerProfileSerializer
    elif isinstance(profile, CustomerProfile):
        return CustomerProfileSerializer
