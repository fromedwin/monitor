# User Data Model

This documentation outlines the structure of the User data model in a Django project. The model extends the default django.contrib.auth user model by adding a Profile object to store additional information.

## Profile Model

The Profile model is linked to the default Django User model using a one-to-one relationship. It includes fields for managing user preferences and settings such as timezone and auto-redirect behavior.

Profile model is defined in `src/profile/models.py`

```{mermaid}
classDiagram
    class User {
        +pk
        +username
        +password
        +email
        +is_staff
        +is_active
        +is_superuser
        +last_login
        +date_joined
    }
    
    class Profile {
        +pk
        +disable_auto_redirect : Boolean
        +timezone : TimeZoneField
        +directory_path() : String
    }

    User "1" -- "1" Profile
```
