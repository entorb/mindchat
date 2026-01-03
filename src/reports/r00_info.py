"""Selbstauskunft."""

import streamlit as st

st.markdown(
    """
# Info

Falls auf dem Handy die Navigation links nicht angezeigt wird, oben links auf den Pfeil klicken.

## Haftungsausschluss

Dies ist eine KI-basierte Chat-Anwendung, die Anreize und Tipps geben könnte. Sie ersetzt **NICHT** professionelle Hilfe. Bei ernsthaften Problemen wende Dich bitte an qualifizierte Fachkräfte, zB unter 0800 - 111 0 111 (Telefonseelsorge)

## Funktionsweise

1. Ausfüllen einer Selbstauskunft
2. Chat mit einem KI-'Therapeuten', der Deine Selbstauskunft als Kontext für Chat und Vorschläge verwendet

## Datenschutz

- Deine Daten werden nur im Speicher verarbeitet und nicht auf dem Server oder in einer Datenbank gespeichert. Alle Daten werden beim Logout und Sitzungsende gelöscht.
- **Achtung:** Deine Daten werden von der OpenAI KI über deren API auf deren Server verarbeitet.
- Vorteil gegenüber einem persönlichem ChatGPT Account etc.: OpenAI kann Deine Daten nicht Deiner Person, sondern nur dieser App zuordnen.
- Der Quellcode dieser App ist öffentlich auf [GitHub](https://github.com/entorb/mindchat) verfügbar, so dass jeder ihn prüfen kann.

## Technologie

Diese Anwendung ist in Python Streamlit geschrieben und verwendet diese externen Dienst: OpenAI für KI, SonarQube für Code-Analyse, Matomo für Zugriffsstatistiken (lokale Instanz ohne personenbezogene Daten) und Sentry für Fehler-Tracking (ohne personenbezogene Daten).
        """  # noqa: E501
)
