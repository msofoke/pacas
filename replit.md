# Replit.md - Pacas Management System

## Overview
A Flask-based web application for managing clothing bundle inventory ("pacas"). The system helps track bundle purchases, classify items by type and quality, calculate profit margins, and manage pricing strategies for different quality categories.

## User Preferences
Preferred communication style: Simple, everyday language.

## Recent Changes (January 2025)
- ✓ Migrated from JSON file storage to PostgreSQL database
- ✓ Added edit functionality for existing bundles
- ✓ Implemented proper database models with SQLAlchemy
- ✓ Created data migration script for seamless transition
- ✓ Enhanced UI with edit buttons throughout the interface

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Data Storage**: PostgreSQL database with proper relational models
- **Application Pattern**: MVC pattern with models, routes, data service layer, and templates
- **Session Management**: Flask sessions with configurable secret key

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default templating)
- **CSS Framework**: Bootstrap 5.3.0 for responsive design
- **Icons**: Bootstrap Icons
- **JavaScript**: Vanilla JavaScript for form validation and dynamic calculations
- **Layout**: Base template with navigation and flash message system

### Key Components

#### Database Models (`models.py`)
- **Bundle Model**: Stores bundle inventory data with JSON fields for complex data
- **Config Model**: Stores application configuration with key-value pairs
- **Features**: Automatic JSON serialization/deserialization, proper timestamps

#### Data Service (`data_service.py`)
- **Purpose**: Handles all database operations through PostgreSQL
- **Features**: CRUD operations, error handling, transaction management
- **Methods**: Bundle and configuration management with proper validation

#### Business Logic (`utils.py`)
- **Purpose**: Calculates bundle metrics, pricing, and profit margins
- **Key Functions**:
  - Cost per piece calculations
  - Quality-based pricing with configurable profit margins
  - Revenue projections (minimum and ideal scenarios)

#### Routes (`routes.py`)
- **Dashboard** (`/`): Summary statistics and bundle overview
- **Configuration** (`/config`): Profit percentage settings
- **Bundle Management**: Full CRUD operations for bundles
  - `/bundle/<id>`: View bundle details
  - `/new_bundle`: Create new bundle
  - `/edit_bundle/<id>`: Edit existing bundle
  - `/delete_bundle/<id>`: Delete bundle
- **Error Handling**: Comprehensive logging and user feedback

## Data Flow

1. **Bundle Creation**: User inputs bundle details (cost, pieces, classification)
2. **Data Processing**: System calculates metrics using profit percentages from config
3. **Storage**: Bundle data saved to JSON files via DataManager
4. **Display**: Dashboard shows aggregated statistics and individual bundle details
5. **Configuration Updates**: Profit margins can be adjusted, affecting all calculations

## External Dependencies

### Python Packages
- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **psycopg2-binary**: PostgreSQL adapter
- **Standard Library**: os, json, datetime, logging

### Frontend Dependencies (CDN)
- **Bootstrap 5.3.0**: UI framework and components
- **Bootstrap Icons**: Icon library

## Deployment Strategy

### Current Setup
- **Development Server**: Gunicorn server on port 5000
- **Database**: PostgreSQL with environment-based configuration
- **Environment**: Configured for production deployment
- **Session Security**: Environment variable for production secret key
- **Data Storage**: PostgreSQL database with proper migrations

### Production Considerations
- PostgreSQL database provides scalability and reliability
- Environment variables properly configured for database connection
- Gunicorn server for production-ready deployment
- Session secret configured via environment variable
- Data migration support for seamless upgrades

### Key Architectural Decisions

1. **PostgreSQL Database vs File Storage**
   - **Chosen**: PostgreSQL with SQLAlchemy ORM
   - **Rationale**: Scalability, data integrity, concurrent access support
   - **Pros**: ACID compliance, concurrent users, proper relationships, backup support
   - **Cons**: Requires database server, more complex deployment initially

2. **Flask over Django**
   - **Chosen**: Flask for lightweight web framework
   - **Rationale**: Simple application requirements, faster development
   - **Pros**: Minimal overhead, flexible structure, easy to understand
   - **Cons**: Less built-in functionality, more manual configuration

3. **Bootstrap for UI**
   - **Chosen**: Bootstrap 5 with CDN delivery
   - **Rationale**: Rapid development, responsive design, professional appearance
   - **Pros**: Pre-built components, mobile-first design, consistent styling
   - **Cons**: Larger payload, less unique visual identity

4. **Server-Side Rendering**
   - **Chosen**: Traditional server-side rendering with Jinja2
   - **Rationale**: Simple application, no complex client-side interactions needed
   - **Pros**: SEO friendly, faster initial load, simpler architecture
   - **Cons**: Less interactive user experience, full page reloads