<p align="center">
  <img src="logo.png" alt="BlaulichtSMS Dashboard Logo" width="200">
</p>

# BlaulichtSMS Dashboard für Home Assistant

Eine Home Assistant Custom Component, um aktive Einsatzalarme von [BlaulichtSMS](https://blaulichtsms.net/) abzufragen und darzustellen.

## Eigenschaften
- Fragt die BlaulichtSMS Dashboard API ab.
- Asynchrones Polling.
- Eigener Sensor mit Einsatzdetails (Ort, alarmierte Gruppen, Anzahl Zugesagt/Abgesagt).
- Einfache Einrichtung über die Home Assistant Benutzeroberfläche.

## Installation via HACS (Empfohlen)

1. Öffne **HACS** in deiner Home Assistant Instanz.
2. Klicke auf **Integrationen**.
3. Klicke oben rechts auf das Drei-Punkte-Menü und wähle **Benutzerdefinierte Repositories**.
4. Füge die URL dieses GitHub Repositories ein.
5. Wähle als Kategorie **Integration**.
6. Klicke auf Hinzufügen.
7. Suche nun in HACS nach "BlaulichtSMS Dashboard" und klicke auf "Herunterladen".
8. Starte Home Assistant neu.
9. Gehe zu **Einstellungen -> Geräte & Dienste -> Integration hinzufügen**, suche nach "BlaulichtSMS Dashboard" und gib deine Zugangsdaten ein.

## Manuelle Installation

1. Lade dir dieses Repository als ZIP herunter.
2. Entpacke den Ordner `custom_components/blaulichtsms_dashboard` in dein Home Assistant `custom_components` Verzeichnis.
3. Starte Home Assistant neu.
4. Richte die Integration über **Einstellungen -> Geräte & Dienste** ein.
