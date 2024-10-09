import logging
import os
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import Profile

@receiver(post_delete, sender=Profile)
def delete_user_directory(sender, instance=None, **kwargs):
    logger = logging.getLogger(__name__)
    dir_path = instance.directory_path()
    if default_storage.exists(dir_path):
        try:
            # List all files and directories within the directory
            dirs, files = default_storage.listdir(dir_path)
            # Recursively delete all subdirectories and files
            for file in files:
                file_path = os.path.join(dir_path, file)
                default_storage.delete(file_path)
            for subdir in dirs:
                subdir_path = os.path.join(dir_path, subdir)
                default_storage.delete(subdir_path)
            # Delete the now-empty directory
            default_storage.delete(dir_path)
        except Exception as e:
            logger.error(f"Error deleting folder: {e}")
            # Optionally, re-raise the exception if you want to prevent deletion
            # raise e
