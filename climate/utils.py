def is_admin(user):
    if user and user.is_superuser is not None:
        return user.is_superuser
    raise ValueError("User does not have is_superuser property")


def can_upload(user):
    if user and user.profile is not None and user.profile.canUpload is not None:
        return user.profile.canUpload
    raise ValueError("User does not have canUpload property")
