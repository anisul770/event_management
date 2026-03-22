# Event Management System (Django MVT)

A modern Django MVT-based application for organizing events, roles, and participant interactions.

## Project Overview

This project implements an event management platform using Django architecture:

- `models` for event/category/user roles/participants
- `views` handling listing, detail, and registration logic
- `templates` for UI (home, event list, category, profile, permission pages)
- `forms` for auth, role, and event data handling
- `URLs` for logical app routing
- `signals` for domain triggers
- role-based access via groups and permissions
- static/media handling with Tailwind CSS
- PostgreSQL-ready setup

## Repository Structure

```
event_management/
├── core/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── tests.py
│   ├── templates/
│   │   ├── event_list.html
│   │   ├── hero.html
│   │   ├── home.html
│   │   ├── logged_nav.html
│   │   ├── no_permission.html
│   │   ├── non_logged.html
│   │   └── ...
│   ├── templatetags/
│   │   └── role_filters.py
│   └── migrations/
├── event/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── signals.py
│   ├── templates/
│   │   ├── category.html
│   │   ├── event.html
│   │   └── participant.html
│   └── migrations/
├── users/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── signals.py
│   ├── templates/
│   │   ├── sign_in.html
│   │   ├── sign_up.html
│   │   ├── reset_email.html
│   │   ├── reset_password.html
│   │   ├── create_group.html
│   │   ├── group_list.html
│   │   └── accounts/
│   └── migrations/
├── event_management/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── __init__.py
├── media/
│   ├── event_asset/
│   └── profile_images/
├── static/
│   └── css/
│       ├── input.css
│       └── output.css
├── db.sqlite3
├── package.json
├── package-lock.json
├── requirements.txt
├── render_build.sh
└── manage.py
```

## Features

- User-specific roles: Admin, Organizer, Participant
- Signup, login, logout, password reset flows
- Role assignment and restrictions via user groups
- Event category listing and filtering
- Event registration and participant views
- Reusable templates with Tailwind support
- Environments with environment variables and secure config

## Setup Instructions

1. Clone repository:
   ```bash
   git clone <repo-url>
   cd event_management
   ```

2. Create and activate virtual environment

   Windows:
   ```bat
   python -m venv event_env
   event_env\Scripts\activate
   ```

   macOS/Linux:
   ```bash
   python3 -m venv event_env
   source event_env/bin/activate
   ```

3. Install Python dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Setup Tailwind (if using for CSS build)

   ```bash
   npm install
   npm run watch:tailwind
   ```

6. Collect static assets

   ```bash
   python manage.py collectstatic --no-input
   ```

7. Create admin user

   ```bash
   python manage.py createsuperuser
   ```

8. Start server

   ```bash
   python manage.py runserver
   ```

## Testing

Run:

```bash
python manage.py test
```

## Env Config

Use `.env` or `python-decouple` for:

- `SECRET_KEY`
- `DEBUG`
- `DATABASE_URL`
- `ALLOWED_HOSTS`

## Deployment Checklist

- Set `DEBUG=False` in production
- Configure `ALLOWED_HOSTS`
- Use PostgreSQL by updating `DATABASE_URL`
- Use `whitenoise` for static file serving
- Run migrations and `collectstatic`

## Commands
For demo data use this commands

- `python manage.py check`
- `python manage.py migrate --plan`
- `python manage.py dumpdata > data.json`
- `python manage.py loaddata data.json`

## Contribution

1. Fork project
2. Branch: `feat/` or `fix/`
3. Add tests
4. PR with description

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- Maintainer: Anisul Haque
- Email: anisulhaque773@gmail.com
- GitHub: https://github.com/anisul770
