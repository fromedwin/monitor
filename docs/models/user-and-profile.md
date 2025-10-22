# User and Profile

This documentation outlines the structure of the User data model in a Django project. The model extends the default django.contrib.auth user model by adding a Profile object to store additional information.

## User Model

The User model is Django's default authentication model from `django.contrib.auth.models.User`. It provides core authentication functionality and user management capabilities.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | AutoField | Auto-increment | Primary key |
| username | CharField | - | Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only |
| password | CharField | - | Required. Hashed password |
| email | EmailField | - | Optional email address |
| is_staff | BooleanField | False | Designates whether this user can access the admin site |
| is_active | BooleanField | True | Designates whether this user account should be considered active |
| is_superuser | BooleanField | False | Designates that this user has all permissions without explicitly assigning them |
| last_login | DateTimeField | null | Last login timestamp |
| date_joined | DateTimeField | auto_now_add | Date when user account was created |

## Profile Model

The Profile model extends the default Django User model using a one-to-one relationship. It includes fields for managing user preferences and settings such as timezone and auto-redirect behavior.

Profile model is defined in `src/profile/models.py`

### Core Profile Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | AutoField | Auto-increment | Primary key |
| user | OneToOneField | - | One-to-one relationship with User model |
| disable_auto_redirect | BooleanField | False | When True, prevents automatic redirect from `/` to `/dashboard` for this user |
| timezone | TimeZoneField | - | User's preferred timezone |
| directory_path | method | - | Returns the directory path for user-specific files |
