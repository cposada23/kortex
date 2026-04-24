---
title: "Claude.ai Projects + GitHub sync — setup playbook"
type: playbook
layer: wiki
language: es
tags: [claude-ai, github-integration, playbook, project-knowledge, capa/2-wiki]
updated: 2026-04-24
status: active
distillation_level: 3
confidence: high
source_count: 3
last_verified: 2026-04-24
related_paths:
  - ../../.claude/rules/write-authority.md
---

# Claude.ai Projects + GitHub sync — setup playbook

Paso-a-paso para conectar un Claude.ai Project a un repositorio GitHub
como knowledge source. Portable — funciona para cualquier instancia
Kortex (o cualquier repo markdown-heavy).

**Lo que resuelve:** eliminar el copy-paste manual de archivos del repo
al Claude.ai Project knowledge. Cualquier edit en los archivos
seleccionados se refleja en el Project con 1 click "Sync now" en vez
de re-upload manual.

**Lo que NO resuelve:** write path de Claude.ai chat → GitHub. La
integración es **read-only** (confirmado en test 2026-04-24). Captures
de ideas generadas en mobile siguen requiriendo paso humano (paste a
`/inbox/` via GitHub web o via Claude Code next session).

**Steps validados con test físico contra sandbox dedicado 2026-04-24.**
Si la UI de Claude.ai cambia, las observaciones de este playbook pueden
quedar desactualizadas — verificá contra
[docs oficiales](https://support.claude.com/en/articles/10167454-using-the-github-integration)
antes de tratar los UI labels como autoritativos.

---

## Cuándo usar este playbook

- Tenés un repo Kortex (o similar) con proyectos + wiki + references.
- Mantenés Claude.ai Projects para pensar, planear, validar cross-AI.
- Hoy subís manualmente archivos al Project Knowledge y los re-subís
  cuando editás en el repo.
- Querés que ese re-upload sea automático (1 click sync).

## Cuándo NO usar

- Si esperás que Claude.ai commitee de vuelta al repo → no funciona.
  Usá Claude Code para writes.
- Si el repo es enorme (>500 archivos relevantes) sin curar selección —
  tokens por chat se inflan.

---

## Requisitos

- Cuenta Claude.ai activa (cualquier plan, incluido Free).
- Cuenta GitHub con acceso al repo.
- Si el repo es **privado**: leer Paso 3 sub-sección "Gotcha private
  repo" antes de empezar.

---

## Paso 1 — Preparar el repo

Confirmá que el repo tiene los archivos que necesitás como knowledge.
Típicamente:

- `README.md` del proyecto
- Briefs: `references/project-brief.md`, `channel-context.md`, etc.
- Playbooks específicos del proyecto
- Referencias del wiki que ese Project usa

Si el repo tiene carpetas grandes que NO querés sincronizar
(`output/`, `sources/courses/` con raw material, assets binarios) →
tenélas identificadas para excluirlas en Paso 3.

## Paso 2 — Crear el Claude.ai Project

1. En claude.ai (desktop browser), sidebar izquierda → **Projects** →
   **Create Project**.
2. Nombre: el del proyecto o dominio (ej. `Milo IA`, `Sistema QA`,
   `Content Hub`).
3. Descripción opcional — contexto alto-nivel.

> **Mobile:** Projects SE PUEDEN CREAR desde la app mobile, pero la
> conexión GitHub NO se puede hacer desde la app. Creá el Project
> desde desktop (o desde el navegador web del celular, no la app).

## Paso 3 — Conectar el repo GitHub

**Labels exactos dated 2026-04-24 (Claude.ai en inglés):**

1. Dentro del project, sección **Project Knowledge** → click **"+"**
   (esquina sup derecha). Dropdown muestra: **GitHub** · **Drive** ·
   **Upload from Device** · **Add Text Content**.
2. Click **GitHub**.
3. Si no auth'd: redirige a GitHub → autorizá el Claude GitHub App.

### Gotcha private repo (importante)

Autorizar el Claude GitHub App por primera vez **típicamente da
acceso solo a repos públicos**. El file picker lista solo repos
públicos del usuario. Para conectar un repo privado, **dos
workarounds**:

**Workaround A — pegar URL directa:**
- En el file picker, buscá el campo **Paste GitHub URL** (en vez del
  search).
- Pegá la URL completa del repo privado
  (ej. `https://github.com/<owner>/<repo>`).
- Claude te pide un paso extra de autorización específica para ese repo
  y lo carga.

**Workaround B — configurar el GitHub App manualmente:**
- Abrí `https://github.com/settings/installations`.
- Buscá "Claude" → click **Configure**.
- En "Repository access" → seleccionar **Only select repositories** o
  agregar repos específicos a la lista si ya tenés "Only select
  repositories".
- Agregá el repo privado → **Save**.
- Volvé a Claude.ai y el file picker ya lista el repo.

Ambos workarounds funcionan. A es más rápido, B es más explícito y
queda configurado para futuros Projects.

### File browser

Tras seleccionar el repo, aparece el file browser. **Características
observadas:**

- **No es tree expandible** — es navegación flat estilo Finder.
  Navegás entrando a carpetas.
- **Checkboxes por archivo Y por carpeta**, independientes. Marcar
  una carpeta selecciona todos sus hijos auto; podés desmarcar
  individuales después.
- **Search solo por nombre de archivo**, no por path. Si hay nombres
  duplicados, verificá el path mostrado debajo del search result.
- **Contador "X files selected"** visible.
- **No hay vista resumen pre-confirmación** — hay que navegar para
  verificar qué quedó marcado.
- **No hay glob patterns** — exclusión es manual, por archivo.

### Estrategia de selección — dos modelos

La pregunta previa es **cuántos Claude.ai Projects mantenés**, y la
respuesta define qué archivos selecciona cada uno.

**Modelo A — Claude.ai Projects generales (cross-cutting):**

Pocos Projects, cada uno cubre un dominio amplio que toca varios
proyectos Kortex. Ej: un único Project "Content Hub" que cubre Milo IA
+ Café Moreno + Sistema QA con briefs + playbooks compartidos.
Pros: menos mantenimiento, contexto transversal. Cons: más tokens
por chat.

**Modelo B — Claude.ai Project por proyecto Kortex (1-a-1):**

Un Project por cada folder de `projects/<nombre>/`. Cada uno
sincroniza estricto lo suyo. Pros: tokens mínimos por chat, contexto
focalizado. Cons: más Projects que mantener, sync más frecuente por
Project, conversaciones cross-proyecto requieren cambiar de Project.

**Regla general (ambos modelos):** seleccioná el mínimo que dé
contexto útil. Más archivos = más tokens por turno de chat.

### Ejemplos concretos

**Modelo A — "Content Hub" general:**

- `projects/milo-ia/references/` (briefs + brand + channel)
- `projects/cafe-moreno/references/` (si aplica — briefs de otro proyecto)
- `projects/<otros>/references/` cross-cutting
- `wiki/playbooks/cross-ai-validation.md`
- `wiki/playbooks/milo-ia-ideation-to-production.md`
- `wiki/concepts/strategy/FICHA_NICHO.md`
- `wiki/references/glossary.md`

**Modelo B — "Milo IA" per-project:**

- `projects/milo-ia/README.md`
- `projects/milo-ia/CLAUDE.md`
- `projects/milo-ia/TODO.md`
- `projects/milo-ia/INDEX.md`
- `projects/milo-ia/references/` (carpeta completa)
- `wiki/playbooks/milo-ia-ideation-to-production.md`
- `wiki/playbooks/cross-ai-validation.md`

### NO sincronizar (ambos modelos)

- `output/` — efímero, infla tokens sin valor.
- `sources/courses/` — raw course material, demasiado grande.
- `.claude/` — framework internals, no son contexto del proyecto.
  Excepción: si el Project necesita un rule específico (ej.
  `idea-frontmatter.md` para un Project que genera ideas), selec-
  cionar solo ese archivo.
- `node_modules/`, `.git/`, binarios — obvio.
- Assets en `assets/` salvo que el Project necesite leer metadata
  textual (rara vez).

4. Confirmar selección con botón **Add Files**.

## Paso 4 — Primer sync + verificación

1. En un chat nuevo del Project, pedí:
   ```
   Listame los archivos que tenés en conocimiento con su path relativo.
   ```
2. Verificá que la lista coincide con la selección del Paso 3.
3. Pedí contenido de 1-2 archivos específicos:
   ```
   Mostrame el README.md completo.
   ```
   Confirma que lee correctamente.

## Paso 5 — Cadence de sync

**Cuándo clickear "Sync now":**

- Después de cada merge a `main` que toque archivos seleccionados en
  el Project — el diff es visible en `git log --oneline` del repo.
- Antes de iniciar un chat importante donde vas a pedir síntesis o
  decisiones basadas en el estado actual del proyecto.

**Sync es MANUAL — no auto-refresh.** Confirmado en test 2026-04-24:
tras pushear un commit al repo, el chat del Project no ve el cambio
hasta que se clickea Sync explícitamente.

**Sync es PER-PROJECT.** Si un archivo está sincronizado en 3 Projects
distintos, cada Project requiere su propio Sync click después de un
cambio en el archivo.

**UI del Sync:** icono + label "Sync" (visible en el card del repo en
Project Knowledge). Al clickear, muestra mini loader dentro del card.
Tras loader, el nuevo contenido es accesible.

Workflow sugerido: **sync semanal** + manual on-demand cuando sabés
que editaste algo material.

## Paso 6 — Desde mobile

**Claude app mobile (iOS + Android) NO muestra GitHub como knowledge
source.** Menú "+" en la app mobile lista solo: Subir desde dispositivo
/ Tomar foto / Elegir imagen / Crear nuevo documento. Confirmado en
Android y iPad 2026-04-24.

**Para agregar o sincronizar GitHub knowledge desde mobile:**

1. Abrí Safari / Chrome del celular → claude.ai → login.
2. Projects → abrí tu Project.
3. Usá el "+" de Project Knowledge (en mobile web funciona igual que
   desktop).
4. El Sync button también está en mobile web.

**Una vez sincronizado:**

- La Claude app mobile SÍ puede leer el knowledge — al preguntar por
  contenido de un archivo sincronizado, Claude responde correctamente.
- La app es útil para conversar con el context, no para gestionar el
  context.

## Paso 7 — Workflow de captura mobile-to-repo (la brecha real)

Dado que GitHub sync es read-only, capturar una idea generada en mobile
al repo requiere paso humano. Dos workflows:

### Workflow A — GitHub web desde mobile

1. En Claude.ai mobile (web o app — chat funciona igual), pedí al
   Project que genere el archivo completo con frontmatter:
   ```
   Redactá el markdown completo de esta idea con frontmatter
   idea-schema listo para pegar a inbox/ del repo. Status inbox,
   target_channel [X], language es, updated [hoy].
   ```
2. Copia el output al clipboard.
3. Mobile browser → github.com → tu repo → carpeta `inbox/` →
   **Add file** → **Create new file** → nombre `<slug>.md` → pegá →
   commit directo a `main` o en branch nuevo.

### Workflow B — Claude Code next session

1. En Claude.ai mobile, generá el markdown como en A.
2. Copia al clipboard.
3. Próxima sesión Claude Code (desktop o IDE), pedí:
   ```
   Pegá esto en inbox/<slug>.md:
   [paste]
   ```
4. Claude Code valida frontmatter + commitea via `/safe-change` o
   inline.

**Recomendación:** usar **B** si la idea no es urgente (batch en
sesión Code, aprovecha hooks de validación). Usar **A** si la idea es
volátil y querés commitearla ya.

---

## Troubleshooting

- **Repo privado no aparece en file browser:** ver sección "Gotcha
  private repo" del Paso 3 — usar Workaround A (paste URL) o B
  (configurar GitHub App).
- **Sync no trae cambios pusheados:** esperá 30-60s y re-clickeá. Si
  sigue igual, verificá que efectivamente pusheaste al branch que
  Claude.ai lee (por defecto `main`).
- **Claude chat dice "no tengo acceso a X.md" después de sync:**
  verificá en el file browser que el archivo está marcado — los
  checkboxes son por archivo, easy miss.
- **Project come demasiados tokens por chat:** revisar la selección
  del Paso 3 — probablemente sincronizaste una carpeta grande sin
  querer. Desmarcá carpetas y dejá solo archivos específicos.
- **Mobile no tiene "+ GitHub" o Sync:** esperado — ver Paso 6, usar
  navegador móvil web en lugar de la app.

---

## Relación con write-authority.md

Este playbook **refuerza**, no contradice,
[.claude/rules/write-authority.md](../../.claude/rules/write-authority.md):

- Claude Code sigue siendo el único escritor estructural del repo.
- Claude.ai Projects ahora leen del repo vía sync nativo (era manual
  upload hasta ahora).
- El write path desde mobile/Claude.ai al repo sigue pasando por una
  mano humana (Workflow A) o por Claude Code (Workflow B).

No hay excepción al rule de write-authority — GitHub sync es una
mejora del READ channel, no una apertura del write channel.

---

## Sources

- [Using the GitHub Integration — Claude Help Center](https://support.claude.com/en/articles/10167454-using-the-github-integration) (last fetched 2026-04-24)
- [GitHub integration — Claude.ai Documentation](https://claude.com/docs/connectors/github) (last fetched 2026-04-24)
- Test físico en vivo 2026-04-24 — steps validados contra sandbox repo dedicado con proyecto ficticio + wiki genérico (8 archivos seleccionados en 5 carpetas distintas). Los 2 gotchas de repo privado + mobile apps documentados arriba fueron observados durante ese test.
