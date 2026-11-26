# Live Track Internet

[English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Nederlands](README.nl.md) · [简体中文](README.zh-Hans.md) · **Español** · [Italiano](README.it.md) · [Українська](README.uk.md) · [العربية](README.ar.md) · [Todos los idiomas](#idiomas)

**Cortes de internet, cables submarinos y enlaces de fibra para Home Assistant,
en un solo mapa.** Live Track Internet pone en tu mapa de Home Assistant los
cortes de internet que Cloudflare Radar registra en cualquier parte del mundo,
con su causa. También dibuja cada cable submarino con sus puntos de amarre, y
los enlaces de fibra y de microondas entre poblaciones que registra la UIT.
Cuando un corte nombra un cable, ese cable se dibuja en rojo.

> **Live Track Internet es un módulo de Live Track**, una familia de
> integraciones de Home Assistant que dibujan todo lo que se mueve, y el tiempo
> que atraviesa, en un mapa compartido: aviones, barcos, trenes y el tiempo.
> Instálalo solo o junto a los demás módulos
> ([lista más abajo](#parte-de-live-track-los-demás-módulos)).

> **En crecimiento, y abierto a ideas.** Hoy Live Track Internet cubre cortes,
> cables y enlaces terrestres en todo el mundo, y estamos añadiendo más fuentes
> de datos (están previstos los puntos de intercambio de internet y los centros
> de datos). ¿Falta algo? [Sugiérelo](#ayúdanos-a-hacerlo-crecer), o añádelo tú
> mismo: te ayudaremos a hacerlo.

**Estado: 0.3.0, la primera versión.** Añadido al Marketplace por su enlace
([más abajo](#instalación-paso-a-paso)); todavía no está en el catálogo del
Marketplace.

Obra original de StrausbergAutomationWorks. Sin relación con, ni respaldo de,
Cloudflare, Tristan Hotham, TeleGeography, la Unión Internacional de
Telecomunicaciones (UIT), ni ningún propietario de cables u operador de red.

> ⚠ **No vigila tu propia conexión a internet.** Los cortes son registros que
> escriben personas de Cloudflare, a menudo horas después de que empiece un
> corte, y solo de cortes lo bastante grandes como para verse desde la red de
> Cloudflare. **Un mapa vacío no significa que internet funcione en todas
> partes.** Un cable o un enlace en el mapa no dice si hoy transporta tráfico.

---

## Contenido

1. [Todo lo que hace](#todo-lo-que-hace)
2. [Dónde funciona](#dónde-funciona)
3. [Parte de Live Track: los demás módulos](#parte-de-live-track-los-demás-módulos)
4. [Antes de empezar](#antes-de-empezar)
5. [Instalación, paso a paso](#instalación-paso-a-paso)
6. [Configuración, paso a paso](#configuración-paso-a-paso)
7. [Claves gratuitas que activan más, paso a paso](#claves-gratuitas-que-activan-más-paso-a-paso)
8. [Poner el mapa en un panel](#poner-el-mapa-en-un-panel)
9. [Usarlo en automatizaciones](#usarlo-en-automatizaciones)
10. [Todo lo que hay en el mapa, en detalle](#todo-lo-que-hay-en-el-mapa-en-detalle)
11. [Todas las entidades que crea](#todas-las-entidades-que-crea)
12. [Qué envía y descarga](#qué-envía-y-descarga)
13. [Ayúdanos a hacerlo crecer](#ayúdanos-a-hacerlo-crecer)
14. [Idiomas](#idiomas)
15. [Créditos y licencias](#créditos-y-licencias)
16. [Palabras clave](#palabras-clave)

---

## Todo lo que hace

### En el mapa, sin configurar nada

Cada una de estas capas tiene su propia casilla en el control de capas del
mapa. Todas empiezan **desactivadas**: marca una casilla para mostrarla.

| Qué | Dónde | De dónde |
|---|---|---|
| **Todos los cables**: cada cable submarino, 608 en servicio y 105 previstos, como líneas finas; haz clic en uno para ver su nombre, sus propietarios, su longitud y sus países de amarre | todo el mundo | el conjunto de datos de Tristan Hotham con los datos de cables de TeleGeography, incluido con la integración |
| **Puntos de amarre**: los 1.928 lugares donde los cables llegan a tierra, como puntos pequeños | todo el mundo | el mismo |
| **Enlaces terrestres**: enlaces de fibra y de microondas entre poblaciones en tierra, dibujados en línea recta de un nodo al siguiente | los países donde la UIT los ha recogido ([dónde](#dónde-funciona)) | ITU Broadband Maps (BBmaps), descargados por tu Home Assistant una vez por semana |

### Activado con tu propia clave o cuenta gratuita

| Clave o cuenta gratuita | Lo que añade |
|---|---|
| Token de API de **Cloudflare** | **Cortes**: un marcador por cada corte de internet abierto que registra Cloudflare Radar, en el país o la región que nombra, coloreado y dibujado según su causa; activado por defecto. **Cables con problemas**: cada cable submarino que nombra un corte abierto, dibujado grueso y en rojo; activado por defecto |

Se consigue en unos minutos: [paso a paso más abajo](#claves-gratuitas-que-activan-más-paso-a-paso).

---

## Dónde funciona

| Región | Lo que obtienes | De dónde | Necesita |
|---|---|---|---|
| **Todo el mundo** | cortes de internet, en el país o la región que nombra cada registro | Cloudflare Radar | un token gratuito |
| **Todo el mundo** | cables submarinos con problemas | Cloudflare Radar, y los datos de cables | un token gratuito |
| **Todo el mundo** | todos los cables submarinos y puntos de amarre | el conjunto de datos de Tristan Hotham con los datos de TeleGeography | nada |
| **África y Oriente Medio** | unos 5.400 enlaces terrestres | ITU Broadband Maps | nada |
| **América Central y del Sur** | unos 5.500 enlaces terrestres | ITU Broadband Maps | nada |
| **Europa** | unos 12.400 enlaces terrestres | ITU Broadband Maps | nada |
| **América del Norte** | unos 4.700 enlaces terrestres | ITU Broadband Maps | nada |
| **Oceanía** | unos 1.400 enlaces terrestres | ITU Broadband Maps | nada |
| **Rusia, Asia del Norte y del Este** | unos 1.500 enlaces terrestres | ITU Broadband Maps | nada |
| **Asia del Sur y del Sudeste** | unos 9.500 enlaces terrestres | ITU Broadband Maps | nada |

Las cifras de enlaces se midieron el 25 de noviembre de 2026 y son
aproximadas: cada enlace se cuenta por su primer extremo. La UIT publica unos
40.000 enlaces en total.

⚠ **La cobertura de enlaces terrestres es desigual.** La UIT muestra lo que le
han dado los operadores y los reguladores. Algunos países están dibujados con
detalle (India, Brasil, gran parte de Europa); otros tienen pocos enlaces o
ninguno.

¿No está en la lista? [Dínoslo](#ayúdanos-a-hacerlo-crecer). Donde alguien
publique los datos de forma abierta, estudiaremos añadirlos.

---

## Parte de Live Track: los demás módulos

Live Track es un conjunto de integraciones de Home Assistant, una por cada tipo
de cosa que se mueve, todas dibujadas en la misma tarjeta de mapa. Cada una
funciona por sí sola; juntas forman una imagen en directo. Comparten la tarjeta
de mapa y una biblioteca de Python
([saw-livetrack](https://github.com/StrausbergAutomationWorks/LiveTrackCore)),
así que instalar otra no añade peticiones a una fuente que otra ya lee.

| Módulo | Lo que pone en el mapa | Estado |
|---|---|---|
| [Live Track Aircraft](https://github.com/StrausbergAutomationWorks/LiveTrackAircraft) | aviones sobre ti por ADS-B, con rutas e iconos por tipo | publicado |
| [Live Track Ships](https://github.com/StrausbergAutomationWorks/LiveTrackShips) | barcos y embarcaciones por AIS, cerca de ti o en cualquier parte | publicado |
| [Live Track Commuter Rail](https://github.com/StrausbergAutomationWorks/LiveTrackCommuterRail) | trenes de cercanías en Norteamérica, Europa y Australia | publicado |
| [Live Track Intercity Rail](https://github.com/StrausbergAutomationWorks/LiveTrackIntercityRail) | trenes interurbanos y de larga distancia en Norteamérica, Europa y Australia | publicado |
| [Live Track SALT](https://github.com/StrausbergAutomationWorks/LiveTrackSALT) | aviones y barcos de inmigración y de las fuerzas federales del orden, según listas públicas | publicado |
| [Live Track Weather](https://github.com/StrausbergAutomationWorks/LiveTrackWeather) | tiempo, tormentas y riesgos naturales | publicado |
| **Live Track Internet** | cortes de internet, cables submarinos y enlaces terrestres (este módulo) | publicado |
| Live Track Stations | paneles de salidas y avisos de "hora de salir" para cada estación | previsto |
| Live Track Satellites | satélites que pasan sobre ti | previsto |
| Live Track Freight Trains | trenes de mercancías y de obras donde los ferrocarriles los publican | previsto |
| Live Track Transit | autobuses urbanos, tranvías, transbordadores y metro | previsto |
| Live Track Intercity Buses | autocares interurbanos y regionales | previsto |
| Live Track Commuter Buses | autobuses de cercanías | previsto |
| [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard) | la tarjeta de mapa compartida en la que dibuja cada módulo | publicada, instalada con cada módulo |

Todo es gratuito y de código abierto. No se reserva nada para patrocinadores.

---

## Antes de empezar

* **Home Assistant** 2026.11 o posterior.
* **El Marketplace** (HACS) en tu Home Assistant, para instalarlo y
  actualizarlo de forma sencilla. Sin él puedes copiar los archivos a mano.
* **Acceso a internet** para Home Assistant: los cortes y los enlaces
  terrestres vienen de servicios públicos.
* Nada que pagar y ninguna cuenta necesaria para los cables y los enlaces. El
  token gratuito de Cloudflare de arriba es opcional.
* Home Assistant instala por sí mismo el paquete de Python que necesita
  (`saw-livetrack`) la primera vez que carga la integración.

---

## Instalación, paso a paso

### Desde el Marketplace (recomendado)

Live Track Internet todavía no está en el catálogo del Marketplace. Añádelo
por su enlace:

1. En Home Assistant, abre **Configuración → Marketplace** (HACS).
2. Elige la pestaña **Añadir desde enlace**.
3. En **Enlace de GitHub**, escribe
   `https://github.com/StrausbergAutomationWorks/LiveTrackInternet`
   y, si te pide el **Tipo**, elige **Integración**.
4. Busca **Live Track Internet** en la lista y elige **Instalar**.
5. **Reinicia Home Assistant**: **Configuración → Sistema → Reparaciones**
   ofrece el reinicio, o usa **Configuración → Sistema → Reiniciar Home
   Assistant**.

Después, el Marketplace te ofrece cada nueva versión como actualización.

### A mano

1. Descarga el código fuente de la
   [última versión](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/releases/latest).
2. Copia su carpeta `custom_components/live_track_internet` en la carpeta
   `custom_components` de tu carpeta de configuración de Home Assistant (crea
   `custom_components` si no existe).
3. Reinicia Home Assistant.

Para actualizar a mano, sustituye la carpeta por la de la nueva versión y
reinicia.

---

## Configuración, paso a paso

1. Abre **Configuración → Dispositivos y servicios**.
2. Elige **Añadir integración** (abajo a la derecha) y busca **Live Track
   Internet**.
3. **Token de API de Cloudflare**: pega tu token si tienes uno
   ([cómo conseguir uno](#claves-gratuitas-que-activan-más-paso-a-paso)).
   Déjalo vacío para mostrar solo los cables y los enlaces; puedes añadir un
   token más tarde.
4. **Enlaces terrestres de la UIT**: déjalo marcado. Desmárcalo si no quieres
   que tu Home Assistant descargue los enlaces de la UIT una vez por semana
   (alrededor de 1 MB).
5. Elige **Enviar**.

Eso es todo. La entrada se llama **Cloudflare Radar** con un token, o
**Submarine cables** sin él. Solo hay una entrada: una segunda dibujaría cada
corte dos veces, así que se rechaza.

* Las capas de los cables y de los puntos de amarre están ahí de inmediato.
* Con un token, los cortes abiertos aparecen en menos de un minuto.
* Los enlaces terrestres aparecen unos minutos después de la configuración,
  cuando ha terminado la primera descarga de la UIT.

Cada capa empieza desactivada. Márcala en el control de capas del mapa para
verla ([Poner el mapa en un panel](#poner-el-mapa-en-un-panel)).

### Cambiar más tarde el token o la casilla de la UIT

1. Abre **Configuración → Dispositivos y servicios → Live Track Internet**.
2. Abre el menú de tres puntos de la entrada y elige **Reconfigurar**.
3. Pega un token nuevo, o deja el campo vacío para conservar el que tienes.
   Marca o desmarca **Enlaces terrestres de la UIT**.
4. Elige **Enviar**.

Para quitar el token, elimina la entrada (**Eliminar** en el mismo menú) y
añade de nuevo Live Track Internet sin token. Si más tarde Cloudflare rechaza
tu token (se borró o caducó), los marcadores de los cortes se detienen, y Home
Assistant te pide un token nuevo en **Configuración → Dispositivos y
servicios**.

---

## Claves gratuitas que activan más, paso a paso

El token es gratuito y personal: cada persona que instala Live Track Internet
crea el suyo. Necesitas una cuenta gratuita de Cloudflare; no necesitas un
sitio web ni un dominio en Cloudflare.

### Token de API de Cloudflare (cortes de internet, todo el mundo)

1. Inicia sesión en Cloudflare, o crea una cuenta gratuita, en
   <https://dash.cloudflare.com>.
2. Abre <https://dash.cloudflare.com/profile/api-tokens> (**My Profile → API
   Tokens**) y elige **Create Token**.
3. No uses una plantilla: empieza desde cero, con un token personalizado.
   Ponle un nombre, por ejemplo `Live Track Internet`.
4. En los permisos, elige **Account**, luego **Radar**, luego **Read**. No
   hace falta nada más.
5. Elige **Continue to summary** y después **Create Token**.
6. Copia el token enseguida: Cloudflare solo lo muestra una vez.
7. Pégalo en **Token de API de Cloudflare** cuando
   [configures](#configuración-paso-a-paso) Live Track Internet, o más tarde
   con **Reconfigurar**.

Live Track Internet comprueba el token con una petición real a Cloudflare Radar
antes de guardarlo. El token se queda en tu Home Assistant y solo se envía a
Cloudflare. No hace falta ninguna contraseña ni otro secreto aparte del token.
Los nombres de los botones aparecen aquí como Cloudflare los muestra en
inglés; si Cloudflare te muestra sus páginas en español, allí tienen otros
nombres.

---

## Poner el mapa en un panel

El mapa es [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard),
la tarjeta en la que dibuja cada módulo de Live Track. **Se instala con Live
Track Internet**: nada que descargar, nada que copiar, ningún recurso que
añadir.

1. Abre un panel, elige el lápiz (**Editar panel de control**) y después
   **Añadir tarjeta**.
2. Baja hasta el final y elige **Manual**.
3. Pega esto y elige **Guardar**:

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

Las capas de los cables y los enlaces aparecen por sí solas. Los marcadores de
los cortes llegan por el filtro de arriba.

Los demás módulos de Live Track van en `entity_filter` del mismo modo: una
regla `- domain: geo_location` más por cada fuente.

**En el mapa:**

* El **control de capas** de arriba a la derecha tiene una casilla para cada
  capa: **Cables con problemas**, **Todos los cables**, **Puntos de amarre** y
  **Enlaces terrestres**. La elección de cada persona que mira se guarda en su
  propio navegador.
* Cada corte es una imagen redonda de su causa con el código de dos letras del
  país al lado. **Apunta** a ella para ver dónde y por qué; **haz clic** para
  ver la descripción de Cloudflare y un enlace a la noticia.
* **Haz clic** en un cable para ver su nombre, sus propietarios, su longitud y
  sus países de amarre. Los enlaces terrestres no se pueden pulsar.
* La **tarjeta de filtro** (`custom:live-track-map-filter-card`) puede ocultar
  los cortes según su causa.
* El crédito de cada fuente aparece en la línea de atribución del mapa
  mientras se muestran sus datos.

La tarjeta mantiene exactamente una fila de recurso del panel para todos los
módulos de Live Track juntos: la versión más reciente de la tarjeta que traiga
cualquiera de ellos, nunca una más antigua. Una tarjeta que hayas instalado tú
desde el Marketplace no se toca. Si los recursos de tus paneles están
definidos en YAML (`lovelace: resource_mode: yaml`), no se puede registrar
nada por ti: entonces un aviso en **Reparaciones** te da la línea exacta que
debes añadir, que tiene este aspecto, con la dirección propia de la
integración en lugar de los marcadores de posición:

```yaml
lovelace:
  resource_mode: yaml
  resources:
    - url: /live_track_internet/map-card/<12 hex>/live-track-map-card.js?v=<version>&h=<12 hex>
      type: module
```

Al eliminar la entrada de Live Track Internet, la fila pasa a otro módulo de
Live Track, o se quita si no queda ninguno. Si se borran los archivos de la
integración mientras su entrada sigue configurada, y no hay otro módulo de
Live Track instalado, quita tú la fila de la tarjeta en **Configuración →
Paneles de control → Recursos**. Para instalar la tarjeta a mano, sigue el
README de la tarjeta. Una fila que hayas creado tú, para una copia en
`/local/` o en cualquier otra dirección, nunca se cambia ni se quita. Mientras
cargue la tarjeta, cada módulo de Live Track le deja la tarjeta, aunque un
módulo traiga una versión más nueva, y nada en **Reparaciones** lo dice. Para
volver a la copia del módulo, quita tu fila en **Configuración → Paneles de
control → Recursos** y reinicia Home Assistant. Si borras el archivo de tu
copia, quita también su fila: mientras quede una fila cuyo archivo ya no está,
el módulo no añade una fila propia. Cualquier otra tarjeta de mapa que muestre
entidades `geo_location` muestra también los marcadores de los cortes, pero no
los cables ni los enlaces.

---

## Usarlo en automatizaciones

Todo es una entidad normal de Home Assistant, así que el editor de
automatizaciones funciona con ella, sin código.

**Una notificación en el teléfono cuando Cloudflare registra un nuevo corte de
internet** (para esto hace falta el token de Cloudflare):

1. **Configuración → Automatizaciones y escenas → Crear automatización →
   Crear nueva automatización**.
2. **Cuando**: **Añadir disparador**, escribe `numeric` en el cuadro de
   búsqueda y elige **El estado numérico cruzó el umbral**. Elige la
   **Entidad** **Cloudflare Radar Cortes de internet**, y en **Por encima de**
   escribe `0`.
3. **Entonces hacer**: **Añadir acción**, busca la acción de notificación de
   tu teléfono (lleva el nombre de tu teléfono) y escribe un mensaje, por
   ejemplo:

   ```text
   Cloudflare Radar informa de un corte de internet
   ```

4. **Guardar**.

**Otras ideas:** una notificación cuando un corte nombra un cable submarino,
con **Submarine cables Cables con problemas** por encima de 0; un mosaico del
panel con el número de cortes abiertos, desde **Cloudflare Radar Cortes de
internet**.

---

## Todo lo que hay en el mapa, en detalle

### Cortes

[Cloudflare Radar](https://radar.cloudflare.com) mantiene un Outage Center:
registros de cortes de internet en todo el mundo, escritos por personas de
Cloudflare, cada uno con una causa, un tipo (nacional, regional o de una sola
red), los países o regiones afectados, una hora de inicio y casi siempre un
enlace a una noticia.

Live Track Internet pide los registros de las últimas 24 horas cada
15 minutos y dibuja un marcador por cada registro abierto en cada lugar que
nombra: en la región cuando el registro nombra una, si no en el país. Un
registro que termina sale del mapa. Los registros sobre un servicio en línea en
lugar de un lugar (el corte de un proveedor de nube, por ejemplo) no se
dibujan; el sensor **Cloudflare Radar Cortes de internet** los enumera en su
atributo `not_on_map`.

⚠ **Un registro que solo nombra una red se coloca en el centro de su país**,
lo que en un país grande puede quedar lejos del corte. El texto del clic lo
dice. Por ejemplo, Cloudflare clasifica dos redes de Lugansk y Donetsk
(Ucrania) bajo Rusia, así que sus cortes quedan en el centro de Siberia, y las
redes de EE. UU. quedan en Kansas.

⚠ Los registros de cortes los escriben personas, a menudo horas después de que
empiece un corte. Cuando medimos un año de registros (hasta el 23 de noviembre
de 2026), hubo 143, nunca más de 4 abiertos a la vez, y ninguno abierto el 43 %
del tiempo. La mayor parte del tiempo el mapa no muestra ningún corte.

Cada marcador se dibuja según su causa:

| Causa | Color | Imagen |
|---|---|---|
| Cable cortado | rojo | tijeras abiertas |
| Corte de electricidad | ámbar | rayo |
| Ordenado por un gobierno (un apagón de internet) | índigo | candado |
| Acción militar | negro | punto de mira |
| Tiempo o catástrofe natural | azul | nube de tormenta |
| Ciberataque | verde azulado | escudo con `!` |
| Problema técnico (red, software, DNS, mantenimiento) | gris azulado | llave inglesa |
| Causa desconocida | gris | `?` |

En cada marcador: `outage_cause` y `outage_type` (las palabras propias de
Cloudflare, por ejemplo `POWER_OUTAGE`, `NATIONWIDE`), `started_at`,
`place_kind` (`region`, `country` o `network`), `country_code`,
`country_name`, `region_name`, `asns` y `asn_names` cuando el registro nombra
redes, `description`, `linked_url` (la noticia), `cables_named` cuando la
descripción nombra un cable, y `marker_group` (la causa, para la tarjeta de
filtro).

### Cables con problemas

Con el token de Cloudflare, cada cable submarino nombrado en la descripción de
un corte abierto se dibuja grueso y en rojo con un borde blanco, activado por
defecto. Casi siempre no hay ninguno. El cable se reconoce por su nombre,
escrito de cualquiera de las formas habituales (`SEA-ME-WE 5`, `SeaMeWe-5`);
los nombres cortos solo se reconocen como palabras completas.

⚠ El campo de causa de Cloudflare no dice si un cable cortado es submarino:
en el año que medimos, el único registro clasificado como cable cortado era un
cable en tierra, y una avería del cable SEA-ME-WE 5 estaba clasificada como
causa desconocida. Por eso el cable se busca en la descripción, sea cual sea la
causa.

### Todos los cables y los puntos de amarre

Cada cable submarino del conjunto de datos de 2026 de Tristan Hotham con los
datos de cables de TeleGeography: 713 cables, 608 en servicio (dibujados en
azul) y 105 previstos (dibujados en naranja), como líneas finas y tenues, y
1.928 puntos de amarre como puntos pequeños (naranja donde solo llegan cables
previstos). Haz clic en un cable para ver su nombre, la fecha en que entró o
entrará en servicio, su longitud, sus países de amarre, sus propietarios y su
proveedor. Los datos vienen con la integración y solo cambian con una nueva
versión.

⚠ Un cable tendido después de crearse el conjunto de datos (noviembre de 2026)
solo aparece tras una versión que traiga datos más recientes.

### Enlaces terrestres

Los enlaces de fibra y de microondas en tierra que registran los Broadband Maps
de la UIT (Infrastructure Connectivity Map), a partir de operadores y
reguladores. Cada enlace se dibuja como lo publica la UIT: una línea recta de
un nodo al siguiente, no el recorrido que sigue el cable sobre el terreno.

| Línea | Qué es |
|---|---|
| ciruela | fibra, en servicio |
| amarillo con borde negro | microondas, en servicio |
| naranja | previsto, propuesto o en construcción (los de microondas con borde negro) |
| gris | sin estado indicado (los de microondas con borde negro) |

⚠ Con el grosor fino y tenue de las líneas del mapa, las de microondas parecen
más bien oliva o caqui que amarillas; el borde negro es lo que las distingue de
la fibra.

⚠ La UIT no registra operador, nombre, capacidad ni fecha de un enlace, así que
un enlace no se puede pulsar, y ningún corte se asocia a uno.

Tu Home Assistant descarga toda la capa de la UIT una vez por semana, en su
propio día y a su propia hora, y la guarda. Si una descarga falla o llega
incompleta, se queda la última copia buena, por antigua que sea.

---

## Todas las entidades que crea

| Entidad | Qué es |
|---|---|
| `sensor.live_track_internet_outages` | **Cloudflare Radar Cortes de internet**: cuántos marcadores de corte hay en el mapa (solo con el token) |
| `sensor.live_track_internet_cables_in_trouble` | **Submarine cables Cables con problemas**: cuántos cables nombra un corte abierto (solo con el token) |
| `sensor.live_track_internet_all_cables` | **Submarine cables Todos los cables**: el número de cables, 713 |
| `sensor.live_track_internet_landing_points` | **Submarine cables Puntos de amarre**: el número de puntos de amarre, 1.928 |
| `sensor.live_track_internet_terrestrial_links` | **ITU Broadband Maps Enlaces terrestres**: cuántos enlaces están dibujados (solo mientras **Enlaces terrestres de la UIT** esté marcado) |
| `geo_location.outage_…` | uno por cada corte abierto y lugar, con el número de registro de Cloudflare en el nombre (`geo_location.outage_1754`); aparece y desaparece con el registro |

Cada marcador lleva `source: live_track_internet`, y su estado es su distancia
a tu casa en kilómetros. Los sensores están en tres dispositivos:
**Cloudflare Radar**, **Submarine cables** e **ITU Broadband Maps**.

Los atributos del sensor de cortes: `open_records` (todos los registros
abiertos, también los que no están en el mapa), `not_on_map` y
`last_success`.

⚠ **Los marcadores no tienen ID único, a propósito.** Los registros de cortes
van y vienen, y una fila de registro por cada uno se quedaría para siempre. Por
eso no se pueden renombrar, ocultar ni asignar a un área en la interfaz. Los
sensores sí tienen ID únicos y se pueden renombrar.

Los atributos que cambian en cada actualización, y las listas grandes que lee
el mapa, se mantienen fuera del historial de Home Assistant, para que tu base
de datos no crezca con ellos.

---

## Qué envía y descarga

**Sobre tu ubicación.** Nada. La ubicación de tu casa solo se usa dentro de tu
Home Assistant, para calcular la distancia de cada marcador. Cloudflare recibe
tu token y el intervalo de tiempo de la petición; la UIT recibe la petición de
sus enlaces. Los datos de los cables vienen con la integración y no se
descargan. Cada servicio ve tu dirección de internet, como cualquier sitio web.

**Cuánto.** Tamaños medidos el 25 de noviembre de 2026, salvo que la tabla diga
otra cosa.

| Fuente | Qué y cada cuánto | Tamaño medido | Tras un error |
|---|---|---|---|
| Cloudflare Radar, cortes | una petición cada 15 minutos, con tu token: los registros de las últimas 24 horas | 447 bytes transferidos (un registro) | un token rechazado detiene las peticiones y te pide uno nuevo. HTTP 429: espera lo que pida Cloudflare, o 15 minutos, duplicando hasta 2 horas. Otros errores: nuevo intento a los 15, 30 y 60 minutos, y luego cada 2 horas. La última respuesta buena se guarda 2 horas; después desaparecen los marcadores |
| Cloudflare Radar, lugares | los puntos centrales de los países una vez al día; el punto de una región la primera vez que un registro la nombra, y luego se guarda | la lista de países: 36.905 bytes (23 de noviembre de 2026) | se sigue usando la copia que tienes |
| ITU Broadband Maps | toda la capa una vez por semana, en 9 peticiones separadas por 3 segundos, unos 36 segundos en total | unos 0,9 MB transferidos (111.537 bytes por cada 5.000 enlaces) | HTTP 429: espera lo que pida la UIT, o una hora, duplicando hasta un día. Otros errores: nuevo intento al día siguiente. Se queda la última copia buena |
| Tu navegador | desde tu Home Assistant, no desde internet: el archivo de cables cuando **Todos los cables** está marcado, los puntos de amarre cuando **Puntos de amarre** está marcado, y el archivo de enlaces cuando **Enlaces terrestres** está marcado | cables 113.323 bytes; puntos de amarre 38.160 bytes; enlaces 296.105 bytes | |

Desmarca **Enlaces terrestres de la UIT** (**Reconfigurar**) para detener la
descarga semanal. Elimina la entrada para detenerlo todo.

Los archivos descargados se guardan en la carpeta `.storage` de Home Assistant
con nombres que empiezan por `saw_` (`saw_radar_locations.json`,
`saw_radar_geolocations.json`, `saw_itu_bbmaps_links.json.gz`), para que otro
módulo de Live Track pueda compartirlos. Si quitas Live Track Internet y ningún
otro módulo de Live Track los usa, puedes borrarlos a mano.

---

## Ayúdanos a hacerlo crecer

Live Track Internet sigue creciendo. Añadimos fuentes de datos a medida que
las encontramos, y queremos saber qué te gustaría después.

### Sugiere algo

¿Falta una fuente de datos? ¿Hay algo mal o difícil de entender? Dínoslo como
te resulte más fácil:

* [**Rellena un formulario corto**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=es.yml)
  en español. Necesitas una cuenta gratuita de GitHub.
* **Escribe un correo** a
  [StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org).
  No hace falta cuenta.

En cualquier caso, nos ayuda que nos digas:

* qué te gustaría ver, y en qué lugar del mundo;
* un enlace a donde se publican los datos, si conoces alguno (una página de
  datos abiertos, un feed público, la web de un servicio): no es necesario,
  pero ayuda;
* el idioma de tu Home Assistant, si el problema es la redacción o una
  traducción.

Escribe en inglés o en tu propio idioma, lo que te resulte más fácil.

### Añádelo tú mismo, con nuestra ayuda

Si quieres añadir algo tú mismo, te ayudaremos a hacerlo, desde la primera
pregunta hasta la versión terminada. No necesitas ser desarrollador para
empezar:

* **Una traducción.** Los textos del diálogo de configuración son una lista
  corta de frases en un solo archivo de texto. Te mostraremos qué archivo y
  qué líneas.
* **Una fuente nueva.** Dinos dónde se publican los datos. Podemos escribir el
  código juntos o revisar el tuyo.
* **Probarlo donde vives.** Instálalo, mira tu parte del mapa y dinos qué
  está bien y qué no.
* **Una corrección de este README.** Si un paso no coincidía con lo que
  viste, dinos qué viste.

[**Cuéntanos qué tienes en mente**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=es.yml)
o escribe a
[StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org),
y te responderemos con los siguientes pasos.

---

## Idiomas

Este README: [English](README.md), [Deutsch](README.de.md),
[Français](README.fr.md), [Nederlands](README.nl.md),
[简体中文](README.zh-Hans.md), **Español**, [Italiano](README.it.md),
[Українська](README.uk.md) y [العربية](README.ar.md). Cada README traducido
está completo. Ninguno lo ha leído todavía un hablante nativo. Si uno de estos
es tu idioma, dinos si su README se lee bien: consulta
[Ayúdanos a hacerlo crecer](#ayúdanos-a-hacerlo-crecer).

El diálogo de configuración aparece en el idioma de tu Home Assistant cuando
es uno de estos: English, Deutsch, Español, Français, Italiano, Nederlands,
简体中文, Українська y العربية. Cualquier otro idioma muestra inglés. Las
traducciones del diálogo también se escribieron sin un hablante nativo. Las
palabras del mapa (los nombres de los cortes y los textos del clic, los nombres
de las causas en la tarjeta de filtro y los créditos) están en inglés en todos
los idiomas.

¿Has encontrado un error en una traducción, o necesitas otro idioma? Dínoslo
en <https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues>, o
[tradúcelo con nuestra ayuda](#añádelo-tú-mismo-con-nuestra-ayuda).

---

## Créditos y licencias

* **Cloudflare Radar** (Cloudflare, Inc., <https://radar.cloudflare.com>): los
  registros de cortes, bajo
  [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), leídos con
  el token propio de cada usuario. Esta integración coloca cada registro en el
  mapa; no cambia los registros. Al instalar esta integración usas la API de
  Cloudflare, y sus condiciones se aplican a ti.
* **Cables submarinos y puntos de amarre**: Hotham, T. (2026), *The
  internet's seabed: submarine cables, when they were laid, who owns them and
  where they crowd together*, Zenodo, <https://doi.org/10.5281/zenodo.23856607>,
  derivado del
  [Submarine Cable Map](https://www.submarinecablemap.com/) de TeleGeography,
  bajo [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
  Esta integración unió las líneas de los cables a la tabla de cables,
  convirtió ambas en archivos de mapa y redondeó los puntos de amarre a
  4 decimales; no se añadió ni se corrigió nada. Los archivos convertidos de
  `custom_components/live_track_internet/cables/` se comparten bajo la misma
  licencia, con su texto legal y un archivo de créditos al lado
  ([CREDIT.md](custom_components/live_track_internet/cables/CREDIT.md)).
* **Enlaces terrestres**: ITU Broadband Maps (BBmaps), el Infrastructure
  Connectivity Map, <https://bbmaps.itu.int>, © UIT. Usados según las
  condiciones de uso de la UIT para uso no comercial, citando la fuente. Este
  repositorio no incluye nada de la UIT: cada instalación descarga los enlaces
  para su propio usuario. Esta integración los dibuja como la UIT los publica,
  redondeados a 3 decimales (unos 110 m), y los enlaces repetidos del mismo
  tipo se dibujan una sola vez.
* **Las imágenes de los cortes** se dibujaron para StrausbergAutomationWorks,
  bajo la licencia MIT.
* **La tarjeta de mapa** es [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard),
  MIT, una copia de [ha-map-card](https://github.com/nathan-gs/ha-map-card) de
  nathan-gs, MIT. Sus mosaicos de mapa y sus créditos están en su README.

⚠ **Solo para uso no comercial.** Las tres fuentes de datos solo permiten el
uso no comercial. El código es MIT, pero los datos que muestra no se pueden
usar con fines comerciales.

Ninguna de estas organizaciones creó ni respaldó esta integración. Qué
licencia cubre cada parte de este repositorio: [ATTRIBUTION.md](ATTRIBUTION.md).

**Código**: MIT, en [LICENSE](LICENSE).

**Para desarrolladores:** las entidades siguen el contrato de mapa compartido
de Live Track, así que cada módulo se ve en un solo mapa.
`tools/build_cables.py` reconstruye los archivos de cables a partir del
repositorio de Hotham. Las pruebas se ejecutan con
`python -m unittest discover -s tests`.

---

## Palabras clave

Home Assistant corte de internet · mapa de cortes de internet · apagón de
internet · caída de internet · corte de red · caída del proveedor · Cloudflare
Radar · Radar Outage Center · cables submarinos · cable submarino · mapa de
cables submarinos · cable cortado · puntos de amarre · TeleGeography ·
Submarine Cable Map · fibra terrestre · mapa de fibra óptica · red troncal de
fibra · enlaces de microondas · UIT · ITU Broadband Maps · BBmaps ·
Infrastructure Connectivity Map · internet outage · submarine cables ·
Internetausfall · Seekabel · panne internet · câbles sous-marins ·
internetstoring · zeekabels · 断网 · 海底光缆 · interruzione internet · cavi
sottomarini · відключення інтернету · підводні кабелі · انقطاع الإنترنت ·
كابلات بحرية · geo_location · tarjeta de mapa · Lovelace · HACS ·
Marketplace · Live Track · LiveTrack · StrausbergAutomationWorks

---

**Reconocimiento.** StrausbergAutomationWorks reconoce a los pueblos indígenas
de todas las tierras y aguas de este mapa, en todo el mundo, y presenta sus
respetos a sus Mayores del pasado y del presente.
