# Prusseit und Reiss - Suchtool für Ausschreibungstexte

* [Übersicht](#übersicht)
* [Installation](#installation)
* [Benutzung](#benutzung)


## Übersicht

Das Tool hilft bei der Suche nach relevanten Informationen in Ausschreibungstexten.

Funktionsweise:

1. Die PDF-Ausschreibungen werden vorbearbeitet: 
sie werden nach Kapiteln, Abschnitten usw. in Chunks unterteilt. Ein LLM generiert für jeden Chunk Stichwörter, die auf meta-Ebene beschreiben, worum es sich in dem jeweiligen Chunk handelt.
2. Das Tool nimmt eine Suchanfrage an und extrahiert daraus auch Stichwörter, also was der/die Nutzer*in mit der Anfrage suchen möchte.
3. Die von der Anfrage extrahierten und in den vorbereiteten Daten liegenden Stichwörter werden nach semantischer Ähnlichkeit abgeglichen, und dem/der Nutzer*in werden die Chunks ausgegeben, die am ehesten zur Anfrage passen.

Weitere Informationen zum Ansatz finden Sie in der [Präsentation](./Prusseit_u_Reiss_aktueller_Stand.pptx).


## Installation

### Voraussetzungen

1. Git: Sie müssen auf Ihrem Gerät Git installiert haben. Wenn Sie es noch nicht installiert haben, installieren Sie es von der Webseite https://git-scm.com.
1. Docker Desktop App: Wenn Sie die Docker Desktop App noch nicht auf Ihrem Gerät installiert haben, laden Sie es bitte unter https://www.docker.com/products/docker-desktop/ herunter und folgen den Installationsanweisungen.
2. Das Tool benutzt das OpenAI GPT-4 Modell, daher müssen Sie einen OpenAI-Account erstellen, wenn Sie ihn noch nicht haben: https://platform.openai.com/docs/overview, und einen API-Key erteilen lassen unter https://platform.openai.com/settings/organization/api-keys. **Ihr API-Key sollte in keinem Fall weitergegeben werden!**


### Installationsschritte

1. Die Docker Desktop App starten.

2. Das github-Repo (s.u.) auf Ihr Gerät klonen. 
Dazu öffnen/erstellen Sie in Ihrem Windows-Explorer unter dem gewünschten Pfad den/einen Ordner, unter dem Sie das Tool speichern möchten.
Machen Sie dort (in diesem Explorer-Fenster) einen Rechtsklick und öffnen Sie Git Bash. 
Geben Sie in Git Bash nacheinander die folgenden Befehle ein (jeweils danach mit der Enter-Taste bestätigen).
(Ggf. funktioniert Str+v zum hinein kopieren nicht. Stattdessen Rechtsklick + Einfügen):

```bash

git clone https://github.com/paolopappe/MDZ_Ausschreibung_LLM.git

cd MDZ_Ausschreibung_LLM
```

3. Den API-Key in den File _env.template_ einsetzen und den File auf _.env_ umbenennen.

4. Den Docker-Image erstellen: das macht Ihre eigene Kopie des Tools auf Ihrem Gerät. In Terminal den Kommand eingeben:

```bash
docker build -t prusseit_reiss_suchtool:latest . 
```

Es wird wenige Minuten brauchen.

5. Jetzt starten Sie das Tool.

```bash
docker run -p 8501:8501 --env-file .env --volume prusseit_reiss:/ausschreibungen_storage prusseit_reiss_suchtool:latest
```

6. Nachdem Sie den letzten Kommand ausgeführt haben, läuft auf Ihrem Gerät das Tool. Um darauf zuzugreifen, gehen Sie auf den beliebigen Browser und geben Sie ein:

```text
http://localhost:8501
```


## Benutzung

1. Als erstes sollen Sie die Ausschreibungen auf das Tool hochladen. Das machen Sie direkt im Tool im Tab "Datenverwaltung". Die Vorbereitung dauert eine Zeit, weil es die Stichwörter mit dem LLM extrahiert werden. **Das muss nur einmal nach der Installation gemacht werden**, die Daten werden also gespeichert. Sie können später weitere Ausschreibungen dazuladen oder alte entfernen.

2. Gehen Sie dann auf den Tab Suche und geben Ihre Anfrage ein.

3. Nach der Benutzung stoppen Sie den Container, indem Sie im selben Terminal _Ctrl+C_ clicken.

4. Für wiederholte Benutzung brauchen Sie nach der Installation nur Punkte 5 und 6 des Abschnitts [Installationsschritte](#installationsschritte) durchführen (aus dem Ordner _MDZ_Ausschreibung_LLM_ aus dem 2. Punkt).
