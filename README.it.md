# Live Track Internet

[English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Nederlands](README.nl.md) · [简体中文](README.zh-Hans.md) · [Español](README.es.md) · **Italiano** · [Українська](README.uk.md) · [العربية](README.ar.md) · [Tutte le lingue](#lingue)

**Interruzioni di internet, cavi sottomarini e collegamenti in fibra per Home
Assistant, su un'unica mappa.** Live Track Internet porta sulla tua mappa di
Home Assistant le interruzioni di internet che Cloudflare Radar registra in
qualsiasi parte del mondo, con la loro causa. Disegna anche ogni cavo
sottomarino con i suoi punti di approdo, e i collegamenti in fibra e a
microonde tra le località che l'UIT registra. Quando un'interruzione nomina un
cavo, quel cavo viene disegnato in rosso.

> **Live Track Internet è un modulo di Live Track**, una famiglia di
> integrazioni di Home Assistant che disegnano tutto ciò che si muove, e il
> tempo che attraversa, su una mappa condivisa: aerei, navi, treni e meteo.
> Installalo da solo o accanto agli altri moduli
> ([elenco più sotto](#parte-di-live-track-gli-altri-moduli)).

> **In crescita, e aperto alle idee.** Oggi Live Track Internet copre
> interruzioni, cavi e collegamenti terrestri in tutto il mondo, e stiamo
> aggiungendo altre fonti di dati (sono previsti i punti di interscambio
> internet e i data center). Manca qualcosa?
> [Suggeriscilo](#aiutaci-a-farlo-crescere), o aggiungilo tu: ti aiuteremo a
> farlo.

**Stato: 0.3.4, pubblicato.** Nel catalogo del Marketplace ([installalo più
sotto](#installazione-passo-dopo-passo)).

Opera originale di StrausbergAutomationWorks. Non affiliato con, né approvato
da, Cloudflare, Tristan Hotham, TeleGeography, l'Unione internazionale delle
telecomunicazioni (UIT), o qualsiasi proprietario di cavi od operatore di rete.

> ⚠ **Non sorveglia la tua connessione a internet.** Le interruzioni sono
> schede scritte da persone di Cloudflare, spesso ore dopo l'inizio di
> un'interruzione, e solo per interruzioni abbastanza grandi da vedersi dalla
> rete di Cloudflare. **Una mappa vuota non significa che internet funzioni
> ovunque.** Un cavo o un collegamento sulla mappa non dice se oggi trasporta
> traffico.

---

## Indice

1. [Tutto quello che fa](#tutto-quello-che-fa)
2. [Dove funziona](#dove-funziona)
3. [Parte di Live Track: gli altri moduli](#parte-di-live-track-gli-altri-moduli)
4. [Prima di iniziare](#prima-di-iniziare)
5. [Installazione, passo dopo passo](#installazione-passo-dopo-passo)
6. [Configurazione, passo dopo passo](#configurazione-passo-dopo-passo)
7. [Chiavi gratuite che attivano di più, passo dopo passo](#chiavi-gratuite-che-attivano-di-più-passo-dopo-passo)
8. [Mettere la mappa su una plancia](#mettere-la-mappa-su-una-plancia)
9. [Usarlo nelle automazioni](#usarlo-nelle-automazioni)
10. [Tutto sulla mappa, nel dettaglio](#tutto-sulla-mappa-nel-dettaglio)
11. [Tutte le entità che crea](#tutte-le-entità-che-crea)
12. [Cosa invia e scarica](#cosa-invia-e-scarica)
13. [Aiutaci a farlo crescere](#aiutaci-a-farlo-crescere)
14. [Lingue](#lingue)
15. [Riconoscimenti e licenze](#riconoscimenti-e-licenze)
16. [Parole chiave](#parole-chiave)

---

## Tutto quello che fa

### Sulla mappa, senza configurare nulla

Ognuno di questi è un livello con la sua casella nel controllo dei livelli
della mappa. Tutti partono **spenti**: spunta una casella per mostrarlo.

| Cosa | Dove | Da |
|---|---|---|
| **Tutti i cavi**: ogni cavo sottomarino, 608 in servizio e 105 previsti, come linee sottili; clicca su uno per nome, proprietari, lunghezza e paesi di approdo | tutto il mondo | il dataset di Tristan Hotham con i dati dei cavi di TeleGeography, fornito con l'integrazione |
| **Punti di approdo**: i 1.928 luoghi in cui i cavi arrivano a terra, come piccoli punti | tutto il mondo | lo stesso |
| **Collegamenti terrestri**: collegamenti in fibra e a microonde tra località sulla terraferma, disegnati in linea retta da un nodo al successivo | i paesi in cui l'UIT li ha raccolti ([dove](#dove-funziona)) | ITU Broadband Maps (BBmaps), scaricati dal tuo Home Assistant una volta alla settimana |

### Attivato dalla tua chiave o dal tuo account gratuito

| Chiave o account gratuito | Cosa aggiunge |
|---|---|
| Token API di **Cloudflare** | **Interruzioni**: un indicatore per ogni interruzione di internet in corso che Cloudflare Radar registra, nel paese o nella regione che nomina, colorato e disegnato secondo la sua causa; acceso di default. **Cavi con problemi**: ogni cavo sottomarino nominato da un'interruzione in corso, disegnato spesso e in rosso; acceso di default |

Si ottiene in pochi minuti: [passo dopo passo più sotto](#chiavi-gratuite-che-attivano-di-più-passo-dopo-passo).

---

## Dove funziona

| Regione | Cosa ottieni | Da | Serve |
|---|---|---|---|
| **Tutto il mondo** | interruzioni di internet, nel paese o nella regione che ogni scheda nomina | Cloudflare Radar | un token gratuito |
| **Tutto il mondo** | cavi sottomarini con problemi | Cloudflare Radar, e i dati dei cavi | un token gratuito |
| **Tutto il mondo** | tutti i cavi sottomarini e i punti di approdo | il dataset di Tristan Hotham con i dati di TeleGeography | niente |
| **Africa e Medio Oriente** | circa 5.400 collegamenti terrestri | ITU Broadband Maps | niente |
| **America centrale e meridionale** | circa 5.500 collegamenti terrestri | ITU Broadband Maps | niente |
| **Europa** | circa 12.400 collegamenti terrestri | ITU Broadband Maps | niente |
| **America del Nord** | circa 4.700 collegamenti terrestri | ITU Broadband Maps | niente |
| **Oceania** | circa 1.400 collegamenti terrestri | ITU Broadband Maps | niente |
| **Russia, Asia settentrionale e orientale** | circa 1.500 collegamenti terrestri | ITU Broadband Maps | niente |
| **Asia meridionale e sud-orientale** | circa 9.500 collegamenti terrestri | ITU Broadband Maps | niente |

I numeri dei collegamenti sono stati misurati il 25 novembre 2026 e sono
approssimativi: ogni collegamento è contato dal suo primo estremo. L'UIT
pubblica in tutto circa 40.000 collegamenti.

⚠ **La copertura dei collegamenti terrestri è disomogenea.** L'UIT mostra ciò
che operatori e autorità di regolamentazione le hanno fornito. Alcuni paesi sono
disegnati nel dettaglio (India, Brasile, gran parte dell'Europa); altri hanno
pochi collegamenti o nessuno.

Non è nell'elenco? [Diccelo](#aiutaci-a-farlo-crescere). Dove qualcuno pubblica
i dati apertamente, valuteremo di aggiungerli.

---

## Parte di Live Track: gli altri moduli

Live Track è un insieme di integrazioni di Home Assistant, una per ogni tipo
di cosa che si muove, tutte disegnate sulla stessa scheda mappa. Ognuna
funziona da sola; insieme formano un'unica immagine dal vivo. Condividono la
scheda mappa e una libreria Python
([saw-livetrack](https://github.com/StrausbergAutomationWorks/LiveTrackCore)),
quindi installarne un'altra non aggiunge richieste a una fonte che un'altra
già legge.

| Modulo | Cosa mette sulla mappa | Stato |
|---|---|---|
| [Live Track Aircraft](https://github.com/StrausbergAutomationWorks/LiveTrackAircraft) | aerei sopra di te tramite ADS-B, con rotte e icone per tipo | pubblicato |
| [Live Track Ships](https://github.com/StrausbergAutomationWorks/LiveTrackShips) | navi e imbarcazioni tramite AIS, vicino a te o ovunque | pubblicato |
| [Live Track Commuter Rail](https://github.com/StrausbergAutomationWorks/LiveTrackCommuterRail) | treni suburbani in Nord America, Europa e Australia | pubblicato |
| [Live Track Intercity Rail](https://github.com/StrausbergAutomationWorks/LiveTrackIntercityRail) | treni intercity e a lunga percorrenza in Nord America, Europa e Australia | pubblicato |
| [Live Track SALT](https://github.com/StrausbergAutomationWorks/LiveTrackSALT) | aerei e imbarcazioni dell'immigrazione e delle forze dell'ordine federali, da elenchi pubblici | pubblicato |
| [Live Track Weather](https://github.com/StrausbergAutomationWorks/LiveTrackWeather) | meteo, tempeste e rischi naturali | pubblicato |
| **Live Track Internet** | interruzioni di internet, cavi sottomarini e collegamenti terrestri (questo modulo) | pubblicato |
| Live Track Stations | tabelloni delle partenze e avvisi "è ora di andare" per ogni stazione | previsto |
| Live Track Satellites | satelliti che passano sopra di te | previsto |
| Live Track Freight Trains | treni merci e di servizio dove le ferrovie li pubblicano | previsto |
| Live Track Transit | autobus urbani, tram, traghetti e metropolitana | previsto |
| Live Track Intercity Buses | autobus interurbani e regionali | previsto |
| Live Track Commuter Buses | autobus per pendolari | previsto |
| [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard) | la scheda mappa condivisa su cui disegna ogni modulo | pubblicata, installata con ogni modulo |

Tutto è gratuito e open source. Niente è riservato agli sponsor.

---

## Prima di iniziare

* **Home Assistant** 2026.11 o successivo.
* **Il Marketplace** (HACS) nel tuo Home Assistant, per installarlo e
  aggiornarlo nel modo più semplice. Senza, puoi copiare i file a mano.
* **Accesso a internet** per Home Assistant: le interruzioni e i collegamenti
  terrestri arrivano da servizi pubblici.
* Niente da pagare e nessun account necessario per i cavi e i collegamenti.
  Il token gratuito di Cloudflare qui sopra è facoltativo.
* Home Assistant installa da solo il pacchetto Python che gli serve
  (`saw-livetrack`) la prima volta che l'integrazione si carica.

---

## Installazione, passo dopo passo

### Dal Marketplace (consigliato)

1. In Home Assistant, apri **Impostazioni → Marketplace** (HACS).
2. Cerca **Live Track Internet** e aprilo.
3. Scegli **Scarica** (o **Installa**).
4. **Riavvia Home Assistant**: **Impostazioni → Sistema → Riparazioni** offre
   il riavvio, oppure usa **Impostazioni → Sistema → Riavvia Home Assistant**.

Se la ricerca non lo trova, aggiungilo tramite il suo collegamento: scegli la
scheda **Aggiungi dal collegamento** (oppure il menu a tre puntini →
**Repository personalizzati**), inserisci `StrausbergAutomationWorks/LiveTrackInternet`,
scegli **Integrazione** se viene chiesto il tipo, poi prosegui dal passo 3.

Il Marketplace offre poi ogni nuova versione come aggiornamento.

### A mano

1. Scarica il codice sorgente dell'[ultima versione](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/releases/latest).
2. Copia la sua cartella `custom_components/live_track_internet` nella cartella
   `custom_components` della cartella di configurazione di Home Assistant
   (crea `custom_components` se non c'è).
3. Riavvia Home Assistant.

Per aggiornare a mano, sostituisci la cartella con quella della nuova versione
e riavvia.

---

## Configurazione, passo dopo passo

1. Apri **Impostazioni → Dispositivi e servizi**.
2. Scegli **Aggiungi integrazione** (in basso a destra) e cerca **Live Track
   Internet**.
3. **Token API di Cloudflare**: incolla il tuo token se ne hai uno
   ([come ottenerne uno](#chiavi-gratuite-che-attivano-di-più-passo-dopo-passo)).
   Lascialo vuoto per mostrare solo i cavi e i collegamenti; puoi aggiungere
   un token in seguito.
4. **Collegamenti terrestri dall'UIT**: lascialo spuntato. Togli la spunta se
   non vuoi che il tuo Home Assistant scarichi i collegamenti dall'UIT una
   volta alla settimana (circa 1 MB).
5. Scegli **Invia**.

È tutto. La voce si chiama **Cloudflare Radar** con un token, oppure
**Submarine cables** senza. C'è una sola voce: una seconda disegnerebbe ogni
interruzione due volte, quindi viene rifiutata.

* I livelli dei cavi e dei punti di approdo ci sono subito.
* Con un token, le interruzioni in corso compaiono entro un minuto.
* I collegamenti terrestri compaiono qualche minuto dopo la configurazione,
  quando il primo scaricamento dall'UIT è finito.

Ogni livello parte spento. Spuntalo nel controllo dei livelli della mappa per
vederlo ([Mettere la mappa su una plancia](#mettere-la-mappa-su-una-plancia)).

### Cambiare in seguito il token o la casella UIT

1. Apri **Impostazioni → Dispositivi e servizi → Live Track Internet**.
2. Apri il menu a tre puntini della voce e scegli **Riconfigura**.
3. Incolla un nuovo token, o lascia il campo vuoto per tenere quello che hai.
   Spunta o togli la spunta a **Collegamenti terrestri dall'UIT**.
4. Scegli **Invia**.

Per togliere il token, elimina la voce (**Elimina** nello stesso menu) e
aggiungi di nuovo Live Track Internet senza token. Se in seguito Cloudflare
rifiuta il tuo token (è stato cancellato o è scaduto), gli indicatori delle
interruzioni si fermano, e Home Assistant ti chiede un nuovo token in
**Impostazioni → Dispositivi e servizi**.

---

## Chiavi gratuite che attivano di più, passo dopo passo

Il token è gratuito e personale: ogni persona che installa Live Track Internet
crea il proprio. Ti serve un account Cloudflare gratuito; non ti serve un sito
web né un dominio su Cloudflare.

### Token API di Cloudflare (interruzioni di internet, tutto il mondo)

1. Accedi a Cloudflare, o crea un account gratuito, su
   <https://dash.cloudflare.com>.
2. Apri <https://dash.cloudflare.com/profile/api-tokens> (**My Profile → API
   Tokens**) e scegli **Create Token**.
3. Non usare un modello: parti da zero, con un token personalizzato. Dagli un
   nome, per esempio `Live Track Internet`.
4. Nei permessi, scegli **Account**, poi **Radar**, poi **Read**. Non serve
   altro.
5. Scegli **Continue to summary**, poi **Create Token**.
6. Copia subito il token: Cloudflare lo mostra una sola volta.
7. Incollalo in **Token API di Cloudflare** quando
   [configuri](#configurazione-passo-dopo-passo) Live Track Internet, o in
   seguito con **Riconfigura**.

Live Track Internet controlla il token con una vera richiesta a Cloudflare
Radar prima di salvarlo. Il token resta nel tuo Home Assistant e viene inviato
solo a Cloudflare. Oltre al token non serve nessuna password né altro segreto.
I nomi dei pulsanti sono riportati qui come Cloudflare li mostra in inglese; se
Cloudflare ti mostra le sue pagine in italiano, lì hanno altri nomi.

---

## Mettere la mappa su una plancia

La mappa è [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard),
la scheda su cui disegna ogni modulo di Live Track. **Viene installata con Live
Track Internet**: niente da scaricare, niente da copiare, nessuna risorsa da
aggiungere.

1. Apri una plancia, scegli la matita (**Modifica la plancia**), poi
   **Aggiungi scheda**.
2. Scorri fino in fondo e scegli **Manuale**.
3. Incolla questo e scegli **Salva**:

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

I livelli dei cavi e dei collegamenti compaiono da soli. Gli indicatori delle
interruzioni arrivano tramite il filtro qui sopra.

Gli altri moduli di Live Track vanno in `entity_filter` allo stesso modo: una
regola `- domain: geo_location` in più per ogni fonte.

**Sulla mappa:**

* Il **controllo dei livelli** in alto a destra ha una casella per ogni
  livello: **Cavi con problemi**, **Tutti i cavi**, **Punti di approdo** e
  **Collegamenti terrestri**. La scelta di ogni persona che guarda viene
  conservata nel suo browser.
* Ogni interruzione è un'immagine rotonda della sua causa, con accanto il
  codice di due lettere del paese. **Punta** su di essa per vedere dove e
  perché; **clicca** per la descrizione di Cloudflare, un collegamento alla
  notizia e la pagina del traffico di Cloudflare Radar per ogni rete, regione
  o paese che l'interruzione nomina, dal giorno prima del suo inizio (al
  massimo quattro collegamenti).
* **Clicca** su un cavo per nome, proprietari, lunghezza e paesi di approdo. I
  collegamenti terrestri non sono cliccabili.
* La **scheda filtro** (`custom:live-track-map-filter-card`) può nascondere le
  interruzioni in base alla causa.
* Il riconoscimento di ogni fonte compare nella riga di attribuzione della
  mappa finché i suoi dati sono mostrati.

La scheda mantiene esattamente una riga di risorsa delle plance per tutti i
moduli di Live Track insieme: la versione più recente della scheda portata da
uno di essi, mai una più vecchia. Una scheda che hai installato tu dal
Marketplace non viene toccata. Se le risorse delle tue plance sono definite in
YAML (`lovelace: resource_mode: yaml`), non si può registrare nulla per te:
allora un problema in **Riparazioni** ti dà la riga esatta da aggiungere, che
ha questo aspetto, con l'indirizzo proprio dell'integrazione al posto dei
segnaposto:

```yaml
lovelace:
  resource_mode: yaml
  resources:
    - url: /live_track_internet/map-card/<12 hex>/live-track-map-card.js?v=<version>&h=<12 hex>
      type: module
```

Eliminando la voce di Live Track Internet, la riga passa a un altro modulo di
Live Track, oppure viene tolta se non ne resta nessuno. Se i file
dell'integrazione vengono rimossi mentre la sua voce è ancora configurata, e
non è installato nessun altro modulo di Live Track, togli tu la riga della
scheda in **Impostazioni → Plance → Risorse**. Per installare invece la scheda
a mano, segui il README della scheda. Una riga che hai creato tu, per una copia
sotto `/local/` o a qualsiasi altro indirizzo, non viene mai cambiata né tolta.
Finché carica la scheda, ogni modulo di Live Track le lascia la scheda, anche
quando un modulo porta una versione più nuova, e in **Riparazioni** non compare
nulla. Per tornare alla copia del modulo, togli la tua riga in **Impostazioni →
Plance → Risorse** e riavvia Home Assistant. Se cancelli il file della tua
copia, togli anche la sua riga: finché resta una riga il cui file non c'è più,
il modulo non aggiunge una riga sua. Qualsiasi altra scheda mappa che mostri le
entità `geo_location` mostra anche gli indicatori delle interruzioni, ma non i
cavi né i collegamenti.

---

## Usarlo nelle automazioni

Tutto è un'entità normale di Home Assistant, quindi l'editor delle automazioni
funziona con essa, senza codice.

**Una notifica sul telefono quando Cloudflare registra una nuova interruzione
di internet** (serve il token di Cloudflare):

1. **Impostazioni → Automazioni e scenari → Crea automazione → Crea una nuova
   automazione**.
2. **Quando**: **Aggiungi attivazione**, scrivi `numeric` nella casella di
   ricerca e scegli **Stato numerico oltre la soglia**. Scegli l'**Entità**
   **Cloudflare Radar Interruzioni di internet**, e in **Maggiore di** inserisci
   `0`.
3. **Allora**: **Aggiungi azione**, cerca l'azione di notifica del tuo telefono
   (porta il nome del tuo telefono) e scrivi un messaggio, per esempio:

   ```text
   Cloudflare Radar segnala un'interruzione di internet
   ```

4. **Salva**.

**Altre idee:** una notifica quando un'interruzione nomina un cavo
sottomarino, con **Submarine cables Cavi con problemi** maggiore di 0; un
riquadro della plancia con il numero di interruzioni in corso, da
**Cloudflare Radar Interruzioni di internet**.

---

## Tutto sulla mappa, nel dettaglio

### Interruzioni

[Cloudflare Radar](https://radar.cloudflare.com) tiene un Outage Center: schede
sulle interruzioni di internet nel mondo, scritte da persone di Cloudflare,
ognuna con una causa, un tipo (nazionale, regionale o una sola rete), i paesi o
le regioni colpiti, un'ora di inizio e di solito un collegamento a una notizia.

Live Track Internet chiede le schede delle ultime 24 ore ogni 15 minuti e
disegna un indicatore per ogni scheda in corso in ogni luogo che nomina: nella
regione quando la scheda ne nomina una, altrimenti nel paese. Una scheda che si
chiude lascia la mappa. Le schede su un servizio online invece che su un luogo
(l'interruzione di un fornitore cloud, per esempio) non vengono disegnate; il
sensore **Cloudflare Radar Interruzioni di internet** le elenca nel suo
attributo `not_on_map`.

⚠ **Una scheda che nomina solo una rete viene messa al centro del suo paese**,
che in un paese grande può essere lontano dall'interruzione. Il testo del clic
lo dice. Per esempio, Cloudflare classifica due reti di Luhansk e Donetsk
(Ucraina) sotto la Russia, quindi le loro interruzioni finiscono nella Siberia
centrale, e le reti degli Stati Uniti finiscono in Kansas.

⚠ Le schede delle interruzioni sono scritte da persone, spesso ore dopo
l'inizio di un'interruzione. Quando abbiamo misurato un anno di schede (fino al
23 novembre 2026), erano 143, mai più di 4 in corso insieme, e per il 43% del
tempo nessuna era in corso. Il più delle volte la mappa non mostra alcuna
interruzione.

Ogni indicatore è disegnato secondo la sua causa:

| Causa | Colore | Immagine |
|---|---|---|
| Cavo tagliato | rosso | forbici aperte |
| Interruzione di corrente | ambra | fulmine |
| Disposta da un governo (un blocco) | indaco | lucchetto |
| Azione militare | nero | mirino |
| Meteo o calamità naturale | blu | nuvola temporalesca |
| Attacco informatico | verde acqua | scudo con `!` |
| Problema tecnico (rete, software, DNS, manutenzione) | grigio bluastro | chiave inglese |
| Causa sconosciuta | grigio | `?` |

Su ogni indicatore: `outage_cause` e `outage_type` (le parole di Cloudflare,
per esempio `POWER_OUTAGE`, `NATIONWIDE`), `started_at`, `place_kind`
(`region`, `country` o `network`), `country_code`, `country_name`,
`region_name`, `asns` e `asn_names` quando la scheda nomina delle reti,
`description`, `linked_url` (la notizia), `marker_links` (i collegamenti che mostra un clic), `cables_named` quando la descrizione
nomina un cavo, e `marker_group` (la causa, per la scheda filtro).

### Cavi con problemi

Con il token di Cloudflare, ogni cavo sottomarino nominato nella descrizione di
un'interruzione in corso viene disegnato spesso e in rosso con un bordo bianco,
acceso di default. Di solito non ce n'è nessuno. Il cavo viene riconosciuto dal
suo nome, scritto in uno dei modi abituali (`SEA-ME-WE 5`, `SeaMeWe-5`); i nomi
brevi vengono riconosciuti solo come parole intere.

⚠ Il campo della causa di Cloudflare non dice se un cavo tagliato è
sottomarino: nell'anno misurato, l'unica scheda classificata come cavo tagliato
riguardava un cavo a terra, e un guasto sul cavo SEA-ME-WE 5 era classificato
come causa sconosciuta. Per questo il cavo viene cercato nella descrizione,
qualunque sia la causa.

### Tutti i cavi e i punti di approdo

Ogni cavo sottomarino del dataset 2026 di Tristan Hotham con i dati dei cavi di
TeleGeography: 713 cavi, 608 in servizio (disegnati in blu) e 105 previsti
(disegnati in arancione), come linee sottili e tenui, e 1.928 punti di approdo
come piccoli punti (arancioni dove approdano solo cavi previsti). Clicca su un
cavo per il suo nome, la data in cui è entrato o entrerà in servizio, la sua
lunghezza, i suoi paesi di approdo, i suoi proprietari e il suo fornitore. I
dati sono forniti con l'integrazione e cambiano solo con una nuova versione.

⚠ Un cavo posato dopo la creazione del dataset (novembre 2026) compare solo
dopo una versione che porti dati più recenti.

### Collegamenti terrestri

I collegamenti in fibra e a microonde sulla terraferma registrati dalle
Broadband Maps dell'UIT (Infrastructure Connectivity Map), da operatori e
autorità di regolamentazione. Ogni collegamento è disegnato come l'UIT lo
pubblica: una linea retta da un nodo al successivo, non il percorso che il cavo
segue sul terreno.

| Linea | Cos'è |
|---|---|
| prugna | fibra, in servizio |
| giallo con bordo nero | microonde, in servizio |
| arancione | previsto, proposto o in costruzione (quelli a microonde con bordo nero) |
| grigio | senza stato indicato (quelli a microonde con bordo nero) |

⚠ Con lo spessore sottile e tenue delle linee della mappa, quelle a microonde
sembrano più oliva o cachi che gialle; è il bordo nero a distinguerle dalla
fibra.

⚠ L'UIT non registra operatore, nome, capacità né data di un collegamento,
quindi un collegamento non è cliccabile, e nessuna interruzione gli viene
associata.

Il tuo Home Assistant scarica tutto il livello dall'UIT una volta alla
settimana, nel suo giorno e alla sua ora, e lo conserva. Se uno scaricamento
non riesce o arriva incompleto, resta l'ultima copia buona, per quanto vecchia.

---

## Tutte le entità che crea

| Entità | Cos'è |
|---|---|
| `sensor.live_track_internet_outages` | **Cloudflare Radar Interruzioni di internet**: quanti indicatori di interruzione ci sono sulla mappa (solo con il token) |
| `sensor.live_track_internet_cables_in_trouble` | **Submarine cables Cavi con problemi**: quanti cavi nomina un'interruzione in corso (solo con il token) |
| `sensor.live_track_internet_all_cables` | **Submarine cables Tutti i cavi**: il numero di cavi, 713 |
| `sensor.live_track_internet_landing_points` | **Submarine cables Punti di approdo**: il numero di punti di approdo, 1.928 |
| `sensor.live_track_internet_terrestrial_links` | **ITU Broadband Maps Collegamenti terrestri**: quanti collegamenti sono disegnati (solo finché **Collegamenti terrestri dall'UIT** è spuntato) |
| `geo_location.outage_…` | uno per ogni interruzione in corso e per luogo, con il numero di scheda di Cloudflare nel nome (`geo_location.outage_1754`); va e viene con la scheda |

Ogni indicatore porta `source: live_track_internet`, e il suo stato è la sua
distanza da casa tua in chilometri. I sensori stanno su tre dispositivi:
**Cloudflare Radar**, **Submarine cables** e **ITU Broadband Maps**.

Gli attributi del sensore delle interruzioni: `open_records` (tutte le schede
in corso, anche quelle non sulla mappa), `not_on_map` e `last_success`.

⚠ **Gli indicatori non hanno un ID univoco, di proposito.** Le schede delle
interruzioni vanno e vengono, e una riga di registro per ciascuna resterebbe
per sempre. Quindi non si possono rinominare, nascondere o assegnare a un'area
nell'interfaccia. I sensori hanno ID univoci e si possono rinominare.

Gli attributi che cambiano a ogni aggiornamento, e i grandi elenchi che la
mappa legge, sono tenuti fuori dalla cronologia di Home Assistant, così il tuo
database non cresce con essi.

---

## Cosa invia e scarica

**Sulla tua posizione.** Niente. La posizione di casa tua viene usata solo
dentro il tuo Home Assistant, per calcolare la distanza di ogni indicatore.
Cloudflare riceve il tuo token e l'intervallo di tempo della richiesta; l'UIT
riceve la richiesta dei suoi collegamenti. I dati dei cavi sono forniti con
l'integrazione e non vengono scaricati. Ogni servizio vede il tuo indirizzo
internet, come qualsiasi sito web.

**Quanto.** Dimensioni misurate il 25 novembre 2026, salvo diversa indicazione
nella tabella.

| Fonte | Cosa e quanto spesso | Dimensione misurata | Dopo un errore |
|---|---|---|---|
| Cloudflare Radar, interruzioni | una richiesta ogni 15 minuti, con il tuo token: le schede delle ultime 24 ore | 447 byte trasferiti (una scheda) | un token rifiutato ferma le richieste e te ne chiede uno nuovo. HTTP 429: aspetta quanto chiede Cloudflare, o 15 minuti, raddoppiando fino a 2 ore. Altri errori: nuovo tentativo dopo 15, 30 e 60 minuti, poi ogni 2 ore. L'ultima risposta buona viene tenuta 2 ore; poi gli indicatori spariscono |
| Cloudflare Radar, luoghi | i punti centrali dei paesi una volta al giorno; il punto di una regione la prima volta che una scheda la nomina, poi conservato | l'elenco dei paesi: 36.905 byte (23 novembre 2026) | resta in uso la copia che hai |
| ITU Broadband Maps | tutto il livello una volta alla settimana, in 9 richieste a 3 secondi di distanza, circa 36 secondi in tutto | circa 0,9 MB trasferiti (111.537 byte per ogni 5.000 collegamenti) | HTTP 429: aspetta quanto chiede l'UIT, o un'ora, raddoppiando fino a un giorno. Altri errori: nuovo tentativo il giorno dopo. Resta l'ultima copia buona |
| Il tuo browser | dal tuo Home Assistant, non da internet: il file dei cavi quando **Tutti i cavi** è spuntato, i punti di approdo quando **Punti di approdo** è spuntato, e il file dei collegamenti quando **Collegamenti terrestri** è spuntato | cavi 113.323 byte; punti di approdo 38.160 byte; collegamenti 296.105 byte | |

Togli la spunta a **Collegamenti terrestri dall'UIT** (**Riconfigura**) per
fermare lo scaricamento settimanale. Elimina la voce per fermare tutto.

I file scaricati sono conservati nella cartella `.storage` di Home Assistant
con nomi che iniziano con `saw_` (`saw_radar_locations.json`,
`saw_radar_geolocations.json`, `saw_itu_bbmaps_links.json.gz`), così un altro
modulo di Live Track può condividerli. Se togli Live Track Internet e nessun
altro modulo di Live Track li usa, puoi cancellarli a mano.

---

## Aiutaci a farlo crescere

Live Track Internet sta ancora crescendo. Aggiungiamo fonti di dati man mano
che le troviamo, e vogliamo sapere cosa ti piacerebbe dopo.

### Suggerisci qualcosa

Manca una fonte di dati? Qualcosa è sbagliato o difficile da capire? Diccelo
nel modo più facile per te:

* [**Compila un breve modulo**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=it.yml)
  in italiano. Ti serve un account GitHub gratuito.
* **Scrivi un'email** a
  [StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org).
  Non serve un account.

In entrambi i casi, ci aiuta se ci dici:

* cosa ti piacerebbe vedere, e dove nel mondo;
* un link a dove vengono pubblicati i dati, se ne conosci uno (una pagina di
  open data, un feed pubblico, il sito di un servizio): non è necessario, ma
  aiuta;
* la lingua del tuo Home Assistant, se il problema riguarda il testo o una
  traduzione.

Scrivi in inglese o nella tua lingua, come ti è più facile.

### Aggiungilo tu, con il nostro aiuto

Se vuoi aggiungere qualcosa tu stesso, ti aiuteremo a farlo, dalla prima
domanda fino alla versione finita. Non devi essere uno sviluppatore per
iniziare:

* **Una traduzione.** I testi della finestra di configurazione sono un breve
  elenco di frasi in un unico file di testo. Ti mostreremo quale file e quali
  righe.
* **Una nuova fonte.** Dicci dove vengono pubblicati i dati. Possiamo scrivere
  il codice insieme, o rivedere il tuo.
* **Provarlo dove vivi.** Installalo, guarda la tua parte della mappa e dicci
  cosa è giusto e cosa no.
* **Una correzione a questo README.** Se un passaggio non corrispondeva a
  quello che hai visto, dicci cosa hai visto.

[**Raccontaci cosa hai in mente**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=it.yml)
o scrivi a
[StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org),
e ti risponderemo con i passi successivi.

---

## Lingue

Questo README: [English](README.md), [Deutsch](README.de.md),
[Français](README.fr.md), [Nederlands](README.nl.md),
[简体中文](README.zh-Hans.md), [Español](README.es.md), **Italiano**,
[Українська](README.uk.md) e [العربية](README.ar.md). Ogni README tradotto è
completo. Nessuno è ancora stato letto da un madrelingua. Se una di queste è la
tua lingua, dicci se il suo README si legge bene: vedi
[Aiutaci a farlo crescere](#aiutaci-a-farlo-crescere).

La finestra di configurazione compare nella lingua del tuo Home Assistant
quando è una di queste: English, Deutsch, Español, Français, Italiano,
Nederlands, 简体中文, Українська e العربية. Qualsiasi altra lingua mostra
l'inglese. Anche le traduzioni della finestra sono state scritte senza un
madrelingua. Le parole sulla mappa (i nomi delle interruzioni e i testi del
clic, i nomi delle cause nella scheda filtro e i riconoscimenti) sono in
inglese in tutte le lingue.

Hai trovato un errore in una traduzione, o ti serve un'altra lingua? Diccelo
su <https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues>, o
[traducilo con il nostro aiuto](#aggiungilo-tu-con-il-nostro-aiuto).

---

## Riconoscimenti e licenze

* **Cloudflare Radar** (Cloudflare, Inc., <https://radar.cloudflare.com>): le
  schede delle interruzioni, con licenza
  [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), lette con il
  token proprio di ogni utente. Questa integrazione mette ogni scheda sulla
  mappa; non cambia le schede. Installando questa integrazione usi l'API di
  Cloudflare, e le sue condizioni si applicano a te.
* **Cavi sottomarini e punti di approdo**: Hotham, T. (2026), *The internet's
  seabed: submarine cables, when they were laid, who owns them and where they
  crowd together*, Zenodo, <https://doi.org/10.5281/zenodo.23856607>, derivato
  dalla [Submarine Cable Map](https://www.submarinecablemap.com/) di
  TeleGeography, con licenza
  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
  Questa integrazione ha collegato le linee dei cavi alla tabella dei cavi,
  convertito entrambe in file di mappa e arrotondato i punti di approdo a
  4 decimali; non è stato aggiunto né corretto nulla. I file convertiti in
  `custom_components/live_track_internet/cables/` sono condivisi con la stessa
  licenza, con il suo testo legale e un file di riconoscimento accanto
  ([CREDIT.md](custom_components/live_track_internet/cables/CREDIT.md)).
* **Collegamenti terrestri**: ITU Broadband Maps (BBmaps), l'Infrastructure
  Connectivity Map, <https://bbmaps.itu.int>, © UIT. Usati secondo le
  condizioni d'uso dell'UIT per uso non commerciale, citando la fonte. Questo
  repository non contiene nulla dell'UIT: ogni installazione scarica i
  collegamenti per il proprio utente. Questa integrazione li disegna come
  l'UIT li pubblica, arrotondati a 3 decimali (circa 110 m), con i
  collegamenti ripetuti dello stesso tipo disegnati una sola volta.
* **Le immagini delle interruzioni** sono state disegnate per
  StrausbergAutomationWorks, con licenza MIT.
* **La scheda mappa** è [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard),
  MIT, una copia di [ha-map-card](https://github.com/nathan-gs/ha-map-card) di
  nathan-gs, MIT. Le sue tessere di mappa e i loro riconoscimenti sono nel suo
  README.

⚠ **Solo per uso non commerciale.** Tutte e tre le fonti di dati consentono
solo l'uso non commerciale. Il codice è MIT, ma i dati che mostra non possono
essere usati a fini commerciali.

Nessuna di queste organizzazioni ha creato o approvato questa integrazione.
Quale licenza copre quale parte di questo repository:
[ATTRIBUTION.md](ATTRIBUTION.md).

**Codice**: MIT, in [LICENSE](LICENSE).

**Per gli sviluppatori:** le entità seguono il contratto di mappa condiviso di
Live Track, così ogni modulo compare su un'unica mappa.
`tools/build_cables.py` ricostruisce i file dei cavi dal repository di Hotham.
I test si eseguono con `python -m unittest discover -s tests`.

---

## Parole chiave

Home Assistant interruzione di internet · mappa delle interruzioni di
internet · blocco di internet · blackout internet · guasto di rete · guasto
del provider · Cloudflare Radar · Radar Outage Center · cavi sottomarini ·
cavo sottomarino · mappa dei cavi sottomarini · cavo tagliato · punti di
approdo · TeleGeography · Submarine Cable Map · fibra terrestre · mappa della
fibra ottica · dorsale in fibra · ponti radio a microonde · UIT · ITU
Broadband Maps · BBmaps · Infrastructure Connectivity Map · internet outage ·
submarine cables · Internetausfall · Seekabel · panne internet · câbles
sous-marins · internetstoring · zeekabels · 断网 · 海底光缆 · corte de
internet · cables submarinos · відключення інтернету · підводні кабелі ·
انقطاع الإنترنت · كابلات بحرية · geo_location · scheda mappa · Lovelace ·
HACS · Marketplace · Live Track · LiveTrack · StrausbergAutomationWorks

---

**Riconoscimento.** StrausbergAutomationWorks riconosce i popoli indigeni di
tutte le terre e le acque di questa mappa, in tutto il mondo, e rende omaggio ai
loro Anziani del passato e del presente.
