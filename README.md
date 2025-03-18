# URL Shortener Service

A Django-based URL shortener service that converts long URLs into short, manageable links with analytics tracking.

## System Architecture

### Tech Stack
- Django (Web Framework)
- PostgreSQL (Database)
- Django REST Framework (API Layer)

### Core Components
1. URL Shortening Service
   - Base62 encoding for generating short URLs
   - Collision detection and handling
   - URL validation and sanitization

2. Database Layer
   - URL mappings storage
   - Analytics data management
   - PostgreSQL for robust data persistence

3. API Layer
   - RESTful endpoints for CRUD operations
   - Analytics data retrieval
   - Rate limiting and security measures

## Implementation Plan

### 1. Project Setup
- Initialize Django project
- Configure PostgreSQL database
- Set up Django REST Framework
- Configure project settings and environment variables

### 2. Data Models

#### URL Model
- long_url: Original URL (TextField)
- short_url: Generated short code (CharField)
- created_at: Creation timestamp (DateTimeField)
- access_count: Number of redirects (IntegerField)
- is_active: URL status (BooleanField)

### 3. Core Features

#### URL Shortening Logic
- Implement base62 encoding for short URL generation
- Ensure uniqueness of generated short URLs
- Handle URL validation and sanitization

#### URL Redirection
- Implement redirect view for short URLs
- Track access counts
- Handle invalid/expired URLs

#### Analytics Tracking
- Increment access counter on each redirect
- Store timestamp of each access
- Generate basic analytics reports

### 4. API Endpoints

#### URL Management
- POST /api/urls/ - Create new short URL
- GET /api/urls/{short_code} - Get URL details
- DELETE /api/urls/{short_code} - Delete short URL

#### Analytics
- GET /api/urls/{short_code}/stats - Get URL statistics
- GET /api/urls/stats - Get overall statistics

### 5. Error Handling

#### Edge Cases
- Invalid URL formats
- URL collisions
- Rate limiting exceeded
- Database connection issues
- Maximum URL length exceeded

#### Error Responses
- 404: URL not found
- 400: Invalid URL format
- 429: Too many requests
- 500: Server errors

### 6. Testing Strategy

#### Unit Tests
- URL shortening logic
- Model validations
- API endpoints
- Error handling

#### Integration Tests
- Database operations
- URL redirection flow
- Analytics tracking

#### Load Tests
- Concurrent URL creation
- Multiple redirects handling
- Database performance

### 7. Security Measures

#### Input Validation
- URL format validation
- Length restrictions
- Content type verification

#### Rate Limiting
- API endpoint restrictions
- IP-based limiting
- User-based quotas

### 8. Monitoring and Maintenance

#### Performance Monitoring
- Database query optimization
- Cache implementation
- Response time tracking

#### Regular Maintenance
- Database cleanup
- Invalid URL purging
- Analytics data aggregation

## Development Workflow
1. Set up development environment
2. Implement core URL shortening logic
3. Create database models and migrations
4. Develop API endpoints
5. Implement analytics tracking
6. Add error handling and validation
7. Write tests
8. Deploy and monitor

## Project Structure

### Directory Layout
```
urlshortener/
├── manage.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
└── urlshortener/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── core/
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── models.py          # URL and analytics models
        ├── serializers.py     # DRF serializers
        ├── services/
        │   ├── __init__.py
        │   ├── shortener.py   # URL shortening logic
        │   └── analytics.py   # Analytics processing
        ├── views/
        │   ├── __init__.py
        │   ├── api.py         # API endpoints
        │   └── redirect.py    # URL redirection views
        ├── tests/
        │   ├── __init__.py
        │   ├── test_models.py
        │   ├── test_views.py
        │   └── test_services.py
        ├── migrations/        # Database migrations
        ├── templates/
        │   └── core/          # HTML templates if needed
        ├── static/
        │   └── core/
        │       ├── css/       # Stylesheets
        │       └── js/        # JavaScript files
        └── utils/             # Helper functions and utilities
```

### Key Directories

#### Core Application
- `core/models.py`: Contains URL and analytics models
- `core/serializers.py`: DRF serializers for API responses
- `core/views/`: Separated views for better organization
  - `api.py`: API endpoints using DRF
  - `redirect.py`: URL redirection logic

#### Business Logic
- `core/services/`: Contains core business logic
  - `shortener.py`: URL shortening implementation
  - `analytics.py`: Analytics processing logic

#### Testing
- `core/tests/`: Organized test files by component
  - Unit tests for models, views, and services
  - Integration tests for complete workflows

#### Assets and Templates
- `core/static/`: Static files (CSS, JavaScript)
- `core/templates/`: HTML templates if needed

#### Support Files
- `migrations/`: Database migration files
- `utils/`: Helper functions and utilities

## Future Enhancements
- Custom short URL support
- User authentication
- Advanced analytics
- API documentation
- Cache layer implementation
- Bulk URL processing