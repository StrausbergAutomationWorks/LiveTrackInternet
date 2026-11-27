# Live Track Internet

[English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · **Nederlands** · [简体中文](README.zh-Hans.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Українська](README.uk.md) · [العربية](README.ar.md) · [Alle talen](#talen)

**Internetstoringen, zeekabels en glasvezelverbindingen voor Home Assistant, op
één kaart.** Live Track Internet zet de internetstoringen die Cloudflare Radar
waar ook ter wereld registreert, met hun oorzaak, op je Home Assistant-kaart.
Het tekent ook elke zeekabel met zijn aanlandingspunten, en de glasvezel- en
straalverbindingen tussen plaatsen die de ITU registreert. Als een storing een
kabel noemt, wordt die kabel rood getekend.

> **Live Track Internet is één module van Live Track**, een familie van Home
> Assistant-integraties die alles wat beweegt, en het weer waar het doorheen
> beweegt, op één gedeelde kaart tekenen: vliegtuigen, schepen, treinen en
> het weer. Installeer het los of naast de andere modules
> ([lijst hieronder](#onderdeel-van-live-track-de-andere-modules)).

> **Het groeit, en ideeën zijn welkom.** Live Track Internet dekt vandaag
> storingen, kabels en verbindingen over land wereldwijd, en we voegen meer
> gegevensbronnen toe (internetknooppunten en datacenters staan gepland).
> Ontbreekt er iets? [Stel het voor](#help-het-groeien), of voeg het zelf toe:
> we helpen je daarbij.

**Status: 0.3.3, uitgebracht.** In de catalogus van de Marktplaats ([installeer
het hieronder](#installeren-stap-voor-stap)).

Eigen werk van StrausbergAutomationWorks. Niet verbonden met, of
onderschreven door, Cloudflare, Tristan Hotham, TeleGeography, de
Internationale Telecommunicatie-unie (ITU), of een kabeleigenaar of
netwerkbeheerder.

> ⚠ **Geen bewaking van je eigen internetverbinding.** De storingen zijn
> meldingen die mensen bij Cloudflare schrijven, vaak uren nadat een storing
> begon, en alleen voor storingen die groot genoeg zijn om vanuit het netwerk
> van Cloudflare te zien. **Een lege kaart betekent niet dat het internet
> overal werkt.** Een kabel of verbinding op de kaart zegt niets over of er
> vandaag verkeer overheen gaat.

---

## Inhoud

1. [Alles wat het doet](#alles-wat-het-doet)
2. [Waar het werkt](#waar-het-werkt)
3. [Onderdeel van Live Track: de andere modules](#onderdeel-van-live-track-de-andere-modules)
4. [Voordat je begint](#voordat-je-begint)
5. [Installeren, stap voor stap](#installeren-stap-voor-stap)
6. [Instellen, stap voor stap](#instellen-stap-voor-stap)
7. [Gratis sleutels die meer aanzetten, stap voor stap](#gratis-sleutels-die-meer-aanzetten-stap-voor-stap)
8. [De kaart op een dashboard zetten](#de-kaart-op-een-dashboard-zetten)
9. [Gebruiken in automatiseringen](#gebruiken-in-automatiseringen)
10. [Alles op de kaart, in detail](#alles-op-de-kaart-in-detail)
11. [Alle entiteiten die het aanmaakt](#alle-entiteiten-die-het-aanmaakt)
12. [Wat het verstuurt en downloadt](#wat-het-verstuurt-en-downloadt)
13. [Help het groeien](#help-het-groeien)
14. [Talen](#talen)
15. [Vermeldingen en licenties](#vermeldingen-en-licenties)
16. [Trefwoorden](#trefwoorden)

---

## Alles wat het doet

### Op de kaart, zonder iets in te stellen

Elk van deze lagen heeft een eigen vakje in de laagkeuze van de kaart. Ze
staan allemaal eerst **uit**: vink een vakje aan om de laag te tonen.

| Wat | Waar | Van |
|---|---|---|
| **Alle kabels**: elke zeekabel, 608 in gebruik en 105 gepland, als dunne lijnen; klik er een aan voor naam, eigenaars, lengte en aanlandingslanden | de hele wereld | de dataset van Tristan Hotham met de kabelgegevens van TeleGeography, meegeleverd met de integratie |
| **Aanlandingspunten**: de 1.928 plaatsen waar kabels aan land komen, als kleine stippen | de hele wereld | dezelfde |
| **Verbindingen over land**: glasvezel- en straalverbindingen tussen plaatsen op het land, recht van het ene knooppunt naar het volgende getekend | de landen waar de ITU ze heeft verzameld ([waar](#waar-het-werkt)) | ITU Broadband Maps (BBmaps), eens per week door je Home Assistant opgehaald |

### Aangezet met je eigen gratis sleutel of account

| Gratis sleutel of account | Wat het toevoegt |
|---|---|
| **Cloudflare**-API-token | **Storingen**: een markering voor elke lopende internetstoring die Cloudflare Radar registreert, in het land of de regio die ze noemt, gekleurd en getekend naar haar oorzaak; standaard aan. **Kabels met storing**: elke zeekabel die een lopende storing noemt, dik en rood getekend; standaard aan |

Je hebt het in een paar minuten: [stap voor stap hieronder](#gratis-sleutels-die-meer-aanzetten-stap-voor-stap).

---

## Waar het werkt

| Regio | Wat je krijgt | Van | Nodig |
|---|---|---|---|
| **De hele wereld** | internetstoringen, in het land of de regio die elke melding noemt | Cloudflare Radar | een gratis token |
| **De hele wereld** | zeekabels met storing | Cloudflare Radar, en de kabelgegevens | een gratis token |
| **De hele wereld** | alle zeekabels en aanlandingspunten | de dataset van Tristan Hotham met de gegevens van TeleGeography | niets |
| **Afrika en het Midden-Oosten** | ongeveer 5.400 verbindingen over land | ITU Broadband Maps | niets |
| **Midden- en Zuid-Amerika** | ongeveer 5.500 verbindingen over land | ITU Broadband Maps | niets |
| **Europa** | ongeveer 12.400 verbindingen over land | ITU Broadband Maps | niets |
| **Noord-Amerika** | ongeveer 4.700 verbindingen over land | ITU Broadband Maps | niets |
| **Oceanië** | ongeveer 1.400 verbindingen over land | ITU Broadband Maps | niets |
| **Rusland, Noord- en Oost-Azië** | ongeveer 1.500 verbindingen over land | ITU Broadband Maps | niets |
| **Zuid- en Zuidoost-Azië** | ongeveer 9.500 verbindingen over land | ITU Broadband Maps | niets |

De aantallen verbindingen zijn gemeten op 25 november 2026 en zijn grof: elke
verbinding wordt geteld bij haar eerste uiteinde. De ITU publiceert in totaal
ongeveer 40.000 verbindingen.

⚠ **De dekking met verbindingen over land is ongelijk.** De ITU toont wat
netwerkbeheerders en toezichthouders haar hebben gegeven. Sommige landen zijn
gedetailleerd getekend (India, Brazilië, een groot deel van Europa); andere
hebben weinig verbindingen of geen.

Staat het er niet bij? [Laat het ons weten](#help-het-groeien). Waar iemand de
gegevens openlijk publiceert, kijken we of we ze kunnen toevoegen.

---

## Onderdeel van Live Track: de andere modules

Live Track is een reeks Home Assistant-integraties, één per soort bewegend
ding, allemaal getekend op dezelfde kaartkaart. Elk werkt op zichzelf; samen
vormen ze één levend beeld. Ze delen de kaartkaart en een Python-bibliotheek
([saw-livetrack](https://github.com/StrausbergAutomationWorks/LiveTrackCore)),
dus een extra integratie installeren voegt geen verzoeken toe aan een bron die
een andere al leest.

| Module | Wat het op de kaart zet | Status |
|---|---|---|
| [Live Track Aircraft](https://github.com/StrausbergAutomationWorks/LiveTrackAircraft) | vliegtuigen boven je via ADS-B, met routes en typepictogrammen | uitgebracht |
| [Live Track Ships](https://github.com/StrausbergAutomationWorks/LiveTrackShips) | schepen en boten via AIS, bij je in de buurt of waar dan ook | uitgebracht |
| [Live Track Commuter Rail](https://github.com/StrausbergAutomationWorks/LiveTrackCommuterRail) | forensentreinen in Noord-Amerika, Europa en Australië | uitgebracht |
| [Live Track Intercity Rail](https://github.com/StrausbergAutomationWorks/LiveTrackIntercityRail) | intercity- en langeafstandstreinen in Noord-Amerika, Europa en Australië | uitgebracht |
| [Live Track SALT](https://github.com/StrausbergAutomationWorks/LiveTrackSALT) | vliegtuigen en schepen van immigratie- en federale opsporingsdiensten, uit openbare lijsten | uitgebracht |
| [Live Track Weather](https://github.com/StrausbergAutomationWorks/LiveTrackWeather) | weer, stormen en natuurgevaren | uitgebracht |
| **Live Track Internet** | internetstoringen, zeekabels en verbindingen over land (deze module) | uitgebracht |
| Live Track Stations | vertrekborden en "tijd om te gaan"-meldingen voor elk station | gepland |
| Live Track Satellites | satellieten die over je heen trekken | gepland |
| Live Track Freight Trains | goederen- en werktreinen waar spoorwegen ze publiceren | gepland |
| Live Track Transit | stadsbussen, trams, veerboten en metro | gepland |
| Live Track Intercity Buses | intercity- en streekbussen | gepland |
| Live Track Commuter Buses | forensenbussen | gepland |
| [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard) | de gedeelde kaartkaart waarop elke module tekent | uitgebracht, met elke module geïnstalleerd |

Alles is gratis en open source. Niets wordt achtergehouden voor sponsors.

---

## Voordat je begint

* **Home Assistant** 2026.11 of nieuwer.
* **De Marktplaats** (Marketplace, HACS) in je Home Assistant, om het
  makkelijk te installeren en bij te werken. Zonder kun je de bestanden met de
  hand kopiëren.
* **Internettoegang** voor Home Assistant: de storingen en de verbindingen over
  land komen van openbare diensten.
* Niets te betalen en geen account nodig voor de kabels en verbindingen. Het
  gratis Cloudflare-token hierboven is optioneel.
* Home Assistant installeert het Python-pakket dat het nodig heeft
  (`saw-livetrack`) zelf, de eerste keer dat de integratie laadt.

---

## Installeren, stap voor stap

### Via de Marktplaats (aanbevolen)

1. Open in Home Assistant **Instellingen → Marktplaats** (HACS).
2. Zoek **Live Track Internet** en open het.
3. Kies **Downloaden** (of **Installeren**).
4. **Herstart Home Assistant**: **Instellingen → Systeem → Reparaties** biedt
   de herstart aan, of gebruik **Instellingen → Systeem → Herstart Home
   Assistant**.

Vindt de zoekfunctie het niet, voeg het dan toe via de link: kies het tabblad
**Via koppeling toevoegen** (of het menu met drie puntjes → **Aangepaste
repositories**), voer `StrausbergAutomationWorks/LiveTrackInternet` in, kies
**Integratie** als om het type wordt gevraagd en ga daarna verder bij stap 3.

De Marktplaats biedt daarna elke nieuwe release als update aan.

### Met de hand

1. Download de broncode van de
   [nieuwste release](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/releases/latest).
2. Kopieer de map `custom_components/live_track_internet` daarvan naar de map
   `custom_components` van je Home Assistant-configuratiemap (maak
   `custom_components` aan als die er niet is).
3. Herstart Home Assistant.

Om met de hand bij te werken vervang je de map door die van de nieuwe release
en herstart je.

---

## Instellen, stap voor stap

1. Open **Instellingen → Apparaten en diensten**.
2. Kies **Integratie toevoegen** (rechtsonder) en zoek naar **Live Track
   Internet**.
3. **Cloudflare-API-token**: plak je token als je er een hebt
   ([zo krijg je er een](#gratis-sleutels-die-meer-aanzetten-stap-voor-stap)).
   Laat het leeg om alleen de kabels en verbindingen te tonen; een token kun
   je later toevoegen.
4. **Verbindingen over land van de ITU**: laat dit aangevinkt. Vink het uit als
   je niet wilt dat je Home Assistant de verbindingen eens per week bij de ITU
   ophaalt (ongeveer 1 MB).
5. Kies **Verzend**.

Dat is alles. Het item heet **Cloudflare Radar** met een token, of **Submarine
cables** zonder. Er is maar één item: een tweede zou elke storing twee keer
tekenen, dus dat wordt geweigerd.

* De lagen van de kabels en aanlandingspunten zijn er meteen.
* Met een token verschijnen lopende storingen binnen een minuut.
* De verbindingen over land verschijnen een paar minuten na het instellen,
  als de eerste ophaalbeurt bij de ITU klaar is.

Elke laag staat eerst uit. Vink hem aan in de laagkeuze van de kaart om hem te
zien ([De kaart op een dashboard zetten](#de-kaart-op-een-dashboard-zetten)).

### Het token of het ITU-vakje later wijzigen

1. Open **Instellingen → Apparaten en diensten → Live Track Internet**.
2. Open het menu met drie puntjes van het item en kies **Herconfigureer**.
3. Plak een nieuw token, of laat het veld leeg om het token te houden dat je
   hebt. Vink **Verbindingen over land van de ITU** aan of uit.
4. Kies **Verzend**.

Om het token te verwijderen verwijder je het item (**Verwijder** in hetzelfde
menu) en voeg je Live Track Internet opnieuw toe zonder token. Als Cloudflare
je token later weigert (het is verwijderd of verlopen), stoppen de
markeringen van de storingen, en vraagt Home Assistant je onder
**Instellingen → Apparaten en diensten** om een nieuw token.

---

## Gratis sleutels die meer aanzetten, stap voor stap

Het token is gratis en persoonlijk: iedereen die Live Track Internet
installeert, maakt zijn eigen. Je hebt een gratis Cloudflare-account nodig; een
website of domein bij Cloudflare heb je niet nodig.

### Cloudflare-API-token (internetstoringen, de hele wereld)

1. Meld je aan bij Cloudflare, of maak een gratis account aan, op
   <https://dash.cloudflare.com>.
2. Open <https://dash.cloudflare.com/profile/api-tokens> (**My Profile → API
   Tokens**) en kies **Create Token**.
3. Gebruik geen sjabloon: begin vanaf nul, met een eigen token. Geef het een
   naam, bijvoorbeeld `Live Track Internet`.
4. Kies bij de rechten **Account**, dan **Radar**, dan **Read**. Meer is niet
   nodig.
5. Kies **Continue to summary**, dan **Create Token**.
6. Kopieer het token meteen: Cloudflare toont het maar één keer.
7. Plak het in **Cloudflare-API-token** als je Live Track Internet
   [instelt](#instellen-stap-voor-stap), of later met **Herconfigureer**.

Live Track Internet controleert het token met één echt verzoek aan Cloudflare
Radar voordat het wordt opgeslagen. Het token blijft in je Home Assistant en
wordt alleen naar Cloudflare gestuurd. Behalve het token is geen wachtwoord of
geheim nodig. De namen van de knoppen staan hier zoals Cloudflare ze in het
Engels toont; als Cloudflare zijn pagina's in het Nederlands toont, heten ze
daar anders.

---

## De kaart op een dashboard zetten

De kaart is [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard),
de kaart waarop elke Live Track-module tekent. **Hij wordt met Live Track
Internet geïnstalleerd**: niets te downloaden, niets te kopiëren, geen bron
toe te voegen.

1. Open een dashboard, kies het potlood (**Wijzig dashboard**), dan **Kaart
   toevoegen**.
2. Scrol naar beneden en kies **Handmatig**.
3. Plak dit en kies **Bewaar**:

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

De lagen van de kabels en verbindingen verschijnen vanzelf. De markeringen van
de storingen komen via het filter hierboven.

Andere Live Track-modules gaan op dezelfde manier in `entity_filter`: nog een
regel `- domain: geo_location` voor elke bron.

**Op de kaart:**

* De **laagkeuze** rechtsboven heeft een vakje voor elke laag: **Kabels met
  storing**, **Alle kabels**, **Aanlandingspunten** en **Verbindingen over
  land**. De keuze van elke kijker wordt in zijn eigen browser bewaard.
* Elke storing is een rond plaatje van haar oorzaak met de landcode van twee
  letters ernaast. **Wijs** het aan om te zien waar en waarom; **klik** erop
  voor de beschrijving van Cloudflare en een link naar het bericht.
* **Klik** op een kabel voor naam, eigenaars, lengte en aanlandingslanden.
  Verbindingen over land zijn niet aanklikbaar.
* De **filterkaart** (`custom:live-track-map-filter-card`) kan storingen naar
  oorzaak verbergen.
* De bronvermelding van elke bron verschijnt in de attributieregel van de
  kaart zolang de gegevens ervan getoond worden.

De kaart houdt voor alle Live Track-modules samen precies één bronregel in je
dashboards: de nieuwste kaartversie die een van hen meebrengt, nooit een
oudere. Een kaart die je zelf via de Marktplaats hebt geïnstalleerd, blijft
ongemoeid. Als de bronnen van je dashboards in YAML zijn ingesteld
(`lovelace: resource_mode: yaml`), kan er niets voor je worden geregistreerd:
een melding onder **Reparaties** geeft dan de precieze regel om toe te voegen.
Die ziet er zo uit, met het eigen adres van de integratie in plaats van de
plaatshouders:

```yaml
lovelace:
  resource_mode: yaml
  resources:
    - url: /live_track_internet/map-card/<12 hex>/live-track-map-card.js?v=<version>&h=<12 hex>
      type: module
```

Verwijder je het item van Live Track Internet, dan neemt een andere Live
Track-module de regel over, of wordt hij verwijderd als er geen meer over is.
Worden de bestanden van de integratie verwijderd terwijl het item nog is
ingesteld, en is er geen andere Live Track-module geïnstalleerd, verwijder de
regel van de kaart dan zelf onder **Instellingen → Dashboards → Bronnen**. Om
de kaart in plaats daarvan met de hand te installeren, volg je de README van
de kaart. Een regel die je zelf hebt gemaakt, voor een kopie onder `/local/`
of op een ander adres, wordt nooit gewijzigd of verwijderd. Zolang die de
kaart laadt, laat elke Live Track-module de kaart eraan over, ook als een
module een nieuwere release meebrengt, en onder **Reparaties** staat daar
niets over. Om terug te gaan naar de kopie van de module, verwijder je je
regel onder **Instellingen → Dashboards → Bronnen** en herstart je Home
Assistant. Verwijder je het bestand van je kopie, verwijder dan ook de regel:
zolang een regel blijft staan waarvan het bestand weg is, voegt de module geen
eigen regel toe. Elke andere kaartkaart die `geo_location`-entiteiten toont,
laat ook de markeringen van de storingen zien, maar niet de kabels of
verbindingen.

---

## Gebruiken in automatiseringen

Alles is een gewone Home Assistant-entiteit, dus de automatiseringseditor
werkt ermee, zonder code.

**Een melding op je telefoon als Cloudflare een nieuwe internetstoring
registreert** (hiervoor is het Cloudflare-token nodig):

1. **Instellingen → Automatiseringen en scènes → Maak automatisering aan →
   Nieuwe automatisering aanmaken**.
2. **Wanneer**: **Trigger toevoegen**, typ `numeric` in het zoekvak en kies
   **Numerieke status heeft drempelwaarde overschreden**. Kies als
   **Entiteit** **Cloudflare Radar Internetstoringen**, en vul onder **Boven**
   `0` in.
3. **Doe dan**: **Actie toevoegen**, zoek de meldingsactie van je telefoon (die
   draagt de naam van je telefoon), en voer een bericht in, bijvoorbeeld:

   ```text
   Cloudflare Radar meldt een internetstoring
   ```

4. **Bewaar**.

**Andere ideeën:** een melding als een storing een zeekabel noemt, met
**Submarine cables Kabels met storing** boven 0; een dashboardtegel met het
aantal lopende storingen, uit **Cloudflare Radar Internetstoringen**.

---

## Alles op de kaart, in detail

### Storingen

[Cloudflare Radar](https://radar.cloudflare.com) houdt een Outage Center bij:
meldingen over internetstoringen over de hele wereld, geschreven door mensen
bij Cloudflare, elk met een oorzaak, een soort (landelijk, regionaal of één
netwerk), de getroffen landen of regio's, een begintijd en meestal een link
naar een nieuwsbericht.

Live Track Internet vraagt elke 15 minuten de meldingen van de laatste
24 uur op en tekent een markering voor elke lopende melding op elke plaats die
ze noemt: in de regio als de melding er een noemt, anders in het land. Een
melding die eindigt, verdwijnt van de kaart. Meldingen over een onlinedienst in
plaats van over een plaats (de storing van een cloudaanbieder, bijvoorbeeld)
worden niet getekend; de sensor **Cloudflare Radar Internetstoringen** noemt ze
in zijn attribuut `not_on_map`.

⚠ **Een melding die alleen een netwerk noemt, wordt in het midden van haar
land gezet**, wat in een groot land ver van de storing kan liggen. De tekst bij
het klikken zegt dat. Zo zet Cloudflare twee netwerken in Loehansk en Donetsk
(Oekraïne) onder Rusland, waardoor hun storingen in Midden-Siberië staan, en
staan netwerken in de VS in Kansas.

⚠ Storingsmeldingen worden door mensen geschreven, vaak uren nadat een storing
begon. Toen we een jaar aan meldingen maten (tot 23 november 2026), waren het
er 143, nooit meer dan 4 tegelijk lopend, en 43% van de tijd liep er geen. Meestal
toont de kaart helemaal geen storing.

Elke markering wordt getekend naar haar oorzaak:

| Oorzaak | Kleur | Plaatje |
|---|---|---|
| Kabelbreuk | rood | open schaar |
| Stroomstoring | amber | bliksemschicht |
| Door de overheid opgelegd (een afsluiting) | indigo | hangslot |
| Militaire actie | zwart | vizierkruis |
| Weer of natuurramp | blauw | onweerswolk |
| Cyberaanval | blauwgroen | schild met `!` |
| Technisch probleem (netwerk, software, DNS, onderhoud) | blauwgrijs | moersleutel |
| Onbekende oorzaak | grijs | `?` |

Op elke markering: `outage_cause` en `outage_type` (de eigen woorden van
Cloudflare, bijvoorbeeld `POWER_OUTAGE`, `NATIONWIDE`), `started_at`,
`place_kind` (`region`, `country` of `network`), `country_code`,
`country_name`, `region_name`, `asns` en `asn_names` als de melding netwerken
noemt, `description`, `linked_url` (het bericht), `cables_named` als de
beschrijving een kabel noemt, en `marker_group` (de oorzaak, voor de
filterkaart).

### Kabels met storing

Met het Cloudflare-token wordt elke zeekabel die in de beschrijving van een
lopende storing wordt genoemd, dik en rood met een witte rand getekend,
standaard aan. Meestal is er geen. De kabel wordt herkend aan zijn naam, in elk
van de gebruikelijke schrijfwijzen (`SEA-ME-WE 5`, `SeaMeWe-5`); korte namen
worden alleen als hele woorden herkend.

⚠ Het oorzaakveld van Cloudflare zegt niet of een gebroken kabel een zeekabel
is: in het gemeten jaar was de enige melding met kabelbreuk als oorzaak een
kabel op het land, en een storing op de kabel SEA-ME-WE 5 stond als onbekende
oorzaak geregistreerd. Daarom wordt de kabel in de beschrijving gezocht,
welke oorzaak er ook staat.

### Alle kabels en aanlandingspunten

Elke zeekabel in de dataset van 2026 van Tristan Hotham met de kabelgegevens
van TeleGeography: 713 kabels, 608 in gebruik (blauw getekend) en 105 gepland
(oranje getekend), als dunne, vage lijnen, en 1.928 aanlandingspunten als
kleine stippen (oranje waar alleen geplande kabels aan land komen). Klik op een
kabel voor zijn naam, de datum waarop hij in gebruik kwam of komt, zijn lengte,
zijn aanlandingslanden, zijn eigenaars en zijn leverancier. De gegevens worden
met de integratie meegeleverd en veranderen alleen met een nieuwe release.

⚠ Een kabel die na het maken van de dataset (november 2026) is gelegd,
verschijnt pas na een release met nieuwere gegevens.

### Verbindingen over land

De glasvezel- en straalverbindingen op het land die de Broadband Maps van de
ITU (Infrastructure Connectivity Map) registreren, uit gegevens van
netwerkbeheerders en toezichthouders. Elke verbinding wordt getekend zoals de
ITU haar publiceert: een rechte lijn van het ene knooppunt naar het volgende,
niet de weg die de kabel in het terrein volgt.

| Lijn | Wat het is |
|---|---|
| pruim | glasvezel, in gebruik |
| geel met een zwarte rand | straalverbinding, in gebruik |
| oranje | gepland, voorgesteld of in aanleg (straalverbindingen met een zwarte rand) |
| grijs | zonder opgegeven status (straalverbindingen met een zwarte rand) |

⚠ Bij de dunne, vage lijndikte van de kaart lijken de straalverbindingen eerder
olijfgroen of kaki dan geel; de zwarte rand onderscheidt ze van glasvezel.

⚠ De ITU registreert voor een verbinding geen beheerder, naam, capaciteit of
datum, dus een verbinding is niet aanklikbaar, en geen storing wordt eraan
gekoppeld.

Je Home Assistant haalt de hele laag eens per week bij de ITU op, op zijn eigen
dag van de week en zijn eigen uur, en bewaart haar. Mislukt een ophaalbeurt of
komt die onvolledig terug, dan blijft de laatste goede kopie staan, hoe oud
ook.

---

## Alle entiteiten die het aanmaakt

| Entiteit | Wat het is |
|---|---|
| `sensor.live_track_internet_outages` | **Cloudflare Radar Internetstoringen**: hoeveel storingsmarkeringen er op de kaart staan (alleen met het token) |
| `sensor.live_track_internet_cables_in_trouble` | **Submarine cables Kabels met storing**: hoeveel kabels een lopende storing noemt (alleen met het token) |
| `sensor.live_track_internet_all_cables` | **Submarine cables Alle kabels**: het aantal kabels, 713 |
| `sensor.live_track_internet_landing_points` | **Submarine cables Aanlandingspunten**: het aantal aanlandingspunten, 1.928 |
| `sensor.live_track_internet_terrestrial_links` | **ITU Broadband Maps Verbindingen over land**: hoeveel verbindingen er getekend zijn (alleen zolang **Verbindingen over land van de ITU** is aangevinkt) |
| `geo_location.outage_…` | één per lopende storing en plaats, genoemd naar het meldingsnummer van Cloudflare (`geo_location.outage_1754`); hij komt en gaat met de melding |

Elke markering draagt `source: live_track_internet`, en haar status is haar
afstand tot je huis in kilometers. De sensoren horen bij drie apparaten:
**Cloudflare Radar**, **Submarine cables** en **ITU Broadband Maps**.

De attributen van de storingssensor: `open_records` (alle lopende meldingen,
ook die niet op de kaart), `not_on_map` en `last_success`.

⚠ **De markeringen hebben met opzet geen unieke ID.** Storingsmeldingen komen
en gaan, en een registerregel voor elke melding zou voor altijd blijven. Je
kunt ze daarom in de interface niet hernoemen, verbergen of aan een ruimte
toewijzen. De sensoren hebben unieke ID's en kunnen hernoemd worden.

Attributen die bij elke update veranderen, en de grote lijsten die de kaart
leest, worden uit de geschiedenis van Home Assistant gehouden, zodat je
database er niet door groeit.

---

## Wat het verstuurt en downloadt

**Over je locatie.** Niets. De locatie van je huis wordt alleen in je Home
Assistant gebruikt, om de afstand van elke markering te berekenen. Cloudflare
krijgt je token en de periode van het verzoek; de ITU krijgt het verzoek om
haar verbindingen. De kabelgegevens worden met de integratie meegeleverd en
niet gedownload. Elke dienst ziet je internetadres, zoals elke website.

**Hoeveel.** Groottes gemeten op 25 november 2026, tenzij de tabel iets anders
zegt.

| Bron | Wat en hoe vaak | Gemeten grootte | Na een fout |
|---|---|---|---|
| Cloudflare Radar, storingen | één verzoek elke 15 minuten, met je token: de meldingen van de laatste 24 uur | 447 bytes over de lijn (één melding) | een geweigerd token stopt de verzoeken en vraagt je om een nieuw. HTTP 429: wacht zo lang als Cloudflare vraagt, of 15 minuten, verdubbelend tot 2 uur. Andere fouten: opnieuw na 15, 30 en 60 minuten, daarna elke 2 uur. Het laatste goede antwoord blijft 2 uur bewaard; daarna verdwijnen de markeringen |
| Cloudflare Radar, plaatsen | de middelpunten van de landen eens per dag; het punt van een regio de eerste keer dat een melding haar noemt, daarna bewaard | de landenlijst: 36.905 bytes (23 november 2026) | de kopie die je hebt blijft in gebruik |
| ITU Broadband Maps | de hele laag eens per week, in 9 verzoeken met 3 seconden ertussen, samen ongeveer 36 seconden | ongeveer 0,9 MB over de lijn (111.537 bytes per 5.000 verbindingen) | HTTP 429: wacht zo lang als de ITU vraagt, of een uur, verdubbelend tot een dag. Andere fouten: opnieuw de volgende dag. De laatste goede kopie blijft |
| Je browser | van je Home Assistant, niet van het internet: het kabelbestand als **Alle kabels** is aangevinkt, de aanlandingspunten als **Aanlandingspunten** is aangevinkt, en het verbindingenbestand als **Verbindingen over land** is aangevinkt | kabels 113.323 bytes; aanlandingspunten 38.160 bytes; verbindingen 296.105 bytes | |

Vink **Verbindingen over land van de ITU** uit (**Herconfigureer**) om de
wekelijkse ophaalbeurt te stoppen. Verwijder het item om alles te stoppen.

De gedownloade bestanden worden bewaard in de map `.storage` van Home
Assistant, onder namen die met `saw_` beginnen (`saw_radar_locations.json`,
`saw_radar_geolocations.json`, `saw_itu_bbmaps_links.json.gz`), zodat een
andere Live Track-module ze kan delen. Verwijder je Live Track Internet en
gebruikt geen andere Live Track-module ze, dan kun je ze met de hand
verwijderen.

---

## Help het groeien

Live Track Internet groeit nog. We voegen gegevensbronnen toe zodra we ze
vinden, en we willen weten wat je hierna graag zou zien.

### Stel iets voor

Ontbreekt er een gegevensbron? Klopt er iets niet, of is iets moeilijk te
begrijpen? Laat het ons weten op de manier die voor jou het makkelijkst is:

* [**Vul een kort formulier in**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=nl.yml)
  in het Nederlands. Je hebt een gratis GitHub-account nodig.
* **Stuur een e-mail** naar
  [StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org).
  Geen account nodig.

Hoe je ons ook bereikt, het helpt als je vertelt:

* wat je graag zou zien, en waar ter wereld;
* een link naar waar de gegevens gepubliceerd worden, als je er een kent (een
  open-datapagina, een openbare feed, de website van een dienst): niet nodig,
  maar het helpt;
* de taal van je Home Assistant, als het probleem de tekst of een vertaling
  is.

Schrijf in het Engels of in je eigen taal, wat voor jou het makkelijkst is.

### Voeg het zelf toe, met onze hulp

Als je zelf iets wilt toevoegen, helpen we je daarbij, van de eerste vraag tot
de afgeronde release. Je hoeft geen ontwikkelaar te zijn om te beginnen:

* **Een vertaling.** De teksten in het instellingsvenster zijn een korte lijst
  zinnen in één tekstbestand. We laten je zien welk bestand en welke regels.
* **Een nieuwe bron.** Vertel ons waar de gegevens gepubliceerd worden. We
  kunnen de code samen schrijven, of die van jou nakijken.
* **Testen waar je woont.** Installeer het, bekijk jouw deel van de kaart, en
  vertel ons wat klopt en wat niet.
* **Een correctie op deze README.** Als een stap niet overeenkwam met wat je
  zag, vertel ons wat je zag.

[**Vertel ons wat je van plan bent**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=nl.yml)
of schrijf naar
[StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org),
en we antwoorden met de volgende stappen.

---

## Talen

Deze README: [English](README.md), [Deutsch](README.de.md),
[Français](README.fr.md), **Nederlands**, [简体中文](README.zh-Hans.md),
[Español](README.es.md), [Italiano](README.it.md),
[Українська](README.uk.md) en [العربية](README.ar.md). Elke vertaalde README
is volledig. Geen enkele is al door een moedertaalspreker gelezen. Is een van
deze talen de jouwe, laat ons dan weten of de README goed leest: zie
[Help het groeien](#help-het-groeien).

Het instellingsvenster verschijnt in de taal van je Home Assistant als het een
van deze is: English, Deutsch, Español, Français, Italiano, Nederlands,
简体中文, Українська en العربية. Elke andere taal toont Engels. Ook de
vertalingen van het venster zijn zonder moedertaalspreker geschreven. De
woorden op de kaart (de namen van de storingen en de teksten bij het klikken,
de namen van de oorzaken in de filterkaart en de bronvermeldingen) zijn in
elke taal Engels.

Een fout gevonden in een vertaling, of een andere taal nodig? Laat het ons
weten op <https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues>, of
[vertaal het met onze hulp](#voeg-het-zelf-toe-met-onze-hulp).

---

## Vermeldingen en licenties

* **Cloudflare Radar** (Cloudflare, Inc., <https://radar.cloudflare.com>): de
  storingsmeldingen, onder
  [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), gelezen met
  het eigen token van elke gebruiker. Deze integratie zet elke melding op de
  kaart; ze verandert de meldingen niet. Door deze integratie te installeren
  gebruik je de API van Cloudflare, en gelden de voorwaarden daarvan voor jou.
* **Zeekabels en aanlandingspunten**: Hotham, T. (2026), *The internet's
  seabed: submarine cables, when they were laid, who owns them and where they
  crowd together*, Zenodo, <https://doi.org/10.5281/zenodo.23856607>, afgeleid
  van de [Submarine Cable Map](https://www.submarinecablemap.com/) van
  TeleGeography, onder
  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Deze
  integratie heeft de kabellijnen aan de kabeltabel gekoppeld, beide omgezet
  in kaartbestanden en de aanlandingspunten afgerond op 4 decimalen; er is
  niets toegevoegd of verbeterd. De omgezette bestanden in
  `custom_components/live_track_internet/cables/` worden gedeeld onder dezelfde
  licentie, met de juridische tekst en een vermeldingsbestand ernaast
  ([CREDIT.md](custom_components/live_track_internet/cables/CREDIT.md)).
* **Verbindingen over land**: ITU Broadband Maps (BBmaps), de Infrastructure
  Connectivity Map, <https://bbmaps.itu.int>, © ITU. Gebruikt volgens de
  gebruiksvoorwaarden van de ITU voor niet-commercieel gebruik, met
  vermelding van de bron. Niets van de ITU wordt in deze repository
  meegeleverd: elke installatie haalt de verbindingen op voor haar eigen
  gebruiker. Deze integratie tekent ze zoals de ITU ze publiceert, afgerond op
  3 decimalen (ongeveer 110 m), met herhaalde verbindingen van dezelfde soort
  één keer getekend.
* **De plaatjes van de storingen** zijn getekend voor StrausbergAutomationWorks,
  onder de MIT-licentie.
* **De kaartkaart** is [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard),
  MIT, een kopie van [ha-map-card](https://github.com/nathan-gs/ha-map-card)
  van nathan-gs, MIT. De kaarttegels en hun vermeldingen staan in de README
  daarvan.

⚠ **Alleen voor niet-commercieel gebruik.** Alle drie de gegevensbronnen staan
alleen niet-commercieel gebruik toe. De code is MIT, maar de gegevens die ze
toont, mogen niet commercieel worden gebruikt.

Geen van deze organisaties heeft deze integratie gemaakt of onderschreven.
Welke licentie welk deel van deze repository dekt:
[ATTRIBUTION.md](ATTRIBUTION.md).

**Code**: MIT, in [LICENSE](LICENSE).

**Voor ontwikkelaars:** de entiteiten volgen het gedeelde kaartcontract van
Live Track, zodat elke module op één kaart verschijnt.
`tools/build_cables.py` bouwt de kabelbestanden opnieuw uit de repository van
Hotham. De tests draaien met `python -m unittest discover -s tests`.

---

## Trefwoorden

Home Assistant internetstoring · internetstoringskaart · internetafsluiting ·
internet-blackout · netwerkstoring · storing bij de provider · Cloudflare
Radar · Radar Outage Center · zeekabels · onderzeese kabels · zeekabelkaart ·
kabelbreuk · aanlandingspunten · TeleGeography · Submarine Cable Map ·
glasvezel over land · glasvezelkaart · glasvezel-backbone ·
straalverbindingen · ITU · ITU Broadband Maps · BBmaps · Infrastructure
Connectivity Map · internet outage · submarine cables · Internetausfall ·
Seekabel · panne internet · câbles sous-marins · 断网 · 海底光缆 · corte de
internet · cables submarinos · interruzione internet · cavi sottomarini ·
відключення інтернету · підводні кабелі · انقطاع الإنترنت · كابلات بحرية ·
geo_location · kaartkaart · Lovelace · HACS · Marketplace · Marktplaats ·
Live Track · LiveTrack · StrausbergAutomationWorks

---

**Erkenning.** StrausbergAutomationWorks erkent de inheemse volken van alle
landen en wateren op deze kaart, overal ter wereld, en betuigt zijn respect aan
hun Elders, van vroeger en nu.
