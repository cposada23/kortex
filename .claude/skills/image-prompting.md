---
scope: framework
---

# Image Prompting — Domain Context

Load this when writing, reviewing, or iterating image generation prompts.

## Prompt structure (4 elements)

1. **Contexto / Rol** — who the AI should think as (director, photographer, etc.)
2. **Objetivo** — what the image needs to achieve
3. **Detalles** — subject, lighting, style, mood, format, restrictions
4. **Tipo de respuesta** — aspect ratio, platform, output format

Optional: add quality criteria ("cinematic, no HDR, no stock feel")

## Copy-paste template

```
Act as [ROLE / visual director].

Subject: [who or what]
Setting: [location / environment]
Lighting: [source, temperature, direction, quality]
Style: [photographic / cinematic / editorial / etc.]
Mood: [emotional tone]
Format: [aspect ratio — 9:16 / 4:5 / 1:1]
Restrictions: [what to avoid]
```

## Key principles

- **Lighting first** — describe light source, temperature (3200K warm / 6500K cool),
  direction (camera left/right), quality (hard / soft / diffuse)
- **Specificity beats adjectives** — "Rembrandt lighting" beats "dramatic lighting"
- **Negative prompts matter** — always include what to exclude
- **Iterate on master** — use one canonical base prompt; variations tweak one element
- **Aesthetic before prompt** — decide mood/style before writing copy

## Tools in this stack

| Tool | Best for |
|---|---|
| Flux | Shadow, texture, lighting control |
| Midjourney | Style consistency, --style raw for realism |
| Ideogram | Text in images |
| Leonardo AI | Batch variation |
| Whisk | Reference image composition |

## Canonical sources

Master guide: wiki/playbooks/prompts/PROMPT_GUIA.md
Image tool: wiki/playbooks/prompts/HERRAMIENTA_PROMPT_IMAGEN_IA.md
Aesthetic tool: wiki/playbooks/prompts/HERRAMIENTA_ESTETICA_IMAGEN_IA.md
Sandbag character prompts: projects/sandbag-fuerza-tres-dias/prompts/imagen-ia/
