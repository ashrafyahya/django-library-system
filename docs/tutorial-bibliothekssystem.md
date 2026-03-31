# Django Tutorial: Bibliothekssystem für Studierende

## 1) Was wir bauen
Wir bauen ein kleines Webprojekt mit Django:
- Studierende sehen Bücher und verfügbare Anzahl.
- Studierende buchen Bücher.
- Studierende stornieren Buchungen.
- Studierende sehen ihre Buchungen (Statusliste).
- Admin verwaltet Bücher und Buchungsstatus.

### Mini-Beispiel für die Logik
Ein Buch hat `available_copies = 2`:
1. Student bucht das Buch -> `available_copies = 1`
2. Student storniert die Buchung -> `available_copies = 2`
3. Admin setzt später eine Buchung auf `borrowed` und danach auf `returned` -> bei `returned` wird der Bestand wieder erhöht

### Wichtige Begriffe (einfach erklärt)
- **Model**: Datenstruktur in Python (z. B. Buch, Buchung).
- **Migration**: Datenbank-Update auf Basis der Models.
- **View**: Python-Logik für eine Seite/Aktion.
- **Template**: HTML-Datei für die Darstellung.
- **Admin**: Django-Backend zur Datenverwaltung.

## 2) Voraussetzungen
- Windows 10/11
- PowerShell
- Python **3.12.x** installiert
- Internet für Paketinstallation

Prüfen:
```powershell
python --version
```
Erwartung: `Python 3.12.x`

## 3) Projekt anlegen
In den Zielordner wechseln:
```powershell
cd C:\Users\dell\Programming\django-project
```

Django-Projekt, App und Docs-Ordner erzeugen:
```powershell
python -m django startproject config .
python manage.py startapp library
mkdir docs
```

### Projektstruktur direkt nach dem Anlegen (mit Kurzkommentaren)
```txt
django-project/
|-- manage.py                           # Django Kommando-Einstieg (runserver, migrate, test)
|-- config/                             # Projektweite Konfiguration
|   |-- settings.py                     # Apps, Datenbank, Templates, Login-Redirects
|   |-- urls.py                         # Zentrale URL-Verteilung
|   |-- asgi.py                         # ASGI-Startpunkt (Deployment/Async)
|   `-- wsgi.py                         # WSGI-Startpunkt (klassisches Deployment)
|-- library/                            # Unsere Fach-App Bibliothekssystem
|   |-- models.py                       # Datenmodelle: Category, Book, Booking
|   |-- views.py                        # Seitenlogik: Liste, Buchen, Stornieren
|   |-- admin.py                        # Admin-Ansichten und Admin-Aktionen
|   |-- urls.py                         # App-URLs für library
|   |-- tests.py                        # Einfache Logiktests
|   `-- migrations/                     # Automatisch erzeugte DB-Migrationen
|-- templates/                          # HTML Templates für UI
|   |-- base.html                       # Grundlayout/Navigation/Messages
|   |-- registration/login.html         # Login-Seite
|   `-- library/                        # Fachseiten der library-App
|       |-- book_list.html              # Buchkatalog + Buchen-Button
|       `-- my_bookings.html            # Eigene Buchungen + Storno-Button
|-- requirements.txt                    # Fixe Python-Abhängigkeiten
|-- .gitignore                          # Nicht zu versionierende Dateien
`-- docs/
    |-- plan.md                         # Anforderungen, Regeln, Leitplanken
    `-- tutorial-bibliothekssystem.md   # Schritt-für-Schritt Tutorial
```

## 4) Abhängigkeiten festlegen
Datei `requirements.txt` anlegen:
```txt
Django==5.1.3
```

## 5) `.gitignore` für Python-Projekt
Datei `.gitignore` auf diesen Inhalt setzen:
```txt
.vscode/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.venv/
venv/
env/
ENV/
build/
dist/
*.egg-info/
db.sqlite3
.pytest_cache/
```

## 6) Django Settings konfigurieren
Datei `config/settings.py` anpassen:
- `library` zu `INSTALLED_APPS` hinzufügen
- Template-Ordner aktivieren
- Login/Logout Redirects setzen

Relevanter Endstand:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'book_list'
LOGOUT_REDIRECT_URL = 'login'
```

## 7) URL-Struktur aufbauen
Datei `config/urls.py` komplett auf diesen Stand bringen:
```python
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('library.urls')),
]
```

Neue Datei `library/urls.py`:
```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('books/<int:book_id>/book/', views.create_booking, name='create_booking'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]
```

## 8) Models implementieren (Kernlogik)
Datei `library/models.py` komplett ersetzen:
```python
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='books')
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def clean(self):
        if self.available_copies > self.total_copies:
            raise ValidationError('Available copies cannot be greater than total copies.')

    def __str__(self):
        return f'{self.title} - {self.author}'


class Booking(models.Model):
    class Status(models.TextChoices):
        BOOKED = 'booked', 'Booked'
        CANCELLED = 'cancelled', 'Cancelled'
        BORROWED = 'borrowed', 'Borrowed'
        RETURNED = 'returned', 'Returned'

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BOOKED)
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booked_at']

    def __str__(self):
        return f'{self.student.username} - {self.book.title} ({self.status})'

    @classmethod
    def create_booking(cls, student, book):
        with transaction.atomic():
            locked_book = Book.objects.select_for_update().get(pk=book.pk)
            if locked_book.available_copies < 1:
                raise ValidationError('No copies are currently available.')

            has_active_booking = cls.objects.filter(
                student=student,
                book=locked_book,
                status__in=[cls.Status.BOOKED, cls.Status.BORROWED],
            ).exists()
            if has_active_booking:
                raise ValidationError('You already have an active booking for this book.')

            locked_book.available_copies -= 1
            locked_book.save(update_fields=['available_copies'])
            return cls.objects.create(student=student, book=locked_book, status=cls.Status.BOOKED)

    def cancel_by_student(self):
        if self.status != self.Status.BOOKED:
            raise ValidationError('Only booked items can be cancelled by students.')
        self._cancel_and_restore_inventory()

    def cancel_by_admin(self):
        if self.status != self.Status.BOOKED:
            raise ValidationError('Only booked items can be cancelled.')
        self._cancel_and_restore_inventory()

    def mark_as_borrowed(self):
        if self.status != self.Status.BOOKED:
            raise ValidationError('Only booked items can be marked as borrowed.')
        self.status = self.Status.BORROWED
        self.save(update_fields=['status', 'updated_at'])

    def mark_as_returned(self):
        if self.status != self.Status.BORROWED:
            raise ValidationError('Only borrowed items can be marked as returned.')

        with transaction.atomic():
            locked_book = Book.objects.select_for_update().get(pk=self.book.pk)
            locked_book.available_copies += 1
            if locked_book.available_copies > locked_book.total_copies:
                locked_book.available_copies = locked_book.total_copies
            locked_book.save(update_fields=['available_copies'])

            self.status = self.Status.RETURNED
            self.save(update_fields=['status', 'updated_at'])

    def _cancel_and_restore_inventory(self):
        with transaction.atomic():
            locked_book = Book.objects.select_for_update().get(pk=self.book.pk)
            locked_book.available_copies += 1
            if locked_book.available_copies > locked_book.total_copies:
                locked_book.available_copies = locked_book.total_copies
            locked_book.save(update_fields=['available_copies'])

            self.status = self.Status.CANCELLED
            self.save(update_fields=['status', 'updated_at'])
```

### Statusregeln (wichtig)
| Aktion | Erlaubt von Status | Neuer Status | Bestand (`available_copies`) |
|---|---|---|---|
| Student bucht | - | `booked` | `-1` |
| Student storniert | `booked` | `cancelled` | `+1` |
| Admin storniert | `booked` | `cancelled` | `+1` |
| Admin setzt ausgeliehen | `booked` | `borrowed` | unverändert |
| Admin setzt zurückgegeben | `borrowed` | `returned` | `+1` |

## 9) Views implementieren
Datei `library/views.py` komplett ersetzen:
```python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from .models import Book, Booking


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('book_list')
    return redirect('login')


@login_required
def book_list(request):
    books = Book.objects.select_related('category').all()
    return render(request, 'library/book_list.html', {'books': books})


@login_required
def my_bookings(request):
    bookings = Booking.objects.select_related('book').filter(student=request.user)
    return render(request, 'library/my_bookings.html', {'bookings': bookings})


@login_required
def create_booking(request, book_id):
    if request.method != 'POST':
        return redirect('book_list')

    book = get_object_or_404(Book, pk=book_id)
    try:
        Booking.create_booking(student=request.user, book=book)
        messages.success(request, 'Buchung erfolgreich erstellt.')
    except ValidationError as exc:
        messages.error(request, exc.message)

    return redirect('book_list')


@login_required
def cancel_booking(request, booking_id):
    if request.method != 'POST':
        return redirect('my_bookings')

    booking = get_object_or_404(Booking, pk=booking_id, student=request.user)
    try:
        booking.cancel_by_student()
        messages.success(request, 'Buchung wurde storniert.')
    except ValidationError as exc:
        messages.error(request, exc.message)

    return redirect('my_bookings')
```

## 10) Admin konfigurieren
Datei `library/admin.py` komplett ersetzen:
```python
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Book, Booking, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'total_copies', 'available_copies')
    list_filter = ('category',)
    search_fields = ('title', 'author')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'status', 'booked_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('student__username', 'book__title')
    actions = ('action_cancel', 'action_mark_borrowed', 'action_mark_returned')

    @admin.action(description='Set selected bookings to cancelled')
    def action_cancel(self, request, queryset):
        updated = 0
        for booking in queryset:
            try:
                booking.cancel_by_admin()
                updated += 1
            except ValidationError:
                continue
        self.message_user(request, f'{updated} booking(s) set to cancelled.')

    @admin.action(description='Set selected bookings to borrowed')
    def action_mark_borrowed(self, request, queryset):
        updated = 0
        for booking in queryset:
            try:
                booking.mark_as_borrowed()
                updated += 1
            except ValidationError:
                continue
        self.message_user(request, f'{updated} booking(s) set to borrowed.')

    @admin.action(description='Set selected bookings to returned')
    def action_mark_returned(self, request, queryset):
        updated = 0
        for booking in queryset:
            try:
                booking.mark_as_returned()
                updated += 1
            except ValidationError:
                continue
        self.message_user(request, f'{updated} booking(s) set to returned.')
```

## 11) Templates erstellen
Ordnerstruktur:
```txt
templates/
  base.html
  registration/
    login.html
  library/
    book_list.html
    my_bookings.html
```

Datei `templates/base.html`:
```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bibliothekssystem</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; }
        nav a { margin-right: 1rem; }
        .msg-success { color: #0a7a0a; }
        .msg-error { color: #b40000; }
        table { border-collapse: collapse; width: 100%; margin-top: 1rem; }
        th, td { border: 1px solid #ddd; padding: 0.5rem; text-align: left; }
    </style>
</head>
<body>
    <nav>
        {% if user.is_authenticated %}
            <a href="{% url 'book_list' %}">Bücher</a>
            <a href="{% url 'my_bookings' %}">Meine Buchungen</a>
            <form method="post" action="{% url 'logout' %}" style="display:inline;">
                {% csrf_token %}
                <button type="submit">Logout</button>
            </form>
        {% endif %}
    </nav>

    {% if messages %}
        <ul>
            {% for message in messages %}
                <li class="msg-{{ message.tags }}">{{ message }}</li>
            {% endfor %}
        </ul>
    {% endif %}

    {% block content %}{% endblock %}
</body>
</html>
```

Datei `templates/registration/login.html`:
```html
{% extends 'base.html' %}

{% block content %}
<h1>Login</h1>
<p>Bitte melde dich mit deinem Benutzerkonto an.</p>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Einloggen</button>
</form>
{% endblock %}
```

Datei `templates/library/book_list.html`:
```html
{% extends 'base.html' %}

{% block content %}
<h1>Bücherkatalog</h1>

<table>
    <thead>
        <tr>
            <th>Titel</th>
            <th>Autor</th>
            <th>Kategorie</th>
            <th>Verfügbar</th>
            <th>Gesamt</th>
            <th>Aktion</th>
        </tr>
    </thead>
    <tbody>
    {% for book in books %}
        <tr>
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.category.name }}</td>
            <td>{{ book.available_copies }}</td>
            <td>{{ book.total_copies }}</td>
            <td>
                {% if book.available_copies > 0 %}
                    <form method="post" action="{% url 'create_booking' book.id %}">
                        {% csrf_token %}
                        <button type="submit">Buchen</button>
                    </form>
                {% else %}
                    Nicht verfügbar
                {% endif %}
            </td>
        </tr>
    {% empty %}
        <tr>
            <td colspan="6">Keine Bücher vorhanden.</td>
        </tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}
```

Datei `templates/library/my_bookings.html`:
```html
{% extends 'base.html' %}

{% block content %}
<h1>Meine Buchungen</h1>

<table>
    <thead>
        <tr>
            <th>Buch</th>
            <th>Status</th>
            <th>Gebucht am</th>
            <th>Aktion</th>
        </tr>
    </thead>
    <tbody>
    {% for booking in bookings %}
        <tr>
            <td>{{ booking.book.title }}</td>
            <td>{{ booking.get_status_display }}</td>
            <td>{{ booking.booked_at }}</td>
            <td>
                {% if booking.status == 'booked' %}
                    <form method="post" action="{% url 'cancel_booking' booking.id %}">
                        {% csrf_token %}
                        <button type="submit">Stornieren</button>
                    </form>
                {% else %}
                    -
                {% endif %}
            </td>
        </tr>
    {% empty %}
        <tr>
            <td colspan="4">Du hast noch keine Buchungen.</td>
        </tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}
```

## 12) Migrationen ausführen
```powershell
python manage.py makemigrations library
python manage.py migrate
```

Erwartung: Migrationen für `library` und Standard-Apps werden erfolgreich angewendet.

## 13) Testdatei für Logiktests
Datei `library/tests.py` komplett ersetzen:
```python
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Book, Booking, Category


class BookingWorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='student1', password='test12345')
        self.category = Category.objects.create(name='Programming')
        self.book = Book.objects.create(
            title='Django Basics',
            author='Team Tutorial',
            category=self.category,
            total_copies=3,
            available_copies=3,
        )

    def test_create_booking_reduces_available_copies(self):
        Booking.create_booking(self.user, self.book)
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 2)

    def test_cancel_booking_increases_available_copies(self):
        booking = Booking.create_booking(self.user, self.book)
        booking.cancel_by_student()
        self.book.refresh_from_db()
        booking.refresh_from_db()
        self.assertEqual(self.book.available_copies, 3)
        self.assertEqual(booking.status, Booking.Status.CANCELLED)

    def test_returned_booking_restores_inventory(self):
        booking = Booking.create_booking(self.user, self.book)
        booking.mark_as_borrowed()
        booking.mark_as_returned()
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 3)

    def test_cannot_book_unavailable_book(self):
        self.book.available_copies = 0
        self.book.save(update_fields=['available_copies'])
        with self.assertRaises(ValidationError):
            Booking.create_booking(self.user, self.book)
```

Tests starten:
```powershell
python manage.py test
```

## 14) Superuser erstellen und Testdaten anlegen
Superuser:
```powershell
python manage.py createsuperuser
```

Danach Server starten:
```powershell
python manage.py runserver
```

Aufrufen:
- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

Admin-Testdaten anlegen:
1. Kategorie erstellen (z. B. `Programming`)
2. Buch erstellen (`total_copies=5`, `available_copies=5`)
3. Student-User in Admin anlegen
4. Als Student einloggen und Buch buchen
5. Prüfen: `available_copies` sinkt
6. Buchung stornieren
7. Prüfen: `available_copies` steigt wieder

## 15) Smoke-Check (Muss funktionieren)
- Login funktioniert
- Buchliste zeigt Verfügbarkeit
- Buchen reduziert Bestand
- Storno erhöht Bestand
- Admin kann Status per Aktion setzen (`cancelled`, `borrowed`, `returned`)

## 16) Typische Fehler und Lösungen
- **`No module named django`**  
  -> `pip install -r requirements.txt`
- **Migration-Fehler**  
  -> prüfen, ob `library` in `INSTALLED_APPS` steht
- **Template not found**  
  -> `TEMPLATES['DIRS'] = [BASE_DIR / 'templates']` prüfen
- **Login redirectet falsch**  
  -> `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` prüfen

## 17) Warum dieses Projekt für Anfänger gut ist
- Klein genug, um alles zu verstehen
- Trotzdem echte Praxis: Auth, CRUD, Business-Regeln, Admin
- Klare Trennung: Models (Daten), Views (Logik), Templates (UI)
