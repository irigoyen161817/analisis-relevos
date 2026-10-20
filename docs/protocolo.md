# Protocolo de grabación

Cómo grabar las entregas del 4x100 para que `relevos` las pueda analizar. La idea es que solo
tengas que **preparar la pista y grabar**: no hace falta rellenar ninguna hoja. Todo lo demás
(sentido de carrera, resultado de la entrega, marca usada, si la cámara se ha movido) se saca
del propio vídeo.

Cada regla de este protocolo tiene un motivo: si se salta, alguna medida deja de ser fiable.

## 1. Resumen

- Una cámara **fija** (iPhone en trípode) grabando a **60 fps**.
- Una **rejilla de 21 platillos** sobre la pista, que **se queda puesta toda la sesión**. Es lo que
  permite pasar de píxeles a metros.
- **Un vídeo por intento**, que empieza con la pista vacía durante 1–2 s.

## 2. Material

| Material | Notas |
|---|---|
| iPhone | Batería cargada y espacio libre (ver [ajustes](#4-ajustes-del-iphone)) |
| Trípode firme | Con peso colgado si hace viento |
| Disparador remoto | Bluetooth o Apple Watch: grabar sin tocar el móvil |
| Cinta métrica de 50 m | Para colocar la rejilla |
| 21 platillos planos por zona | En tres colores (ver [rejilla](#5-colocación-de-la-rejilla)) |
| Batería externa | Grabar a 4K gasta mucha batería |

## 3. Roles

Con dos personas además de los atletas:

| Rol | Tareas |
|---|---|
| **Cámara** | Encuadre y ajustes del iPhone, grabar y parar con el disparador |
| **Pista** (ayudante) | Colocar y revisar los platillos, mover el indicador cuando cambia la marca, avisar a los atletas, vigilar que nadie entra en plano |

## 4. Ajustes del iPhone

Los nombres pueden variar un poco según la versión de iOS.

En **Ajustes → Cámara → Grabar vídeo**:

| Ajuste | Valor | Por qué |
|---|---|---|
| Resolución | **4K a 60 fps** (o 1080p a 60 fps si falta espacio) | 60 fps reducen a la mitad el error en la reacción frente a 30 fps |
| **FPS automáticos** | **Desactivado** | Si no, el iPhone baja a 30 fps cuando hay poca luz |
| **Estabilización mejorada** y **Modo Acción** | **Desactivados** | Recolocan la imagen aunque el móvil esté fijo, y eso rompe la calibración |
| **Vídeo HDR** | Desactivado | Evita problemas de color y de lectura del vídeo |
| **Bloquear cámara** | **Activado** | Impide que cambie de lente sola durante la grabación |

En **Ajustes → Cámara**:

- **Formatos → Alta eficiencia** (HEVC). El iPhone solo permite 4K a 60 fps con este formato.
  Si al pasar `relevos info` el vídeo no se lee bien, cambia a «Más compatible» y graba a 1080p 60 fps.
- **Control macro**: desactivado (cambiaría de lente al acercarse algo).
- **Conservar ajustes**: activado, para no tener que repetirlos cada vez.

En la app **Cámara**, antes del primer intento:

1. Modo **Vídeo**, lente **1x** (la principal; el 0,5x deforma las rectas).
2. Comprobar en la esquina que pone **4K · 60** (o **HD · 60**).
3. **Mantener pulsado** sobre la pista hasta que aparezca **Bloqueo AE/AF**: fija enfoque y exposición
   y evita que cambien al pasar los atletas.
4. Modo avión activado y brillo de pantalla bajo.

Espacio orientativo: 4K a 60 fps ocupa unos 400 MB por minuto. Una sesión de 30 intentos de 15 s
son unos 3 GB.

## 5. Colocación de la rejilla

Por cada zona, **21 platillos planos**: 10 en cada borde de la calle, cada 5 m desde 15 m antes
de la zona hasta su final, y un indicador de la marca de salida.

```
 sentido de carrera  ──────────────────────────────────────────────▶

 −15   −10    −5     0     5    10    15    20    25    30   (m)
                     │◀────────── zona de entrega (30 m) ──────────▶│
  ●     ●     ●     ◆     ●     ●     ●     ●     ●     ◆     fila exterior  (verde)
 ─────────────────────────────────────────────────────────────────  borde exterior de la calle
                         calle (1,22 m)
 ─────────────────────────────────────────────────────────────────  borde interior de la calle
  ○     ○     ○     ◆     ○     ○     ○     ○     ○     ◆     fila interior  (amarillo)

      ◆ indicador de marca: 30–50 cm por fuera de la fila exterior, a la altura de la cinta del atleta
 ○ amarillo   ● verde flúor   ◆ tercer color (límites de zona e indicador)
```

### Colores

Los colores dependen de la pista. Deben contrastar con la pista y entre sí, y nunca ser blancos
(se confunden con las líneas). Se configuran **una vez por pista**, no en cada sesión.

| Elemento | Pista azul | Pista roja |
|---|---|---|
| Fila interior | Amarillo | Amarillo |
| Fila exterior | Verde flúor | Verde flúor |
| Límites de zona (0 y 30 m) e indicador | Naranja | Azul |

Antes de comprar todos los platillos, comprueba los colores en tu pista (issue #5).

### Cómo colocarlos

1. Platillos **planos**, no conos altos: el programa usa la base como referencia.
2. **Sobre las líneas de la calle o justo por fuera**, nunca dentro, para que nadie los pise.
3. En **recta**: medir los 5 m con la cinta a lo largo de cada línea.
4. En **curva**: medir los 5 m **solo a lo largo de la línea interior** y poner cada platillo
   exterior **justo enfrente**, en perpendicular a la calle (como las líneas de la zona). Si se
   miden por separado, las filas se desalinean porque el borde exterior es más largo.
5. Los límites (0 y 30 m) deben coincidir con las líneas pintadas de la zona.
6. El **indicador de marca** se coloca cuando el receptor pone su cinta, y se mueve con ella. Así
   el programa mide la marca real usada sin que nadie la apunte.
7. **No quitar ni mover la rejilla durante la sesión**: es la referencia de todos los vídeos.

## 6. Encuadre

- Hay que cubrir unos **45 m**: los 15 m previos con la marca y los 30 m de la zona.
- Cámara **lo más alta posible**: la grada es lo ideal; como mínimo 2–3 m. Desde abajo, un píxel
  de error son muchos centímetros.
- **Por fuera** de la pista y **centrada** respecto a esos 45 m.
- En **horizontal**, con el **sol a la espalda o de lado**, nunca de frente.
- Deben verse **los 21 platillos con margen** en los bordes de la imagen.
- No hace falta medir la posición ni la altura de la cámara: las calcula el programa a partir de
  la rejilla.

## 7. Procedimiento

**Antes de empezar**

1. *Pista*: colocar la rejilla.
2. *Cámara*: montar el trípode, encuadrar y aplicar los ajustes del iPhone.

**Cada intento**

3. *Pista*: el receptor coloca su cinta y el ayudante pone el indicador a su altura.
4. *Cámara*: empezar a grabar con la **pista vacía**, al menos **1–2 s antes de que aparezca el que
   llega**. Esos primeros fotogramas son los que usa el programa para calibrar y para comprobar que
   la cámara no se ha movido.
5. Parar cuando **los dos han salido de la zona**.
6. *Pista*: revisar que ningún platillo se ha movido. Si alguno se ha movido, recolocarlo en su sitio.

**Si cambia la marca**: el ayudante mueve el indicador con la cinta. No hace falta apuntar nada.

## 8. Después de la sesión

1. **Pasar los vídeos al ordenador sin recomprimir**: por cable USB, con
   *Ajustes → Fotos → Transferir a Mac o PC → Mantener originales*. **Nunca** por WhatsApp,
   Telegram o similares: recomprimen el vídeo y pueden cambiar los fps.
2. Guardar los vídeos de cada sesión en una carpeta (la carpeta `data/` no se sube al repositorio):

   ```
   data/
     sesiones/
       2026-10-25/
         IMG_1202.MOV
         IMG_1203.MOV
         ...
   ```

3. Comprobar un vídeo:

   ```bash
   relevos info data/sesiones/2026-10-25/IMG_1202.MOV
   ```

   Debe dar unos **60 fps reales** y ningún aviso de frecuencia variable.

### Opcional: atletas

Para ver el historial de cada pareja y que la recomendación de la marca aprenda con cada intento,
el programa necesita saber quién corre en cada vídeo; eso no se puede sacar del vídeo. Es opcional:
sin ello, cada vídeo se evalúa igual, solo que por separado.

- Se indica la pareja al analizar el vídeo (por ejemplo, `--pareja ATL1-ATL2`).
- Para dar la marca en **pies** del atleta, apunta una vez la longitud de su pie en
  `data/atletas.csv` ([plantilla](plantillas/atletas.csv)). Sin ella, la marca se da en metros y en
  pies de 30 cm.

  ```csv
  alias,pie_cm,notas
  ATL1,28.5,
  ATL2,27.0,
  ```

## 9. Errores a evitar

- Que alguien se ponga **delante de la cámara** o dentro del plano en la calle, incluido el entrenador.
- Empezar a grabar **con el atleta ya en el plano**: el vídeo no tendrá fotogramas con la pista vacía.
- **Platillos desplazados** por pisadas: revisarlos entre intentos.
- **Tocar el móvil** entre vídeos: usar siempre el disparador.
- Grabar con **poca luz** o a **contraluz**.
- Dejar activados los **FPS automáticos** o la **estabilización**.
- Pasar los vídeos por **mensajería**.

## 10. Privacidad

- En el repositorio solo hay plantillas vacías y ejemplos con **alias** (ATL1, ATL2…).
- Los vídeos y, si se usan, los nombres reales se guardan solo en `data/`, que no se sube.
- Si hay **menores**, hay que tener el consentimiento de sus padres o tutores para grabarlos.
