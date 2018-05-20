"""Util functions to use in decorators in views"""


def is_admin(user):
    """
    Is administrator

    :param user: primary key for User
    :return: boolean -- True if current user is administrator
    """
    if user and user.is_superuser is not None:
        return user.is_superuser
    raise ValueError("User does not have is_superuser property")


def can_upload(user):
    """
    Has batch data upload permission

    :param user: primary key for User
    :return: boolean -- True if current user has permission for upload data files
    """
    if user and user.profile is not None and user.profile.canUpload is not None:
        return user.profile.canUpload
    raise ValueError("User does not have canUpload property")
