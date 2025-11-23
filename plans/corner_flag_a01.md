# Build Plan - corner_flag_a01

- Purpose: soccer corner flag (prop)
- Hero tier: background
- Targets: Roblox, Unreal
- Budget: <= 900 tris; textures: ORM 512px, Normal 512px, BaseColor 512px

## Constraints (sorted by severity)

- BLOCKER: Each MeshPart must have <= 10,000 triangles. [tris] (ref: OPT:ROBLOX:MESHPART_TRIS_MAX)
- BLOCKER: Export with -Z forward and Y up. [axes] (ref: EXPORT:AXIS:NEG_Z_FWD_Y_UP)
- BLOCKER: Provide at least three LODs: HIGH, MED, LOW; remove tertiary then secondary detail first. [levels] (ref: LOD:PRESENT_HIGH_MED_LOW)

## Blender Build Plan (phase order)

### MODEL - model_hardsurface_v1

- Blockout with primary forms to establish silhouette clarity (10-20 m test).
- Apply Mirror/Array/Bevel modifiers non-destructively; keep quads-first with controlled poles.
- Reserve micro-geometry; plan bevels for bake rather than runtime geo.
- Prepare low-poly topology for clean shading; mark hard edges where needed.

**Metrics:** triangles_estimate=8000 tris
**Definition of Done:** Sec LOD:PRESENT_HIGH_MED_LOW

### UV - uv_standard_trim_v1

- Mark seams on least-visible edges; split by shading discontinuities.
- Pack islands with >= 4 px padding @1k; scale to keep TD within +/-10%.
- Mirror/overlap only on symmetrical, wear-agnostic areas; unique UVs for decals/hero wear.

**Metrics:** texel_density_variance=10 percent
**Definition of Done:** Sec UV:TD_VARIANCE_MAX_10PCT

### BAKE - bake_hardsurface_cage_v1

- Name high/low meshes with clear suffixes for batch bakes.
- Generate an outward cage for tight bevels; avoid projection skew on glancing angles.
- Bake Normal, AO, Curvature; add Thickness where material needs it.

**Metrics:** projection_errors=0 count
**Definition of Done:** Sec EXPORT:AXIS:NEG_Z_FWD_Y_UP

### TEXTURE - texturing_pbr_pack_orm_v1

- Author Basecolor/Metallic/Roughness/Normal/AO within engine-safe ranges.
- Channel-pack ORM when applicable to reduce texture count.
- Keep roughness readable; avoid crushed blacks; prefer tiling mats on large areas.

**Metrics:** texture_sets=3 count
**Definition of Done:** Sec TEX:SIZE_RANGE

### EXPORT - export_fbx_modern_engines_v1

- Apply transforms; normalize scale; set pivot/origin as planned.
- FBX export: scale 1.0; smoothing/tangents per target engine; include animations only if required.
- Axis check: -Z forward, Y up; verify per-material limits and mesh merging policy.

**Metrics:** axis_compliance=1 boolean
**Definition of Done:** Sec EXPORT:AXIS:NEG_Z_FWD_Y_UP

### QA - optimization_lod_plan_v1

- Define HIGH/MED/LOW meshes; remove tertiary then secondary details per step-down.
- Verify decal removal thresholds and screen-size targets.
- Confirm collision uses simple primitives or engine-native low-poly shapes.

**Metrics:** lod_levels=3 count
**Definition of Done:** Sec LOD:PRESENT_HIGH_MED_LOW

## Checklists

### After Import

- Tri count matches plan; shading and tangents correct.
- Scale & units correct (1 unit = 1 m unless engine overrides; Roblox mapping documented).
- LOD switching thresholds verified at screen distances.
- Collision behaves as intended with simple primitives.
- No runtime MeshId swaps on server for Roblox templates.

### Before Export

- Tri count <= budget; MeshPart <= 10,000 tris.
- HIGH/MED/LOW LODs present and linked.
- Transforms applied; scale normalized; pivot/origin correct.
- UVs valid; no unintended overlaps; TD within +/-10%; padding >= 4 px @1k.
- Materials limited; channel packing (ORM) applied when planned.
- Axis: -Z forward, Y up; naming & hierarchy clean.

## Provenance

- Unknown Unknowns 2025 - /mnt/data/unknown-unknowns-2025.md
- PaaS Validation Principles - /mnt/data/paas-validation-principles.md

