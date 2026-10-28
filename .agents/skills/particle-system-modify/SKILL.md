---
name: particle-system-modify
description: Modify a `UnityEngine.ParticleSystem` component on a GameObject. Pass `SerializedMember` payloads only for the modules you want to change; everything else is left alone. Use 'particle-system-get' first to inspect the current structure.
metadata:
  generated-by: mcp-plugin-dotnet
---

# ParticleSystem / Modify

Modify a `UnityEngine.ParticleSystem` component on a GameObject. Pass `SerializedMember` payloads only for the modules you want to change; omitted modules are left untouched. Use 'particle-system-get' first to inspect the current structure so the diff is targeted.

## Inputs

- `gameObjectRef` — the GameObject hosting the `ParticleSystem` component (required).
- `componentRef` — optional. Resolves a specific `ParticleSystem` when the GameObject has more than one; otherwise the first `ParticleSystem` found is used.
- `main`, `emission`, `shape`, `velocityOverLifetime`, `limitVelocityOverLifetime`, `inheritVelocity`, `lifetimeByEmitterSpeed`, `forceOverLifetime`, `colorOverLifetime`, `colorBySpeed`, `sizeOverLifetime`, `sizeBySpeed`, `rotationOverLifetime`, `rotationBySpeed`, `externalForces`, `noise`, `collision`, `trigger`, `subEmitters`, `textureSheetAnimation`, `lights`, `trails`, `customData`, `renderer` — optional `SerializedMember` payloads per module. Include only the properties you want to change.

## Behavior

Each non-null module is applied via `Reflector.TryModify` and logged with a `[ModuleName]` prefix in the response's `logs` array. The `renderer` payload targets the sibling `UnityEngine.ParticleSystemRenderer` component on the same GameObject; if absent, the call logs the miss instead of throwing. When at least one module was modified, the GameObject and the `ParticleSystem` are marked dirty so the change persists. The whole call runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool particle-system-modify --input '{
  "gameObjectRef": "string_value",
  "componentRef": "string_value",
  "main": "string_value",
  "emission": "string_value",
  "shape": "string_value",
  "velocityOverLifetime": "string_value",
  "limitVelocityOverLifetime": "string_value",
  "inheritVelocity": "string_value",
  "lifetimeByEmitterSpeed": "string_value",
  "forceOverLifetime": "string_value",
  "colorOverLifetime": "string_value",
  "colorBySpeed": "string_value",
  "sizeOverLifetime": "string_value",
  "sizeBySpeed": "string_value",
  "rotationOverLifetime": "string_value",
  "rotationBySpeed": "string_value",
  "externalForces": "string_value",
  "noise": "string_value",
  "collision": "string_value",
  "trigger": "string_value",
  "subEmitters": "string_value",
  "textureSheetAnimation": "string_value",
  "lights": "string_value",
  "trails": "string_value",
  "customData": "string_value",
  "renderer": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool particle-system-modify --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool particle-system-modify --input-file - <<'EOF'
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
| `main` | `string` | No | Main module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `emission` | `string` | No | Emission module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `shape` | `string` | No | Shape module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `velocityOverLifetime` | `string` | No | Velocity over Lifetime module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `limitVelocityOverLifetime` | `string` | No | Limit Velocity over Lifetime module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `inheritVelocity` | `string` | No | Inherit Velocity module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `lifetimeByEmitterSpeed` | `string` | No | Lifetime by Emitter Speed module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `forceOverLifetime` | `string` | No | Force over Lifetime module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `colorOverLifetime` | `string` | No | Color over Lifetime module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `colorBySpeed` | `string` | No | Color by Speed module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `sizeOverLifetime` | `string` | No | Size over Lifetime module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `sizeBySpeed` | `string` | No | Size by Speed module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `rotationOverLifetime` | `string` | No | Rotation over Lifetime module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `rotationBySpeed` | `string` | No | Rotation by Speed module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `externalForces` | `string` | No | External Forces module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `noise` | `string` | No | Noise module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `collision` | `string` | No | Collision module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `trigger` | `string` | No | Trigger module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `subEmitters` | `string` | No | Sub Emitters module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `textureSheetAnimation` | `string` | No | Texture Sheet Animation module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `lights` | `string` | No | Lights module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `trails` | `string` | No | Trails module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `customData` | `string` | No | Custom Data module data to apply. Only include properties you want to change. RQL: SerializedMember |
| `renderer` | `string` | No | Renderer module data to apply. Only include properties you want to change. RQL: SerializedMember |

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
    "main": {
      "type": "string"
    },
    "emission": {
      "type": "string"
    },
    "shape": {
      "type": "string"
    },
    "velocityOverLifetime": {
      "type": "string"
    },
    "limitVelocityOverLifetime": {
      "type": "string"
    },
    "inheritVelocity": {
      "type": "string"
    },
    "lifetimeByEmitterSpeed": {
      "type": "string"
    },
    "forceOverLifetime": {
      "type": "string"
    },
    "colorOverLifetime": {
      "type": "string"
    },
    "colorBySpeed": {
      "type": "string"
    },
    "sizeOverLifetime": {
      "type": "string"
    },
    "sizeBySpeed": {
      "type": "string"
    },
    "rotationOverLifetime": {
      "type": "string"
    },
    "rotationBySpeed": {
      "type": "string"
    },
    "externalForces": {
      "type": "string"
    },
    "noise": {
      "type": "string"
    },
    "collision": {
      "type": "string"
    },
    "trigger": {
      "type": "string"
    },
    "subEmitters": {
      "type": "string"
    },
    "textureSheetAnimation": {
      "type": "string"
    },
    "lights": {
      "type": "string"
    },
    "trails": {
      "type": "string"
    },
    "customData": {
      "type": "string"
    },
    "renderer": {
      "type": "string"
    }
  },
  "required": [
    "gameObjectRef"
  ]
}
```

## Output

This tool does not return structured output.

