import logging
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import Profile

logger = logging.getLogger(__name__)

def delete_directory_contents(path):
    if default_storage.exists(path):
        dirs, files = default_storage.listdir(path)
        for file in files:
            file_path = os.path.join(path, file)
            default_storage.delete(file_path)
            logger.info(f"Deleted file: {file_path}")
        for subdir in dirs:
            subdir_path = os.path.join(path, subdir)
            delete_directory_contents(subdir_path)
        default_storage.delete(path)
        logger.info(f"Deleted directory: {path}")

@receiver(post_delete, sender=Profile)
def delete_user_directory(sender, instance=None, **kwargs):
    if instance is None:
        logger.warning("delete_user_directory called with None instance")
        return

    dir_path = instance.directory_path()
    try:
        delete_directory_contents(dir_path)
        logger.info(f"Successfully deleted user directory: {dir_path}")
    except PermissionError as e:
        logger.error(f"Permission error deleting directory {dir_path}: {e}")
    except FileNotFoundError as e:
        logger.warning(f"Directory not found {dir_path}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error deleting directory {dir_path}: {e}")