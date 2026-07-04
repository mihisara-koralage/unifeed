# UniFeed 🎓

A full-featured university social platform that unifies student life in one place. Built with Django, Django Channels, PostgreSQL, and Redis.

## Features

| Module | Description |
|---|---|
| **User Management** | Email-based auth, three roles (Student, Page, Admin), JWT-secured API routes |
| **Social Feed** | Post text and images, like posts, hashtag filtering |
| **Real-time Messaging** | WebSocket-powered chat, typing indicators, message history |
| **Study Resources** | Share and search study links by category, URL validation |
| **Events** | Page accounts create events with banners, students RSVP |
| **Campus Marketplace** | List items with photos, safety disclaimers, report system |
| **Admin Dashboard** | Platform analytics, user role management, content moderation |

---

## Tech Stack

- **Backend** — Django 4.x (Python 3.11+)
- **Real-time** — Django Channels + Redis
- **Database** — PostgreSQL
- **Media storage** — Cloudinary
- **ASGI server** — Daphne
- **Frontend** — Django templates + Bootstrap 5

---

## Running Locally

### 1. Prerequisites

Make sure you have these installed:

- Python 3.11 or higher
- PostgreSQL
- Redis

**Install Redis on Windows (via Docker):**
```bash
docker run -d -p 6379:6379 redis
```

**Install Redis on Mac:**
```bash
brew install redis
brew services start redis
```

**Verify Redis is running:**
```bash
redis-cli ping
# Should respond: PONG
```

---

### 2. Clone the repository

```bash
git clone https://github.com/mihisara-koralage/unifeed.git
cd unifeed
```

---

### 3. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Create a PostgreSQL database

Open your PostgreSQL terminal (psql) and run:

```sql
CREATE DATABASE unifeed_db;
CREATE USER unifeed_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE unifeed_db TO unifeed_user;
```

---

### 6. Create a `.env` file

Create a file called `.env` in the root of the project (same folder as `manage.py`):

```env
SECRET_KEY=your_long_random_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1

DATABASE_NAME=unifeed_db
DATABASE_USER=unifeed_user
DATABASE_PASSWORD=yourpassword
DATABASE_HOST=localhost
DATABASE_PORT=5432

CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(50))"
```

**Get Cloudinary credentials:**
Sign up free at [cloudinary.com](https://cloudinary.com) → Dashboard → copy Cloud Name, API Key, and API Secret.

---

### 7. Settings changes needed for local development

When running locally, `config/settings.py` already handles everything via the `.env` file. No manual changes needed **except** make sure `DEBUG=True` is set in your `.env`.

The one thing that differs locally vs production is static file serving. Locally Django handles it automatically. No changes needed to `urls.py` for local development.

---

### 8. Run migrations

```bash
python manage.py migrate
```

---

### 9. Create a superuser

```bash
python manage.py createsuperuser
```

Enter your email and password. Then set the role to `admin` so you can access the dashboard:

```bash
python manage.py shell
```
```python
from users.models import CustomUser
u = CustomUser.objects.get(email='your@email.com')
u.role = 'admin'
u.save()
exit()
```

---

### 10. Collect static files (first time only)

```bash
python manage.py collectstatic
```

---

### 11. Start the server

UniFeed uses Daphne (not Django's built-in `runserver`) because of WebSocket support:

```bash
daphne -p 8000 config.asgi:application
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 12. Test accounts to create

| Role | How to create |
|---|---|
| Student | Register at `/users/register/` — default role |
| Page / Org | Register, then go to `/admin/` and change role to `page` |
| Admin | Use the shell command above |

---

## Project Structure

```
unifeed/
├── config/
│   ├── settings.py       # All project settings
│   ├── urls.py           # Root URL configuration
│   └── asgi.py           # ASGI config for WebSockets
├── users/                # Module 1 — Auth & profiles
├── feed/                 # Module 2 — Social feed
├── messaging/            # Module 3 — Real-time chat
├── resources/            # Module 4 — Study resources
├── events/               # Module 5 — Events & RSVP
├── marketplace/          # Module 6 — Campus marketplace
├── dashboard/            # Module 7 — Admin dashboard
├── templates/            # Shared base templates
├── static/               # Source static files (CSS, JS, images)
├── staticfiles/          # Collected static files (auto-generated, not in Git)
├── media/                # Uploaded files locally (not in Git)
├── start.sh              # Production startup script
├── nixpacks.toml         # Railway build configuration
├── Procfile              # Process declaration
├── requirements.txt      # Python dependencies
├── runtime.txt           # Python version
└── .env                  # Local environment variables (not in Git)
```

---

## Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Django secret key — keep this private |
| `DEBUG` | Yes | `True` locally, `False` in production |
| `ALLOWED_HOSTS` | Yes | Comma-separated list of allowed hosts |
| `DATABASE_URL` | Production only | Full database URL — auto-set by Railway |
| `DATABASE_NAME` | Local only | PostgreSQL database name |
| `DATABASE_USER` | Local only | PostgreSQL username |
| `DATABASE_PASSWORD` | Local only | PostgreSQL password |
| `DATABASE_HOST` | Local only | Usually `localhost` |
| `DATABASE_PORT` | Local only | Usually `5432` |
| `REDIS_URL` | Production only | Redis URL — auto-set by Railway |
| `CLOUDINARY_CLOUD_NAME` | Yes | From Cloudinary dashboard |
| `CLOUDINARY_API_KEY` | Yes | From Cloudinary dashboard |
| `CLOUDINARY_API_SECRET` | Yes | From Cloudinary dashboard |
| `STATIC_ROOT` | Production only | Set to `/app/staticfiles` on Railway |

---

## Deploying to Railway

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/unifeed.git
git push -u origin main
```

### 2. Create a Railway project

1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub → select your repo
3. Click **+ New** → Database → **Add PostgreSQL**
4. Click **+ New** → Database → **Add Redis**

### 3. Add environment variables

In your app service → Variables tab, add:

```
SECRET_KEY=your_long_secret_key
DEBUG=False
ALLOWED_HOSTS=your-app.up.railway.app
STATIC_ROOT=/app/staticfiles
CLOUDINARY_CLOUD_NAME=your_value
CLOUDINARY_API_KEY=your_value
CLOUDINARY_API_SECRET=your_value
```

`DATABASE_URL` and `REDIS_URL` are auto-injected by Railway — do not add them manually.

### 4. After first successful deploy, run in Railway shell

```bash
python manage.py migrate
python manage.py createsuperuser
```

Then set the superuser role to admin via the shell:

```bash
python manage.py shell
```
```python
from users.models import CustomUser
u = CustomUser.objects.get(email='your@email.com')
u.role = 'admin'
u.save()
exit()
```

---

## Key URLs

| URL | Description |
|---|---|
| `/` | Social feed (home) |
| `/users/register/` | Create a student account |
| `/users/login/` | Log in |
| `/users/profile/` | Edit profile and avatar |
| `/messages/` | Chat inbox |
| `/resources/` | Study resource directory |
| `/events/` | Campus events |
| `/marketplace/` | Buy and sell items |
| `/dashboard/` | Admin dashboard (admin role only) |
| `/admin/` | Django admin panel (staff only) |

---

## Common Issues

**WebSocket connection fails locally**

Make sure Redis is running:
```bash
redis-cli ping
```
And use Daphne, not `python manage.py runserver`.

**Static files not loading in production**

SSH into Railway shell and run:
```bash
python manage.py collectstatic --noinput --clear
```

**Admin panel has no styles**

Same fix as above — run collectstatic. The `start.sh` script does this automatically on every deploy.

**`Apps aren't loaded yet` error on startup**

Check `config/asgi.py` — `django.setup()` must appear before any app imports.

**Media uploads disappear after redeploy**

Make sure Cloudinary credentials are set in Railway Variables. Without Cloudinary, uploaded files are stored in the container and lost on every redeploy.

---

## License

MIT