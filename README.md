<p align="center">
  <img src="https://raw.githubusercontent.com/seipekm/ha-blaulichtsms-dashboard/main/logo.png" alt="BlaulichtSMS Dashboard Logo" width="200">
</p>

# BlaulichtSMS Dashboard für Home Assistant

Eine Home Assistant Custom Component, um aktive Einsatzalarme von [BlaulichtSMS](https://blaulichtsms.net/) abzufragen und darzustellen.

## Eigenschaften
- Fragt die BlaulichtSMS Dashboard API ab.
- Asynchrones Polling.
- Eigener Sensor mit Einsatzdetails (Ort, alarmierte Gruppen, Anzahl Zugesagt/Abgesagt).
- Einfache Einrichtung über die Home Assistant Benutzeroberfläche.

## Voraussetzungen

Bevor du diese Integration nutzen kannst, musst du zwingend ein **Dashboard (Einsatzmonitor)** in BlaulichtSMS angelegt haben. Die Integration loggt sich in dieses Dashboard ein, um die Daten abzurufen.

1. Logge dich unter [start.blaulichtsms.net](https://start.blaulichtsms.net) in die Web-Plattform ein.
2. Gehe im Menü auf **Einsatzmonitor** -> **Anzeige & Konfiguration**.
3. Klicke auf **Neuen Einsatzmonitor anlegen**.
4. Vergib einen Namen und ein Passwort.
*(Genau diese speziellen Dashboard-Zugangsdaten benötigst du später für die Einrichtung in Home Assistant!)*
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

## Automatisierungs-Beispiel

Sobald ein Einsatz eingeht, wechselt der Sensor **Einsatzstatus** von `Inaktiv` auf `Aktiv`. Nach einer Stunde ohne neues Alarm-Datum wechselt er automatisch zurück. Diesen Statuswechsel kannst du optimal als Auslöser (Trigger) für Home Assistant Automatisierungen nutzen.

Hier ist ein Beispiel, wie du bei einem Alarm automatisch das Licht einschaltest und eine Push-Nachricht mit dem Einsatzort auf dein Handy schickst:

```yaml
alias: "Feuerwehr: Neuer Alarm (BlaulichtSMS)"
description: "Wird ausgelöst, wenn ein neuer Alarm über BlaulichtSMS reinkommt."
mode: single

trigger:
  - platform: state
    entity_id: sensor.blaulichtsms_einsatzstatus
    from: "Inaktiv"
    to: "Aktiv"

action:
  # 1. Licht im Flur einschalten (Beispiel)
  - service: light.turn_on
    target:
      entity_id: light.flur
    data:
      brightness_pct: 100
      color_name: red

  # 2. Eine Push-Benachrichtigung mit allen Infos an dein Handy schicken
  - service: notify.notify
    data:
      title: "🚨 FEUERWEHR EINSATZ 🚨"
      message: >
        Alarmierungs-Text: {{ states('sensor.blaulichtsms_alarm_text') }}
        
        Einsatzort: {{ states('sensor.blaulichtsms_einsatzort') }}
        Alarmierte Gruppen: {{ states('sensor.blaulichtsms_alarm_gruppen') }}
```
