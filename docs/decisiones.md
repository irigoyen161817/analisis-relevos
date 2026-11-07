# Decisiones y estado del proyecto

Cuaderno del proyecto: **qué se ha decidido, por qué, con qué valores y en qué punto está**. Sirve
para retomar el plan sin depender de la memoria y para que Claude tenga el contexto al abrir una
sesión nueva.

**Cómo mantenerlo**

- Cuando se tome una decisión técnica, se añade una entrada en [Decisiones](#3-decisiones) (no se
  borran: si cambia, se marca como *sustituida por D-xxx* y se añade la nueva).
- Cuando cambie un valor (fps, distancias, umbrales, colores…), se actualiza
  [Ajustes](#4-ajustes-y-parámetros).
- Al cerrar una issue o terminar una sesión de trabajo, se actualiza [Estado](#1-estado-actual) y
  se añade una línea a la [Bitácora](#6-bitácora).
- Lo que va en otros documentos no se repite aquí, se enlaza: comandos y convenciones en
  [CLAUDE.md](../CLAUDE.md) y [CONTRIBUTING.md](../CONTRIBUTING.md), grabación en
  [protocolo.md](protocolo.md), detalle de cada tarea en su issue.
- El repo es público: nada de nombres reales ni datos de atletas, solo alias.

## Objetivo del proyecto

**Qué problema resuelve.** En el 4x100, la marca de salida del receptor (a cuántos pies de la zona
arranca) decide si la entrega sale bien: si sale tarde, el que llega se le echa encima y frena; si
sale pronto, el que llega no lo alcanza o el pase se hace al final de la zona o fuera de ella. Hoy
la marca se ajusta a ojo. `relevos` la mide en vídeo y dice cuánto moverla.

**Qué se quiere conseguir.** Grabar cada intento con un móvil fijo, subir el vídeo y obtener, sin
rellenar nada:

```
marca usada: 28 pies · pase a 21 m de la zona · recomendación: alejar 1,5 pies
```

**A qué se aspira**, por etapas:

1. **MVP (F3–F5)**: con unos clics sobre el vídeo (platillos y eventos), dar por cada intento la
   marca usada, dónde se hizo el pase, los tiempos y la marca recomendada (`relevos analizar`, #21).
2. **Automático (F6)**: lo mismo sin clics. Detecta los platillos, a los atletas, el pase y si la
   cámara se ha movido.
3. **Útil en el entrenamiento (F7–F8)**: vídeo anotado y gráfica de velocidad, historial por
   pareja y una recomendación que mejora con cada intento. Validado contra cronometraje
   independiente para saber cuánto fiarse.

**Principios que no se negocian**

- **Cero datos a mano**: lo que sale del vídeo no se pregunta (D-001). Solo son opcionales la
  pareja y el pie.
- **Medidas fiables y con su error**: tiempos reales de cada fotograma, calibración validada y
  avisos cuando algo no es de fiar, antes que un número bonito.
- **Montaje barato y repetible**: un iPhone, un trípode y platillos. Nada de material
  especializado.
- **Privacidad**: el repo es público. Vídeos y nombres reales solo en `data/`.

**Fuera del alcance (por ahora)**: grabar con varias cámaras o con la cámara en movimiento, y el
análisis en tiempo real durante la sesión.

## 1. Estado actual

*Actualizado: 2026-11-07*

- **F1 Entorno**: terminada (#1, #2, #3, #4, #34, #37). Paquete, CLI, CI, hooks, plantillas,
  `relevos info`. Añadidos después este documento, las skills de antislop (#41) y la pestaña
  «Disponibilidad» del Project (#43).
- **F2 Grabación**: protocolo hecho (#6). Pendiente probar colores y comprar platillos (#5) y la
  primera sesión de grabación (#7).
- **Siguiente**: F3 Calibración, empezando por el modelo de la rejilla (#8) y la calibración manual
  con clics (#9). El diseño de #8 está cerrado (D-015, D-016, D-017) y el del modelo y el flujo
  del MVP también (D-018 a D-023). Se puede avanzar con datos sintéticos mientras no haya vídeos
  reales. Antes de comprar platillos, probar el encuadre en #5.

## 2. Hoja de ruta

Primero todo en manual (clics), después se automatiza. El objetivo final es subir un vídeo sin
rellenar nada (ver D-001 y D-002).

| Fase | Contenido | Issues |
|---|---|---|
| F1 Entorno | Esqueleto, CI, hooks, plantillas, `relevos info` | #1–#4, #34, #37 (cerradas) |
| F2 Grabación | Protocolo, colores de platillos, primera sesión | #5, #6 (cerrada), #7 |
| F3 Calibración | Rejilla y configuración, clics en platillos, homografía por tramos, `solvePnP`, validación leave-one-out, cámara movida, (Plan B) distorsión 0,5x | #8–#14 |
| F4 Eventos manuales | Visor fotograma a fotograma, marcado de eventos y posiciones | #15, #16 |
| F5 Métricas y marca | Tiempos, distancias, modelo de marca, ajuste por intento, `relevos analizar` (MVP) | #17–#21 |
| F6 Análisis automático | YOLO-pose + tracking, suavizado, eventos automáticos, platillos por color | #22–#24, #27 |
| F7 Visualización | Gráfica velocidad–distancia, vídeo anotado | #25, #26 |
| F8 Historial y extras | Historial por pareja, análisis técnico, validación con cronometraje | #28–#30 |

## 3. Decisiones

Formato: **D-nnn · título** — fecha · issue. Decisión, motivo y alternativas descartadas.

### D-001 · Subir el vídeo sin rellenar nada
2026-10-20 · #6, #8

- **Decisión**: todo lo que se pueda sacar del vídeo se infiere (sentido de carrera, tipo de zona,
  calibración, marca usada, resultado de la entrega, cámara movida). Solo son opcionales la pareja
  de atletas (para historial) y la longitud del pie (para dar la marca en pies).
- **Motivo**: rellenar hojas en pista no es realista; el usuario quiere subir el vídeo y ya.
- **Descartado**: hoja de registro por sesión e intento.

### D-002 · Manual primero, automatizar después
2026-10-20

- **Decisión**: F3–F5 se hacen con clics (calibración y eventos); F6 y F8 automatizan.
- **Motivo**: tener un MVP medible pronto y una referencia manual para validar lo automático.

### D-003 · Cámara fija a 60 fps con marcas de tiempo reales
2026-10-20 · #4

- **Decisión**: iPhone fijo en trípode, 4K60 (o 1080p60). En el código se usan siempre las marcas
  de tiempo reales de cada fotograma (`InfoVideo.timestamps`), nunca `índice / fps`.
- **Motivo**: 60 fps reducen a la mitad el error de la reacción frente a 30; los móviles graban
  con frecuencia variable, así que el índice no da el tiempo real.
- Lo dudoso (VFR, < 50 fps, fps nominales ≠ reales) se avisa, no da error.

### D-004 · Rejilla de 21 platillos como referencia métrica
2026-10-20 · #6, #8

- **Decisión**: por zona, 10 platillos en cada borde de la calle cada 5 m de −15 a 30 m, más un
  indicador de marca. La rejilla se queda puesta toda la sesión. En curva se mide solo a lo largo
  de la línea interior y el exterior se pone enfrente.
- **Motivo**: da puntos de suelo conocidos para pasar de píxeles a metros sin suponer la geometría
  de la pista. El indicador permite medir la marca real usada sin apuntarla.

### D-005 · Homografía por tramos a coordenadas de pista (s, d)
2026-10-20 · #10

- **Decisión**: una homografía por cada tramo de 5 m (cuadrilátero entre pares interior/exterior
  consecutivos). Coordenadas: `s` a lo largo de la calle y `d` desde el borde.
- **Motivo**: funciona igual en recta y en curva; no hay que modelar la curva.

### D-006 · Pose de la cámara con `solvePnP`
2026-10-20 · #11

- **Decisión**: la posición y altura de la cámara se calculan a partir de la rejilla, no se miden.
  Sirven para proyectar puntos que no están en el suelo (cadera ≈ 1 m, manos) y corregir el
  paralaje.

### D-007 · Calibración y control de cámara con los primeros fotogramas
2026-10-20 · #6, #13

- **Decisión**: cada vídeo empieza con 1–2 s de pista vacía; se usan para calibrar y para detectar
  si la cámara se ha movido respecto a la referencia de la sesión (`sesion.json`, generado por el
  programa).

### D-008 · Colores de platillos configurables por pista
2026-10-20 · #5, #8

- **Decisión**: los colores no están fijos en el código; se configuran una vez por pista. Como
  mucho 3 colores, nunca blanco ni el color de la pista.
- **Motivo**: la pista de pruebas es azul y otras son rojas; el naranja se confunde con el rojo.

### D-009 · Modelo de la marca de salida
2026-10-20 · #19

- **Decisión**: `T = tr + t_receptor(L)`, `marca = v·T − L + d_libre`. Se da en pies del atleta si
  se conoce su pie (`data/atletas.csv`); si no, en metros y en pies de 30 cm.
- Caso de prueba: 9 m/s, 0,2 s, 2,9 s en 20 m → ≈ 9,1 m ≈ 30 pies.

### D-010 · Detección automática con YOLO-pose como extra opcional
2026-10-20 · #22, #23

- **Decisión**: ultralytics (YOLO-pose + ByteTrack/BoT-SORT) en el extra `[deteccion]`, no en las
  dependencias base. Roles asignados solos: receptor = parado cerca de la marca al inicio.
  Trayectorias suavizadas con Savitzky-Golay (o Kalman) sobre `s`.

### D-011 · Lente 1x; el 0,5x solo como Plan B
2026-10-20 · #6, #14

- **Decisión**: grabar con la lente principal. Corregir la distorsión del gran angular
  (`calibrateCamera`) solo si no hay forma de alejarse.

### D-012 · Flujo de trabajo del repo
2026-10-20 · #2, #3, #37

- **Decisión**: una issue por unidad de trabajo, ramas `feat|fix|docs/<n>-slug`, commits y PR
  `[#n] descripción`, solo squash merge, CI con ruff + pytest en 3.10–3.12, hooks de pre-commit.
  Todo en español. Detalle en [CONTRIBUTING.md](../CONTRIBUTING.md).

### D-013 · Skills de antislop para Claude, sin las de interfaz
2026-11-01 · #41

- **Decisión**: se copian a `.claude/skills/` las skills `antislop`, `antislop-code` y
  `antislop-copywriting` (v3.2.25, MIT), en modo *during* por defecto.
- **Motivo**: evitar comentarios de relleno y textos con pinta de IA en código, docs e issues.
- **Descartado**: instalar el plugin completo, porque trae las skills de UI y un servidor MCP de
  contraste que este proyecto no usa. Ver [.claude/skills/README.md](../.claude/skills/README.md).

### D-014 · Disponibilidad de las issues calculada por una Action
2026-11-01 · #43

- **Decisión**: la sección «Depende de» de cada issue es la fuente. `scripts/disponibilidad.py`
  crea las dependencias nativas (*blocked by*) y rellena el campo «Disponibilidad» del Project
  (Lista / Bloqueada / Hecha). Lo ejecuta la Action `disponibilidad.yml` con cada cambio de issue
  y una vez al día.
- **Motivo**: ver de un vistazo qué se puede empezar sin repasar las dependencias a mano.
- **Coste**: el `GITHUB_TOKEN` no escribe en Projects de usuario; hace falta un token personal
  en el secret `PROJECT_TOKEN`, que hay que renovar cuando caduque.

### D-015 · Coordenadas de pista y platillos centrados sobre la línea
2026-11-07 · #8

- **Decisión**: `s = 0` en el inicio de la zona y positiva en el sentido de carrera; en curva se
  mide a lo largo de la línea interior. `d = 0` en el borde interior y positiva hacia fuera. Los
  platillos van centrados sobre la línea, así que la fila interior está en `d = 0` y la exterior
  en `d = 1,22`. La rejilla tiene solo los 20 platillos fijos: el indicador de marca se localiza
  en cada vídeo (#18).
- **Motivo**: con «sobre la línea o justo por fuera» quedaban ±10 cm de duda en `d`. A la
  homografía no le afecta (en recta solo reescala `d`), pero a `solvePnP` (D-006) sí.
- **Descartado**: platillo tocando la línea por fuera con su radio como parámetro.

### D-016 · `sesion.json` con una lista de calibraciones
2026-11-07 · #8, #13 · *ubicación sustituida por D-022*

- **Decisión**: `sesion.json` (en la carpeta de los vídeos, generado por el programa) tiene un
  campo `version` y una lista de calibraciones. Cada una guarda `id`, `creada`, `video`,
  `instante_ms`, `resolucion`, los parámetros de la rejilla, los píxeles de cada platillo (o
  `null` si no se ve) y el nombre del PNG del fotograma de referencia, que se guarda al lado. Los
  píxeles van en la resolución nativa y es un error aplicarlos a un vídeo de otra resolución. Qué
  calibración usa cada vídeo lo calcula #13 en cada análisis; no se guarda.
- **Motivo**: si se golpea el trípode o se cambia de zona, se recalibra sin perder la calibración
  de los vídeos anteriores. Guardar la rejilla en cada calibración evita que una sesión antigua se
  lea con otros valores por defecto. El PNG le sirve a #13 para comparar features (sin #27 no se
  pueden volver a detectar platillos) y permite revisar los clics a ojo.
- **Descartado**: una sola calibración por carpeta que se sobrescribe; coordenadas normalizadas
  (esconderían cambios de encuadre); tabla vídeo → calibración (se desfasa al borrar o renombrar
  vídeos); pydantic (bastan `dataclasses` + `json`, como `InfoVideo`). La configuración de
  colores de pista sale de #8 y pasa a #27, que es el único que la usa.

### D-017 · La fila interior queda a la izquierda del sentido de carrera
2026-11-07 · #8, #9

- **Decisión**: la rejilla incluye esta regla y la validación de la calibración da error si la
  homografía sale reflejada (determinante negativo).
- **Motivo**: en el 4x100 se corre en sentido antihorario y una cámara real no refleja la imagen.
  Si alguien marca las filas al revés, `d` sale invertida y la pose de #11 es absurda; así se
  detecta al calibrar.

### D-018 · MVP en casa, entre intentos a partir de F6
2026-11-07 · #46

- **Decisión**: en el MVP (F3–F5) los vídeos se analizan después de la sesión y la marca
  corregida se usa en la siguiente. El objetivo de F6 es analizar entre intentos, con un portátil
  en la pista y 1–2 minutos por intento. En el MVP el vídeo llega por cable USB; para F6 se
  quiere una página web servida por el portátil en la red local para subirlo desde Safari, si se
  comprueba que iOS no lo recomprime (#7).
- **Motivo**: la marca sirve más si se corrige en la misma sesión, pero con clics manuales no da
  tiempo entre intentos. Fijarlo ahora condiciona la velocidad del análisis automático y si
  YOLO-pose tiene que correr sin GPU.
- **Descartado**: analizar en el propio iPhone.

### D-019 · Objetivos de la entrega y cómo se juzga un intento
2026-11-07 · #46, #17, #19, #21

- **Decisión**: objetivos por defecto `L = 20 m` y `d_libre = 1,2 m`, que se pueden cambiar por
  pareja. Se busca que el pase se haga entre 15 y 20 m. Cada intento se juzga con dos medidas: el
  veredicto «pase en 15–20 m» y el tiempo del testigo en la zona, aproximado con las caderas
  (desde que el que llega cruza `s = 0` hasta que el receptor cruza `s = 30`). La marca se
  recomienda para la velocidad grabada y el resumen dice cuál es («marca para 8,6 m/s»); no se
  extrapola a competición.
- **Motivo**: el modelo de D-009 necesita los objetivos y no salen del vídeo. El tiempo en zona es
  lo que gana carreras; el rango 15–20 m es el objetivo técnico del grupo.
- **Descartado**: preguntar los objetivos en cada análisis (contra D-001); aprenderlos de los
  mejores intentos; dar la marca para otra velocidad o analizar vídeos de competición.

### D-020 · `v` media de la marca al pase y `tr` desde el pie en la marca
2026-11-07 · #46, #15, #17, #18, #19

- **Decisión**: en `marca = v·T − L + d_libre`, `v` es la velocidad media del que llega entre la
  marca y el punto del pase. La velocidad de los últimos metros (#18) queda como dato informativo
  para ver si llega frenando. `tr` va desde el primer apoyo del pie del que llega a la altura de
  la marca o después hasta el primer movimiento del pie adelantado o la cadera del receptor; la
  misma definición vale en F6, con los tobillos de YOLO-pose.
- **Motivo**: `v·T` es la distancia que recorre el que llega en ese tramo, así que la media del
  tramo es la que encaja con la fórmula; la velocidad final, más baja si va frenando, acortaría la
  marca. El pie en la marca es a lo que reacciona el receptor.
- **Descartado**: la cadera cruzando la `s` del indicador como inicio de `tr`.

### D-021 · Clasificación de intentos y ajuste dentro de la sesión
2026-11-07 · #46, #20, #21

- **Decisión**: cada intento se clasifica como *válido*, *receptor frenó* (su velocidad cae antes
  del pase), *sin pase o fuera de zona* o *problema de grabación* (#13). Solo los válidos
  alimentan el modelo y el ajuste; en los otros se da la dirección (acercar o alejar la marca) y la
  distancia del pase, sin cifra recomendada. El ajuste (#20) usa los intentos válidos de la misma
  sesión y pareja, con más peso a los últimos, y da la cifra con su dispersión («28,5 pies,
  4 intentos, ±1 pie»). Las sesiones anteriores se muestran solo como referencia.
- **Motivo**: si el receptor frena para esperar, su `t_receptor(L)` no es el de una salida a tope
  y la cifra saldría mal. Entre sesiones cambian el cansancio, la forma y el viento.
- **Descartado**: combinar con menos peso las sesiones anteriores; usar solo el último intento.

### D-022 · Pareja por subcarpeta y resultados junto al vídeo
2026-11-07 · #46, #21, #28 · *sustituye la ubicación de `sesion.json` de D-016*

- **Decisión**: dentro de la carpeta de la sesión, una subcarpeta por pareja
  (`data/sesiones/2026-11-20/ATL1-ATL2/`), que se ordena después viendo las miniaturas; los vídeos
  sueltos en la raíz son de pareja desconocida. `--pareja` fuerza la pareja. `ATL1-ATL2` quiere
  decir que ATL1 entrega a ATL2, y la marca va en pies del receptor. `sesion.json` está en la raíz
  de la sesión y vale para todas las subcarpetas. Cada vídeo tiene al lado su
  `IMG_xxxx.resultado.json` con las métricas, la clasificación, la calibración usada y los clics
  manuales; #20 y #28 recorren las carpetas, sin base de datos.
- **Motivo**: apuntar en pista quién corre cada intento sería volver a la hoja de registro que se
  descartó en D-001. Guardar los clics evita repetirlos al volver a analizar.
- **Descartado**: SQLite para el historial; un JSON de eventos separado del de resultados.

### D-023 · Clics del MVP: una lista cerrada de eventos
2026-11-07 · #46, #15, #16

- **Decisión**: en el MVP cada vídeo pide unos 10 clics, en orden, cada uno sobre el pie o el
  testigo en un fotograma (la homografía da su `s`): indicador y pie adelantado del receptor
  parado; pie del que llega en la marca; primer movimiento del receptor; pase (fotograma y
  posición del testigo); el que llega cruzando `s = 0`; el receptor cruzando 20 y 30 m; y dos o
  tres posiciones del receptor antes del pase. Las trayectorias completas llegan con F6.
- **Motivo**: con esos puntos salen todas las medidas del modelo (D-019, D-020, D-021) sin marcar a
  los atletas fotograma a fotograma.

## 4. Ajustes y parámetros

Valores vigentes. Si cambian, se edita aquí y se explica en una decisión nueva.

| Parámetro | Valor | Dónde / por qué |
|---|---|---|
| Frecuencia de grabación | 60 fps (aviso si < 50 fps reales) | D-003, `video.py` |
| Resolución | 4K60 HEVC; 1080p60 «Más compatible» si no se lee | protocolo §4 |
| Platillos por zona | 21 (10 + 10 + indicador) | D-004 |
| Separación de platillos | 5 m, de −15 a 30 m | D-004 |
| Posición de las filas | Centradas sobre la línea: `d = 0` (interior) y `d = 1,22` (exterior) | D-015 |
| Longitud de la zona | 30 m (+15 m previos con la marca) | protocolo §5 |
| Ancho de calle | 1,22 m | protocolo §5 |
| Altura de la cámara | Lo más alta posible; mínimo 2–3 m | protocolo §6 |
| Pista vacía al empezar | 1–2 s | D-007 |
| Colores pista azul | Interior amarillo, exterior verde flúor, límites/indicador naranja | D-008, #5 (por confirmar) |
| Colores pista roja | Amarillo, verde flúor, azul | D-008 |
| Altura de cadera para proyectar | ≈ 1 m | D-006 |
| Ventana de velocidad | 0,3–0,5 s o por zancada | #23 |
| Pie por defecto | 30 cm | D-009 |
| Punto del pase objetivo (`L`) | 20 m | D-019 |
| Zona objetivo del pase | 15–20 m | D-019 |
| Distancia libre objetivo (`d_libre`) | 1,2 m | D-019 |
| Error de reproyección admisible | «unos cm» (umbral por fijar) | #10 |

## 5. Preguntas abiertas

- ¿El verde flúor se distingue bien sobre la pista azul? Si no, rosa/magenta (#5).
- Umbral concreto de error de reproyección para avisar (#10).
- ¿Los vídeos HEVC 4K60 del iPhone se leen bien con OpenCV en Windows? Comprobar con
  `relevos info` en la primera sesión (#7).
- ¿Un vídeo subido desde Safari llega sin recomprimir y con sus fps? Si no, F6 se queda con el
  cable USB (#7, D-018).
- ¿Caben los 45 m con la lente 1x desde algún sitio real de la pista? A unos 70° de campo hace
  falta estar a unos 35 m de la calle; si no se puede, 0,5x con la homografía por tramos y #12
  decide si hace falta corregir la distorsión (#5, D-011).

## 6. Bitácora

- **2026-10-20** — F1 completa: esqueleto, CI, hooks, plantillas, `relevos info`. Protocolo de
  grabación (#6). Se descarta la hoja de registro (D-001).
- **2026-11-01** — Se crea este documento y se añaden las skills de antislop (#41, D-013).
  Pestaña «Disponibilidad» en el Project y Action que la mantiene (#43, D-014).
- **2026-11-07** — Diseño de #8 cerrado: coordenadas y platillos sobre la línea (D-015),
  `sesion.json` con varias calibraciones (D-016) y regla de la fila interior (D-017). Los colores
  de pista pasan a #27 y el indicador a #18. Protocolo §5: platillos centrados sobre la línea.
- **2026-11-07** — Repaso del proyecto entero (#46): uso en casa y entre intentos en F6 (D-018),
  objetivos y juicio de cada intento (D-019), `v` y `tr` (D-020), clasificación y ajuste por
  sesión (D-021), pareja por subcarpeta y `resultado.json` (D-022), clics del MVP (D-023).
  Protocolo: carpeta por pareja y consentimiento.
