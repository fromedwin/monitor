# Projects

A user can have multiple projects. 

Project model is defined in `src/projects/models.py`

Lighthouse and Report are defined in `src/performances/models.py`

Service, HTTPCodeService and HTTPMockedCodeService are defined in `src/availability/models.py`

## Project

The Project model represents a website or application that a user wants to monitor.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | AutoField | Auto-increment | Primary key |
| user | ForeignKey | - | Reference to the User who owns this project |
| title | CharField | - | Display name for the project |
| url | URLField | - | The main URL of the project |
| favicon | ImageField | null | Project's favicon image |
| sitemap_task_status | CharField | - | Status of sitemap processing task |
| sitemap_last_edited | DateTimeField | null | Last time sitemap was updated |
| is_offline | BooleanField | False | Indicates if the project is currently offline |
| is_degraded | BooleanField | False | Indicates if the project has degraded performance |
| is_warning | BooleanField | False | Indicates if the project has warnings |
| availability | FloatField | - | Overall availability percentage |
| pathname | CharField | - | URL pathname for the project |
| incidents_count | IntegerField | 0 | Number of incidents for this project |
| performance_score | FloatField | - | Overall performance score |
| is_favorite | BooleanField | False | Whether this project is marked as favorite |
| enable_public_page | BooleanField | False | Whether to enable public status page |
| favicon_task_status | CharField | - | Status of favicon processing task |
| favicon_last_edited | DateTimeField | null | Last time favicon was updated |

## Pages

The Pages model represents individual pages within a project that are monitored.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | AutoField | Auto-increment | Primary key |
| project | ForeignKey | - | Reference to the parent Project |
| url | URLField | - | URL of the specific page |
| title | CharField | - | Page title |
| description | TextField | - | Page description |
| created_at | DateTimeField | auto_now_add | When the page was first discovered |
| sitemap_last_seen | DateTimeField | null | Last time page was seen in sitemap |
| scraping_last_seen | DateTimeField | null | Last time page was scraped |

## Lighthouse

The Lighthouse model stores performance metrics for individual pages.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | AutoField | Auto-increment | Primary key |
| page | ForeignKey | - | Reference to the monitored Page |
| performance | FloatField | - | Performance score (0-100) |
| accessibility | FloatField | - | Accessibility score (0-100) |
| best_practices | FloatField | - | Best practices score (0-100) |

## Report

The Report model stores detailed performance reports with screenshots.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | AutoField | Auto-increment | Primary key |
| lighthouse | ForeignKey | - | Reference to the Lighthouse metrics |
| screenshot | ImageField | null | Screenshot of the page |
| form_factor | IntegerField | - | Device form factor (mobile/desktop) |
| score_performance | FloatField | - | Detailed performance score |

## Service

The Service model represents monitoring services for a project.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | AutoField | Auto-increment | Primary key |
| project | ForeignKey | - | Reference to the parent Project |
| title | CharField | - | Service name |
| is_public | BooleanField | False | Whether service status is public |
| is_enabled | BooleanField | True | Whether the service is active |

## HTTPCodeService

The HTTPCodeService model represents HTTP-based monitoring services.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | AutoField | Auto-increment | Primary key |
| url | URLField | - | URL to monitor |
| tls_skip_verify | BooleanField | False | Whether to skip TLS verification |
| service | OneToOneField | - | Reference to the parent Service |

## HTTPMockedCodeService

The HTTPMockedCodeService model represents mocked HTTP responses for testing.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | AutoField | Auto-increment | Primary key |
| code | IntegerField | - | HTTP status code to return |
| service | OneToOneField | - | Reference to the parent Service |

## Incident

The Incident model tracks service outages and issues.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | AutoField | Auto-increment | Primary key |
| service | ForeignKey | - | Reference to the affected Service |
| starts_at | DateTimeField | - | When the incident started |
| ends_at | DateTimeField | null | When the incident ended |
| status | IntegerField | - | Incident status code |

## Notification

The Notification model manages alerts and notifications for projects and services.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | AutoField | Auto-increment | Primary key |
| project | ForeignKey | - | Reference to the parent Project |
| service | ForeignKey | null | Reference to the specific Service |
| severity | IntegerField | - | Notification severity level |

## Emails

The Emails model stores email addresses for project notifications.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | AutoField | Auto-increment | Primary key |
| project | ForeignKey | - | Reference to the parent Project |
| email | EmailField | - | Email address for notifications |
