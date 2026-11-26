# Live Track Internet

[English](README.md) · [Deutsch](README.de.md) · **Français** · [Nederlands](README.nl.md) · [简体中文](README.zh-Hans.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Українська](README.uk.md) · [العربية](README.ar.md) · [Toutes les langues](#langues)

**Pannes d'internet, câbles sous-marins et liaisons en fibre pour Home
Assistant, sur une seule carte.** Live Track Internet affiche sur votre carte
Home Assistant les pannes d'internet que Cloudflare Radar enregistre partout
dans le monde, avec leur cause. Il dessine aussi chaque câble sous-marin et ses
points d'atterrissement, et les liaisons en fibre et par faisceau hertzien
entre les villes que l'UIT recense. Quand une panne nomme un câble, ce câble
est dessiné en rouge.

> **Live Track Internet est un module de Live Track**, une famille
> d'intégrations Home Assistant qui dessinent tout ce qui bouge, et la météo
> que cela traverse, sur une carte partagée : avions, navires, trains et
> météo. Installez-le seul ou à côté des autres modules
> ([liste ci-dessous](#les-autres-modules-de-live-track)).

> **En croissance, et ouvert aux idées.** Aujourd'hui, Live Track Internet
> couvre les pannes, les câbles et les liaisons terrestres dans le monde
> entier, et nous ajoutons d'autres sources de données (les points d'échange
> internet et les centres de données sont prévus). Quelque chose manque ?
> [Proposez-le](#aidez-le-à-grandir), ou ajoutez-le vous-même : nous vous
> aiderons à le faire.

**État : 0.3.0, la première version.** Ajouté au Marketplace par son lien
([ci-dessous](#installation-pas-à-pas)) ; il n'est pas encore dans le
catalogue du Marketplace.

Œuvre originale de StrausbergAutomationWorks. Sans lien avec, ni approbation
de, Cloudflare, Tristan Hotham, TeleGeography, l'Union internationale des
télécommunications (UIT), ni aucun propriétaire de câble ou opérateur de
réseau.

> ⚠ **Ce n'est pas une surveillance de votre propre connexion.** Les pannes
> sont des fiches que des personnes chez Cloudflare rédigent, souvent des
> heures après le début d'une panne, et seulement pour des pannes assez
> grandes pour être vues depuis le réseau de Cloudflare. **Une carte vide ne
> veut pas dire qu'internet fonctionne partout.** Un câble ou une liaison sur
> la carte ne dit pas s'il transporte du trafic aujourd'hui.

---

## Sommaire

1. [Tout ce qu'il fait](#tout-ce-quil-fait)
2. [Où il fonctionne](#où-il-fonctionne)
3. [Les autres modules de Live Track](#les-autres-modules-de-live-track)
4. [Avant de commencer](#avant-de-commencer)
5. [Installation, pas à pas](#installation-pas-à-pas)
6. [Configuration, pas à pas](#configuration-pas-à-pas)
7. [Clés gratuites qui activent davantage, pas à pas](#clés-gratuites-qui-activent-davantage-pas-à-pas)
8. [Mettre la carte sur un tableau de bord](#mettre-la-carte-sur-un-tableau-de-bord)
9. [L'utiliser dans des automatisations](#lutiliser-dans-des-automatisations)
10. [Tout ce qui est sur la carte, en détail](#tout-ce-qui-est-sur-la-carte-en-détail)
11. [Toutes les entités qu'il crée](#toutes-les-entités-quil-crée)
12. [Ce qu'il envoie et télécharge](#ce-quil-envoie-et-télécharge)
13. [Aidez-le à grandir](#aidez-le-à-grandir)
14. [Langues](#langues)
15. [Crédits et licences](#crédits-et-licences)
16. [Mots-clés](#mots-clés)

---

## Tout ce qu'il fait

### Sur la carte, sans rien configurer

Chacune de ces couches a sa propre case dans le sélecteur de couches de la
carte. Toutes commencent **désactivées** : cochez une case pour l'afficher.

| Quoi | Où | Source |
|---|---|---|
| **Tous les câbles** : chaque câble sous-marin, 608 en service et 105 prévus, en lignes fines ; un clic donne son nom, ses propriétaires, sa longueur et ses pays d'atterrissement | le monde entier | le jeu de données de Tristan Hotham tiré des données de câbles de TeleGeography, fourni avec l'intégration |
| **Points d'atterrissement** : les 1 928 lieux où les câbles arrivent à terre, en petits points | le monde entier | le même |
| **Liaisons terrestres** : liaisons en fibre et par faisceau hertzien entre les villes, à terre, dessinées en ligne droite d'un nœud au suivant | les pays où l'UIT les a recueillies ([où](#où-il-fonctionne)) | ITU Broadband Maps (BBmaps), téléchargées par votre Home Assistant une fois par semaine |

### Activé par votre propre clé ou compte gratuit

| Clé ou compte gratuit | Ce qu'il ajoute |
|---|---|
| Jeton d'API **Cloudflare** | **Pannes** : un marqueur pour chaque panne d'internet en cours que Cloudflare Radar enregistre, dans le pays ou la région qu'elle nomme, coloré et dessiné selon sa cause ; activé par défaut. **Câbles touchés** : chaque câble sous-marin qu'une panne en cours nomme, dessiné en rouge et en gras ; activé par défaut |

Il s'obtient en quelques minutes : [pas à pas ci-dessous](#clés-gratuites-qui-activent-davantage-pas-à-pas).

---

## Où il fonctionne

| Région | Ce que vous obtenez | Source | Il faut |
|---|---|---|---|
| **Le monde entier** | les pannes d'internet, dans le pays ou la région que nomme chaque fiche | Cloudflare Radar | un jeton gratuit |
| **Le monde entier** | les câbles sous-marins touchés | Cloudflare Radar, et les données de câbles | un jeton gratuit |
| **Le monde entier** | tous les câbles sous-marins et points d'atterrissement | le jeu de données de Tristan Hotham tiré des données de TeleGeography | rien |
| **Afrique et Moyen-Orient** | environ 5 400 liaisons terrestres | ITU Broadband Maps | rien |
| **Amérique centrale et du Sud** | environ 5 500 liaisons terrestres | ITU Broadband Maps | rien |
| **Europe** | environ 12 400 liaisons terrestres | ITU Broadband Maps | rien |
| **Amérique du Nord** | environ 4 700 liaisons terrestres | ITU Broadband Maps | rien |
| **Océanie** | environ 1 400 liaisons terrestres | ITU Broadband Maps | rien |
| **Russie, Asie du Nord et de l'Est** | environ 1 500 liaisons terrestres | ITU Broadband Maps | rien |
| **Asie du Sud et du Sud-Est** | environ 9 500 liaisons terrestres | ITU Broadband Maps | rien |

Les nombres de liaisons ont été mesurés le 25 novembre 2026 et sont
approximatifs : chaque liaison est comptée par sa première extrémité. L'UIT
publie environ 40 000 liaisons en tout.

⚠ **La couverture des liaisons terrestres est inégale.** L'UIT montre ce que
les opérateurs et les régulateurs lui ont fourni. Certains pays sont dessinés
en détail (l'Inde, le Brésil, une grande partie de l'Europe) ; d'autres ont peu
de liaisons, ou aucune.

Pas dans la liste ? [Dites-le-nous](#aidez-le-à-grandir). Là où quelqu'un
publie les données ouvertement, nous étudierons leur ajout.

---

## Les autres modules de Live Track

Live Track est un ensemble d'intégrations Home Assistant, une par type de
chose qui bouge, toutes dessinées sur la même carte. Chacune fonctionne seule ;
ensemble, elles forment une image en direct. Elles partagent la carte et une
bibliothèque Python
([saw-livetrack](https://github.com/StrausbergAutomationWorks/LiveTrackCore)),
si bien qu'en installer une de plus n'ajoute aucune requête vers une source
qu'une autre lit déjà.

| Module | Ce qu'il met sur la carte | État |
|---|---|---|
| [Live Track Aircraft](https://github.com/StrausbergAutomationWorks/LiveTrackAircraft) | les avions au-dessus de vous par ADS-B, avec routes et icônes de type | publié |
| [Live Track Ships](https://github.com/StrausbergAutomationWorks/LiveTrackShips) | navires et bateaux par AIS, près de vous ou n'importe où | publié |
| [Live Track Commuter Rail](https://github.com/StrausbergAutomationWorks/LiveTrackCommuterRail) | trains de banlieue en Amérique du Nord, en Europe et en Australie | publié |
| [Live Track Intercity Rail](https://github.com/StrausbergAutomationWorks/LiveTrackIntercityRail) | trains intercités et grandes lignes en Amérique du Nord, en Europe et en Australie | publié |
| [Live Track SALT](https://github.com/StrausbergAutomationWorks/LiveTrackSALT) | avions et navires des services d'immigration et des forces de l'ordre fédérales, d'après des listes publiques | publié |
| [Live Track Weather](https://github.com/StrausbergAutomationWorks/LiveTrackWeather) | météo, tempêtes et risques naturels | publié |
| **Live Track Internet** | pannes d'internet, câbles sous-marins et liaisons terrestres (ce module) | publié |
| Live Track Stations | tableaux des départs et rappels « il est temps de partir » pour chaque gare | prévu |
| Live Track Satellites | les satellites qui passent au-dessus de vous | prévu |
| Live Track Freight Trains | trains de marchandises et de travaux là où les chemins de fer les publient | prévu |
| Live Track Transit | bus urbains, tramways, ferries et métros | prévu |
| Live Track Intercity Buses | autocars interurbains et régionaux | prévu |
| Live Track Commuter Buses | bus de banlieue | prévu |
| [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard) | la carte partagée sur laquelle dessine chaque module | publiée, installée avec chaque module |

Tout est gratuit et libre. Rien n'est réservé aux sponsors.

---

## Avant de commencer

* **Home Assistant** 2026.11 ou plus récent.
* **Le Marketplace** (HACS) dans votre Home Assistant, pour l'installer et le
  mettre à jour facilement. Sans lui, vous pouvez copier les fichiers à la
  main.
* **Un accès à Internet** pour Home Assistant : les pannes et les liaisons
  terrestres viennent de services publics.
* Rien à payer et aucun compte nécessaire pour les câbles et les liaisons. Le
  jeton Cloudflare gratuit ci-dessus est facultatif.
* Home Assistant installe tout seul le paquet Python dont il a besoin
  (`saw-livetrack`) au premier chargement de l'intégration.

---

## Installation, pas à pas

### Depuis le Marketplace (recommandé)

Live Track Internet n'est pas encore dans le catalogue du Marketplace.
Ajoutez-le par son lien :

1. Dans Home Assistant, ouvrez **Paramètres → Marketplace** (HACS).
2. Choisissez l'onglet **Ajouter grâce à un lien**.
3. Sous **Lien GitHub**, saisissez
   `https://github.com/StrausbergAutomationWorks/LiveTrackInternet`
   et, si le **Type** est demandé, choisissez **Intégration**.
4. Trouvez **Live Track Internet** dans la liste et choisissez **Installer**.
5. **Redémarrez Home Assistant** : **Paramètres → Système → Corrections**
   propose le redémarrage, ou utilisez **Paramètres → Système → Redémarrer
   Home Assistant**.

Le Marketplace propose ensuite chaque nouvelle version comme mise à jour.

### À la main

1. Téléchargez le code source de la
   [dernière version](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/releases/latest).
2. Copiez son dossier `custom_components/live_track_internet` dans le dossier
   `custom_components` de votre dossier de configuration Home Assistant
   (créez `custom_components` s'il n'existe pas).
3. Redémarrez Home Assistant.

Pour mettre à jour à la main, remplacez le dossier par celui de la nouvelle
version et redémarrez.

---

## Configuration, pas à pas

1. Ouvrez **Paramètres → Appareils et services**.
2. Choisissez **Ajouter une intégration** (en bas à droite) et recherchez
   **Live Track Internet**.
3. **Jeton d'API Cloudflare** : collez votre jeton si vous en avez un
   ([comment en obtenir un](#clés-gratuites-qui-activent-davantage-pas-à-pas)).
   Laissez le champ vide pour n'afficher que les câbles et les liaisons ; vous
   pourrez ajouter un jeton plus tard.
4. **Liaisons terrestres de l'UIT** : laissez la case cochée. Décochez-la si
   vous ne voulez pas que votre Home Assistant télécharge les liaisons auprès
   de l'UIT une fois par semaine (environ 1 Mo).
5. Choisissez **Valider**.

C'est tout. L'entrée s'appelle **Cloudflare Radar** avec un jeton, ou
**Submarine cables** sans jeton. Il n'y a qu'une seule entrée : une deuxième
dessinerait chaque panne deux fois, elle est donc refusée.

* Les couches des câbles et des points d'atterrissement sont là tout de suite.
* Avec un jeton, les pannes en cours apparaissent en moins d'une minute.
* Les liaisons terrestres apparaissent quelques minutes après la
  configuration, quand le premier téléchargement auprès de l'UIT est terminé.

Chaque couche commence désactivée. Cochez-la dans le sélecteur de couches de la
carte pour la voir
([Mettre la carte sur un tableau de bord](#mettre-la-carte-sur-un-tableau-de-bord)).

### Changer plus tard le jeton ou la case UIT

1. Ouvrez **Paramètres → Appareils et services → Live Track Internet**.
2. Ouvrez le menu à trois points de l'entrée et choisissez **Reconfigurer**.
3. Collez un nouveau jeton, ou laissez le champ vide pour garder le jeton que
   vous avez. Cochez ou décochez **Liaisons terrestres de l'UIT**.
4. Choisissez **Valider**.

Pour retirer le jeton, supprimez l'entrée (**Supprimer** dans le même menu) et
ajoutez de nouveau Live Track Internet sans jeton. Si Cloudflare refuse votre
jeton plus tard (il a été supprimé ou a expiré), les marqueurs des pannes
s'arrêtent, et Home Assistant vous demande un nouveau jeton dans
**Paramètres → Appareils et services**.

---

## Clés gratuites qui activent davantage, pas à pas

Le jeton est gratuit et personnel : chaque personne qui installe Live Track
Internet crée le sien. Il vous faut un compte Cloudflare gratuit ; vous n'avez
besoin ni d'un site web ni d'un domaine chez Cloudflare.

### Jeton d'API Cloudflare (pannes d'internet, le monde entier)

1. Connectez-vous à Cloudflare, ou créez un compte gratuit, sur
   <https://dash.cloudflare.com>.
2. Ouvrez <https://dash.cloudflare.com/profile/api-tokens> (**My Profile →
   API Tokens**) et choisissez **Create Token**.
3. N'utilisez pas de modèle : partez de zéro, avec un jeton personnalisé.
   Donnez-lui un nom, par exemple `Live Track Internet`.
4. Dans les autorisations, choisissez **Account**, puis **Radar**, puis
   **Read**. Rien d'autre n'est nécessaire.
5. Choisissez **Continue to summary**, puis **Create Token**.
6. Copiez le jeton tout de suite : Cloudflare ne l'affiche qu'une fois.
7. Collez-le dans **Jeton d'API Cloudflare** lors de la
   [configuration](#configuration-pas-à-pas) de Live Track Internet, ou plus
   tard avec **Reconfigurer**.

Live Track Internet vérifie le jeton par une vraie requête à Cloudflare Radar
avant de l'enregistrer. Le jeton reste dans votre Home Assistant et n'est
envoyé qu'à Cloudflare. Aucun mot de passe ni autre secret n'est nécessaire.
Les noms des boutons sont donnés ici tels que Cloudflare les affiche en
anglais ; si Cloudflare vous montre ses pages en français, ils y portent
d'autres noms.

---

## Mettre la carte sur un tableau de bord

La carte est [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard),
la carte sur laquelle dessine chaque module Live Track. **Elle est installée
avec Live Track Internet** : rien à télécharger, rien à copier, aucune
ressource à ajouter.

1. Ouvrez un tableau de bord, choisissez le crayon (**Modifier le tableau de
   bord**), puis **Ajouter une carte**.
2. Faites défiler jusqu'en bas et choisissez **Manuel**.
3. Collez ceci, et choisissez **Enregistrer** :

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

Les couches des câbles et des liaisons apparaissent d'elles-mêmes. Les marqueurs
des pannes passent par le filtre ci-dessus.

Les autres modules Live Track vont dans `entity_filter` de la même façon : une
règle `- domain: geo_location` de plus pour chaque source.

**Sur la carte :**

* Le **sélecteur de couches** en haut à droite a une case pour chaque
  couche : **Câbles touchés**, **Tous les câbles**, **Points
  d'atterrissement** et **Liaisons terrestres**. Le choix de chaque spectateur
  est gardé dans son propre navigateur.
* Chaque panne est une image ronde de sa cause, avec le code à deux lettres du
  pays à côté. **Pointez** dessus pour voir où et pourquoi ; **cliquez** dessus
  pour la description de Cloudflare et un lien vers l'article.
* **Cliquez** sur un câble pour son nom, ses propriétaires, sa longueur et ses
  pays d'atterrissement. Les liaisons terrestres ne sont pas cliquables.
* La **carte de filtre** (`custom:live-track-map-filter-card`) peut masquer les
  pannes selon leur cause.
* Le crédit de chaque source apparaît dans la ligne d'attribution de la carte
  tant que ses données sont affichées.

La carte garde exactement une ligne de ressource de tableau de bord pour tous
les modules Live Track ensemble : la version de carte la plus récente que l'un
d'eux apporte, jamais une plus ancienne. Une carte que vous avez installée
vous-même par le Marketplace n'est pas touchée. Si les ressources de vos
tableaux de bord sont définies en YAML (`lovelace: resource_mode: yaml`), rien
ne peut être enregistré pour vous : un problème dans **Corrections** donne alors
la ligne exacte à ajouter, qui ressemble à ceci, avec l'adresse propre de
l'intégration à la place des espaces réservés :

```yaml
lovelace:
  resource_mode: yaml
  resources:
    - url: /live_track_internet/map-card/<12 hex>/live-track-map-card.js?v=<version>&h=<12 hex>
      type: module
```

Supprimer l'entrée de Live Track Internet confie la ligne à un autre module
Live Track, ou la retire s'il n'en reste aucun. Si les fichiers de
l'intégration sont retirés alors que son entrée est encore configurée, et
qu'aucun autre module Live Track n'est installé, retirez vous-même la ligne de
la carte dans **Paramètres → Tableaux de bord → Ressources**. Pour installer la
carte à la main, suivez plutôt le README de la carte. Une ligne que vous avez
créée vous-même, pour une copie sous `/local/` ou à toute autre adresse, n'est
jamais modifiée ni retirée. Tant qu'elle charge la carte, chaque module Live
Track lui laisse la carte, même quand un module apporte une version plus
récente, et rien dans **Corrections** ne le signale. Pour revenir à la copie
du module, retirez votre ligne dans **Paramètres → Tableaux de bord →
Ressources** et redémarrez Home Assistant. Si vous supprimez le fichier de
votre copie, retirez aussi sa ligne : tant qu'une ligne dont le fichier a
disparu reste là, le module n'ajoute pas de ligne à lui. Toute autre carte qui
affiche les entités `geo_location` montre aussi les marqueurs des pannes, mais
pas les câbles ni les liaisons.

---

## L'utiliser dans des automatisations

Tout est une entité Home Assistant ordinaire, donc l'éditeur d'automatisations
fonctionne avec, sans code.

**Une notification sur le téléphone quand Cloudflare enregistre une nouvelle
panne d'internet** (il faut pour cela le jeton Cloudflare) :

1. **Paramètres → Automatisations et scènes → Créer une automatisation →
   Créer une nouvelle automatisation**.
2. **Quand** : **Ajouter un déclencheur**, tapez `numeric` dans la zone de
   recherche, et choisissez **L'état numérique a franchi un seuil**.
   Choisissez l'**Entité** **Cloudflare Radar Pannes d'internet**, et sous
   **Au-dessus de** saisissez `0`.
3. **Alors faire** : **Ajouter une action**, cherchez l'action de
   notification de votre téléphone (elle porte le nom de votre téléphone), et
   saisissez un message, par exemple :

   ```text
   Cloudflare Radar signale une panne d'internet
   ```

4. **Enregistrer**.

**Autres idées :** une notification quand une panne nomme un câble sous-marin,
avec **Submarine cables Câbles touchés** au-dessus de 0 ; une tuile de tableau
de bord avec le nombre de pannes en cours, depuis **Cloudflare Radar Pannes
d'internet**.

---

## Tout ce qui est sur la carte, en détail

### Pannes

[Cloudflare Radar](https://radar.cloudflare.com) tient un Outage Center : des
fiches sur les pannes d'internet dans le monde, rédigées par des personnes chez
Cloudflare, chacune avec une cause, un type (nationale, régionale ou un seul
réseau), les pays ou régions touchés, une heure de début et généralement un
lien vers un article de presse.

Live Track Internet demande les fiches des dernières 24 heures toutes les
15 minutes et dessine un marqueur pour chaque fiche en cours, dans chaque lieu
qu'elle nomme : dans la région quand la fiche en nomme une, sinon dans le
pays. Une fiche qui se termine quitte la carte. Les fiches sur un service en
ligne plutôt que sur un lieu (la panne d'un fournisseur de cloud, par exemple)
ne sont pas dessinées ; le capteur **Cloudflare Radar Pannes d'internet** les
liste dans son attribut `not_on_map`.

⚠ **Une fiche qui ne nomme qu'un réseau est placée au centre de son pays**, ce
qui peut être loin de la panne dans un grand pays. Le texte du clic le dit.
Par exemple, Cloudflare classe deux réseaux de Louhansk et de Donetsk
(Ukraine) sous la Russie, si bien que leurs pannes sont placées en Sibérie
centrale, et les réseaux des États-Unis sont placés au Kansas.

⚠ Les fiches de panne sont rédigées par des personnes, souvent des heures après
le début d'une panne. Quand nous avons mesuré une année de fiches (jusqu'au
23 novembre 2026), il y en avait 143, jamais plus de 4 en cours en même temps,
et aucune en cours 43 % du temps. La plupart du temps, la carte ne montre
aucune panne.

Chaque marqueur est dessiné selon sa cause :

| Cause | Couleur | Image |
|---|---|---|
| Câble coupé | rouge | ciseaux ouverts |
| Coupure de courant | ambre | éclair |
| Décidée par un gouvernement (une coupure) | indigo | cadenas |
| Action militaire | noir | réticule |
| Météo ou catastrophe naturelle | bleu | nuage d'orage |
| Cyberattaque | bleu canard | bouclier avec `!` |
| Problème technique (réseau, logiciel, DNS, maintenance) | gris bleuté | clé |
| Cause inconnue | gris | `?` |

Sur chaque marqueur : `outage_cause` et `outage_type` (les mots de Cloudflare,
par exemple `POWER_OUTAGE`, `NATIONWIDE`), `started_at`, `place_kind`
(`region`, `country` ou `network`), `country_code`, `country_name`,
`region_name`, `asns` et `asn_names` quand la fiche nomme des réseaux,
`description`, `linked_url` (l'article), `cables_named` quand la description
nomme un câble, et `marker_group` (la cause, pour la carte de filtre).

### Câbles touchés

Avec le jeton Cloudflare, chaque câble sous-marin nommé dans la description
d'une panne en cours est dessiné en rouge et en gras avec un bord blanc,
activé par défaut. Le plus souvent il n'y en a aucun. Le câble est reconnu par
son nom, écrit de l'une des façons habituelles (`SEA-ME-WE 5`, `SeaMeWe-5`) ;
les noms courts ne sont reconnus que comme mots entiers.

⚠ Le champ de cause de Cloudflare ne dit pas si un câble coupé est un câble
sous-marin : dans l'année mesurée, la seule fiche classée comme câble coupé
concernait un câble à terre, et un défaut sur le câble SEA-ME-WE 5 était classé
comme cause inconnue. Le câble est donc cherché dans la description, quelle que
soit la cause.

### Tous les câbles et les points d'atterrissement

Chaque câble sous-marin du jeu de données 2026 de Tristan Hotham tiré des
données de câbles de TeleGeography : 713 câbles, 608 en service (dessinés en
bleu) et 105 prévus (dessinés en orange), en lignes fines et pâles, et
1 928 points d'atterrissement en petits points (orange là où n'arrivent que
des câbles prévus). Cliquez sur un câble pour son nom, la date de sa mise en
service passée ou prévue, sa longueur, ses pays d'atterrissement, ses
propriétaires et son fournisseur. Les données sont fournies avec l'intégration
et ne changent qu'avec une nouvelle version.

⚠ Un câble posé après la création du jeu de données (novembre 2026)
n'apparaît qu'après une version qui apporte des données plus récentes.

### Liaisons terrestres

Les liaisons en fibre et par faisceau hertzien à terre que recensent les
Broadband Maps de l'UIT (Infrastructure Connectivity Map), d'après les
opérateurs et les régulateurs. Chaque liaison est dessinée telle que l'UIT la
publie : une ligne droite d'un nœud au suivant, pas le chemin que suit le
câble sur le terrain.

| Ligne | Ce que c'est |
|---|---|
| prune | fibre, en service |
| jaune au bord noir | faisceau hertzien, en service |
| orange | prévue, proposée ou en construction (faisceau hertzien au bord noir) |
| gris | sans état indiqué (faisceau hertzien au bord noir) |

⚠ À la largeur fine et pâle des lignes de la carte, les faisceaux hertziens
paraissent olive ou kaki plutôt que jaunes ; c'est le bord noir qui les
distingue de la fibre.

⚠ L'UIT n'enregistre ni opérateur, ni nom, ni capacité, ni date pour une
liaison : une liaison n'est donc pas cliquable, et aucune panne ne lui est
rattachée.

Votre Home Assistant télécharge toute la couche auprès de l'UIT une fois par
semaine, à son propre jour et à sa propre heure, et la conserve. Si un
téléchargement échoue ou revient incomplet, la dernière bonne copie reste,
quel que soit son âge.

---

## Toutes les entités qu'il crée

| Entité | Ce que c'est |
|---|---|
| `sensor.live_track_internet_outages` | **Cloudflare Radar Pannes d'internet** : combien de marqueurs de panne sont sur la carte (avec le jeton seulement) |
| `sensor.live_track_internet_cables_in_trouble` | **Submarine cables Câbles touchés** : combien de câbles une panne en cours nomme (avec le jeton seulement) |
| `sensor.live_track_internet_all_cables` | **Submarine cables Tous les câbles** : le nombre de câbles, 713 |
| `sensor.live_track_internet_landing_points` | **Submarine cables Points d'atterrissement** : le nombre de points d'atterrissement, 1 928 |
| `sensor.live_track_internet_terrestrial_links` | **ITU Broadband Maps Liaisons terrestres** : combien de liaisons sont dessinées (seulement tant que **Liaisons terrestres de l'UIT** est cochée) |
| `geo_location.outage_…` | un par panne en cours et par lieu, nommé d'après le numéro de fiche de Cloudflare (`geo_location.outage_1754`) ; il va et vient avec la fiche |

Chaque marqueur porte `source: live_track_internet`, et son état est sa
distance à votre domicile en kilomètres. Les capteurs sont rattachés à trois
appareils : **Cloudflare Radar**, **Submarine cables** et **ITU Broadband
Maps**.

Les attributs du capteur des pannes : `open_records` (toutes les fiches en
cours, y compris celles qui ne sont pas sur la carte), `not_on_map` et
`last_success`.

⚠ **Les marqueurs n'ont pas d'identifiant unique, exprès.** Les fiches de
panne vont et viennent, et une ligne de registre pour chacune resterait pour
toujours. On ne peut donc pas les renommer, les masquer ni leur attribuer une
pièce dans l'interface. Les capteurs ont des identifiants uniques et peuvent
être renommés.

Les attributs qui changent à chaque mise à jour, et les grandes listes que la
carte lit, sont tenus hors de l'historique de Home Assistant, pour que votre
base de données ne grossisse pas avec eux.

---

## Ce qu'il envoie et télécharge

**À propos de votre position.** Rien. La position de votre domicile ne sert
que dans votre Home Assistant, à calculer la distance de chaque marqueur.
Cloudflare reçoit votre jeton et la période de la requête ; l'UIT reçoit la
demande de ses liaisons. Les données des câbles sont fournies avec
l'intégration et ne sont pas téléchargées. Chaque service voit votre adresse
internet, comme tout site web.

**Combien.** Tailles mesurées le 25 novembre 2026, sauf indication contraire
dans le tableau.

| Source | Quoi et à quelle fréquence | Taille mesurée | Après une erreur |
|---|---|---|---|
| Cloudflare Radar, pannes | une requête toutes les 15 minutes, avec votre jeton : les fiches des dernières 24 heures | 447 octets transférés (une fiche) | un jeton refusé arrête les requêtes et vous en demande un nouveau. HTTP 429 : attend le temps que Cloudflare demande, ou 15 minutes, en doublant jusqu'à 2 heures. Autres erreurs : nouvel essai après 15, 30 et 60 minutes, puis toutes les 2 heures. La dernière bonne réponse est gardée 2 heures ; ensuite les marqueurs disparaissent |
| Cloudflare Radar, lieux | les points centraux des pays une fois par jour ; le point d'une région la première fois qu'une fiche la nomme, puis conservé | la liste des pays : 36 905 octets (23 novembre 2026) | la copie que vous avez reste utilisée |
| ITU Broadband Maps | toute la couche une fois par semaine, en 9 requêtes à 3 secondes d'intervalle, environ 36 secondes en tout | environ 0,9 Mo transférés (111 537 octets par tranche de 5 000 liaisons) | HTTP 429 : attend le temps que l'UIT demande, ou une heure, en doublant jusqu'à un jour. Autres erreurs : nouvel essai le lendemain. La dernière bonne copie reste |
| Votre navigateur | depuis votre Home Assistant, pas depuis internet : le fichier des câbles quand **Tous les câbles** est cochée, les points d'atterrissement quand **Points d'atterrissement** est cochée, et le fichier des liaisons quand **Liaisons terrestres** est cochée | câbles 113 323 octets ; points d'atterrissement 38 160 octets ; liaisons 296 105 octets | |

Décochez **Liaisons terrestres de l'UIT** (**Reconfigurer**) pour arrêter le
téléchargement hebdomadaire. Supprimez l'entrée pour tout arrêter.

Les fichiers téléchargés sont gardés dans le dossier `.storage` de Home
Assistant sous des noms qui commencent par `saw_` (`saw_radar_locations.json`,
`saw_radar_geolocations.json`, `saw_itu_bbmaps_links.json.gz`), pour qu'un
autre module Live Track puisse les partager. Si vous retirez Live Track
Internet et qu'aucun autre module Live Track ne les utilise, vous pouvez les
supprimer à la main.

---

## Aidez-le à grandir

Live Track Internet continue de grandir. Nous ajoutons des sources de données à
mesure que nous les trouvons, et nous voulons savoir ce que vous aimeriez
ensuite.

### Proposer quelque chose

Une source de données manque ? Quelque chose est faux, ou difficile à
comprendre ? Dites-le-nous de la façon la plus simple pour vous :

* [**Remplissez un court formulaire**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=fr.yml)
  en français. Il vous faut un compte GitHub gratuit.
* **Écrivez un e-mail** à
  [StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org).
  Aucun compte n'est nécessaire.

Dans les deux cas, il nous aide que vous nous disiez :

* ce que vous aimeriez voir, et où dans le monde ;
* un lien vers l'endroit où les données sont publiées, si vous en connaissez
  un (une page de données ouvertes, un flux public, le site d'un service) : ce
  n'est pas nécessaire, mais cela aide ;
* la langue de votre Home Assistant, si le problème concerne la formulation ou
  une traduction.

Écrivez en anglais ou dans votre propre langue, ce qui est le plus simple pour
vous.

### L'ajouter vous-même, avec notre aide

Si vous souhaitez ajouter quelque chose vous-même, nous vous aiderons à le
faire, de la première question jusqu'à la version terminée. Vous n'avez pas
besoin d'être développeur pour commencer :

* **Une traduction.** Les textes de la boîte de dialogue de configuration sont
  une courte liste de phrases dans un seul fichier texte. Nous vous montrerons
  quel fichier et quelles lignes.
* **Une nouvelle source.** Dites-nous où les données sont publiées. Nous
  pouvons écrire le code ensemble, ou relire le vôtre.
* **Le tester là où vous habitez.** Installez-le, regardez votre partie de la
  carte, et dites-nous ce qui est juste et ce qui ne l'est pas.
* **Une correction de ce README.** Si une étape ne correspondait pas à ce que
  vous avez vu, dites-nous ce que vous avez vu.

[**Dites-nous ce que vous avez en tête**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=fr.yml)
ou écrivez à
[StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org),
et nous vous répondrons avec les prochaines étapes.

---

## Langues

Ce README : [English](README.md), [Deutsch](README.de.md), **Français**,
[Nederlands](README.nl.md), [简体中文](README.zh-Hans.md),
[Español](README.es.md), [Italiano](README.it.md),
[Українська](README.uk.md) et [العربية](README.ar.md). Chaque README traduit
est complet. Aucun n'a encore été relu par un locuteur natif. Si l'une de ces
langues est la vôtre, dites-nous si son README se lit bien : voir
[Aidez-le à grandir](#aidez-le-à-grandir).

La boîte de dialogue de configuration s'affiche dans la langue de votre Home
Assistant quand c'est l'une de celles-ci : English, Deutsch, Español,
Français, Italiano, Nederlands, 简体中文, Українська et العربية. Toute autre
langue affiche l'anglais. Les traductions de la boîte de dialogue ont elles
aussi été écrites sans locuteur natif. Les mots sur la carte (les noms des
pannes et les textes du clic, les noms des causes dans la carte de filtre et
les crédits) sont en anglais dans toutes les langues.

Vous avez trouvé une erreur dans une traduction, ou il vous faut une autre
langue ? Dites-le-nous sur
<https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues>, ou
[traduisez-le avec notre aide](#lajouter-vous-même-avec-notre-aide).

---

## Crédits et licences

* **Cloudflare Radar** (Cloudflare, Inc., <https://radar.cloudflare.com>) : les
  fiches de panne, sous
  [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), lues avec
  le jeton propre à chaque utilisateur. Cette intégration place chaque fiche
  sur la carte ; elle ne modifie pas les fiches. En installant cette
  intégration, vous utilisez l'API de Cloudflare, et ses conditions
  s'appliquent à vous.
* **Câbles sous-marins et points d'atterrissement** : Hotham, T. (2026), *The
  internet's seabed: submarine cables, when they were laid, who owns them and
  where they crowd together*, Zenodo, <https://doi.org/10.5281/zenodo.23856607>,
  tiré de la
  [Submarine Cable Map](https://www.submarinecablemap.com/) de TeleGeography,
  sous [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
  Cette intégration a relié les lignes des câbles à la table des câbles,
  converti les deux en fichiers de carte et arrondi les points
  d'atterrissement à 4 décimales ; rien n'a été ajouté ni corrigé. Les fichiers
  convertis dans `custom_components/live_track_internet/cables/` sont partagés
  sous la même licence, avec son texte juridique et un fichier de crédit à côté
  ([CREDIT.md](custom_components/live_track_internet/cables/CREDIT.md)).
* **Liaisons terrestres** : ITU Broadband Maps (BBmaps), l'Infrastructure
  Connectivity Map, <https://bbmaps.itu.int>, © UIT. Utilisées selon les
  conditions d'utilisation de l'UIT pour un usage non commercial, avec mention
  de la source. Rien de l'UIT n'est fourni dans ce dépôt : chaque installation
  télécharge les liaisons pour son propre utilisateur. Cette intégration les
  dessine telles que l'UIT les publie, arrondies à 3 décimales (environ 110 m),
  les liaisons répétées du même genre n'étant dessinées qu'une fois.
* **Les images des pannes** ont été dessinées pour StrausbergAutomationWorks,
  sous licence MIT.
* **La carte** est [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard),
  MIT, une copie de [ha-map-card](https://github.com/nathan-gs/ha-map-card) de
  nathan-gs, MIT. Ses fonds de carte et leurs crédits sont dans son README.

⚠ **Usage non commercial seulement.** Les trois sources de données
n'autorisent qu'un usage non commercial. Le code est sous MIT, mais les données
qu'il affiche ne peuvent pas être utilisées à des fins commerciales.

Aucune de ces organisations n'a créé ni approuvé cette intégration. Quelle
licence couvre quelle partie de ce dépôt : [ATTRIBUTION.md](ATTRIBUTION.md).

**Code** : MIT, dans [LICENSE](LICENSE).

**Pour les développeurs :** les entités suivent le contrat de carte commun de
Live Track, si bien que chaque module s'affiche sur une seule carte.
`tools/build_cables.py` reconstruit les fichiers des câbles depuis le dépôt de
Hotham. Les tests se lancent avec `python -m unittest discover -s tests`.

---

## Mots-clés

Home Assistant panne d'internet · carte des pannes d'internet · coupure
d'internet · blackout internet · panne de réseau · panne du fournisseur
d'accès · Cloudflare Radar · Radar Outage Center · câbles sous-marins · câble
sous-marin · carte des câbles sous-marins · câble coupé · points
d'atterrissement · TeleGeography · Submarine Cable Map · fibre terrestre ·
carte de la fibre optique · réseau de fibre · faisceaux hertziens · UIT ·
ITU Broadband Maps · BBmaps · Infrastructure Connectivity Map · internet
outage · submarine cables · Internetausfall · Seekabel · internetstoring ·
zeekabels · 断网 · 海底光缆 · corte de internet · cables submarinos ·
interruzione internet · cavi sottomarini · відключення інтернету · підводні
кабелі · انقطاع الإنترنت · كابلات بحرية · geo_location · carte · Lovelace ·
HACS · Marketplace · Live Track · LiveTrack · StrausbergAutomationWorks

---

**Reconnaissance.** StrausbergAutomationWorks reconnaît les peuples autochtones
de toutes les terres et de toutes les eaux de cette carte, partout dans le
monde, et rend hommage à leurs Aînés d'hier et d'aujourd'hui.
