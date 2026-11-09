# Decisiones y estado del proyecto

Cuaderno del proyecto: **qué se ha decidido, por qué, con qué valores y en qué punto está**. Sirve
para retomar el plan sin depender de la memoria y para que Claude tenga el contexto al abrir una
sesión nueva.

**Cómo mantenerlo**

- [Decisiones](#3-decisiones) describe el estado vigente, agrupado por tema. Si una decisión
  cambia, se reescribe (con lo descartado en su apartado) y se añade una línea a la
  [Bitácora](#6-bitácora); el texto anterior queda en git. Un tema nuevo es una D-nn nueva.
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
marca usada: 28 pies · pase a 23 m de la zona · recomendación: acercar 1,5 pies (para 8,6 m/s)
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

- **Cero datos a mano**: lo que sale del vídeo no se pregunta (D-01). Solo son opcionales la
  pareja y el pie.
- **Medidas fiables y con su error**: tiempos reales de cada fotograma, calibración validada y
  avisos cuando algo no es de fiar, antes que un número bonito.
- **Montaje barato y repetible**: un iPhone, un trípode y platillos. Nada de material
  especializado.
- **Privacidad**: el repo es público. Vídeos y nombres reales solo en `data/`, con el
  consentimiento de cada atleta (protocolo §10).

**Fuera del alcance (por ahora)**: grabar con varias cámaras o con la cámara en movimiento, y el
análisis en directo mientras se corre. Analizar entre intentos sí es objetivo de F6 (D-01).

## 1. Estado actual

*Actualizado: 2026-11-09*

- **F1 Entorno**: terminada (#1, #2, #3, #4, #34, #37). Paquete, CLI, CI, hooks, plantillas,
  `relevos info`. Añadidos después este documento, las skills de antislop (#41), la pestaña
  «Disponibilidad» del Project (#43) y el plugin superpowers (#50).
- **F2 Grabación**: protocolo hecho (#6). Pendiente probar colores y comprar platillos (#5) y la
  primera sesión de grabación (#7).
- **Siguiente**: F3 Calibración, empezando por el modelo de la rejilla (#8) y la calibración manual
  con clics (#9). El diseño de la rejilla, la calibración, el modelo y el flujo del MVP está
  cerrado (D-03 a D-09). Se puede avanzar con datos sintéticos mientras no haya vídeos
  reales. Antes de comprar platillos, probar el encuadre en #5.

## 2. Hoja de ruta

Primero todo en manual (clics), después se automatiza. El objetivo final es subir un vídeo sin
rellenar nada (D-01).

| Fase | Contenido | Issues |
|---|---|---|
| F1 Entorno | Esqueleto, CI, hooks, plantillas, `relevos info` | #1–#4, #34, #37 (cerradas) |
| F2 Grabación | Protocolo, colores de platillos, primera sesión | #5, #6 (cerrada), #7 |
| F3 Calibración | Rejilla y `sesion.json`, clics en platillos, homografía por tramos, `solvePnP`, validación leave-one-out, cámara movida, (Plan B) distorsión 0,5x | #8–#14 |
| F4 Eventos manuales | Visor fotograma a fotograma, marcado de eventos y posiciones | #15, #16 |
| F5 Métricas y marca | Tiempos, distancias, modelo de marca, ajuste por intento, `relevos analizar` (MVP) | #17–#21 |
| F6 Análisis automático | YOLO-pose + tracking, suavizado, eventos automáticos, platillos por color | #22–#24, #27 |
| F7 Visualización | Gráfica velocidad–distancia, vídeo anotado | #25, #26 |
| F8 Historial y extras | Historial por pareja, análisis técnico, validación con cronometraje | #28–#30 |

## 3. Decisiones

Formato: **D-nn · título** · issues. Qué se ha decidido (estado vigente), por qué y qué se descartó.

### D-01 · Producto: subir el vídeo sin rellenar nada
#6, #8, #46

- **Decisión**: todo lo que se pueda sacar del vídeo se infiere (sentido de carrera, tipo de zona,
  calibración, marca usada, resultado de la entrega, cámara movida). Solo son opcionales la pareja
  (para historial) y la longitud del pie (para dar la marca en pies). Primero se hace todo con
  clics (F3–F5) y después se automatiza (F6, F8). En el MVP los vídeos se analizan en casa,
  después de la sesión, y llegan por cable USB. El objetivo de F6 es analizar entre intentos, con
  un portátil en la pista y 1–2 minutos por intento, subiendo el vídeo desde Safari a una página
  servida por el portátil si iOS no lo recomprime (#7).
- **Motivo**: rellenar hojas en pista no es realista. El MVP manual da algo medible pronto y una
  referencia para validar lo automático. La marca sirve más si se corrige en la misma sesión, pero
  con clics no da tiempo entre intentos.
- **Descartado**: hoja de registro por sesión e intento; analizar en el propio iPhone.

### D-02 · Grabación: cámara fija a 60 fps y primeros fotogramas sin el que llega
#4, #6, #13, #14

- **Decisión**: iPhone fijo en trípode, 4K60 (o 1080p60), con la lente principal 1x; el 0,5x con
  corrección de distorsión (#14) solo si no hay forma de alejarse. En el código se usan siempre
  las marcas de tiempo reales de cada fotograma (`InfoVideo.timestamps`), nunca `índice / fps`; lo
  dudoso (VFR, < 50 fps, fps nominales ≠ reales) se avisa, no da error. Cada vídeo empieza con
  1–2 s sin el que llega en plano: sirven para calibrar y para detectar si la cámara se ha movido.
  El receptor puede estar ya en su sitio si no pisa ni tapa platillos.
- **Motivo**: 60 fps reducen a la mitad el error de la reacción frente a 30; los móviles graban
  con frecuencia variable. El 0,5x deforma las rectas. Pedir al receptor que se aparte en cada
  intento no es realista, y el primer clic del MVP (D-07) es su pie parado.

### D-03 · Rejilla de platillos y coordenadas de pista
#5, #6, #8, #18

- **Decisión**: por zona, 20 platillos fijos en los dos bordes de la calle, cada 5 m de −15 a 30 m,
  **centrados sobre la línea**, que se quedan puestos toda la sesión. En curva se mide a lo largo
  de la línea interior y cada platillo exterior va enfrente. Coordenadas: `s = 0` en el inicio de
  la zona y positiva en el sentido de carrera; `d = 0` en el borde interior y positiva hacia fuera
  (fila exterior en `d = 1,22`). El indicador de marca no forma parte de la rejilla: se mueve con
  cada cambio de marca y se localiza en cada vídeo (#18). Los colores se configuran una vez por
  pista (#27): como mucho 3, nunca blanco ni el color de la pista.
- **Motivo**: puntos de suelo conocidos para pasar de píxeles a metros sin suponer la geometría de
  la pista. Con los platillos «sobre la línea o justo por fuera» quedaban ±10 cm de duda en `d`,
  que desvían la pose de la cámara. La pista de pruebas es azul y otras son rojas.
- **Descartado**: platillo tocando la línea por fuera con su radio como parámetro.

### D-04 · Calibración: homografía por tramos y pose con la forma de la pista
#9, #10, #11, #12

- **Decisión**: una homografía por cada tramo de 5 m (cuadrilátero entre pares interior/exterior
  consecutivos) para pasar de píxel a `(s, d)`. Para los puntos que no están en el suelo (cadera
  ≈ 1 m, testigo), #11 ajusta a la vez la pose y la focal de la cámara y la forma de la pista
  (radio de la curva y punto donde empieza la recta; la recta es radio infinito) que mejor
  reproyectan los 20 platillos. La validación da error si las filas están cambiadas: en el 4x100
  se corre en sentido antihorario, así que la fila interior queda a la izquierda del sentido de
  carrera, y una homografía reflejada (determinante negativo) delata el error de clic.
- **Motivo**: la homografía por tramos funciona igual en recta y en curva. `solvePnP` necesita
  posiciones cartesianas y en curva `s` es un arco; las tres zonas del 4x100 mezclan curva y
  recta, y la focal del iPhone no se mide. Con 20 puntos para unos 9 parámetros hay margen.
- **Descartado**: medir a mano la posición de la cámara; suponer la geometría oficial de la pista
  (exige saber la calle); `solvePnP` con solo los 4 platillos del tramo cercano (pose ruidosa).

### D-05 · `sesion.json` con una lista de calibraciones
#8, #9, #13

- **Decisión**: `sesion.json` está en la carpeta de la sesión, lo genera el programa y vale para
  todos sus vídeos, también los de las subcarpetas por pareja (D-06). Tiene un campo `version` y
  una lista de calibraciones; cada una guarda `id`, `creada`, `video`, `instante_ms`,
  `resolucion`, los parámetros de la rejilla, el píxel de cada platillo (o `null` si no se ve) y
  el nombre del PNG del fotograma de referencia (`calibracion_<id>.png`, al lado). Los píxeles van
  en la resolución nativa y es un error aplicarlos a un vídeo de otra resolución. Qué calibración
  usa cada vídeo lo calcula #13 en cada análisis, comparando features con los PNG; no se guarda.
  `dataclasses` + `json`, validando en `__post_init__` como `InfoVideo`.
- **Motivo**: si se golpea el trípode o se cambia de zona, se recalibra sin perder la calibración
  de los vídeos anteriores. Guardar la rejilla evita leer una sesión antigua con otros valores por
  defecto. Sin #27 no se pueden volver a detectar platillos, así que #13 compara imágenes.
- **Descartado**: una sola calibración que se sobrescribe; coordenadas normalizadas (esconderían
  cambios de encuadre); tabla vídeo → calibración (se desfasa al borrar o renombrar vídeos);
  pydantic.

### D-06 · Pareja por subcarpeta y resultados junto al vídeo
#21, #28

- **Decisión**: dentro de la carpeta de la sesión, una subcarpeta por pareja
  (`data/sesiones/2026-11-20/ATL1-ATL2/`), que se ordena después viendo las miniaturas; los vídeos
  sueltos en la raíz son de pareja desconocida y `--pareja` la fuerza. `ATL1-ATL2` quiere decir
  que ATL1 entrega a ATL2. Cada vídeo tiene al lado su `IMG_xxxx.resultado.json` con las
  métricas, la clasificación, la calibración usada y los clics manuales; el ajuste (#20) y el
  historial (#28) recorren las carpetas.
- **Motivo**: apuntar en pista quién corre cada intento sería volver a la hoja de registro (D-01).
  Guardar los clics evita repetirlos al volver a analizar.
- **Descartado**: SQLite para el historial; un JSON de eventos separado del de resultados.

### D-07 · Clics del MVP: una lista cerrada de eventos
#15, #16

- **Decisión**: cada vídeo pide unos 10 clics, en orden, cada uno sobre el pie o el testigo en un
  fotograma (la homografía da su `s`): indicador y pie adelantado del receptor parado; pie del que
  llega en la marca; primer movimiento del receptor; pase (inicio y fin, con la posición del
  testigo); el que llega cruzando `s = 0`; el receptor cruzando 20 y 30 m; y dos o tres posiciones
  del receptor antes del pase. Las trayectorias completas llegan con F6.
- **Motivo**: con esos puntos salen todas las medidas de D-08 y D-09 sin marcar a los atletas
  fotograma a fotograma.

### D-08 · Modelo de la marca de salida
#17, #18, #19

- **Decisión**: `T = tr + t_receptor(L)` y `marca = v·T − L + d_libre`, con:
  - `v`: velocidad media del que llega entre la marca y el punto del pase. La de los últimos
    metros solo se muestra, para ver si llega frenando.
  - `tr`: desde el primer apoyo del pie del que llega a la altura de la marca o después hasta el
    primer movimiento del pie adelantado o la cadera del receptor (en F6, con los tobillos de
    YOLO-pose).
  - Objetivos por defecto `L = 20 m` y `d_libre = 1,2 m` (Ajustes), que se pueden cambiar por
    pareja.

  La marca se da en pies del receptor si su pie está en `data/atletas.csv`; si no, en metros y en
  pies de 30 cm. Se recomienda para la velocidad grabada y el resumen dice cuál es («para
  8,6 m/s»). Caso de prueba: 9 m/s, 0,2 s, 2,9 s en 20 m → ≈ 9,1 m ≈ 30 pies.
- **Motivo**: `v·T` es la distancia que recorre el que llega en ese tramo, así que la media del
  tramo es la que encaja; la velocidad final, más baja si frena, acortaría la marca. El pie en la
  marca es a lo que reacciona el receptor. Los objetivos no salen del vídeo.
- **Descartado**: preguntar los objetivos en cada análisis (contra D-01) o aprenderlos de los
  mejores intentos; la cadera cruzando el indicador como inicio de `tr`; dar la marca para otra
  velocidad o analizar vídeos de competición.

### D-09 · Juicio de cada intento y ajuste de la marca
#17, #18, #20, #21

- **Decisión**: cada intento se juzga con el veredicto «pase en 15–20 m» y con el tiempo del
  testigo en la zona, aproximado con las caderas (desde que el que llega cruza `s = 0` hasta que
  el receptor cruza `s = 30`). Se clasifica como *válido*, *receptor frenó* (su velocidad cae
  antes del pase), *sin pase o fuera de zona* o *problema de grabación* (#13). Solo los válidos
  alimentan el modelo; en los demás se da la dirección (acercar o alejar) y la distancia del pase,
  sin cifra. El ajuste (#20) usa los intentos válidos de la misma sesión y pareja, con más peso a
  los últimos, y da la cifra con su dispersión («28,5 pies, 4 intentos, ±1 pie»); las sesiones
  anteriores se muestran solo como referencia.
- **Motivo**: el tiempo en zona es lo que gana carreras y 15–20 m es el objetivo técnico del grupo.
  Si el receptor frena para esperar, su `t_receptor(L)` no es el de una salida a tope. Entre
  sesiones cambian el cansancio, la forma y el viento.
- **Descartado**: combinar con menos peso las sesiones anteriores; usar solo el último intento.

### D-10 · Detección automática con YOLO-pose
#22, #23

- **Decisión**: ultralytics (YOLO-pose + ByteTrack/BoT-SORT) en el extra `[deteccion]`, no en las
  dependencias base. Roles con la calibración: el receptor es la persona parada dentro de la calle
  (`0 ≤ d ≤ 1,22`) en los primeros fotogramas; el que llega es quien entra corriendo en la calle
  desde atrás; se ignora a quien esté fuera de la calle. Trayectorias suavizadas con
  Savitzky-Golay (o Kalman) sobre `s`.
- **Motivo**: la detección pesa mucho para quien solo use el MVP manual. Con `(s, d)` los roles
  salen sin preguntar y se descarta al entrenador y a otras calles.

### D-11 · Herramientas del repo
#41, #43, #50

- **Decisión**: las skills `antislop`, `antislop-code` y `antislop-copywriting` (v3.2.25, MIT) se
  copian a `.claude/skills/`, en modo *during*. El plugin superpowers (MIT) se instala completo,
  declarado en `.claude/settings.json`; sus skills no se tocan y `CLAUDE.md` fija dónde manda el
  repo (PR con squash merge, specs y planes en español en `docs/superpowers/`, subagentes en
  paralelo solo si se piden). Las PRs se revisan con su `requesting-code-review`. La sección «Depende de» de cada issue es la fuente
  de las dependencias: `scripts/disponibilidad.py`, desde la Action `disponibilidad.yml`, crea las
  dependencias nativas y rellena el campo «Disponibilidad» del Project (Lista / Bloqueada /
  Hecha). El flujo de ramas, commits y PRs está en [CONTRIBUTING.md](../CONTRIBUTING.md).
- **Motivo**: evitar textos con pinta de IA en código, docs e issues, ver de un vistazo qué se
  puede empezar y que Claude trabaje con un método fijo (diseño antes de programar, TDD,
  verificar antes de dar algo por hecho).
- **Coste**: la Action necesita un token personal en el secret `PROJECT_TOKEN`, que hay que
  renovar cuando caduque.
- **Descartado**: instalar el plugin completo de antislop (trae skills de UI y un servidor MCP que
  el proyecto no usa). Con superpowers no se hace la copia selectiva, porque el hook que carga
  `using-superpowers` al empezar cada sesión solo llega con el plugin.

## 4. Ajustes y parámetros

Valores vigentes. Si cambian, se edita aquí y se explica en una decisión nueva.

| Parámetro | Valor | Dónde / por qué |
|---|---|---|
| Frecuencia de grabación | 60 fps (aviso si < 50 fps reales) | D-02, `video.py` |
| Resolución | 4K60 HEVC; 1080p60 «Más compatible» si no se lee | protocolo §4 |
| Platillos por zona | 21 (10 + 10 + indicador) | D-03 |
| Separación de platillos | 5 m, de −15 a 30 m | D-03 |
| Posición de las filas | Centradas sobre la línea: `d = 0` (interior) y `d = 1,22` (exterior) | D-03 |
| Longitud de la zona | 30 m (+15 m previos con la marca) | protocolo §5 |
| Ancho de calle | 1,22 m | protocolo §5 |
| Altura de la cámara | Lo más alta posible; mínimo 2–3 m | protocolo §6 |
| Pista vacía al empezar | 1–2 s | D-02 |
| Colores pista azul | Interior amarillo, exterior verde flúor, límites/indicador naranja | D-03, #5 (por confirmar) |
| Colores pista roja | Amarillo, verde flúor, azul | D-03 |
| Altura de cadera para proyectar | ≈ 1 m | D-04 |
| Ventana de velocidad | 0,3–0,5 s o por zancada | #23 |
| Pie por defecto | 30 cm | D-08 |
| Punto del pase objetivo (`L`) | 20 m | D-08 |
| Zona objetivo del pase | 15–20 m | D-09 |
| Distancia libre objetivo (`d_libre`) | 1,2 m | D-08 |
| Error de reproyección admisible | «unos cm» (umbral por fijar) | #10 |
| Precisión objetivo de la calibración | 10–20 cm (leave-one-out) | #12 |

## 5. Preguntas abiertas

- ¿El verde flúor se distingue bien sobre la pista azul? Si no, rosa/magenta (#5).
- Umbral concreto de error de reproyección para avisar (#10).
- ¿Los vídeos HEVC 4K60 del iPhone se leen bien con OpenCV en Windows? Comprobar con
  `relevos info` en la primera sesión (#7).
- ¿Un vídeo subido desde Safari llega sin recomprimir y con sus fps? Si no, F6 se queda con el
  cable USB (#7, D-01).
- ¿Caben los 45 m con la lente 1x desde algún sitio real de la pista? A unos 70° de campo hace
  falta estar a unos 35 m de la calle; si no se puede, 0,5x con la homografía por tramos y #12
  decide si hace falta corregir la distorsión (#5, D-02).

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
- **2026-11-07** — Docs e issues puestas al día con D-015 a D-023 (#48). `CLAUDE.md` pide tener
  en cuenta este documento en cualquier tarea. #14 pasa a depender de la prueba de encuadre (#5).
  «Pista vacía» sin el que llega (D-024), pose y forma de la pista ajustadas a la vez (D-025) y
  roles con la calibración (D-026).
- **2026-11-07** — Decisiones simplificadas (#48): las 26 antiguas (D-001…D-026) se agrupan por tema
  en D-01…D-11 y pasan a describir el estado vigente. Equivalencias: D-01 ← 001, 002, 018;
  D-02 ← 003, 007, 011, 024; D-03 ← 004, 008, 015; D-04 ← 005, 006, 017, 025; D-05 ← 016 y
  parte de 022; D-06 ← resto de 022; D-07 ← 023; D-08 ← 009, 020 y parte de 019; D-09 ← resto
  de 019 y 021; D-10 ← 010, 026; D-11 ← 013, 014 (012 queda en `CONTRIBUTING.md`). Las líneas
  anteriores de la bitácora usan la numeración antigua.
- **2026-11-09** — Plugin superpowers en `.claude/settings.json`, con las reglas del repo en
  `CLAUDE.md`; las PRs se revisan con `requesting-code-review` (#50, D-11).
