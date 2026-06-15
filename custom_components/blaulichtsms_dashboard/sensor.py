"""Sensor platform for BlaulichtSMS Dashboard."""
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the BlaulichtSMS sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([BlaulichtSMSEinsatzSensor(coordinator)])


class BlaulichtSMSEinsatzSensor(CoordinatorEntity, SensorEntity):
    """Representation of a BlaulichtSMS Sensor."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:fire-truck"

    def __init__(self, coordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"blaulichtsms_{coordinator.customer_id}_einsatzstatus"
        self._attr_name = "Einsatzstatus"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        # Aktiv, wenn mindestens ein Alarm in der Liste ist
        if self.coordinator.data:
            return "Aktiv"
        return "Inaktiv"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        alarms = self.coordinator.data or []
        attributes = {
            "aktive_alarme_anzahl": len(alarms),
            "alarme_details": alarms,
        }

        # Falls ein Einsatz aktiv ist, extrahieren wir die Details des aktuellsten Alarms
        if alarms:
            latest_alarm = alarms[0]
            attributes["alarm_text"] = latest_alarm.get("alarmText", "Unbekannt")
            attributes["alarm_date"] = latest_alarm.get("alarmDate", "Unbekannt")
            attributes["alarm_autor"] = latest_alarm.get("authorName", "Unbekannt")
            
            # Alarmgruppen auslesen
            groups = latest_alarm.get("alarmGroups", [])
            attributes["alarm_gruppen"] = ", ".join(g.get("groupName", "") for g in groups if g.get("groupName"))
            
            # Anzahl der alarmierten Personen
            attributes["anzahl_alarmiert"] = latest_alarm.get("usersAlertedCount", 0)
            
            # Rückmeldungen auswerten
            recipients = latest_alarm.get("recipients", [])
            attributes["teilnehmer_zugesagt"] = sum(1 for r in recipients if r.get("participation") == "yes")
            attributes["teilnehmer_abgesagt"] = sum(1 for r in recipients if r.get("participation") == "no")
            attributes["teilnehmer_ausstehend"] = sum(1 for r in recipients if r.get("participation") == "pending")
            
            # Geolocation / Adresse
            geo = latest_alarm.get("geolocation", {})
            if geo and geo.get("address"):
                attributes["einsatzort"] = geo.get("address")
            elif latest_alarm.get("coordinates"):
                attributes["einsatzort_koordinaten"] = latest_alarm.get("coordinates")

        return attributes
