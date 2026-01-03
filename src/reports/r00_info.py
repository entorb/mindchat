"""Selbstauskunft."""

import streamlit as st

st.markdown(
    """
# Info

## Haftungsausschluss

Dies ist eine KI-basierte Chat-Anwendung, die Anreize und Tipps geben könnte. Sie ersetzt **NICHT** professionelle Hilfe. Bei ernsthaften Problemen wende Dich bitte an qualifizierte Fachkräfte, zB unter 0800 - 111 0 111 (Telefonseelsorge)

## Funktionsweise

- Ausfüllen einer Selbstauskunft
- Chat mit einem KI-'Therapeuten', der Deine Selbstauskunft als Kontext für Chat und Vorschläge verwendet

## Datenschutz

- Deine Daten werden nur im Speicher verarbeitet und nicht auf dem Server oder in einer Datenbank gespeichert. Alle Daten werden beim Logout und Sitzungsende gelöscht.
- **Achtung:** Deine Daten werden von der OpenAI KI über deren API verarbeitet.
- Die Kommunikation ist über HTTPS verschlüsselt.
- Der Quellcode dieser App ist öffentlich auf [GitHub](https://github.com/entorb/mindchat) verfügbar.

## Technologie

Die Anwendung verwendet Python 3.11, Streamlit, UV, SonarQube für statische Code-Analyse, Matomo für Zugriffsstatistiken (ohne personenbezogene Daten) und Sentry für Fehlermeldungen (ohne Benutzerdaten).
        """  # noqa: E501
)
