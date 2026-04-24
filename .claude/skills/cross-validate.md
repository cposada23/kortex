---
scope: framework
---

# /cross-validate — Multi-LLM Cross-Validation

Automatiza el flow completo del playbook
[wiki/playbooks/cross-ai-validation.md](../../wiki/playbooks/cross-ai-validation.md)
desde Claude Code: extrae riesgos del input, genera 4 prompts
role-specialized, los manda a 4 validators en paralelo
(OpenAI / Gemini / Perplexity / Claude Opus nativo), recoge raws,
sintetiza summary con 6 secciones, y appendea cost log.

**Reemplaza el flow manual de 4+ copy-pastes** (pegar station en
Claude.ai → recibir 4 prompts → pegar c/u en su servicio → traer
4 verdicts → síntesis) **por una sola invocación.**

## When to use

Mismo criterio que el playbook §"When to use this":

- **Yes:** decisiones brand/positioning, copy multi-surface, arquitectura
  con blast radius alto, content pieces antes de pasar de borrador a
  producción, decisions del wiki, scripts de venta de productos.
- **No:** copy de borrador, thumbnails, decisions con 5-min revert.

## Invocation

```bash
# Default — 4 validators con modelos Pro
/cross-validate <path-to-input-file>

# Específicos — sólo los validators cuyo flag pasés (Claude Opus siempre corre)
/cross-validate <file> --gemini-model gemini-2.5-flash
  → corre SOLO Gemini Flash + Claude Opus

/cross-validate <file> --openai-model gpt-5.4 --gemini-model gemini-3.1-pro
  → corre OpenAI Pro + Gemini Pro + Claude Opus (sin Perplexity)

# Menú interactivo per-proveedor (override total)
/cross-validate <file> --ask-model
```

### Reglas de flags

- **0 flags** → defaults Pro de los 3 externos: `gpt-5.4`,
  `gemini-3.1-pro`, `perplexity/sonar-pro` + Claude Opus nativo.
- **1+ flags** → solo los proveedores nombrados + Claude Opus siempre.
  (Filtro, no aditivo.)
- **`--ask-model`** → menú interactivo: pregunta per proveedor
  (Pro / barato / skip).
- **Claude Opus 4.7 nativo SIEMPRE corre** — gratis vía Max 5x, además
  es el sintetizador que produce `summary.md`.

### Modelos válidos

Cada flag se valida contra la sección "Modelos disponibles — enum"
del playbook del proveedor:

- `--openai-model` → enum en
  [wiki/playbooks/api-onboarding/openai.md](../../wiki/playbooks/api-onboarding/openai.md)
- `--gemini-model` → enum en
  [wiki/playbooks/api-onboarding/google-gemini.md](../../wiki/playbooks/api-onboarding/google-gemini.md)
- `--perplexity-model` → enum en
  [wiki/playbooks/api-onboarding/openrouter.md](../../wiki/playbooks/api-onboarding/openrouter.md)

Si pasás un modelo que no está en el enum, el skill aborta con el listado
de valores válidos.

## Inputs aceptados (V1)

`<path-to-input-file>` debe ser un archivo `.md` con frontmatter válido
(`title`, `type`, `language`, `tags`). V1 acepta SOLO archivos, no
folders. Casos de uso típicos:

| Tipo input | Ejemplo path |
|---|---|
| Content piece antes de producción | `projects/<your-project>/content/<slug>.md` |
| Decision page del wiki | `wiki/decisions/<topic>.md` |
| Script o copy de venta | `projects/<your-product>/content/<doc>.md` |
| Idea triada de un bank | `projects/<your-project>/inbox/processed/<idea>.md` |

V2 (futuro) puede soportar folders con auto-discovery de archivos
relacionados. No en este safe-change.

## Output structure

Todos los outputs viven al lado del input file, en
`<input-dir>/cross-validations/YYYY-MM-DD/`:

```
<input-dir>/
├── <input-file>.md               ← input (no se toca)
└── cross-validations/
    └── YYYY-MM-DD/                ← una corrida = un folder por fecha
        ├── risks.md               ← pre-pass Opus: 5-8 risks + asignación a validators
        ├── prompts/               ← lo que se mandó (con role-specialization)
        │   ├── chatgpt-prompt.md
        │   ├── gemini-prompt.md
        │   ├── perplexity-prompt.md
        │   └── claude-prompt.md
        ├── chatgpt-raw.md         ← respuestas crudas
        ├── gemini-raw.md
        ├── perplexity-raw.md
        ├── claude-raw.md          ← Opus como validator (llamada 1, separada de la síntesis)
        └── summary.md             ← Opus como sintetizador (llamada 2 — 6 secciones)
```

Si por alguna razón hay 2 corridas el mismo día sobre el mismo input,
el segundo folder es `YYYY-MM-DD-2`, tercero `YYYY-MM-DD-3`, etc.

**Cost log es global**, no co-located. Vive en
[output/costs/cross-validate-log.md](../../output/costs/cross-validate-log.md).

## Procedure (orden de ejecución)

Claude Code sigue estos pasos al invocar `/cross-validate`. Los pasos
están numerados — cada uno termina antes de empezar el siguiente,
excepto el grupo paralelo del Paso 6 (los 4 validators corren en
paralelo).

### Paso 0 — Validar invocación

1. Verificar que `<file>` existe y termina en `.md`. Si no, abortar
   con mensaje claro.
2. Leer frontmatter del archivo. Verificar campos básicos (`title`,
   `type`, `language`). Si falta alguno, advertir pero continuar — el
   skill funciona aunque el frontmatter esté incompleto.
3. Parsear flags. Validar cada model flag contra el enum del playbook
   correspondiente. Si un valor es inválido, abortar con la lista de
   valores válidos.
4. Determinar set de validators activos:
   - Si 0 flags → `[openai, gemini, perplexity, claude]` con defaults Pro.
   - Si 1+ flags → solo los proveedores nombrados + `claude` siempre.
   - Si `--ask-model` → menú interactivo per proveedor.

### Paso 1 — Verificar API keys disponibles

Para cada validator activo (excepto `claude`):
- `openai` → require `$OPENAI_API_KEY`
- `gemini` → require `$GEMINI_API_KEY`
- `perplexity` → require `$OPENROUTER_API_KEY` (Perplexity vía OpenRouter)

Si falta una key requerida, abortar con el playbook de onboarding
del proveedor (`wiki/playbooks/api-onboarding/<provider>.md`).

### Paso 2 — Estimar costo y chequear MTD cap

1. Contar tokens del input file (rough heuristic: ~chars/4 ≈ tokens).
   Llamar `input_tokens`.
2. Estimar `output_tokens` por validator: ~2k para verdicts típicos.
3. Estimar costo per validator usando pricing del playbook del
   proveedor (en `## Pricing` o `## Modelos disponibles — enum`):
   - OpenAI gpt-5.4: $2.50/$20 per 1M tokens (in/out)
   - Gemini 3.1 Pro: $2.00/$12 per 1M tokens
   - Perplexity Sonar Pro vía OpenRouter: ~$3/$15 per 1M tokens
     (passthrough + 5.5% fee solo en compras de crédito)
   - Claude Opus nativo: $0.00 (Max 5x)
4. Sumar `total_estimated`.
5. Leer
   [output/costs/cross-validate-log.md](../../output/costs/cross-validate-log.md).
   Filtrar filas del mes en curso (`date` empieza con `YYYY-MM`).
   Filtrar filas con `vendor != TOTAL`. Sumar `cost_usd`. Llamar `mtd`.
6. Si `mtd + total_estimated > 10.00`, **abortar** con mensaje claro:
   ```
   Cap mensual alcanzado.
   MTD actual: $X.XX
   Esta corrida hubiera costado: $Y.YY adicionales
   Cap: $10.00

   Opciones:
   - Esperá al próximo mes
   - Corré manualmente (pegar prompts en chats web)
   - Reducí el set de validators con flags (--gemini-model gemini-2.5-flash es free)
   ```
7. Si OK, mostrar al usuario:
   ```
   File: <path>
     ✓ frontmatter válido (type: <type>, lang: <lang>)

   Validators activos:
     - openai <model> ($X.XX estimado)
     - gemini <model> ($X.XX estimado)
     - perplexity <model> ($X.XX estimado)
     - claude opus-4.7-native ($0.00)

   Total estimado: $X.XX
   MTD actual: $X.XX / $10.00
   Después de esta corrida: $X.XX / $10.00

   Output destination:
     <input-dir>/cross-validations/<date>/

   Procedo? (y/n)
   ```
8. Si `n`, abortar sin escribir nada.

### Paso 3 — Pre-pass Opus: extraer risks + asignar a validators

1. Crear el output folder: `<input-dir>/cross-validations/<date>/`
   (si ya existe del mismo día, usar `<date>-2`, `<date>-3`, etc.).
2. Crear subfolder `prompts/` adentro.
3. Llamar a Opus 4.7 nativo (este mismo Code) con un prompt que pida:
   - Leer el contenido del input file.
   - Extraer 5-8 "risks to challenge" específicos al input (mismo
     pattern que §3 del station format del playbook
     `cross-ai-validation.md`).
   - Asignar cada risk a 1-2 validators según sus lenses:
     - openai (Brand Strategy Challenger): audience, hook, positioning
     - gemini (Designer-Critic): scope coherence, visual hierarchy,
       executability
     - perplexity (Competitive Intel): saturación del tema,
       claims factuales verificables
     - claude (Repo-Context Coherence): coherencia con framework,
       overlap con otros archivos del repo, contradicción con decisions
4. Escribir el output a
   `<input-dir>/cross-validations/<date>/risks.md` con frontmatter
   (`type: reference`, `tags: [cross-validate, risks, capa/4-output]`)
   + body con 2 secciones:
   - §1 Riesgos identificados (5-8 numerados)
   - §2 Asignación a validators (matriz risk → validators)

### Paso 4 — Generar los 4 prompts (template fill)

1. Leer los 4 templates de `.claude/skills/cross-validate/templates/`:
   - `chatgpt-prompt-template.md`
   - `gemini-prompt-template.md`
   - `perplexity-prompt-template.md`
   - `claude-prompt-template.md`
2. Para cada template, sustituir placeholders:
   - `{{INPUT_PATH}}` → path absoluto al input file
   - `{{INPUT_TYPE}}` → valor de `type` del frontmatter
   - `{{INPUT_LANG}}` → valor de `language` del frontmatter
   - `{{INPUT_CONTENT}}` → contenido completo del input file (incluido
     el frontmatter)
   - `{{RISKS_FOR_THIS_VALIDATOR}}` → subset de risks de `risks.md`
     asignados a este validator (formato: lista numerada con un par
     de líneas de descripción cada uno)
   - `{{INVOCATION_DATE}}` → fecha de la corrida
3. Escribir cada prompt final a
   `<input-dir>/cross-validations/<date>/prompts/<vendor>-prompt.md`.

### Paso 5 — Mandar 4 calls en paralelo

Para cada validator activo, lanzar el call. Los 3 externos via `curl`
en background (`&` + `wait`); Opus directo (en este mismo Code).

#### OpenAI (gpt-5.4 default)

```bash
curl -s https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.4",
    "messages": [{"role": "user", "content": <PROMPT_BODY>}],
    "max_completion_tokens": 4096
  }'
```

Parsear respuesta JSON: `choices[0].message.content` → body del raw,
`usage.prompt_tokens` → `tokens_in`, `usage.completion_tokens` →
`tokens_out` (este último ya incluye reasoning tokens si el modelo
los usa — `completion_tokens_details.reasoning_tokens` es informativo,
ya está sumado en `completion_tokens`).

**Param crítico:** modelos reasoning (gpt-5.x, o1, o3) requieren
`max_completion_tokens` — NO `max_tokens` (deprecado para esta clase
de modelos, retorna `unsupported_parameter` error). Verificado live
2026-04-24 con `gpt-5.4`.

#### Gemini (gemini-3.1-pro default)

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": <PROMPT_BODY>}]}],
    "generationConfig": {"maxOutputTokens": 4096}
  }'
```

Parsear: `candidates[0].content.parts[0].text` → body. Cost-relevant
token fields:

- `usageMetadata.promptTokenCount` → `tokens_in`
- `usageMetadata.candidatesTokenCount` + `usageMetadata.thoughtsTokenCount`
  → `tokens_out` (Gemini 2.5+ y 3.x facturan thinking tokens al mismo
  rate que output tokens; sumarlos es necesario para el cost real,
  verificado live 2026-04-24 contra `gemini-2.5-flash`)

**Endpoint correcto:** `v1beta` (no `v1`). El path `v1` rechaza modelos
2.5+/3.x. Verificado live 2026-04-24.

#### Perplexity (perplexity/sonar-pro default, vía OpenRouter)

```bash
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "perplexity/sonar-pro",
    "messages": [{"role": "user", "content": <PROMPT_BODY>}],
    "max_tokens": 4096
  }'
```

Parsear: `choices[0].message.content` → body. Cost-relevant fields:

- `usage.prompt_tokens` → `tokens_in`
- `usage.completion_tokens` → `tokens_out`
- **`usage.cost` → `cost_usd` directo** — OpenRouter retorna el costo
  real de la corrida en USD como campo top-level. Más exacto que
  estimar desde token rates. Verificado live 2026-04-24 con
  `perplexity/sonar`.

**Parseo JSON defensivo:** Perplexity Sonar a veces incluye caracteres
de control en el texto de respuesta (citations con line breaks raros).
Usar `json.loads(raw, strict=False)` en Python o equivalente para
no fallar con `Invalid control character`. Verificado live 2026-04-24.

#### Claude Opus nativo

Llamar directamente desde este Code: leer el prompt de
`prompts/claude-prompt.md`, ejecutar el verdict como Opus 4.7. No hay
HTTP — es la misma sesión Claude Code. Token counts no aplican (cost
es $0). Para trazabilidad, registrar en cost log con
`tokens_in/out = 0` y `cost_usd = $0.00`.

### Paso 6 — Escribir los 4 raws

Para cada validator que respondió OK, escribir
`<input-dir>/cross-validations/<date>/<vendor>-raw.md` con frontmatter:

```yaml
---
title: "<Vendor> raw — <input-slug> <date>"
type: reference
layer: output
language: <input-lang>
tags: [cross-validate, raw, <vendor>, capa/4-output]
updated: <date>
vendor: <vendor>
model: <model-id>
tokens_in: <int>
tokens_out: <int>
cost_usd: <float>
prompt_file: prompts/<vendor>-prompt.md
input_file: <relative-path-from-cross-validations-folder>
---
```

Body = la respuesta cruda del validator, sin edits.

Si un validator FALLÓ (timeout, 5xx, parse error), escribir igual el
raw con frontmatter `status: failed` + `error_msg: <mensaje>` + body
explicando qué pasó. El skill continúa con los demás — no aborta toda
la corrida por 1 fallo.

### Paso 7 — Síntesis del summary (Opus llamada 2)

Llamar a Opus 4.7 nativo (segunda llamada, separada de la del Paso 5 —
evita prompt-bleed). Pasarle:
- Los N raws que llegaron OK
- Instrucción de sintetizar siguiendo las 6 secciones de la spec
  (ver `cross-ai-validation.md` §"Synthesis format" + el formato
  detallado abajo)

Escribir output a `<input-dir>/cross-validations/<date>/summary.md`
con frontmatter:

```yaml
---
title: "Summary — <input-slug> <date>"
type: reference
layer: output
language: <input-lang>
tags: [cross-validate, summary, capa/4-output]
updated: <date>
input_file: <path>
validators_run: [openai, gemini, perplexity, claude]
validators_failed: []
final_verdict: KEEP | REFINE | REJECT  # del consenso de los validators
score_consolidated: XX/50              # promedio de scores propios
---
```

Body con las 6 secciones canónicas (basadas en
[wiki/playbooks/cross-ai-validation.md](../../wiki/playbooks/cross-ai-validation.md)
§"Synthesis format"):

1. **Tabla principal** — fila por LLM (qué sugiere / cómo afecta lo
   actual / cómo modificar / posibles soluciones / riesgos o
   trade-offs). Cada celda con bullets, scanneable en <60s.
2. **Coincidencias** — donde 3+ validators apuntan a lo mismo (señal
   fuerte).
3. **Divergencias** — donde no hay acuerdo. Cada una con "opción A vs
   opción B + razón de cada lado + recomendación del synth".
4. **Claims factuales** — separar opinión estilística de afirmaciones
   verificables (Rule 1 de
   [.claude/rules/verification.md](../../.claude/rules/verification.md)).
5. **Decisiones propuestas** — 3-5 bullets accionables.
6. **Referencias a raws + prompts** — links relativos a los archivos
   del folder.

### Paso 8 — Append cost log (filas por vendor + TOTAL)

Para cada validator (incluido Claude con $0.00), append una fila a
[output/costs/cross-validate-log.md](../../output/costs/cross-validate-log.md):

```
| <date> | <input-slug> | <vendor> | <model> | <tokens_in> | <tokens_out> | $X.XX |
```

Donde `<input-slug>` = filename del input sin `.md`, o slug derivado
del path si filename es genérico (ej. `master` → usar el folder
parent: `decidir-con-ia-que-comprar`).

Después de las N filas por vendor, agregar 1 fila TOTAL:

```
| <date> | <input-slug> | TOTAL | — | <suma> | <suma> | $X.XX |
```

`vendor: TOTAL` se ignora en la suma MTD del Paso 2.

### Paso 9 — Report final al usuario

Mostrar resumen:

```
✓ Cross-validation completa.

Summary: <input-dir>/cross-validations/<date>/summary.md
Risks: <input-dir>/cross-validations/<date>/risks.md
Prompts: <input-dir>/cross-validations/<date>/prompts/ (<N> archivos)
Raws: <input-dir>/cross-validations/<date>/ (<N> archivos)

Validators OK: openai, gemini, perplexity, claude
Validators failed: <none|list>

Verdict consolidado: <KEEP|REFINE|REJECT>
Score promedio: <XX>/50

Costo real: $X.XX (vs estimado $X.XX)
MTD: $X.XX / $10.00

Abrí summary.md y revisá §5 (decisiones propuestas) para ver qué
tocar antes de avanzar.
```

## Cost cap behavior

- **Hard stop a $10/mes.** No hay soft-pass. Si el estimado del Paso 2
  excede el cap, el skill aborta antes de hacer cualquier API call.
- **MTD se calcula por mes calendario.** Filas de meses anteriores no
  cuentan. No hace falta limpiar el log.
- **Claude Opus nativo no cuenta** ($0.00 — Max 5x ya pagado).
- **Si el cap se agota, el flujo manual sigue funcionando.** El skill
  es acelerador, no único path.

## Failure modes y mitigaciones

| Failure | Comportamiento del skill |
|---|---|
| API key faltante | Abort en Paso 1 con pointer al playbook de onboarding. |
| Modelo flag inválido | Abort en Paso 0 con lista de valores válidos del enum. |
| Cap MTD excedido | Abort en Paso 2 con MTD actual + opciones. |
| 1 validator falla (timeout, 5xx) | Continúa con los demás. Raw se escribe con `status: failed`. Summary documenta. |
| Todos los validators fallan | Aborta antes del Paso 7. No escribe summary vacío. |
| Input file sin frontmatter | Warning en Paso 0, continúa. Algunos placeholders quedan vacíos pero el flow termina. |
| Output folder ya existe | Crea `<date>-2`, `<date>-3`, etc. |

## Templates de prompts

Los 4 templates viven en
[.claude/skills/cross-validate/templates/](cross-validate/templates/):

- [chatgpt-prompt-template.md](cross-validate/templates/chatgpt-prompt-template.md) —
  Brand Strategy Challenger
- [gemini-prompt-template.md](cross-validate/templates/gemini-prompt-template.md) —
  Designer-Critic
- [perplexity-prompt-template.md](cross-validate/templates/perplexity-prompt-template.md) —
  Competitive Intelligence
- [claude-prompt-template.md](cross-validate/templates/claude-prompt-template.md) —
  Repo-Context Coherence Checker

Cada template usa los placeholders descriptos en el Paso 4. Cuando se
agreguen modelos nuevos a los enum de los playbooks de onboarding, los
templates no requieren cambios — solo el flag --vendor-model acepta
nuevos valores.

## Related

- Playbook canónico: [wiki/playbooks/cross-ai-validation.md](../../wiki/playbooks/cross-ai-validation.md)
- API onboarding: [wiki/playbooks/api-onboarding/](../../wiki/playbooks/api-onboarding/)
- Cost log: `output/costs/cross-validate-log.md` (creado al primer run del skill)
- Pre-commit hook que bloquea API keys en commits: [.claude/hooks/validate-api-keys.py](../hooks/validate-api-keys.py)
- Verification rule (claims factuales): [.claude/rules/verification.md](../rules/verification.md)
