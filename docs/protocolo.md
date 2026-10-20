# Protocolo de grabación

Cómo grabar una sesión de entregas del 4x100 para que los vídeos se puedan analizar con
`relevos`. Cada regla tiene un motivo: si se salta, alguna medida deja de ser fiable.

Para llevar a pista: [hoja imprimible](hoja_imprimible.md). Plantillas para pasarla al
ordenador: [`plantillas/`](plantillas/).

## 1. Resumen

- Una cámara **fija** (iPhone en trípode) por zona, grabando a **60 fps**.
- Una **rejilla de 21 platillos** sobre la pista, que sirve para pasar de píxeles a metros.
- Al empezar y al acabar, unos segundos de **pista vacía** (vídeos de calibración).
- **Un vídeo por intento**, y una fila por intento en la hoja de registro.

## 2. Material

| Material | Notas |
|---|---|
| iPhone | Batería cargada y espacio libre (ver [ajustes](#4-ajustes-del-iphone)) |
| Trípode firme | Con peso colgado si hace viento |
| Disparador remoto | Bluetooth o Apple Watch: grabar sin tocar el móvil |
| Cinta métrica de 50 m | Para colocar la rejilla |
| 21 platillos planos por zona | En tres colores (ver [rejilla](#5-colocación-de-la-rejilla)) |
| Hoja de registro impresa y bolígrafo | [hoja_imprimible.md](hoja_imprimible.md) |
| Batería externa | Grabar a 4K gasta mucha batería |

## 3. Roles

La sesión está pensada para dos personas además de los atletas.

| Rol | Tareas |
|---|---|
| **Cámara y hoja** | Encuadre y ajustes del iPhone, grabar y parar con el disparador, apuntar cada intento |
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

En la app **Cámara**, antes del vídeo de calibración:

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
(se confunden con las líneas).

| Elemento | Pista azul | Pista roja |
|---|---|---|
| Fila interior | Amarillo | Amarillo |
| Fila exterior | Verde flúor | Verde flúor |
| Límites de zona (0 y 30 m) e indicador | Naranja | Azul |

Antes de comprar todos los platillos, comprueba los colores en tu pista (issue #5).
Apunta los colores usados en la hoja de la sesión.

### Cómo colocarlos

1. Platillos **planos**, no conos altos: el programa usa la base como referencia.
2. **Sobre las líneas de la calle o justo por fuera**, nunca dentro, para que nadie los pise.
3. En **recta**: medir los 5 m con la cinta a lo largo de cada línea.
4. En **curva**: medir los 5 m **solo a lo largo de la línea interior** y poner cada platillo
   exterior **justo enfrente**, en perpendicular a la calle (como las líneas de la zona). Si se
   miden por separado, las filas se desalinean porque el borde exterior es más largo.
5. Los límites (0 y 30 m) deben coincidir con las líneas pintadas de la zona. Si no coinciden,
   manda lo pintado: apúntalo en las notas.
6. El **indicador de marca** se coloca cuando el receptor pone su cinta, y se mueve con ella.

## 6. Encuadre

- Hay que cubrir unos **45 m**: los 15 m previos con la marca y los 30 m de la zona.
- Cámara **lo más alta posible**: la grada es lo ideal; como mínimo 2–3 m. Desde abajo, un píxel
  de error son muchos centímetros.
- **Por fuera** de la pista y **centrada** respecto a esos 45 m.
- En **horizontal**, con el **sol a la espalda o de lado**, nunca de frente.
- Deben verse **los 21 platillos con margen** en los bordes de la imagen.
- No hace falta medir la posición ni la altura de la cámara: las calcula el programa a partir de
  la rejilla. Si quieres repetir el encuadre otro día, describe en las notas dónde estaba el trípode
  (por ejemplo, «grada, fila 3, a la altura de la salida del 200»).

## 7. Procedimiento de la sesión

**Antes de empezar**

1. *Cámara y hoja*: rellenar la cabecera de la sesión (fecha, pista, calle, zona, tipo de zona,
   sentido de carrera en la imagen, colores).
2. *Cámara y hoja*: medir el pie de los atletas nuevos (en cm, del talón a la punta, descalzos o
   con la zapatilla con la que miden la marca) y apuntarlo en la lista de atletas.
3. *Pista*: colocar la rejilla.
4. *Cámara y hoja*: montar el trípode, encuadrar y aplicar los ajustes del iPhone.

**Calibración inicial**

5. Comprobar que la pista está **vacía** en todo el plano.
6. Grabar **5–10 s** sin tocar nada. Apuntar el nombre del fichero (por ejemplo `IMG_1201`) como
   `video_calibracion_inicio`.

**Cada intento**

7. *Pista*: el receptor coloca su cinta y el ayudante pone el indicador a su altura.
8. *Cámara y hoja*: empezar a grabar **antes de que aparezca el que llega** en el plano.
9. Parar cuando **los dos han salido de la zona**.
10. *Cámara y hoja*: apuntar la fila: nº de intento, fichero, pareja, marca en pies, grabación y
    resultado.
11. *Pista*: revisar que ningún platillo se ha movido. Si alguno se ha movido, recolocarlo y anotarlo.
12. **Cada 5 intentos**, comprobar en el iPhone que el número del último fichero coincide con la hoja.

**Si cambia la marca**: el ayudante mueve el indicador con la cinta y en la hoja se apuntan los
nuevos pies.

**Al terminar**

13. Grabar otros **5 s con la pista vacía** y apuntarlo como `video_calibracion_fin`. Sirve para
    comprobar que la cámara no se ha movido durante la sesión.

### Grabación y resultado

En cada intento se apuntan dos cosas distintas:

- **Grabación**: `ok` o `problema` (con el motivo: «tapado», «cámara movida», «cortado», «platillo
  movido»…). **Solo se excluyen del análisis los intentos con problema de grabación.**
- **Resultado**, a ojo: `bueno`, `receptor_tarde`, `receptor_pronto`, `no_alcanza`,
  `testigo_caido` o `fuera_zona`. **Todos se analizan**, también los fallidos: suelen ser los que
  más dicen sobre dónde poner la marca.

## 8. Después de la sesión

1. **Pasar los vídeos al ordenador sin recomprimir**: por cable USB, con
   *Ajustes → Fotos → Transferir a Mac o PC → Mantener originales*. **Nunca** por WhatsApp,
   Telegram o similares: recomprimen el vídeo y pueden cambiar los fps.
2. Guardarlos con esta estructura (la carpeta `data/` no se sube al repositorio):

   ```
   data/
     atletas.csv
     sesiones/
       2026-10-25_zona2/
         sesion.csv
         intentos.csv
         IMG_1201.MOV
         IMG_1202.MOV
         ...
   ```

3. Comprobar los vídeos de calibración y un intento:

   ```bash
   relevos info data/sesiones/2026-10-25_zona2/IMG_1201.MOV
   ```

   Deben dar unos **60 fps reales** y ningún aviso de frecuencia variable.
4. Pasar la hoja de papel a los CSV de las [plantillas](plantillas/).

### Ejemplo de hoja rellena

`sesion.csv`

```csv
fecha,hora_inicio,pista,color_pista,calle,zona,tipo_zona,sentido,color_interior,color_exterior,color_limites,video_calibracion_inicio,video_calibracion_fin,condiciones,notas
2026-10-25,17:30,Pista municipal,azul,5,2,mixta,izq-der,amarillo,verde,naranja,IMG_1201,IMG_1240,"nublado, viento flojo de cara","trípode en la grada, fila 3"
```

`atletas.csv`

```csv
alias,pie_cm,notas
ATL1,28.5,
ATL2,27.0,
```

`intentos.csv`

```csv
intento,fichero,hora,llega,recibe,marca_pies,grabacion,motivo_grabacion,resultado,notas
1,IMG_1202,17:42,ATL1,ATL2,28,ok,,bueno,
2,IMG_1203,17:46,ATL1,ATL2,28,ok,,receptor_tarde,grita tarde
3,IMG_1204,17:50,ATL1,ATL2,29,problema,tapado,no_alcanza,el entrenador se cruzó
```

## 9. Errores a evitar

- Que alguien se ponga **delante de la cámara** o dentro del plano en la calle, incluido el entrenador.
- **Platillos desplazados** por pisadas: revisarlos entre intentos.
- **Tocar el móvil** entre vídeos: usar siempre el disparador.
- Grabar con **poca luz** o a **contraluz**.
- Dejar activados los **FPS automáticos** o la **estabilización**.
- Pasar los vídeos por **mensajería**.

## 10. Privacidad

- En el repositorio solo hay plantillas vacías y ejemplos con **alias** (ATL1, ATL2…).
- Los vídeos y, si se usan, los nombres reales se guardan solo en `data/`, que no se sube.
- Si hay **menores**, hay que tener el consentimiento de sus padres o tutores para grabarlos.
