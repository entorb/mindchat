"""Texts."""

# ruff: noqa: E501

# Main app texts
app_title = "Mind Chat"
main_llm_settings_title = "KI Einstellungen"
main_llm_label = "LLM"
main_model_label = "Modell"
main_error_llm_provider = "❌ LLM Fehler: {}"
main_info_check_config = (
    "Überprüfe die Konfiguration oder wähle einen anderen LLM Provider."
)
main_error_unexpected = "Ein unerwarteter Fehler ist aufgetreten."

# Login texts
login_dialog_title = "Login erforderlich"
login_prompt = "Frage Torben nach dem Geheimnis, da die Nutzung Kosten verursacht."
login_input_label = "Geheimnis"
login_btn_label = "Anmelden"
login_error_wrong = "Falsch!"


r00_title = "Info"

r00_info = """
Falls auf dem Handy die Navigation links nicht angezeigt wird, oben links auf `>>` klicken.

## ⚠️ Wichtiger Haftungsausschluss

Dies ist eine KI-basierte Chat-Anwendung, die Anreize und Tipps geben kann. Sie ersetzt **NICHT** professionelle Hilfe!
Bei ernsthaften psychischen Problemen oder in Krisensituationen wende Dich bitte an qualifizierte Fachkräfte, z.B.  Telefonseelsorge 0800-1110111

## 💡Funktionsweise

Die Anwendung funktioniert in zwei Schritten:

1. **Selbstauskunft:** Fülle zunächst eine strukturierte Selbstauskunft aus, in der Du Dich, Deine Situation und Deine Anliegen beschreibst
2. **KI-Chat:** Chatte anschließend mit der KI, die Deine Selbstauskunft als Kontext nutzt

Die Kosten für die KI-Aufrufe trägt Torben, daher ist diese Anwendung mit einem Passwort versehen.

## 🔐 Datenschutz

Technisch versierte Menschen können diese diese Anwendung gerne auf dem eigenen Computer mit einer selbst-geosteten KI verwenden. Siehe dazu diese [Anleitung](https://github.com/entorb/mindchat/blob/main/README.md#run-locally).

### Datenspeicherung auf diesem Server
- Deine Daten werden **nicht** dauerhaft gespeichert, sondern nur temporär im Arbeitsspeicher gehalten
- Beim Logout und Sitzungsende werden alle Daten automatisch gelöscht
- Der Entwickler dieser App hat **keinen Zugriff** auf Deine Eingaben oder Chat-Verläufe

### Verarbeitung durch OpenAI
- **Wichtig:** Deine Eingaben werden zur Verarbeitung an die (kostenpflichtige) KI von OpenAI (GPT-Modell) gesendet. [OpenAI](https://platform.openai.com/docs/guides/your-data) erklärt: "Your data is your data. As of March 1, 2023, data sent to the OpenAI API is not used to train or improve OpenAI models (unless you explicitly opt in to share data with us)."
- **Alternative 1:** Ein persönlichen ChatGPT, Mistral, DeepSeek, ... Account. Dieser hat aber gegenüber dieser App den Nachteil, dass OpenAI dort Deine Daten direkt Deiner Person zuordnen kann. Hier hingegen nur dieser App.
- **Alternative 2:** Diese App lokal auf Deinem Rechner laufen lassen und eine lokale KI verwenden, siehe Hinweis oben.
- Die Kommunikation erfolgt verschlüsselt über HTTPS

### Open Source
- Der Quellcode dieser App ist öffentlich auf [GitHub](https://github.com/entorb/mindchat) einsehbar - jeder kann ihn prüfen und verbessern.
"""


r01_title = "Selbstauskunft"

r01_self_info = """
Fülle diese Selbstauskunft aus, damit Du mit der KI über Dich chatten kannst

- ⏰ **Nimm Dir Zeit:** Je genauer und ausführlicher Du Dich beschreibst, desto hilfreicher werden die KI-Antworten.
- 📋 **Struktur:** Zeilen mit '##' sind Überschriften - lösche gerne irrelevante Abschnitte oder füge eigene hinzu.
- 🔐 **Privatsphäre:** Gib **keine** persönlichen Daten wie Namen, Adressen etc. ein.
- 💡**Optional**
  - **Lokal speichern:** Falls Du diese App später nochmal nutzen möchtest, speichere Deine Selbstauskunft auf Deinem Gerät, denn beim Abmelden werden alle Daten vom Server gelöscht.
  - **KI-Feedback:** Nutze den Button unten, um ein KI-Feedback zur Selbstauskunft zu erhalten.
"""

r01_textarea_label = "Verfassen der Selbstauskunft"
r01_btn_download = "Download"

# Feedback section
r01_header_feedback = "Feedback"
r01_btn_feedback = "KI Feedback einholen"
r01_feedback_prompt = """
Die folgende Selbstauskunft soll später für ein Gespräch mit einem Psychotherapeuten verwendet werden.

Deine Aufgabe ist es, den Text zu überprüfen und Vorschläge zur Verbesserung zu machen.

- schlage Verbesserungen des Textes vor
- halte dich kurz
- führe keine Psychoanalyse durch
- prüfe auf Inkonsistenzen und Redundanzen
- behalte die Kapitel-Struktur unverändert
- schlage weitere Kapitel vor, falls relevante fehlen
- Ausgabe in Markdown Format
"""


r02_title = "Chat"
r02_chat_info = """
Hier kannst Du ein 'Selbstgespräch' mit der KI führen.

Vorschläge für Fragen:
- Was sind meine Stärken?
- Worauf sollte ich achten?
- Wie kann ich meine Probleme lösen?
"""

r02_missing_sd = "Selbstauskunft ist leer"
r02_chat_input = "Stelle eine Frage..."
r02_prompt_prefix = "Du bist ein einfühlsamer und professioneller Psychotherapeut, der diese Person berät:\n"

r02_hist_btn_download = "Download Chatverlauf"
r02_hist_btn_del = "Chat-Verlauf löschen"

r02_export_title = "Chat-Verlauf"
r02_export_heading0 = "KI Anweisung"
r02_export_user_you = "Du"
r02_export_user_ai = "KI"


r99_title = "Logout"
r99_logout = """
## ✅ Erfolgreich abgemeldet

Deine Daten wurden aus dem Arbeitsspeicher des Servers gelöscht
"""


SPINNER_MESSAGES = [
    "Magic happens…",
    "Schmelze Gletscher…",
    "Falte Raum, Zeit und Tokens…",
    "Zeit zum Durchatmen…",
]
