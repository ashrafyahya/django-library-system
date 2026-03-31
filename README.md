# Django Bibliotheksystem

Ein einfaches Bibliothekverwaltungssystem mit Buchkatalog, Buchungslogik und Benutzeranmeldung.

## 🚀 Projektübersicht

- Django-Projekt: `bibliotheksystem`
- App: `library`
- Datenbank: SQLite (`db.sqlite3`)
- Kernmodelle: `Category`, `Book`, `Booking`
- Buchstatus: gebucht, storniert, ausgeliehen, zurückgegeben
- Benutzer: einfache Anmeldung über Django Auth

## ✨ Features

- Kategorieverwaltung (Admin)
- Buchkatalog anzeigen
- Buchung erstellen (wenn verfügbar)
- Eigene Buchungen anzeigen
- Buchung stornieren (Status `booked`)
- Verfügbarkeitsverwaltung (`available_copies` wird atomar aktualisiert)
- Grundlegende Testabdeckung definiert in `library/tests.py`
