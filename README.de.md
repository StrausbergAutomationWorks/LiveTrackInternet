# Live Track Internet

[English](README.md) · **Deutsch** · [Français](README.fr.md) · [Nederlands](README.nl.md) · [简体中文](README.zh-Hans.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Українська](README.uk.md) · [العربية](README.ar.md) · [Alle Sprachen](#sprachen)

**Internetausfälle, Seekabel und Glasfaserverbindungen für Home Assistant, auf
einer Karte.** Live Track Internet bringt die Internetausfälle, die Cloudflare
Radar irgendwo auf der Welt erfasst, mit ihrer Ursache auf Ihre
Home-Assistant-Karte. Es zeichnet außerdem jedes Seekabel mit seinen
Anlandepunkten und die Glasfaser- und Richtfunkverbindungen zwischen Orten, die
die ITU erfasst. Nennt ein Ausfall ein Kabel, wird dieses Kabel rot gezeichnet.

> **Live Track Internet ist ein Modul von Live Track**, einer Familie von
> Home-Assistant-Integrationen, die alles, was sich bewegt, und das Wetter,
> durch das es sich bewegt, auf einer gemeinsamen Karte zeigen: Flugzeuge,
> Schiffe, Züge und Wetter. Installieren Sie es allein oder neben den anderen
> Modulen ([Liste unten](#teil-von-live-track-die-anderen-module)).

> **Es wächst, und Ideen sind willkommen.** Live Track Internet deckt heute
> Ausfälle, Kabel und Landverbindungen weltweit ab, und wir fügen weitere
> Datenquellen hinzu (Internetknoten und Rechenzentren sind geplant). Fehlt
> etwas? [Schlagen Sie es vor](#helfen-sie-mit-es-zu-erweitern), oder fügen Sie
> es selbst hinzu: Wir helfen Ihnen dabei.

**Status: 0.3.1, veröffentlicht.** Dem Marketplace per Link
hinzugefügt ([unten](#installation-schritt-für-schritt)); im Katalog des
Marketplace ist es noch nicht.

Eigenes Werk von StrausbergAutomationWorks. Nicht verbunden mit oder
unterstützt von Cloudflare, Tristan Hotham, TeleGeography, der Internationalen
Fernmeldeunion (ITU) oder einem Kabeleigentümer oder Netzbetreiber.

> ⚠ **Keine Überwachung Ihrer eigenen Internetverbindung.** Die Ausfälle sind
> Einträge, die Menschen bei Cloudflare schreiben, oft Stunden nach Beginn
> eines Ausfalls, und nur für Ausfälle, die groß genug sind, um sie in
> Cloudflares Netz zu sehen. **Eine leere Karte heißt nicht, dass das Internet
> überall funktioniert.** Ein Kabel oder eine Verbindung auf der Karte sagt
> nichts darüber, ob dort heute Daten fließen.

---

## Inhalt

1. [Alles, was es kann](#alles-was-es-kann)
2. [Wo es funktioniert](#wo-es-funktioniert)
3. [Teil von Live Track: die anderen Module](#teil-von-live-track-die-anderen-module)
4. [Bevor Sie beginnen](#bevor-sie-beginnen)
5. [Installation, Schritt für Schritt](#installation-schritt-für-schritt)
6. [Einrichtung, Schritt für Schritt](#einrichtung-schritt-für-schritt)
7. [Kostenlose Schlüssel, die mehr freischalten, Schritt für Schritt](#kostenlose-schlüssel-die-mehr-freischalten-schritt-für-schritt)
8. [Die Karte auf ein Dashboard bringen](#die-karte-auf-ein-dashboard-bringen)
9. [In Automationen verwenden](#in-automationen-verwenden)
10. [Alles auf der Karte im Detail](#alles-auf-der-karte-im-detail)
11. [Alle Entitäten, die es anlegt](#alle-entitäten-die-es-anlegt)
12. [Was es sendet und herunterlädt](#was-es-sendet-und-herunterlädt)
13. [Helfen Sie mit, es zu erweitern](#helfen-sie-mit-es-zu-erweitern)
14. [Sprachen](#sprachen)
15. [Danksagungen und Lizenzen](#danksagungen-und-lizenzen)
16. [Stichwörter](#stichwörter)

---

## Alles, was es kann

### Auf der Karte, ohne Einrichtung

Jede dieser Ebenen hat ein eigenes Kästchen in der Ebenensteuerung der Karte.
Alle sind zu Beginn **aus**: Setzen Sie ein Häkchen, um sie zu zeigen.

| Was | Wo | Woher |
|---|---|---|
| **Alle Kabel**: jedes Seekabel, 608 in Betrieb und 105 geplant, als dünne Linien; ein Klick zeigt Name, Eigentümer, Länge und Anlandeländer | die ganze Welt | Tristan Hothams Datensatz der Kabeldaten von TeleGeography, mit der Integration ausgeliefert |
| **Anlandepunkte**: die 1.928 Orte, an denen Kabel an Land gehen, als kleine Punkte | die ganze Welt | dasselbe |
| **Landverbindungen**: Glasfaser- und Richtfunkverbindungen zwischen Orten an Land, gerade von einem Knoten zum nächsten gezeichnet | die Länder, in denen die ITU sie gesammelt hat ([wo](#wo-es-funktioniert)) | ITU Broadband Maps (BBmaps), einmal pro Woche von Ihrem Home Assistant abgerufen |

### Mit Ihrem eigenen kostenlosen Schlüssel oder Konto

| Kostenloser Schlüssel oder kostenloses Konto | Was es hinzufügt |
|---|---|
| **Cloudflare**-API-Token | **Ausfälle**: eine Markierung für jeden offenen Internetausfall, den Cloudflare Radar erfasst, in dem Land oder der Region, die er nennt, nach Ursache gefärbt und gezeichnet; standardmäßig an. **Kabel mit Störung**: jedes Seekabel, das ein offener Ausfall nennt, kräftig und rot gezeichnet; standardmäßig an |

Es ist in wenigen Minuten erstellt: [Schritt für Schritt unten](#kostenlose-schlüssel-die-mehr-freischalten-schritt-für-schritt).

---

## Wo es funktioniert

| Region | Was Sie bekommen | Woher | Was nötig ist |
|---|---|---|---|
| **Die ganze Welt** | Internetausfälle, in dem Land oder der Region, die jeder Eintrag nennt | Cloudflare Radar | ein kostenloses Token |
| **Die ganze Welt** | Seekabel mit Störung | Cloudflare Radar und die Kabeldaten | ein kostenloses Token |
| **Die ganze Welt** | alle Seekabel und Anlandepunkte | Tristan Hothams Datensatz der Daten von TeleGeography | nichts |
| **Afrika und Naher Osten** | etwa 5.400 Landverbindungen | ITU Broadband Maps | nichts |
| **Mittel- und Südamerika** | etwa 5.500 Landverbindungen | ITU Broadband Maps | nichts |
| **Europa** | etwa 12.400 Landverbindungen | ITU Broadband Maps | nichts |
| **Nordamerika** | etwa 4.700 Landverbindungen | ITU Broadband Maps | nichts |
| **Ozeanien** | etwa 1.400 Landverbindungen | ITU Broadband Maps | nichts |
| **Russland, Nord- und Ostasien** | etwa 1.500 Landverbindungen | ITU Broadband Maps | nichts |
| **Süd- und Südostasien** | etwa 9.500 Landverbindungen | ITU Broadband Maps | nichts |

Die Zahlen der Verbindungen wurden am 25. November 2026 gemessen und sind grob:
Jede Verbindung wird nach ihrem ersten Ende gezählt. Die ITU veröffentlicht
insgesamt etwa 40.000 Verbindungen.

⚠ **Die Abdeckung mit Landverbindungen ist ungleichmäßig.** Die ITU zeigt, was
Netzbetreiber und Regulierungsbehörden ihr gegeben haben. Manche Länder sind
ausführlich gezeichnet (Indien, Brasilien, große Teile Europas); andere haben
wenige Verbindungen oder keine.

Nicht in der Liste? [Sagen Sie es uns](#helfen-sie-mit-es-zu-erweitern). Wo
jemand die Daten offen veröffentlicht, prüfen wir, ob wir sie aufnehmen können.

---

## Teil von Live Track: die anderen Module

Live Track ist eine Reihe von Home-Assistant-Integrationen, eine für jede Art
von beweglichem Ding, alle auf derselben Kartenkarte gezeichnet. Jede
funktioniert allein; zusammen ergeben sie ein lebendiges Bild. Sie teilen sich
die Kartenkarte und eine Python-Bibliothek
([saw-livetrack](https://github.com/StrausbergAutomationWorks/LiveTrackCore)),
sodass eine weitere installierte Integration keine zusätzlichen Anfragen an
eine Quelle stellt, die eine andere bereits liest.

| Modul | Was es auf die Karte bringt | Status |
|---|---|---|
| [Live Track Aircraft](https://github.com/StrausbergAutomationWorks/LiveTrackAircraft) | Flugzeuge über Ihnen per ADS-B, mit Routen und Typsymbolen | veröffentlicht |
| [Live Track Ships](https://github.com/StrausbergAutomationWorks/LiveTrackShips) | Schiffe und Boote per AIS, in Ihrer Nähe oder irgendwo | veröffentlicht |
| [Live Track Commuter Rail](https://github.com/StrausbergAutomationWorks/LiveTrackCommuterRail) | Nahverkehrszüge in Nordamerika, Europa und Australien | veröffentlicht |
| [Live Track Intercity Rail](https://github.com/StrausbergAutomationWorks/LiveTrackIntercityRail) | Intercity- und Fernzüge in Nordamerika, Europa und Australien | veröffentlicht |
| [Live Track SALT](https://github.com/StrausbergAutomationWorks/LiveTrackSALT) | Flugzeuge und Schiffe der Einwanderungs- und Bundespolizeibehörden, aus öffentlichen Listen | veröffentlicht |
| [Live Track Weather](https://github.com/StrausbergAutomationWorks/LiveTrackWeather) | Wetter, Stürme und Naturgefahren | veröffentlicht |
| **Live Track Internet** | Internetausfälle, Seekabel und Landverbindungen (dieses Modul) | veröffentlicht |
| Live Track Stations | Abfahrtstafeln und „Zeit zu gehen“-Hinweise für jeden Bahnhof | geplant |
| Live Track Satellites | Satelliten, die über Sie hinwegziehen | geplant |
| Live Track Freight Trains | Güter- und Arbeitszüge, wo Bahnen sie veröffentlichen | geplant |
| Live Track Transit | Stadtbusse, Straßenbahnen, Fähren und U-Bahnen | geplant |
| Live Track Intercity Buses | Fernbusse und Regionalbusse | geplant |
| Live Track Commuter Buses | Pendlerbusse | geplant |
| [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard) | die gemeinsame Kartenkarte, auf der jedes Modul zeichnet | veröffentlicht, mit jedem Modul installiert |

Alles ist kostenlos und quelloffen. Nichts wird für Sponsoren zurückgehalten.

---

## Bevor Sie beginnen

* **Home Assistant** 2026.11 oder neuer.
* **Der Marketplace** (HACS) in Ihrem Home Assistant, um es bequem zu
  installieren und zu aktualisieren. Ohne ihn können Sie die Dateien von Hand
  kopieren.
* **Internetzugang** für Home Assistant: Die Ausfälle und die Landverbindungen
  kommen von öffentlichen Diensten.
* Für die Kabel und Verbindungen nichts zu bezahlen und kein Konto nötig. Das
  kostenlose Cloudflare-Token oben ist optional.
* Home Assistant installiert das nötige Python-Paket (`saw-livetrack`) beim
  ersten Laden der Integration selbst.

---

## Installation, Schritt für Schritt

### Über den Marketplace (empfohlen)

Live Track Internet ist noch nicht im Katalog des Marketplace. Fügen Sie es
über seinen Link hinzu:

1. Öffnen Sie in Home Assistant **Einstellungen → Marketplace** (HACS).
2. Wählen Sie den Reiter **Über Link hinzufügen**.
3. Geben Sie unter **GitHub-Link**
   `https://github.com/StrausbergAutomationWorks/LiveTrackInternet` ein. Wird
   nach dem **Typ** gefragt, wählen Sie **Integration**.
4. Suchen Sie **Live Track Internet** in der Liste und wählen Sie
   **Installieren**.
5. **Starten Sie Home Assistant neu**: **Einstellungen → System → Reparaturen**
   bietet den Neustart an, oder nutzen Sie **Einstellungen → System → Home
   Assistant neu starten**.

Der Marketplace bietet dann jede neue Veröffentlichung als Aktualisierung an.

### Von Hand

1. Laden Sie den Quellcode der
   [neuesten Veröffentlichung](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/releases/latest)
   herunter.
2. Kopieren Sie dessen Ordner `custom_components/live_track_internet` in den
   Ordner `custom_components` Ihres Home-Assistant-Konfigurationsordners
   (legen Sie `custom_components` an, falls es ihn nicht gibt).
3. Starten Sie Home Assistant neu.

Zum Aktualisieren von Hand ersetzen Sie den Ordner durch den der neuen
Veröffentlichung und starten neu.

---

## Einrichtung, Schritt für Schritt

1. Öffnen Sie **Einstellungen → Geräte & Dienste**.
2. Wählen Sie **Integration hinzufügen** (unten rechts) und suchen Sie nach
   **Live Track Internet**.
3. **Cloudflare-API-Token**: Fügen Sie Ihr Token ein, wenn Sie eines haben
   ([so bekommen Sie eines](#kostenlose-schlüssel-die-mehr-freischalten-schritt-für-schritt)).
   Lassen Sie das Feld leer, um nur die Kabel und Verbindungen zu zeigen; ein
   Token können Sie später hinzufügen.
4. **Landverbindungen von der ITU**: Lassen Sie das Häkchen gesetzt. Entfernen
   Sie es, wenn Ihr Home Assistant die Verbindungen nicht einmal pro Woche von
   der ITU abrufen soll (etwa 1 MB).
5. Wählen Sie **OK**.

Das ist alles. Der Eintrag heißt **Cloudflare Radar** mit einem Token oder
**Submarine cables** ohne. Es gibt nur einen Eintrag: Ein zweiter würde jeden
Ausfall doppelt zeichnen, deshalb wird er abgelehnt.

* Die Ebenen der Kabel und Anlandepunkte sind sofort da.
* Mit einem Token erscheinen offene Ausfälle innerhalb einer Minute.
* Die Landverbindungen erscheinen einige Minuten nach der Einrichtung, wenn
  der erste Abruf bei der ITU fertig ist.

Jede Ebene ist zu Beginn aus. Setzen Sie in der Ebenensteuerung der Karte ein
Häkchen, um sie zu sehen
([Die Karte auf ein Dashboard bringen](#die-karte-auf-ein-dashboard-bringen)).

### Token oder ITU-Kästchen später ändern

1. Öffnen Sie **Einstellungen → Geräte & Dienste → Live Track Internet**.
2. Öffnen Sie das Dreipunktmenü des Eintrags und wählen Sie **Neu
   konfigurieren**.
3. Fügen Sie ein neues Token ein, oder lassen Sie das Feld leer, um Ihr
   bisheriges Token zu behalten. Setzen oder entfernen Sie das Häkchen bei
   **Landverbindungen von der ITU**.
4. Wählen Sie **OK**.

Um das Token zu entfernen, löschen Sie den Eintrag (**Löschen** im selben
Menü) und fügen Live Track Internet ohne Token neu hinzu. Lehnt Cloudflare Ihr
Token später ab (es wurde gelöscht oder ist abgelaufen), enden die
Ausfallmarkierungen, und Home Assistant bittet Sie unter **Einstellungen →
Geräte & Dienste** um ein neues Token.

---

## Kostenlose Schlüssel, die mehr freischalten, Schritt für Schritt

Das Token ist kostenlos und persönlich: Jede Person, die Live Track Internet
installiert, erstellt ihr eigenes. Sie brauchen ein kostenloses
Cloudflare-Konto; eine Website oder Domain bei Cloudflare brauchen Sie nicht.

### Cloudflare-API-Token (Internetausfälle, die ganze Welt)

1. Melden Sie sich bei Cloudflare an, oder legen Sie ein kostenloses Konto an,
   unter <https://dash.cloudflare.com>.
2. Öffnen Sie <https://dash.cloudflare.com/profile/api-tokens> (**My Profile →
   API Tokens**) und wählen Sie **Create Token**.
3. Nehmen Sie keine Vorlage: Beginnen Sie von vorn, mit einem eigenen Token.
   Geben Sie ihm einen Namen, zum Beispiel `Live Track Internet`.
4. Wählen Sie bei den Berechtigungen **Account**, dann **Radar**, dann
   **Read**. Mehr ist nicht nötig.
5. Wählen Sie **Continue to summary**, dann **Create Token**.
6. Kopieren Sie das Token sofort: Cloudflare zeigt es nur einmal.
7. Fügen Sie es bei der [Einrichtung](#einrichtung-schritt-für-schritt) von
   Live Track Internet in **Cloudflare-API-Token** ein, oder später mit **Neu
   konfigurieren**.

Live Track Internet prüft das Token mit einer echten Anfrage an Cloudflare
Radar, bevor es gespeichert wird. Das Token bleibt in Ihrem Home Assistant und
wird nur an Cloudflare gesendet. Außer dem Token ist kein Passwort und kein
Geheimnis nötig. Die Namen der Schaltflächen stehen hier so, wie Cloudflare sie
auf Englisch zeigt; zeigt Cloudflare Ihnen seine Seiten auf Deutsch, heißen sie
dort anders.

---

## Die Karte auf ein Dashboard bringen

Die Karte ist [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard),
die Karte, auf der jedes Live-Track-Modul zeichnet. **Sie wird mit Live Track
Internet installiert**: nichts herunterzuladen, nichts zu kopieren, keine
Ressource hinzuzufügen.

1. Öffnen Sie ein Dashboard, wählen Sie den Stift (**Dashboard bearbeiten**),
   dann **Karte hinzufügen**.
2. Scrollen Sie nach unten und wählen Sie **Manuell**.
3. Fügen Sie dies ein und wählen Sie **Speichern**:

```yaml
type: custom:live-track-map-card
entity_filter:
  include:
    - domain: geo_location
      attributes:
        source: live_track_internet
      options:
        display: attribute
        attribute: marker_label
  exclude:
    - state: unavailable
```

Die Kabel- und Verbindungsebenen erscheinen von selbst. Die Ausfallmarkierungen
kommen über den Filter oben.

Andere Live-Track-Module kommen genauso in `entity_filter`: eine weitere Regel
`- domain: geo_location` für jede Quelle.

**Auf der Karte:**

* Die **Ebenensteuerung** oben rechts hat für jede Ebene ein Kästchen:
  **Kabel mit Störung**, **Alle Kabel**, **Anlandepunkte** und
  **Landverbindungen**. Die Wahl jedes Betrachters wird in seinem eigenen
  Browser gespeichert.
* Jeder Ausfall ist ein rundes Bild seiner Ursache mit dem zweibuchstabigen
  Landeskürzel daneben. **Zeigen** Sie darauf, um zu sehen, wo und warum;
  **klicken** Sie darauf für Cloudflares Beschreibung und einen Link zum
  Bericht.
* **Klicken** Sie auf ein Kabel für Name, Eigentümer, Länge und Anlandeländer.
  Landverbindungen sind nicht anklickbar.
* Die **Filterkarte** (`custom:live-track-map-filter-card`) kann Ausfälle nach
  Ursache ausblenden.
* Der Nachweis jeder Quelle erscheint in der Attributionszeile der Karte,
  solange ihre Daten angezeigt werden.

Die Karte hält für alle Live-Track-Module zusammen genau eine Ressourcenzeile
im Dashboard: die neueste Kartenversion, die eines von ihnen mitbringt, nie
eine ältere. Eine Karte, die Sie selbst über den Marketplace installiert
haben, bleibt unangetastet. Sind die Ressourcen Ihrer Dashboards in YAML
festgelegt (`lovelace: resource_mode: yaml`), kann nichts für Sie registriert
werden: Ein Eintrag unter **Reparaturen** nennt dann die genaue Zeile, die Sie
hinzufügen müssen. Sie sieht so aus, mit der eigenen Adresse der Integration
anstelle der Platzhalter:

```yaml
lovelace:
  resource_mode: yaml
  resources:
    - url: /live_track_internet/map-card/<12 hex>/live-track-map-card.js?v=<version>&h=<12 hex>
      type: module
```

Wird der Eintrag von Live Track Internet gelöscht, übernimmt ein anderes
Live-Track-Modul die Zeile, oder sie wird entfernt, wenn keines übrig ist.
Werden die Dateien der Integration entfernt, während ihr Eintrag noch
eingerichtet ist, und ist kein anderes Live-Track-Modul installiert, entfernen
Sie die Zeile der Karte selbst unter **Einstellungen → Dashboards →
Ressourcen**. Um die Karte stattdessen von Hand zu installieren, folgen Sie
der README der Karte. Eine Zeile, die Sie selbst angelegt haben, für eine
Kopie unter `/local/` oder unter einer anderen Adresse, wird nie geändert oder
entfernt. Solange sie die Karte lädt, überlässt jedes Live-Track-Modul ihr die
Karte, auch wenn ein Modul eine neuere Version mitbringt, und unter
**Reparaturen** steht dazu nichts. Um zur Kopie des Moduls zurückzukehren,
entfernen Sie Ihre Zeile unter **Einstellungen → Dashboards → Ressourcen** und
starten Home Assistant neu. Wenn Sie die Datei Ihrer Kopie löschen, entfernen
Sie auch ihre Zeile: Solange eine Zeile bleibt, deren Datei fehlt, legt das
Modul keine eigene an. Jede andere Kartenkarte, die `geo_location`-Entitäten
zeigt, zeigt auch die Ausfallmarkierungen, aber nicht die Kabel oder
Verbindungen.

---

## In Automationen verwenden

Alles ist eine gewöhnliche Home-Assistant-Entität, also funktioniert der
Automationseditor damit, ganz ohne Code.

**Eine Benachrichtigung aufs Handy, wenn Cloudflare einen neuen
Internetausfall erfasst** (dafür ist das Cloudflare-Token nötig):

1. **Einstellungen → Automationen & Szenen → Automation erstellen → Neue
   Automation erstellen**.
2. **Sobald**: **Auslöser hinzufügen**, tippen Sie `numeric` in das Suchfeld
   und wählen Sie **Numerischer Zustandsschwellenwert überschritten**. Wählen
   Sie als **Entität** **Cloudflare Radar Internetausfälle**, und geben Sie
   unter **Über** `0` ein.
3. **Dann**: **Aktion hinzufügen**, suchen Sie die Benachrichtigungsaktion
   Ihres Handys (sie trägt den Namen Ihres Handys), und geben Sie eine
   Nachricht ein, zum Beispiel:

   ```text
   Cloudflare Radar meldet einen Internetausfall
   ```

4. **Speichern**.

**Weitere Ideen:** eine Benachrichtigung, wenn ein Ausfall ein Seekabel nennt,
mit **Submarine cables Kabel mit Störung** über 0; eine Dashboard-Kachel mit
der Zahl offener Ausfälle, aus **Cloudflare Radar Internetausfälle**.

---

## Alles auf der Karte im Detail

### Ausfälle

[Cloudflare Radar](https://radar.cloudflare.com) führt ein Outage Center:
Einträge über Internetausfälle in aller Welt, geschrieben von Menschen bei
Cloudflare, jeder mit einer Ursache, einer Art (landesweit, regional oder ein
Netz), den betroffenen Ländern oder Regionen, einer Anfangszeit und meist
einem Link zu einem Nachrichtenbericht.

Live Track Internet fragt alle 15 Minuten die Einträge der letzten 24 Stunden
ab und zeichnet eine Markierung für jeden offenen Eintrag an jedem Ort, den er
nennt: in der Region, wenn der Eintrag eine nennt, sonst im Land. Ein Eintrag,
der endet, verschwindet von der Karte. Einträge über einen Online-Dienst statt
über einen Ort (zum Beispiel der Ausfall eines Cloud-Anbieters) werden nicht
gezeichnet; der Sensor **Cloudflare Radar Internetausfälle** führt sie in
seinem Attribut `not_on_map` auf.

⚠ **Ein Eintrag, der nur ein Netz nennt, wird in die Mitte seines Landes
gesetzt**, was in einem großen Land weit vom Ausfall entfernt sein kann. Der
Text beim Klick sagt das. Zum Beispiel ordnet Cloudflare zwei Netze in Luhansk
und Donezk (Ukraine) Russland zu, deshalb stehen ihre Ausfälle in
Zentralsibirien, und Netze in den USA stehen in Kansas.

⚠ Ausfalleinträge werden von Menschen geschrieben, oft Stunden nach Beginn
eines Ausfalls. Als wir ein Jahr an Einträgen gemessen haben (bis zum
23. November 2026), waren es 143, nie mehr als 4 gleichzeitig offen, und 43 %
der Zeit war keiner offen. Meist zeigt die Karte gar keinen Ausfall.

Jede Markierung wird nach ihrer Ursache gezeichnet:

| Ursache | Farbe | Bild |
|---|---|---|
| Kabelschaden | Rot | offene Schere |
| Stromausfall | Bernstein | Blitz |
| Von der Regierung angeordnet (eine Abschaltung) | Indigo | Vorhängeschloss |
| Militärische Handlung | Schwarz | Fadenkreuz |
| Wetter oder Naturkatastrophe | Blau | Gewitterwolke |
| Cyberangriff | Blaugrün | Schild mit `!` |
| Technisches Problem (Netz, Software, DNS, Wartung) | Blaugrau | Schraubenschlüssel |
| Unbekannte Ursache | Grau | `?` |

An jeder Markierung: `outage_cause` und `outage_type` (Cloudflares eigene
Wörter, zum Beispiel `POWER_OUTAGE`, `NATIONWIDE`), `started_at`, `place_kind`
(`region`, `country` oder `network`), `country_code`, `country_name`,
`region_name`, `asns` und `asn_names`, wenn der Eintrag Netze nennt,
`description`, `linked_url` (der Bericht), `cables_named`, wenn die
Beschreibung ein Kabel nennt, und `marker_group` (die Ursache, für die
Filterkarte).

### Kabel mit Störung

Mit dem Cloudflare-Token wird jedes Seekabel, das in der Beschreibung eines
offenen Ausfalls genannt wird, kräftig und rot mit weißem Rand gezeichnet,
standardmäßig an. Meist gibt es keines. Das Kabel wird an seinem Namen
erkannt, in jeder der üblichen Schreibweisen (`SEA-ME-WE 5`, `SeaMeWe-5`);
kurze Namen werden nur als ganze Wörter erkannt.

⚠ Cloudflares Feld für die Ursache sagt nicht, ob ein beschädigtes Kabel ein
Seekabel ist: In dem gemessenen Jahr war der eine als Kabelschaden erfasste
Eintrag ein Kabel an Land, und eine Störung am Kabel SEA-ME-WE 5 war als
unbekannte Ursache erfasst. Deshalb wird das Kabel in der Beschreibung
gesucht, gleich welche Ursache angegeben ist.

### Alle Kabel und Anlandepunkte

Jedes Seekabel in Tristan Hothams Datensatz von 2026 aus den Kabeldaten von
TeleGeography: 713 Kabel, 608 in Betrieb (blau gezeichnet) und 105 geplant
(orange gezeichnet), als dünne, blasse Linien, und 1.928 Anlandepunkte als
kleine Punkte (orange, wo nur geplante Kabel anlanden). Ein Klick auf ein Kabel
zeigt seinen Namen, das Datum, an dem es in Betrieb ging oder gehen soll,
seine Länge, seine Anlandeländer, seine Eigentümer und seinen Lieferanten. Die
Daten werden mit der Integration ausgeliefert und ändern sich nur mit einer
neuen Veröffentlichung.

⚠ Ein Kabel, das nach der Erstellung des Datensatzes (November 2026) verlegt
wurde, erscheint erst nach einer Veröffentlichung mit neueren Daten.

### Landverbindungen

Die Glasfaser- und Richtfunkverbindungen an Land, die die Broadband Maps der
ITU (Infrastructure Connectivity Map) erfassen, aus Angaben von Netzbetreibern
und Regulierungsbehörden. Jede Verbindung wird so gezeichnet, wie die ITU sie
veröffentlicht: als gerade Linie von einem Knoten zum nächsten, nicht als der
Weg, den das Kabel im Gelände nimmt.

| Linie | Was sie ist |
|---|---|
| Pflaume | Glasfaser, in Betrieb |
| Gelb mit schwarzem Rand | Richtfunk, in Betrieb |
| Orange | geplant, vorgeschlagen oder im Bau (Richtfunk mit schwarzem Rand) |
| Grau | ohne Angabe des Zustands (Richtfunk mit schwarzem Rand) |

⚠ In der dünnen, blassen Linienbreite der Karte wirken die Richtfunklinien eher
oliv oder khaki als gelb; der schwarze Rand unterscheidet sie von Glasfaser.

⚠ Die ITU erfasst für eine Verbindung keinen Betreiber, keinen Namen, keine
Kapazität und kein Datum, deshalb ist eine Verbindung nicht anklickbar, und
kein Ausfall wird ihr zugeordnet.

Ihr Home Assistant ruft die ganze Ebene einmal pro Woche bei der ITU ab, an
seinem eigenen Wochentag und zu seiner eigenen Stunde, und bewahrt sie auf.
Schlägt ein Abruf fehl oder kommt er unvollständig zurück, bleibt die letzte
gute Kopie, gleich wie alt.

---

## Alle Entitäten, die es anlegt

| Entität | Was sie ist |
|---|---|
| `sensor.live_track_internet_outages` | **Cloudflare Radar Internetausfälle**: wie viele Ausfallmarkierungen auf der Karte sind (nur mit dem Token) |
| `sensor.live_track_internet_cables_in_trouble` | **Submarine cables Kabel mit Störung**: wie viele Kabel ein offener Ausfall nennt (nur mit dem Token) |
| `sensor.live_track_internet_all_cables` | **Submarine cables Alle Kabel**: die Zahl der Kabel, 713 |
| `sensor.live_track_internet_landing_points` | **Submarine cables Anlandepunkte**: die Zahl der Anlandepunkte, 1.928 |
| `sensor.live_track_internet_terrestrial_links` | **ITU Broadband Maps Landverbindungen**: wie viele Verbindungen gezeichnet sind (nur solange **Landverbindungen von der ITU** angehakt ist) |
| `geo_location.outage_…` | eine je offenem Ausfall und Ort, benannt nach Cloudflares Eintragsnummer (`geo_location.outage_1754`); sie kommt und geht mit dem Eintrag |

Jede Markierung trägt `source: live_track_internet`, und ihr Zustand ist ihre
Entfernung von Ihrem Zuhause in Kilometern. Die Sensoren gehören zu drei
Geräten: **Cloudflare Radar**, **Submarine cables** und **ITU Broadband
Maps**.

Die Attribute des Ausfallsensors: `open_records` (alle offenen Einträge, auch
die nicht auf der Karte), `not_on_map` und `last_success`.

⚠ **Die Markierungen haben absichtlich keine eindeutige ID.** Ausfalleinträge
kommen und gehen, und eine Registerzeile für jeden bliebe für immer. Daher
lassen sie sich in der Oberfläche nicht umbenennen, ausblenden oder einem
Bereich zuordnen. Die Sensoren haben eindeutige IDs und lassen sich umbenennen.

Attribute, die sich bei jeder Aktualisierung ändern, und die großen Listen,
die die Karte liest, werden aus dem Verlauf von Home Assistant herausgehalten,
damit Ihre Datenbank damit nicht wächst.

---

## Was es sendet und herunterlädt

**Über Ihren Standort.** Nichts. Der Standort Ihres Zuhauses wird nur in Ihrem
Home Assistant verwendet, um die Entfernung jeder Markierung zu berechnen.
Cloudflare erhält Ihr Token und den Zeitraum der Anfrage; die ITU erhält die
Anfrage nach ihren Verbindungen. Die Kabeldaten werden mit der Integration
ausgeliefert und nicht heruntergeladen. Jeder Dienst sieht Ihre
Internetadresse, wie jede Website.

**Wie viel.** Größen gemessen am 25. November 2026, wenn die Tabelle nichts
anderes sagt.

| Quelle | Was und wie oft | Gemessene Größe | Nach einem Fehler |
|---|---|---|---|
| Cloudflare Radar, Ausfälle | eine Anfrage alle 15 Minuten, mit Ihrem Token: die Einträge der letzten 24 Stunden | 447 Byte über die Leitung (ein Eintrag) | ein abgelehntes Token beendet die Anfragen und bittet Sie um ein neues. HTTP 429: wartet so lange, wie Cloudflare verlangt, oder 15 Minuten, verdoppelt bis zu 2 Stunden. Andere Fehler: neuer Versuch nach 15, 30 und 60 Minuten, dann alle 2 Stunden. Die letzte gute Antwort wird 2 Stunden behalten; danach verschwinden die Markierungen |
| Cloudflare Radar, Orte | die Mittelpunkte der Länder einmal am Tag; der Punkt einer Region beim ersten Mal, wenn ein Eintrag sie nennt, dann aufbewahrt | die Länderliste: 36.905 Byte (23. November 2026) | die vorhandene Kopie bleibt in Gebrauch |
| ITU Broadband Maps | die ganze Ebene einmal pro Woche, in 9 Anfragen im Abstand von 3 Sekunden, zusammen etwa 36 Sekunden | etwa 0,9 MB über die Leitung (111.537 Byte je 5.000 Verbindungen) | HTTP 429: wartet so lange, wie die ITU verlangt, oder eine Stunde, verdoppelt bis zu einem Tag. Andere Fehler: neuer Versuch am nächsten Tag. Die letzte gute Kopie bleibt |
| Ihr Browser | von Ihrem Home Assistant, nicht aus dem Internet: die Kabeldatei, wenn **Alle Kabel** angehakt ist, die Anlandepunkte, wenn **Anlandepunkte** angehakt ist, und die Verbindungsdatei, wenn **Landverbindungen** angehakt ist | Kabel 113.323 Byte; Anlandepunkte 38.160 Byte; Verbindungen 296.105 Byte | |

Entfernen Sie das Häkchen bei **Landverbindungen von der ITU** (**Neu
konfigurieren**), um den wöchentlichen Abruf zu beenden. Löschen Sie den
Eintrag, um alles zu beenden.

Die heruntergeladenen Dateien liegen im Ordner `.storage` von Home Assistant
unter Namen, die mit `saw_` beginnen (`saw_radar_locations.json`,
`saw_radar_geolocations.json`, `saw_itu_bbmaps_links.json.gz`), damit ein
anderes Live-Track-Modul sie mitnutzen kann. Entfernen Sie Live Track Internet
und nutzt kein anderes Live-Track-Modul sie, können Sie sie von Hand löschen.

---

## Helfen Sie mit, es zu erweitern

Live Track Internet wächst noch. Wir fügen Datenquellen hinzu, sobald wir sie
finden, und wir möchten wissen, was Sie sich als Nächstes wünschen.

### Etwas vorschlagen

Fehlt eine Datenquelle? Ist etwas falsch oder schwer zu verstehen? Sagen Sie
es uns auf dem Weg, der für Sie einfacher ist:

* [**Füllen Sie ein kurzes Formular aus**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=de.yml)
  auf Deutsch. Sie brauchen ein kostenloses GitHub-Konto.
* **Schreiben Sie eine E-Mail** an
  [StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org).
  Kein Konto nötig.

In beiden Fällen hilft es, wenn Sie uns sagen:

* was Sie gern sehen würden, und wo auf der Welt;
* einen Link, wo die Daten veröffentlicht werden, falls Sie einen kennen (eine
  Open-Data-Seite, ein öffentlicher Feed, die Website eines Dienstes): nicht
  nötig, aber hilfreich;
* die Sprache Ihres Home Assistant, wenn es um die Formulierung oder eine
  Übersetzung geht.

Schreiben Sie auf Englisch oder in Ihrer eigenen Sprache, was für Sie
einfacher ist.

### Selbst etwas hinzufügen, mit unserer Hilfe

Wenn Sie selbst etwas hinzufügen möchten, helfen wir Ihnen dabei, von der
ersten Frage bis zur fertigen Veröffentlichung. Sie müssen kein Entwickler
sein, um anzufangen:

* **Eine Übersetzung.** Die Texte im Einrichtungsdialog sind eine kurze Liste
  von Sätzen in einer Textdatei. Wir zeigen Ihnen, welche Datei und welche
  Zeilen.
* **Eine neue Quelle.** Sagen Sie uns, wo die Daten veröffentlicht werden. Wir
  können den Code gemeinsam schreiben oder Ihren durchsehen.
* **Testen, wo Sie wohnen.** Installieren Sie es, sehen Sie sich Ihren Teil
  der Karte an, und sagen Sie uns, was stimmt und was nicht.
* **Eine Korrektur dieser README.** Wenn ein Schritt nicht zu dem passte, was
  Sie gesehen haben, sagen Sie uns, was Sie gesehen haben.

[**Sagen Sie uns, was Sie vorhaben**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=de.yml)
oder schreiben Sie an
[StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org),
und wir antworten mit den nächsten Schritten.

---

## Sprachen

Diese README: [English](README.md), **Deutsch**, [Français](README.fr.md),
[Nederlands](README.nl.md), [简体中文](README.zh-Hans.md),
[Español](README.es.md), [Italiano](README.it.md),
[Українська](README.uk.md) und [العربية](README.ar.md). Jede übersetzte
README ist vollständig. Keine wurde bisher von einem Muttersprachler gelesen.
Ist eine dieser Sprachen Ihre, sagen Sie uns bitte, ob sich ihre README gut
liest: siehe [Helfen Sie mit, es zu erweitern](#helfen-sie-mit-es-zu-erweitern).

Der Einrichtungsdialog erscheint in der Sprache Ihres Home Assistant, wenn es
eine dieser ist: English, Deutsch, Español, Français, Italiano, Nederlands,
简体中文, Українська und العربية. Jede andere Sprache zeigt Englisch. Auch die
Übersetzungen des Dialogs wurden ohne Muttersprachler geschrieben. Die Wörter
auf der Karte (die Namen der Ausfälle und die Texte beim Klick, die Namen der
Ursachen in der Filterkarte und die Nachweise) sind in jeder Sprache englisch.

Einen Fehler in einer Übersetzung gefunden, oder eine andere Sprache nötig?
Sagen Sie es uns unter
<https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues>, oder
[übersetzen Sie mit unserer Hilfe](#selbst-etwas-hinzufügen-mit-unserer-hilfe).

---

## Danksagungen und Lizenzen

* **Cloudflare Radar** (Cloudflare, Inc., <https://radar.cloudflare.com>): die
  Ausfalleinträge, unter
  [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), gelesen mit
  dem eigenen Token jedes Nutzers. Diese Integration setzt jeden Eintrag auf
  die Karte; sie ändert die Einträge nicht. Mit der Installation dieser
  Integration nutzen Sie die API von Cloudflare, und deren Bedingungen gelten
  für Sie.
* **Seekabel und Anlandepunkte**: Hotham, T. (2026), *The internet's seabed:
  submarine cables, when they were laid, who owns them and where they crowd
  together*, Zenodo, <https://doi.org/10.5281/zenodo.23856607>, abgeleitet aus
  TeleGeographys
  [Submarine Cable Map](https://www.submarinecablemap.com/), unter
  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Diese
  Integration hat die Kabellinien mit der Kabeltabelle verbunden, beides in
  Kartendateien umgewandelt und die Anlandepunkte auf 4 Dezimalstellen
  gerundet; nichts wurde hinzugefügt oder korrigiert. Die umgewandelten Dateien
  in `custom_components/live_track_internet/cables/` stehen unter derselben
  Lizenz, mit ihrem Rechtstext und einer Nachweisdatei daneben
  ([CREDIT.md](custom_components/live_track_internet/cables/CREDIT.md)).
* **Landverbindungen**: ITU Broadband Maps (BBmaps), die Infrastructure
  Connectivity Map, <https://bbmaps.itu.int>, © ITU. Genutzt nach den
  Nutzungsbedingungen der ITU für nicht kommerzielle Zwecke, mit Nennung der
  Quelle. Nichts von der ITU wird in diesem Repository ausgeliefert: Jede
  Installation ruft die Verbindungen für ihren eigenen Nutzer ab. Diese
  Integration zeichnet sie so, wie die ITU sie veröffentlicht, auf
  3 Dezimalstellen gerundet (etwa 110 m), wiederholte Verbindungen derselben
  Art nur einmal.
* **Die Bilder der Ausfälle** wurden für StrausbergAutomationWorks gezeichnet,
  unter der MIT-Lizenz.
* **Die Kartenkarte** ist [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard),
  MIT, eine Kopie von [ha-map-card](https://github.com/nathan-gs/ha-map-card)
  von nathan-gs, MIT. Ihre Kartenkacheln und deren Nachweise stehen in ihrer
  README.

⚠ **Nur für nicht kommerzielle Nutzung.** Alle drei Datenquellen erlauben nur
nicht kommerzielle Nutzung. Der Code steht unter MIT, aber die Daten, die er
zeigt, dürfen nicht kommerziell genutzt werden.

Keine dieser Organisationen hat diese Integration erstellt oder unterstützt.
Welche Lizenz welchen Teil dieses Repositorys abdeckt:
[ATTRIBUTION.md](ATTRIBUTION.md).

**Code**: MIT, in [LICENSE](LICENSE).

**Für Entwickler:** Die Entitäten folgen dem gemeinsamen Kartenvertrag von
Live Track, sodass jedes Modul auf einer Karte erscheint.
`tools/build_cables.py` baut die Kabeldateien aus Hothams Repository neu. Die
Tests laufen mit `python -m unittest discover -s tests`.

---

## Stichwörter

Home Assistant Internetausfall · Internetausfall Karte · Internetsperre ·
Internet-Blackout · Netzausfall · Störung beim Internetanbieter · Cloudflare
Radar · Radar Outage Center · Seekabel · Unterseekabel · Tiefseekabel ·
Seekabelkarte · Kabelschaden · Kabelanlandepunkte · TeleGeography · Submarine
Cable Map · Glasfaser an Land · Glasfaserkarte · Glasfaser-Backbone ·
Richtfunk · ITU · ITU Broadband Maps · BBmaps · Infrastructure Connectivity
Map · internet outage · submarine cables · panne internet · câbles
sous-marins · internetstoring · zeekabels · 断网 · 海底光缆 · corte de
internet · cables submarinos · interruzione internet · cavi sottomarini ·
відключення інтернету · підводні кабелі · انقطاع الإنترنت · كابلات بحرية ·
geo_location · Kartenkarte · Lovelace · HACS · Marketplace · Live Track ·
LiveTrack · StrausbergAutomationWorks

---

**Würdigung.** StrausbergAutomationWorks würdigt die indigenen Völker aller
Länder und Gewässer auf dieser Karte, überall auf der Welt, und erweist ihren
Ältesten, in Vergangenheit und Gegenwart, seinen Respekt.
