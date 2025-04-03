# Projects

A user can have multiple projects. 

Project model is defined in `src/projects/models.py`

Lighthouse and Report are defined in `src/performances/models.py`

Service, HTTPCodeService and HTTPMockedCodeService are defined in `src/availability/models.py`

```{mermaid}
classDiagram
    class Project {
        pk
        user : User
        title : String
        url : String
        favicon : ImageField
        sitemap_task_status : String
        sitemap_last_edited : DateTime
        is_offline : Boolean
        is_degraded : Boolean
        is_warning : Boolean
        availability : Float
        pathname : String
        incidents_count : Int
        performance_score : Float
        directory_path() : String
        is_favorite : Boolean
        enable_public_page : Boolean
        favicon_task_status : String
        favicon_last_edited : DateTime
    }

    class Pages {
        pk
        project : Project
        url : String
        title : String
        description : String
        created_at : DateTime
        sitemap_last_seen : DateTime
        scraping_last_seen : DateTime
    }

    class Lighthouse {
        pk
        page : Pages
        performance : Float
        accessibility : Float
        best_practices : Float
    }

    class Report {
        pk
        lighthouse : Lighthouse
        screenshot : ImageField
        form_factor : Int
        score_performance : Float
    }

    class Service {
        pk
        project : Project
        title : String
        is_public : Boolean
        is_enabled : Boolean
    }

    class HTTPCodeService {
        pk
        url : String
        tls_skip_verify : Boolean
        service : Service
    }

    class HTTPMockedCodeService {
        pk
        code : Int
        service : Service
    }

    class Incident {
        pk
        service : Service
        starts_at : DateTime
        ends_at : DateTime
        status : Int
    }

    class Notification {
        pk
        project : Project
        service : Service
        severity : Int
    }

    class Emails {
        pk
        project : Project
        email : String
    }
    

    Project "1" -- "*" Pages
    Pages "1" -- "*" Lighthouse
    Lighthouse "1" -- "*" Report
    Project "1" -- "*" Service
    Service "1" -- "1" HTTPCodeService
    Service "1" -- "1" HTTPMockedCodeService    
    Service "1" -- "*" Incident 
    Project "1" -- "*" Notification
    Service "1" -- "*" Notification
    Project "1" -- "*" Emails
```
