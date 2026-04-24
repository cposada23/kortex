---
title: "API Onboarding — índice"
type: playbook
layer: wiki
language: es
tags: [capa/2-wiki, api, onboarding, cross-validate]
updated: 2026-04-24
confidence: high
source_count: 6
last_verified: 2026-04-24
---

# API Onboarding — índice

Playbooks operacionales para obtener API keys, configurar billing y
guardar la key de forma segura para los proveedores externos que usa
el skill `cross-validate`.

Un playbook por proveedor — cada uno es auto-contenido: abrilo,
seguilo de arriba hacia abajo, terminás con la key cargada como
variable de entorno y saldo suficiente para correr los tests iniciales.

## Proveedores activos

| Proveedor | Acceso | Playbook | Modelo default | Modelo testing (barato/free) | Env var | Flag del skill |
|---|---|---|---|---|---|---|
| OpenAI | Directo | [openai.md](openai.md) | `gpt-5.4` | `gpt-5.4-nano` | `OPENAI_API_KEY` | `--openai-model` |
| Google Gemini | Directo | [google-gemini.md](google-gemini.md) | `gemini-3.1-pro` (paid) | `gemini-2.5-flash` (free) | `GEMINI_API_KEY` | `--gemini-model` |
| Perplexity Sonar | Vía OpenRouter | [openrouter.md](openrouter.md) | `perplexity/sonar-pro` | `perplexity/sonar` | `OPENROUTER_API_KEY` | `--perplexity-model` |

Claude Opus 4.7 nativo es el cuarto validador y no requiere API key
externa (corre en el mismo Claude Code).

## Por qué Perplexity vía OpenRouter

El API Portal directo de Perplexity pide un mínimo alto al sign-up
(observado ~$50 USD), incompatible con presupuestos chicos para
testing del skill. OpenRouter sirve el mismo Sonar Pro (passthrough
sin markup en inference, 5.5% fee sólo al cargar créditos), sin
mínimo de depósito, con budget cap nativo por API key. Ver
[openrouter.md](openrouter.md) para el playbook completo.

OpenRouter también puede servir como fallback para OpenAI/Gemini si
alguno de ellos cambia políticas, pero por default Kortex llama a
OpenAI y Gemini directo (auditing más limpio por proveedor).

## Cap de gasto efectivo por proveedor

Cada proveedor tiene un mecanismo diferente para cappear el gasto
mensual. Vos decidís el monto del cap según tu presupuesto. Resumen
del playbook de cada uno:

| Proveedor | Cómo se cappea el gasto mensual | Hard stop o soft alert? |
|---|---|---|
| OpenAI (directo) | Cargar prepaid + **desactivar auto-recharge** | Hard — API para cuando saldo llega a $0 |
| Gemini (directo) | AI Studio → Spend page → Monthly spend cap → tu monto | Hard (con delay ~10 min de enforcement) |
| Perplexity (via OpenRouter) | OpenRouter Keys → Guardrails → Spending limit mensual | Hard — cap por key, otros keys siguen funcionando |

OpenAI directo no tiene un "budget cap" nativo que frene la API —
depende del saldo prepaid + auto-recharge desactivado. Gemini y
OpenRouter (para Perplexity) sí tienen cap nativo configurable al
dólar.

## Comparativa — costo mínimo para empezar

| Proveedor | Mínimo para activar API paid | Free tier (API)? |
|---|---|---|
| OpenAI | **$5 USD** prepaid | No (sólo créditos gratuitos ocasionales para builders) |
| Gemini | **$10 USD** prepaid (necesario para Pro) | Sólo Flash — Pro paywalled desde 2026-04-01 |
| Perplexity (via OpenRouter) | **Sin mínimo** — $1 gratis al signup, cargás lo que quieras después + 5.5% fee | $1 bonus al verificar cuenta |

**Setup mínimo gratis para validar que el skill anda:** OpenRouter
$1 free al signup + Gemini Flash free + Claude Opus nativo — 3
validators sin gastar nada. Después decidís si cargás los proveedores
paid según el uso real.

## Patrón de flags en el skill `cross-validate`

El skill acepta un flag de modelo **por proveedor** (no un flag global).
Permite cargar diferentes niveles de calidad por validador dentro de
la misma corrida — ej. Gemini Pro (juicio serio) + OpenAI nano (sanity
check barato) cuando estás iterando el prompt.

```bash
# Default — todos los modelos "serios"
/cross-validate <idea-file>

# Testing barato en todos
/cross-validate <idea-file> \
  --openai-model gpt-5.4-nano \
  --gemini-model gemini-2.5-flash \
  --perplexity-model perplexity/sonar

# Mix: Pro en Gemini + Perplexity, barato en OpenAI
/cross-validate <idea-file> --openai-model gpt-5.4-nano

# Menu interactivo — skill pregunta por cada proveedor
/cross-validate <idea-file> --ask-model
```

Los valores aceptados por cada flag están en la sección "Modelos
disponibles — enum" de cada playbook. Cuando Google/OpenAI agregan
modelos nuevos, se actualiza la tabla en el playbook correspondiente y
el skill los reconoce automáticamente (validation del flag lee el enum
de esa tabla). Este mantenimiento es normal — pasa 2-4 veces al año por
proveedor.

## Orden recomendado

1. **Gemini primero** — gratis, sin ingresar tarjeta. Terminás en 3
   minutos con una key activa. Sirve de "hello world" para confirmar
   que el resto del flujo funciona.
2. **OpenRouter segundo** — $1 gratis al signup, 2-3 minutos. Key
   con budget cap mensual creado + monto cargado (opcional si querés
   ir más allá del $1 free) sirve para Perplexity Sonar Pro.
3. **OpenAI tercero** — $5 mínimo, flow de billing prolijo.

## Después de obtener las 3 keys

1. Crear `.env` en la raíz del repo (ver cada playbook para el formato
   exacto de cada variable).
2. Confirmar que `.env` está en `.gitignore` (el template lo trae así
   por default).
3. Ejecutar el pre-commit hook
   [.claude/hooks/validate-api-keys.py](../../../.claude/hooks/validate-api-keys.py)
   — bloquea commits que incluyan patterns de API keys en cualquier
   archivo tracked.
4. Invocar el skill `cross-validate` sobre tu primer archivo.

## Verificación

Info verificada 2026-04-24 contra docs oficiales de los proveedores.
Los flows de UI y los límites de billing caen bajo Rule 1 de
[.claude/rules/verification.md](../../../.claude/rules/verification.md)
— re-verificar antes de asertar cualquier fact específico si pasaron
>30 días desde `last_verified`.
