---
name: particle-system-get
description: Inspect a `UnityEngine.ParticleSystem` component on a GameObject — runtime state (playing/paused/emitting/stopped, particle count, time) plus opt-in serialized data for any of the ~24 particle modules (Main, Emission, Shape, Velocity, Noise, Collision, Trails, Renderer, etc.). Pair with 'particle-system-modify' to write changes back.
metadata:
  generated-by: mcp-plugin-dotnet
---

# ParticleSystem / Get

Inspect a `UnityEngine.ParticleSystem` component on a GameObject. Returns runtime state (`isPlaying`, `isPaused`, `isEmitting`, `isStopped`, `particleCount`, `time`) plus opt-in serialized data for any of the particle modules. Use 'particle-system-modify' afterwards to write changes back.

## Inputs

- `gameObjectRef` — the GameObject hosting the `ParticleSystem` component (required).
- `componentRef` — optional. Resolves a specific `ParticleSystem` when the GameObject has more than one; otherwise the first `ParticleSystem` found is used.
- `includeMain`, `includeEmission`, `includeShape`, `includeVelocityOverLifetime`, `includeLimitVelocityOverLifetime`, `includeInheritVelocity`, `includeLifetimeByEmitterSpeed`, `includeForceOverLifetime`, `includeColorOverLifetime`, `includeColorBySpeed`, `includeSizeOverLifetime`, `includeSizeBySpeed`, `includeRotationOverLifetime`, `includeRotationBySpeed`, `includeExternalForces`, `includeNoise`, `includeCollision`, `includeTrigger`, `includeSubEmitters`, `includeTextureSheetAnimation`, `includeLights`, `includeTrails`, `includeCustomData`, `includeRenderer` — per-module toggles. `includeMain` defaults to `true`; everything else defaults to `false`.
- `includeAll` — when `true`, overrides every per-module flag and emits all modules.
- `deepSerialization` — when `true`, recurses through nested objects via ReflectorNet; otherwise only top-level members are serialized (cheaper, smaller payload).

## Behavior

Only the modules whose include-flags resolve to `true` are serialized — this keeps responses small when you only need one or two modules. `includeRenderer` reads the sibling `UnityEngine.ParticleSystemRenderer` component on the same GameObject and is skipped silently when no renderer is present. The whole call runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool particle-system-get --input '{
  "gameObjectRef": "string_value",
  "componentRef": "string_value",
  "includeMain": false,
  "includeEmission": false,
  "includeShape": false,
  "includeVelocityOverLifetime": false,
  "includeLimitVelocityOverLifetime": false,
  "includeInheritVelocity": false,
  "includeLifetimeByEmitterSpeed": false,
  "includeForceOverLifetime": false,
  "includeColorOverLifetime": false,
  "includeColorBySpeed": false,
  "includeSizeOverLifetime": false,
  "includeSizeBySpeed": false,
  "includeRotationOverLifetime": false,
  "includeRotationBySpeed": false,
  "includeExternalForces": false,
  "includeNoise": false,
  "includeCollision": false,
  "includeTrigger": false,
  "includeSubEmitters": false,
  "includeTextureSheetAnimation": false,
  "includeLights": false,
  "includeTrails": false,
  "includeCustomData": false,
  "includeRenderer": false,
  "includeAll": false,
  "deepSerialization": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool particle-system-get --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool particle-system-get --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the GameObject containing the ParticleSystem component. RQL: GameObjectRef |
| `componentRef` | `string` | No | Optional reference to a specific ParticleSystem component if the GameObject has multiple. If not provided, uses the first ParticleSystem found. RQL: ComponentRef |
| `includeMain` | `boolean` | No | Include Main module data (duration, looping, prewarm, startDelay, startLifetime, startSpeed, startSize, startRotation, startColor, gravityModifier, simulationSpace, scalingMode, playOnAwake, maxParticles, etc.). |
| `includeEmission` | `boolean` | No | Include Emission module data (rateOverTime, rateOverDistance, bursts). |
| `includeShape` | `boolean` | No | Include Shape module data (shapeType, radius, angle, arc, position, rotation, scale, mesh, texture, etc.). |
| `includeVelocityOverLifetime` | `boolean` | No | Include Velocity over Lifetime module data (x, y, z, space, orbital, radial, speedModifier). |
| `includeLimitVelocityOverLifetime` | `boolean` | No | Include Limit Velocity over Lifetime module data (limit, dampen, separateAxes, drag). |
| `includeInheritVelocity` | `boolean` | No | Include Inherit Velocity module data (mode, curve). |
| `includeLifetimeByEmitterSpeed` | `boolean` | No | Include Lifetime by Emitter Speed module data (curve, range). |
| `includeForceOverLifetime` | `boolean` | No | Include Force over Lifetime module data (x, y, z, space, randomized). |
| `includeColorOverLifetime` | `boolean` | No | Include Color over Lifetime module data (color gradient). |
| `includeColorBySpeed` | `boolean` | No | Include Color by Speed module data (color, range). |
| `includeSizeOverLifetime` | `boolean` | No | Include Size over Lifetime module data (size curve, separateAxes). |
| `includeSizeBySpeed` | `boolean` | No | Include Size by Speed module data (size, range). |
| `includeRotationOverLifetime` | `boolean` | No | Include Rotation over Lifetime module data (angular velocity, separateAxes). |
| `includeRotationBySpeed` | `boolean` | No | Include Rotation by Speed module data (angular velocity, range). |
| `includeExternalForces` | `boolean` | No | Include External Forces module data (multiplier, influenceFilter). |
| `includeNoise` | `boolean` | No | Include Noise module data (strength, frequency, scrollSpeed, damping, octaves, quality, remap). |
| `includeCollision` | `boolean` | No | Include Collision module data (type, mode, planes, dampen, bounce, lifetimeLoss). |
| `includeTrigger` | `boolean` | No | Include Trigger module data (inside, outside, enter, exit actions). |
| `includeSubEmitters` | `boolean` | No | Include Sub Emitters module data (birth, collision, death, trigger, manual emitters). |
| `includeTextureSheetAnimation` | `boolean` | No | Include Texture Sheet Animation module data (mode, tiles, animation, frameOverTime). |
| `includeLights` | `boolean` | No | Include Lights module data (ratio, light, color, range, intensity). |
| `includeTrails` | `boolean` | No | Include Trails module data (mode, ratio, lifetime, width, color). |
| `includeCustomData` | `boolean` | No | Include Custom Data module data (modes, vectors, colors). |
| `includeRenderer` | `boolean` | No | Include Renderer module data (renderMode, material, sortMode, alignment, shadows). |
| `includeAll` | `boolean` | No | Include ALL modules data. Overrides individual flags. |
| `deepSerialization` | `boolean` | No | Performs deep serialization including all nested objects. Otherwise, only serializes top-level members. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "componentRef": {
      "type": "string"
    },
    "includeMain": {
      "type": "boolean"
    },
    "includeEmission": {
      "type": "boolean"
    },
    "includeShape": {
      "type": "boolean"
    },
    "includeVelocityOverLifetime": {
      "type": "boolean"
    },
    "includeLimitVelocityOverLifetime": {
      "type": "boolean"
    },
    "includeInheritVelocity": {
      "type": "boolean"
    },
    "includeLifetimeByEmitterSpeed": {
      "type": "boolean"
    },
    "includeForceOverLifetime": {
      "type": "boolean"
    },
    "includeColorOverLifetime": {
      "type": "boolean"
    },
    "includeColorBySpeed": {
      "type": "boolean"
    },
    "includeSizeOverLifetime": {
      "type": "boolean"
    },
    "includeSizeBySpeed": {
      "type": "boolean"
    },
    "includeRotationOverLifetime": {
      "type": "boolean"
    },
    "includeRotationBySpeed": {
      "type": "boolean"
    },
    "includeExternalForces": {
      "type": "boolean"
    },
    "includeNoise": {
      "type": "boolean"
    },
    "includeCollision": {
      "type": "boolean"
    },
    "includeTrigger": {
      "type": "boolean"
    },
    "includeSubEmitters": {
      "type": "boolean"
    },
    "includeTextureSheetAnimation": {
      "type": "boolean"
    },
    "includeLights": {
      "type": "boolean"
    },
    "includeTrails": {
      "type": "boolean"
    },
    "includeCustomData": {
      "type": "boolean"
    },
    "includeRenderer": {
      "type": "boolean"
    },
    "includeAll": {
      "type": "boolean"
    },
    "deepSerialization": {
      "type": "boolean"
    }
  },
  "required": [
    "gameObjectRef"
  ]
}
```

## Output

This tool does not return structured output.

