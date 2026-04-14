# Knowledge Brain

Un sistema personal de conocimiento con IA que crece contigo. Funciona con [Claude Code](https://claude.ai/claude-code).

Agregas material crudo — cursos, artículos, PDFs, ideas. Claude lo lee, lo destila en páginas wiki atómicas, las conecta entre sí, y mantiene todo indexado. Cada sesión hace el sistema más inteligente.

> [English version](README_EN.md)

## El Hemingway Bridge

El problema #1 del trabajo con IA: **pierdes contexto entre sesiones.** Cada chat nuevo empieza desde cero. Vuelves a explicar tu proyecto, tus preferencias, y pierdes los primeros 10 minutos orientándote.

Este framework lo resuelve con el **Hemingway Bridge** — un sistema de continuidad inspirado en el hábito de Hemingway de dejar una frase a medias para saber exactamente dónde retomar al día siguiente.

```
/bridge-out   ← Fin de sesión: captura dónde paraste,
                decisiones tomadas, y la siguiente acción exacta

/bridge       ← Inicio de sesión: lee la nota del bridge,
                te orienta en menos de 60 segundos
```

**El resultado:** cada sesión continúa exactamente donde terminó la anterior. Sin volver a explicar. Sin perder contexto. Tu asistente de IA tiene continuidad total entre sesiones.

## Cómo funciona

Es un **sistema de conocimiento en tres capas** mantenido por Claude Code:

| Capa | Ubicación | Propósito |
|---|---|---|
| Capa 1 — Fuentes | `/sources` | Material crudo inmutable (cursos, artículos, PDFs) |
| Capa 2 — Wiki | `/wiki` | Páginas atómicas sintetizadas — el "cerebro" real |
| Capa 3 — Schema | `.claude/` + `CLAUDE.md` | Reglas que gobiernan cómo se comporta el sistema |

Tú agregas material crudo. Claude lo lee, lo destila en páginas wiki, las conecta, y mantiene el índice actualizado.

```
                         +--------------+
                         |  inbox/      |
                         |  INBOX.md    |  zona de captura
                         |  drop/       |  (texto + archivos)
                         +------+-------+
                                |
                                v
+-------------+     /ingest      +-------------+   consultado    +-------------+
|   FUENTES   | ----------------> |    WIKI      | <------------ |  PROYECTOS  |
|  (Capa 1)   |  leer y destilar |  (Capa 2)    | herramientas  |  (Capa 3)   |
|  inmutable  |                  |  pág. atómicas|   y refs      |  ejecución  |
|  + inbox/   |                  +-------------+                |  + inbox/   |
+-------------+                        ^                        +-------------+
  inbox de curso                  index.md                      inbox de proyecto
  auto-etiquetado               catálogo maestro                auto-etiquetado

                    +----------------------------------+
                    |         .claude/ (SCHEMA)         |
                    |  rules - commands - hooks - skills |
                    |     gobierna las tres capas        |
                    +----------------------------------+
```

## Inicio rápido (5 minutos)

### Requisitos

| Herramienta | Requerido | Para qué |
|---|---|---|
| [Claude Code](https://claude.ai/claude-code) | Sí | Interfaz principal — lee, escribe y mantiene tu base de conocimiento |
| [Plan Pro de Claude](https://claude.ai/pricing) | Sí | Claude Code requiere suscripción Pro ($20/mes) |
| [Git](https://git-scm.com/) | Sí | Control de versiones y red de seguridad |
| [Node.js](https://nodejs.org/) | Sí | Necesario para instalar Claude Code (`npm install -g @anthropic-ai/claude-code`) |
| [Obsidian](https://obsidian.md/) | Opcional | Interfaz visual para navegar las páginas wiki |

### Instalación

```bash
# 1. Crea tu Knowledge Brain desde este template
#    (click "Use this template" en GitHub, o clona directamente)
git clone <url-de-tu-repo> mi-cerebro
cd mi-cerebro

# 2. Instala el hook de pre-commit (valida links + frontmatter en cada commit)
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/sh
ROOT="$(git rev-parse --show-toplevel)"
python3 "$ROOT/.claude/hooks/validate-links.py" || exit 1
python3 "$ROOT/.claude/hooks/validate-frontmatter.py" --staged
HOOK
chmod +x .git/hooks/pre-commit

# 3. Personaliza CLAUDE.md
#    Abre CLAUDE.md y llena las secciones [Owner] y [Active Priorities]

# 4. Abre Claude Code
claude

# 5. Empieza tu primera sesión
/bridge
```

Eso es todo. Claude lee `CLAUDE.md` y `.claude/rules/` automáticamente.

## Los cuatro hábitos

Construye estos cuatro hábitos y el sistema crece solo:

| Hábito | Cuándo | Comando | Qué pasa |
|---|---|---|---|
| **Capturar** | Cuando encuentres algo útil | Agregarlo en `inbox/` | Sin fricción — solo tíralo ahí |
| **Ingerir** | Cuando el inbox tenga items | `/ingest` | Claude lee, destila, crea páginas wiki, indexa |
| **Bridge** | Inicio y fin de cada sesión | `/bridge` + `/bridge-out` | Continuidad total de contexto entre sesiones |
| **Lint** | Una vez al mes | `/lint` | Revisión de salud — encuentra huérfanos, deuda, gaps |

## Comandos

| Comando | Qué hace |
|---|---|
| `/bridge` | **Inicio de sesión.** Lee el log, la memoria y el índice. Te orienta en 60 segundos. |
| `/bridge-out` | **Fin de sesión.** Crea un Hemingway Bridge — captura dónde paraste y la siguiente acción exacta. |
| `/ingest` | **Procesa todos los inboxes.** Escanea inboxes global, de cursos y de proyectos. Crea páginas wiki. Actualiza el índice. |
| `/lint` | **Revisión de salud mensual.** Encuentra páginas huérfanas, deuda de destilación, contenido desactualizado, links rotos. |
| `/query` | **Consulta al knowledge base.** Haz una pregunta, busca en el wiki, sintetiza una respuesta. |
| `/safe-change` | **Workflow de branch.** Crea una rama, hace cambios, muestra resumen, mergea con tu aprobación. |

## Estructura de carpetas

```
mi-cerebro/
+-- inbox/           Zona de captura
|   +-- INBOX.md     Entradas de texto (URLs, ideas, notas rápidas)
|   +-- drop/        Agrega archivos aquí (PDFs, artículos, transcripciones)
|   +-- processed/   Los archivos se mueven aquí después del ingest
+-- sources/         Material crudo inmutable
|   +-- courses/     Carpetas de cursos (estructura estándar)
|       +-- notes/       Notas de lecciones, resúmenes de módulos
|       +-- assignments/ Tareas y ejercicios
|       +-- resources/   Material de referencia, cheat sheets
|       +-- inbox/       Inbox específico del curso para ingest
+-- wiki/            Conocimiento sintetizado — el cerebro
|   +-- areas/       Áreas de enfoque continuas
|   +-- concepts/    Páginas de conceptos atómicos
|   +-- tools/       Catálogo de herramientas y tutoriales
|   +-- playbooks/   Workflows paso a paso
|   +-- decisions/   Decisiones de arquitectura y estrategia
|   +-- references/  Documentos de referencia y guías
+-- projects/        Ejecución de proyectos activos (estructura estándar)
|   +-- references/  Briefs, contexto de marca, investigación
|   +-- prompts/     Prompts específicos del proyecto
|   +-- content/     Guiones, borradores, planes de campaña
|   +-- assets/      Imágenes, videos, media generada
|   +-- inbox/       Inbox específico del proyecto para ingest
+-- output/          Resultados de queries, reportes de lint, notas de sesión
|   +-- sessions/    Notas de sesión del Hemingway Bridge
+-- archive/         Documentos reemplazados
+-- .claude/         Schema del sistema (Capa 3)
|   +-- commands/    Slash commands (/bridge, /ingest, /lint, etc.)
|   +-- rules/       Reglas operacionales (frontmatter, links, idioma)
|   +-- hooks/       Scripts de validación (frontmatter, links, índice)
|   +-- templates/   Templates para nuevos archivos
+-- index.md         Catálogo maestro — Claude busca aquí para encontrar todo
+-- log.md           Log cronológico de operaciones (solo se agrega, nunca se edita)
+-- TODO.md          Índice maestro de tareas — apunta a TODOs por área/proyecto
+-- CLAUDE.md        Schema raíz — gobierna todo el comportamiento de Claude
```

## Sistema de TODOs

Las tareas se organizan en una jerarquía de archivos TODO.md:

```
TODO.md (raíz)              ← Índice maestro: solo links y conteos
  +-- projects/*/TODO.md    ← Tareas por proyecto
  +-- sources/courses/*/TODO.md  ← Progreso por curso
  +-- wiki/TODO.md          ← Tareas generales del wiki
```

- **TODO.md raíz** solo contiene punteros y resúmenes de estado — nunca tareas directas
- **Cada área tiene su propio TODO.md** con secciones: Blocked, In Progress, Backlog, Done
- `/bridge` lee los TODOs activos al inicio de cada sesión
- `/bridge-out` actualiza los TODOs y recuenta el índice al final de cada sesión
- La sección Done solo guarda los últimos 30 días
- Las secciones vacías se omiten — si no hay nada bloqueado, no aparece Blocked

### Ejemplo — TODO de proyecto

```md
# TODO — Mi Proyecto

## In Progress
- [ ] Escribir primer guión de video — since: 2026-04-12

## Backlog
- [ ] Definir estructura de contenido
- [ ] Crear prompts específicos del proyecto

## Done (last 30 days)
- [x] Definir brief del proyecto — 2026-04-10
```

### Ejemplo — TODO raíz

```md
## Projects
- [mi-proyecto](projects/mi-proyecto/TODO.md)
  status: 1 in progress, 2 backlog

## Courses
- [mi-curso](sources/courses/mi-curso/TODO.md)
  status: 1 backlog
```

### Agregar un nuevo proyecto o curso

Cuando crees un nuevo proyecto o curso, también crea un `TODO.md` dentro de la carpeta siguiendo el mismo formato. Agrega una línea al `TODO.md` raíz — `/bridge-out` mantiene los conteos automáticamente.

## Niveles de destilación

Cada página wiki lleva un seguimiento de qué tan procesado está su conocimiento:

| Nivel | Estado | Qué significa |
|---|---|---|
| 0 | Dump crudo | Recién capturado, sin procesar |
| 1 | Primera pasada | Leído, puntos clave identificados |
| 2 | Destilado | Contenido reescrito en tus propias palabras |
| 3 | Sintetizado | Conectado con otras páginas, implicaciones claras |
| 4 | Listo para crear | Puedes generar contenido directamente desde esta página |

Las páginas empiezan en nivel 1 (después del ingest) y suben con cada revisión. Una página nivel 4 es un activo — puedes generar un post, guión de video, o presentación directamente de ella.

## Agregar contenido

### Agregar conocimiento nuevo
Agrega el material en el inbox correcto — el contexto es automático:

| Qué tienes | Dónde ponerlo |
|---|---|
| Una idea rápida o URL | `inbox/INBOX.md` |
| Un PDF, artículo o transcripción | `inbox/drop/` |
| Material de un curso específico | `sources/courses/[curso]/inbox/` |
| Material de un proyecto específico | `projects/[proyecto]/inbox/` |

Luego ejecuta `/ingest`.

### Agregar un curso nuevo
1. Crea `sources/courses/[nombre-del-curso]/`
2. Agrega un `CLAUDE.md` describiendo el curso
3. Crea subcarpetas `inbox/` e `inbox/processed/`
4. Agrega los archivos del curso y ejecuta `/ingest`

### Agregar un proyecto nuevo
1. Crea `projects/[nombre-del-proyecto]/`
2. Agrega un `CLAUDE.md` describiendo el proyecto
3. Crea subcarpetas `references/`, `prompts/`, `inbox/` e `inbox/processed/`
4. Empieza a trabajar — Claude construye el brief del proyecto mientras avanzas

## Qué NO hacer

| Error | Por qué rompe cosas |
|---|---|
| Editar archivos en `/sources` | La Capa 1 es inmutable. Sintetiza en `/wiki` en su lugar. |
| Poner resultados de queries en `/projects` | `/projects` es para ejecución. Resultados de queries van a `/output`. |
| Usar wikilinks `[[así]]` | Solo funcionan en Obsidian. Usa `[texto](ruta/relativa.md)` en su lugar. |
| Crear un `.md` sin indexar | La regla de auto-indexado asegura que Claude encuentre todo via `index.md`. |
| Saltarse el frontmatter | Todo archivo `.md` (excepto CLAUDE.md/README.md) necesita frontmatter YAML. |
| Borrar archivos sin hacer commit primero | Git es tu red de seguridad. Commit, luego borra con confianza. |

## Comparación de funcionalidades

| Funcionalidad | Knowledge Brain | Notion | Obsidian solo | RAG / Vector DB |
|---|---|---|---|---|
| Continuidad de sesión (Hemingway Bridge) | Sí | No | No | No |
| La IA mantiene la wiki por ti | Sí | No | Parcial (plugins) | No |
| Funciona offline | Sí | No | Sí | Depende |
| Portable (markdown + git) | Sí | No | Sí | No |
| Seguimiento de destilación automático | Sí | No | Manual | No |
| Sistema de inbox distribuido | Sí | No | No | No |
| Validación de links pre-commit | Sí | No | No | No |
| Cero vendor lock-in | Sí | No | Casi | No |

## Construido con

- [Claude Code](https://claude.ai/claude-code) — Interfaz de IA que lee, escribe y mantiene la base de conocimiento
- [Git](https://git-scm.com/) — Control de versiones y red de seguridad
- Markdown — Universal, portable, legible por humanos
- Python — Hooks de validación ligeros

## Licencia

MIT
