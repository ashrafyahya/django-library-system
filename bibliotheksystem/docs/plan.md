# Django Bibliothekssystem - Umsetzungsplan

## Zweck
Dieses Dokument definiert die Anforderungen und Regeln fuer das Tutorial-Projekt.  
Ziel ist ein **einfaches, klares und reproduzierbares** Django-Anfaengerprojekt.

## Verbindliche Regeln
- Code, Klassen, Funktionsnamen und Dateinamen: **EN**
- Tutorialtexte, Erklaerungen und Kommentare: **DE**
- Plattform fuer Befehle: **Windows PowerShell**
- Tech-Stack: **Python 3.12**, **Django 5.1.x**, **SQLite**
- Reproduzierbarkeit: Es werden nur Schritte umgesetzt, die im Tutorial dokumentiert sind.

## Fachliche Anforderungen (MVP)
- Studierende koennen:
  - Buchliste ansehen
  - verfuegbare Anzahl sehen
  - Buch buchen
  - Buchung stornieren
  - Liste eigener Buchungen nach Status sehen
- Status in Buchungen:
  - `booked`
  - `cancelled`
  - `borrowed`
  - `returned`
- Bestandslogik:
  - Bei Buchung: `available_copies - 1`
  - Bei Storno: `available_copies + 1`
  - Bei Rueckgabe (`returned`): `available_copies + 1`
- Bibliothek unterstuetzt Bucharten/Kategorien.
- Admin kann:
  - Buecher anlegen, bearbeiten, loeschen
  - Buchungen auf `cancelled`, `borrowed`, `returned` setzen

## Technische Struktur
- Django-Projekt: `config`
- Django-App: `library`
- Modelle:
  - `Category`
  - `Book`
  - `Booking`
- UI:
  - Login
  - Buchkatalog
  - Eigene Buchungen
- Admin:
  - Verwaltung fuer Kategorien, Buecher, Buchungen
  - Admin-Aktionen fuer Statuswechsel

## Didaktische Anforderungen an das Tutorial
- Jeder Schritt enthaelt:
  - Ziel des Schritts
  - exakten Befehl/Code
  - erwartetes Ergebnis
- Fachbegriffe werden kurz erklaert (z. B. Migration, Model, View, Template).
- Troubleshooting-Sektion fuer typische Fehler ist Pflicht.

## Selbstkritik und Nachschaerfung
- Risiko: Zu viel auf einmal fuer Anfaenger.  
  Gegenmassnahme: MVP strikt halten, keine komplexen Zusatzfeatures.
- Risiko: Abweichungen bei Versionen.  
  Gegenmassnahme: Versionen und Befehle im Tutorial explizit fixieren.
- Risiko: Inventarzaehler wird bei Statuswechseln inkonsistent.  
  Gegenmassnahme: Statusregeln klar beschreiben und in Modellmethoden zentral umsetzen.

## Akzeptanzkriterien
- Tutorial kann 1:1 durchgefuehrt werden.
- Buchen/Stornieren/Rueckgabe veraendert `available_copies` korrekt.
- Studierenden-Flow und Admin-Flow sind funktional.
- Einsteiger verstehen Aufbau und Begriffe ohne Vorwissen.
