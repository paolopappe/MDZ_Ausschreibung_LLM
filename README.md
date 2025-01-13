# Prusseit und Reiss - Suchtool für Ausschreibungstexte

* [Übersicht](#übersicht)
* [Installation](#installation)
* [Benutzung](#benutzung)


## Übersicht

Das Tool hilft mit der Suche von relevanten Informationen in den Ausschreibungen nach einer freiförmigen Anfrage.

Es funktioniert folgendermaßen:

1. Die PDF-Ausschreibungen werden vorbearbeitet: sie werden nach Kapiteln, Abschnitten uws. auf Chunks geteilt, wo es mit dem LLM für jeden Chunk Stichwörter generiert werden, worum es sich im Chunk handelt.
2. Das Tool nimmt eine Suchanfrage an und extrahiert daraus auch Stichwörter, also was der/die Nutzer*in mit der Anfrage finden möchte.
3. Die von der Anfrage extrahierten und in den vorbereiteten Daten liegenden Stichwörter werden nach semantyscher Ähnlichkeit abgegliechen, und dem/der Nutzer*in werden die Chunks zurückgegeben, die am nächsten zur Anfrage stehen.

Mehr Informationen zum Ansatz finden Sie in der [Präsentation](./Prusseit_u_Reiss_aktueller_Stand.pptx).


## Installation

### Voraussetzungen

1. Sie müssen auf Ihrem Gerät Git haben. Wenn Sie es noch nicht haben, installieren Sie es von https://git-scm.com.
1. Wenn Sie noch Docker Desktop App auf dem Gerät nicht haben, installieren Sie sie von https://www.docker.com/products/docker-desktop/.
2. Das Tool benutzt das OpenAI GPT-4. Daher müssen Sie einen OpenAI-Account erstellen, wenn Sie ihn noch nicht haben: https://platform.openai.com/docs/overview, und einen API-Key erteilen lassen unter https://platform.openai.com/settings/organization/api-keys. **Der API-Key darf in keinem Fall weitergeleitet werden!**


### Installationsschritte

1. Die Docker Desktop App laufen.

2. Das Repo mit dem Tool-Source-Code clonen. Dafür Terminal (Git Bash) öffnen und die folgenden Kommande eingeben:

```bash
cd pfad/zu/ihrem/ziel/ordner

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