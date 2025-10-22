# Favicons

The favicons module is responsible for automatically fetching and storing favicon images for monitored projects. It provides a complete workflow from scheduling to storage, ensuring that project favicons are kept up-to-date.

## Model Structure

### Favicon

The Favicon model stores favicon-related data and metadata for projects.

**File:** `src/favicons/models.py`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | AutoField | Auto-increment | Primary key |
| project | OneToOneField | - | Reference to the Project this favicon belongs to |
| favicon | ImageField | null | The actual favicon image file |
| task_status | CharField | 'UNKNOWN' | Status of the favicon fetching task |
| last_edited | DateTimeField | timezone.now | Last time the favicon was updated |
| created_at | DateTimeField | auto_now_add | When the favicon record was created |
| updated_at | DateTimeField | auto_now | When the favicon record was last modified |
| celery_task_log | ForeignKey | null | Reference to the associated Celery task log |

#### Task Status Options

The `task_status` field can have the following values:

- `PENDING`: Task is queued but not yet started
- `SUCCESS`: Favicon was successfully fetched and stored
- `FAILURE`: Failed to fetch favicon from the website
- `UNKNOWN`: Default status for new records

#### File Upload Path

Favicons are stored using the following path structure:
```
user_{user_id}/prjct_{project_id}/favicons/{filename}
```

## Workflow Overview

The favicon system operates through a sophisticated workflow involving multiple components:

1. **Scheduler**: Runs periodic tasks to identify projects needing favicon updates
2. **Worker**: Fetches favicons from websites and processes them
3. **API**: Handles communication between components and database operations
4. **Database**: Stores favicon metadata and file references

## API Endpoints

### Fetch Deprecated Favicons

**Endpoint:** `GET /api/fetch_deprecated_favicons/{secret_key}/`

**Purpose:** Returns a list of projects that need favicon updates (older than 6 hours or missing favicon)

**Authentication:** Uses Django SECRET_KEY for worker authentication

**Response:**
```json
{
  "projects": [
    {
      "id": 1,
      "url": "https://example.com"
    }
  ]
}
```

### Save Favicon

**Endpoint:** `POST /api/save_favicon/{secret_key}/{project_id}/`

**Purpose:** Saves the fetched favicon data to the database

**Authentication:** Uses Django SECRET_KEY for worker authentication

**Request Body:**
```json
{
  "favicon_url": "https://example.com/favicon.ico",
  "favicon_content": "base64_encoded_image_data",
  "duration": 2.5
}
```

## Tasks

### queue_deprecated_favicons

**Schedule:** Every 60 seconds (configured in `src/fromedwin/celery.py`)

**Purpose:** 
- Identifies projects with outdated favicons (older than 6 hours)
- Ensures only one instance of this task runs at a time
- Schedules individual `fetch_favicon` tasks for each project

**Workflow:**
1. Revokes any existing queued tasks of the same type
2. Calls the API to get list of projects needing updates
3. Schedules `fetch_favicon` tasks for each project

### fetch_favicon

**Purpose:** Fetches favicon from a website and processes it

**Parameters:**
- `pk`: Project ID
- `url`: Website URL to fetch favicon from

**Workflow:**
1. Fetches the webpage HTML
2. Searches for favicon links in `<link>` tags
3. Downloads and processes each favicon candidate
4. Selects the largest favicon (by pixel area)
5. Prefers SVG format when available
6. Sends results back to the API for storage

**Error Handling:**
- Logs errors for individual favicon URLs
- Falls back to default `/favicon.ico` location
- Reports failure status if no favicon is found

## Configuration

Key settings in `src/fromedwin/celery.py`:

```python
app.conf.beat_schedule = {
    'queue_deprecated_favicons': {
        'task': 'favicons.tasks.queue_deprecated_favicons',
        'schedule': 60,  # Run every 60 seconds
    },
}
```

## Monitoring

The system provides several monitoring capabilities:

- Task status tracking in the Favicon model
- Celery task logs with duration metrics
- API endpoint authentication logging
- Error logging for failed favicon fetches

