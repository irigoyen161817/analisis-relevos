# Skills del proyecto

| Skill | Para qué |
|---|---|
| `antislop` | Núcleo: reglas contra el texto y el código con pinta de generados por IA, y el informe final (Delivery Gate) |
| `antislop-code` | Comentarios de código: quita los de relleno, conserva los útiles y no toca el código |
| `antislop-copywriting` | Textos (docs, issues, PRs): sin vocabulario vacío ni datos inventados |

Copiadas sin cambios de [miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop),
versión 3.2.25 (commit `941b153`), con licencia MIT ([LICENSE-antislop](LICENSE-antislop)).

No se incluyen `antislop-ui`, `antislop-human` ni `antislop-layoutmobile` porque el proyecto no
tiene interfaz web. Si algún día la tiene (p. ej. un visor en navegador), se añaden igual.

## Actualizar

Se copian a mano desde la versión que se quiera del repo de origen, sobrescribiendo estas
carpetas, y se actualiza la versión de arriba y `antislop/VERSION`. No usar `npx antislop-ai
--update`: instalaría también las skills de interfaz.

## Modo

El núcleo pregunta en cada sesión si se aplica *during* (mientras se trabaja) o *after* (auditar
lo que ya existe), salvo que haya una preferencia guardada en `%APPDATA%\antislop\settings.json`
(Windows) o `~/.config/antislop/settings.json`, p. ej. `{"mode":"during"}`. Ese fichero es de
cada ordenador, no del repo.
