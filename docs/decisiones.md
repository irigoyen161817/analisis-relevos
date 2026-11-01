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

*Actualizado: 2026-11-01*

- **F1 Entorno**: terminada (#1, #2, #3, #4, #34, #37). Paquete, CLI, CI, hooks, plantillas,
  `relevos info`. Añadidos después este documento, las skills de antislop (#41) y la pestaña
  «Disponibilidad» del Project (#43).
- **F2 Grabación**: protocolo hecho (#6). Pendiente probar colores y comprar platillos (#5) y la
  primera sesión de grabación (#7).
- **Siguiente**: F3 Calibración, empezando por el modelo de la rejilla (#8) y la calibración manual
  con clics (#9). Se puede avanzar con datos sintéticos mientras no haya vídeos reales.

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

## 4. Ajustes y parámetros

Valores vigentes. Si cambian, se edita aquí y se explica en una decisión nueva.

| Parámetro | Valor | Dónde / por qué |
|---|---|---|
| Frecuencia de grabación | 60 fps (aviso si < 50 fps reales) | D-003, `video.py` |
| Resolución | 4K60 HEVC; 1080p60 «Más compatible» si no se lee | protocolo §4 |
| Platillos por zona | 21 (10 + 10 + indicador) | D-004 |
| Separación de platillos | 5 m, de −15 a 30 m | D-004 |
| Longitud de la zona | 30 m (+15 m previos con la marca) | protocolo §5 |
| Ancho de calle | 1,22 m | protocolo §5 |
| Altura de la cámara | Lo más alta posible; mínimo 2–3 m | protocolo §6 |
| Pista vacía al empezar | 1–2 s | D-007 |
| Colores pista azul | Interior amarillo, exterior verde flúor, límites/indicador naranja | D-008, #5 (por confirmar) |
| Colores pista roja | Amarillo, verde flúor, azul | D-008 |
| Altura de cadera para proyectar | ≈ 1 m | D-006 |
| Ventana de velocidad | 0,3–0,5 s o por zancada | #23 |
| Pie por defecto | 30 cm | D-009 |
| Error de reproyección admisible | «unos cm» (umbral por fijar) | #10 |

## 5. Preguntas abiertas

- ¿El verde flúor se distingue bien sobre la pista azul? Si no, rosa/magenta (#5).
- Umbral concreto de error de reproyección para avisar (#10).
- ¿Los vídeos HEVC 4K60 del iPhone se leen bien con OpenCV en Windows? Comprobar con
  `relevos info` en la primera sesión (#7).

## 6. Bitácora

- **2026-10-20** — F1 completa: esqueleto, CI, hooks, plantillas, `relevos info`. Protocolo de
  grabación (#6). Se descarta la hoja de registro (D-001).
- **2026-11-01** — Se crea este documento y se añaden las skills de antislop (#41, D-013).
  Pestaña «Disponibilidad» en el Project y Action que la mantiene (#43, D-014).
