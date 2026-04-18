# Django Demo-Projekt

Dieses Repository verbindet **Lernmaterial** mit einer lauffähigen **Django-Webanwendung**: Es gibt eine Einführung in Django (Geschichte, Struktur, Funktionsweise) sowie ein schrittweises Tutorial zum Aufbau eines **Bibliotheksystems**.

## Lernmaterial & Tutorials

| Inhalt | Datei |
|--------|--------|
| **Einführung zu Django** – Hintergrund, MVT (Model–View–Template), Modelle, Views, Templates | [`einführung.ipynb`](einführung.ipynb) |
| **Tutorial: Bibliotheksystem** – Projektaufbau, Models, Views, URLs, Templates, Workflow mit `manage.py` | [`bibliotheksystem.ipynb`](bibliotheksystem.ipynb) |

Die Notebooks liegen im **Projektstamm**. Bilder für die Einführung befinden sich im Ordner [`bilder/`](bilder/). Zum Bearbeiten der Notebooks eignen sich Jupyter Lab, VS Code/Cursor mit Jupyter-Erweiterung oder vergleichbare Umgebungen.


## Bibliotheksystem

Ein einfaches Bibliothekverwaltungssystem mit Buchkatalog, Buchungslogik und Benutzeranmeldung.

### Projektübersicht

- Django-Projekt: `bibliotheksystem`
- App: `library`
- Datenbank: SQLite (`db.sqlite3`)
- Kernmodelle: `Category`, `Book`, `Booking`
- Buchstatus: gebucht, storniert, ausgeliehen, zurückgegeben
- Benutzer: einfache Anmeldung über Django Auth

### Features

- Kategorieverwaltung (Admin)
- Buchkatalog anzeigen
- Buchung erstellen (wenn verfügbar)
- Eigene Buchungen anzeigen
- Buchung stornieren (Status `booked`)
- Verfügbarkeitsverwaltung (`available_copies` wird atomar aktualisiert)
- Grundlegende Testabdeckung definiert in `library/tests.py`


## Projekt starten

Voraussetzungen: **Python 3** (empfohlen: aktuelle 3.x-Version).

1. **Virtuelle Umgebung** (empfohlen, im Projektstamm):

   ```bash
   python -m venv .venv
   ```

   Unter Windows (PowerShell) aktivieren:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Abhängigkeiten installieren** (Django ist in [`bibliotheksystem/requirements.txt`](bibliotheksystem/requirements.txt) festgepinnt):

   ```bash
   pip install -r bibliotheksystem/requirements.txt
   ```

3. **In das Django-Projekt wechseln** und **Migrationen** ausführen (legt u. a. die SQLite-Datenbank an):

   ```bash
   cd bibliotheksystem
   python manage.py migrate
   ```

4. **Entwicklungsserver starten**:

   ```bash
   python manage.py runserver
   ```

   Standardmäßig ist die Anwendung unter **http://127.0.0.1:8000/** erreichbar.

Optional: **Superuser für den Admin-Bereich** anlegen:

```bash
python manage.py createsuperuser
```

Der Admin ist unter **http://127.0.0.1:8000/admin/** erreichbar.

---

### Datenbankinhalt anzeigen

Die Datenbank liegt unter `bibliotheksystem/db.sqlite3` (SQLite). So kannst du Inhalte einsehen:

1. **Django Admin (visuell)** — Modelle sind in `library/admin.py` registriert. Superuser anlegen (falls noch nicht), Server starten, dann **http://127.0.0.1:8000/admin/** öffnen. Dort siehst du Kategorien, Bücher, Buchungen und Nutzer.

2. **Django-Shell (ORM)** — Im Ordner `bibliotheksystem`:

   ```bash
   python manage.py shell
   ```

   Beispiel:

   ```python
   from library.models import Book, Category, Booking
   Book.objects.all()
   Category.objects.all()
   Booking.objects.all()
   ```

3. **SQL über Django** — Im Ordner `bibliotheksystem`:

   ```bash
   python manage.py dbshell
   ```

   Beispiel:

   ```sql
   .tables
   SELECT * FROM library_book;
   SELECT * FROM library_booking;
   SELECT * FROM library_category;
   ```

4. **SQLite direkt** (wenn das Programm `sqlite3` installiert ist), vom Projektstamm aus:

   ```bash
   sqlite3 bibliotheksystem/db.sqlite3 ".tables"
   ```


