# Meshy API Integration & Autonomous Asset Bridge

Local Meshy asset-generation bridge for the **LOOPHOLE** Unity project.
Provides programmatic 3D humanoid NPC generation, auto-rigging, and character animation pipelines with strict credit guardrails and zero-credential-leakage security.

---

## Key Features

1. **Official Meshy API Client**: Full integration with Meshy v1/v2 endpoints for Text-to-3D, Image-to-3D, Auto-Rigging, Animation Library, and Text-to-Motion.
2. **Strict Credit Safety Ledger (`credit_budget.json`)**:
   - Hard **1,000-credit budget** limit.
   - **50-credit safety reserve** that blocks any request that would exhaust the account.
   - Every transaction logged with timestamp, task ID, operation type, and cost.
   - Requires explicit `--approve` flag for paid operations; otherwise runs safe `--dry-run`.
3. **Zero API Key Leakage**:
   - Reads `MESHY_API_KEY` strictly from environment variable or Windows User registry.
   - Key is never printed to logs, never committed to git, and never saved in config files.
   - Root `.gitignore` preconfigured to ignore secrets, credentials, and cache folders.
4. **Zero-Credit Local 3D Conversion**:
   - Integrates local headless Blender 5.1 to convert FBX models to GLB at zero API cost.
5. **Standard NPC Asset Architecture**:
   - All assets organized cleanly in Unity:
     ```
     Assets/NPCs/<NPC_Name>/
     ├── Source/       # Original model / textures / GLB conversion
     ├── Rigged/       # Auto-rigged FBX & GLB from Meshy
     ├── Animations/   # Downloaded animation clips (Idle, Walk, Talk, Scared)
     └── Prefab/       # Unity prefab metadata and character controller
     ```
6. **Dedicated NPC Shankar Pipeline**:
   - One-command staging, local conversion, auto-rigging, and 4-clip animation generation for Shankar.

---

## Environment Setup

### Setting the API Key (Windows)

#### PowerShell (User Scope - Persistent):
```powershell
[System.Environment]::SetEnvironmentVariable('MESHY_API_KEY', 'your_api_key_here', 'User')
$env:MESHY_API_KEY = 'your_api_key_here'
```

#### Command Prompt (System/User Scope):
```cmd
setx MESHY_API_KEY "your_api_key_here"
set MESHY_API_KEY=your_api_key_here
```

Verify setup securely without exposing the key:
```powershell
python Assets/_AI_Bridge/meshy/meshy_bridge.py status
```

Output:
```
============================================================
MESHY API BRIDGE STATUS CHECK
============================================================
[Security] API Key Configured: OK (msy_...8Ek1 (40 chars))
[API] Connectivity: CONNECTED (200 OK)
[Account] Live Meshy Balance: 1422 credits
[Budget] Loophole Budget Remaining: 1000 / 1000 credits
[Budget] Safety Reserve: 50 credits (Safe usable: 950)
Status: READY FOR ASSET PIPELINE
```

---

## CLI Commands Reference

### 1. Bridge Status & Budget

#### Check Status:
```bash
python Assets/_AI_Bridge/meshy/meshy_bridge.py status
```

#### View Credit Budget Ledger:
```bash
python Assets/_AI_Bridge/meshy/meshy_bridge.py budget
```

#### Sync Live Account Balance:
```bash
python Assets/_AI_Bridge/meshy/meshy_bridge.py sync-balance
```

#### Browse Meshy Animation Library:
```bash
# List all animations
python Assets/_AI_Bridge/meshy/meshy_bridge.py list-animations

# Filter by query or category
python Assets/_AI_Bridge/meshy/meshy_bridge.py list-animations --query walk
python Assets/_AI_Bridge/meshy/meshy_bridge.py list-animations --category DailyActions
```

---

### 2. NPC Staging & Rigging (`npc_generator.py`)

#### Initialize NPC Folder Hierarchy:
```bash
python Assets/_AI_Bridge/meshy/npc_generator.py init --name Villager_01
```

#### Stage Existing Character Model:
```bash
python Assets/_AI_Bridge/meshy/npc_generator.py stage --name Villager_01 --model-path "Assets/Chandan kumar singh/Art/NPC Characters/Male_2/Bob.Fbx"
```

#### Auto-Rig Model via Meshy:
```bash
# Dry run (verifies format conversion and validates parameters at 0 cost)
python Assets/_AI_Bridge/meshy/npc_generator.py rig --name Villager_01 --model-path "Assets/NPCs/Villager_01/Source/Bob.Fbx" --dry-run

# Live auto-rigging (consumes 5 credits)
python Assets/_AI_Bridge/meshy/npc_generator.py rig --name Villager_01 --model-path "Assets/NPCs/Villager_01/Source/Bob.Fbx" --approve
```

---

### 3. Animation Pipeline (`animation_generator.py`)

#### Run Complete Shankar Pipeline:
```bash
# Dry-run validation (Stages model, converts FBX->GLB locally, validates all 4 clips)
python Assets/_AI_Bridge/meshy/animation_generator.py pipeline-shankar --dry-run

# Live execution (Auto-rigs model + generates Idle, Walk, Talk, and Scared clips)
python Assets/_AI_Bridge/meshy/animation_generator.py pipeline-shankar --approve
```

#### Generate Custom Animation Set for Rigged Character:
```bash
python Assets/_AI_Bridge/meshy/animation_generator.py animate --name Shankar --rig-task-id "<task_id>" --actions 243,613,313,333 --approve
```

---

## Curated Animation Action IDs for Loophole

| Clip Name | Action ID | Category | Description |
|---|---|---|---|
| `Idle_01` | **243** | `DailyActions` | Natural standing idle breathing cycle |
| `Walk_Casual` | **613** | `WalkAndRun` | Casual rural path walking motion |
| `Talk_Gesture` | **313** | `DailyActions` | Expressive dialogue delivery with open hands |
| `Scared_LookAround` | **333** | `DailyActions` | Nervous, frightened searching gesture suited for forest horror |
| `Walk_LookAround` | **341** | `DailyActions` | Cautious slow forward movement scanning surroundings |

---

## Credit Safety Guardrails

- **Hard Budget Limit**: Set to 1,000 credits in `credit_budget.json`.
- **Safety Reserve**: 50 credits are permanently reserved. No request can reduce credits remaining below 50.
- **Approval Gate**: All generative calls require `--approve` (CLI) or `approved=True` (Python API).
- **Transaction History**: Every API cost deduction is immutably logged with timestamp, task ID, and HTTP status.
