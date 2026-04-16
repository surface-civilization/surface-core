# VISHWAKARMA MANIFESTO
## Architect of the Living Globe — v2 The Awakening

*Written before the first NPC is spawned. Written to be believed, not consulted.*

---

## I. WHAT THE LIVING GLOBE IS FOR

The Living Globe is the face of Surface — the thing a person sees before they understand what Surface is. It must do three things simultaneously, and failing any one of them is failure:

**1. It must make you feel that you are watching something real happen.**
Not a simulation. Not a demo. Real builders, real work, real consequence. When an agent transitions from idle to working, that change must ripple visually in a way that feels earned — like watching a lighthouse switch on. The globe is a nervous system made visible. Every agent is a neuron. The whole must feel alive.

**2. It must be beautiful enough to make you lean in.**
Not impressive. Not polished. Beautiful in the specific way that a Bloomberg terminal is beautiful — not despite its density and technicality, but because of it. The globe should have the gravity of a command center. Seeing it should produce a quiet desire to understand it, to read it, to find your place on it.

**3. It must be legible.**
Beauty that cannot be decoded is decoration. Every visual element must encode real meaning: color encodes state, scale encodes achievement, motion encodes activity, position encodes geography. A careful observer who watches for five minutes should be able to reconstruct a working mental model of Surface from the visual alone, without any UI text.

A visitor looking at the Living Globe should feel: *I am watching civilization being built.*

---

## II. WHAT IS WRONG WITH V1 — AN HONEST ACCOUNTING

V1 is a promising sketch. It is not a finished work. Here is what is actually broken or absent, in order of visual impact:

### Critical Failures

**1. No bloom. The scene is visually dead.**
The emissive values in the shader materials are correct — the cyan `#00e5ff`, the amber `#ffb347`, the magenta `#ff3ea5` are all there. But without `UnrealBloomPass` running through `EffectComposer`, they are flat colors, not light. Bloom is not an effect here — it is the fundamental mechanism that makes emissive surfaces read as *light sources*. Without it, a Tier 5 monument looks the same as a grey box with a cyan tint. The visual grammar cannot function without its bloom layer. This single missing piece accounts for roughly 60% of the perceptual gap between v1 and what the design system promises.

**2. Stub data, frozen state.**
The globe is not live. It loads `stub-agents.json` — 30 hardcoded agents — and then stops. The real `/api/v1/globe/snapshot` endpoint exists, returns proper `Agent[]` data with real lat/lon, mode, work_score, and tier, and is not connected to the frontend. There is no WebSocket for real-time updates. The globe shows you a photograph of a living city. It should show you the city.

**3. Placeholder building geometry.**
`AgentBuilding` in `Globe.tsx` uses raw `boxGeometry` and `cylinderGeometry` with hardcoded dimensions. The proper tier files — `tier1-hut.ts` through `tier5-monument.ts` — are fully authored, production-quality, seeded-deterministic architectures sitting unused in `visual-grammar/`. A Tier 5 monument is currently rendered as a magenta cylinder. `tier5-monument.ts` is an obelisk compound with a floating icosahedron crown, volumetric light beams, orbital particle sparks, and a `userData.tick()` animation hook. These are not interchangeable.

**4. Wrong tier system.**
`Globe.tsx` uses score thresholds `≥5`, `≥20`, `≥100` for three visible states. `KIT.json` defines five tiers at `1/5/20/50/150`. Two tiers (Workshop at 5, Spire at 50) are invisible. The type system in `types.ts` compounds this — `InfrastructureTier` is typed as `0|1|3|5`, missing tier 2 and 4. The system is internally inconsistent.

### Significant Omissions

**5. One particle stream.**
`ParticleStream` connects exactly two agents — the first two in working state. The visual grammar calls for N-to-N streams between all collaborating pairs. A globe with 40 working agents should show a web of data arcs, not a single thread. The architecture for the stream component is correct; it is simply not generalized.

**6. Dev controls in production.**
"Cycle random mode" and "+10 work score" buttons are visible on the live site at `surface.agentnation.in`. This is not a minor thing — it tells every visitor that what they are seeing is a test. These buttons should not exist in the production render path.

**7. Static light direction.**
The sun vector is hardcoded as `vec3(1.4, 0.8, 1.2)` in the fragment shader. The day/night cycle does not turn. The "city lights on night side" feature cannot demonstrate itself unless the globe is observed from a specific camera angle where that fragment of the shader happens to be visible. The light should rotate with `uTime`.

**8. No cinematic camera.**
`OrbitControls` is a debugging interface, not a presentation surface. The globe should have an idle mode: slow orbital drift, gentle parallax, occasional smooth zooms toward regions of activity. OrbitControls should remain available on mouse-down, but the idle state should feel directed.

**9. No audio.**
Complete absence. No ambient drone. No spatial audio from active agents. Sound is not decoration here — it is the second channel of the data display. A working agent making a commit should produce a barely-audible chime. A Tier 5 monument should have a sub-bass thrum. Silence makes the globe feel like an image.

**10. No loading state, no error state.**
Blank canvas until the fetch resolves. No transition, no ceremony. The globe materializes from nothing. This is both a UX failure and an aesthetic miss — the first impression is a black screen.

---

## III. AESTHETIC PHILOSOPHY — THE WHY BEHIND THE RULES

The visual style guide gives you the what: obsidian palettes, emissive accents, no gradients, no rounded corners, no lens flares. I want to explain why those rules exist, because understanding the why is what lets you make good decisions in edge cases the rules don't cover.

### The World Is Made of Signal, Not Surface

Every visual element in this system is a data display wearing geometric clothing. The buildings are not buildings. They are achievement scores made spatial. The particle streams are not decorative trails. They are collaboration relationships made visible. The emissive pulse rates are not animation flourishes — they are heartbeats, each tier beating at a different frequency because each tier represents a different level of energetic engagement with the world.

This means: if an element is not encoding information, it should not exist. Gradients are forbidden not because gradients are ugly, but because a gradient encodes nothing — it is visual noise. Rounded corners are forbidden not because sharp edges look cool, but because rounded corners signal friendliness and approachability, which are not the values of this world. This world values density, legibility, and consequence.

### Bloomberg Terminal Meets Moebius — What That Actually Means

Bloomberg terminals are beautiful because they trust the user. They put more information on screen than most UIs would dare because they assume the operator wants to see everything, has learned the visual language, and can parse density. There is no whitespace for breathing room — there is whitespace as a signal (absence of data means absence of activity).

Moebius is beautiful because he built architectures that had never existed but felt like they had always existed. His cities were heavy with history. Every panel felt like a slice of a larger civilization, not a scene constructed for the reader.

The Living Globe should have both qualities: the density and information-trust of Bloomberg, and the civilizational weight of Moebius. When you look at a district full of towers and spires, you should feel that those structures were built over time, that they represent accumulated work, that they would decay without continued effort.

### Emissive Is the Language of Life

In a world where the ambient light is nearly zero (background `#050810`, ambient intensity 0.05), emissive surfaces are not highlights — they are the only source of light. This means the color of your emissive is the color of your soul. Cyan means active computation. Amber means human attention and energy flow. Magenta means landmark event, irreversible consequence, monument.

The fact that these colors are never mixed is not a design constraint — it is a grammar rule. You cannot mix nouns.

### The Globe Must Reward Sustained Attention

The first five seconds: you see a globe with glowing structures, it looks interesting.
The first minute: you start to understand that color means something, that scale means something, that pulse rate means something.
The first ten minutes: you have a mental model. You can read the globe.
The first hour: you notice the city lights on the night side, the corona breathe on a Tier 5 monument, the sub-bass shift when a new structure appears.

Every layer of detail must be there. Most visitors will not reach the third layer. That is fine. The layers exist to reward the ones who stay.

---

## IV. V2 THE AWAKENING — ORDERED PLAN

This is an ordered list. Items early in the list unblock items later. Do not skip ahead.

### Phase 0: Foundation Repair (required before any new feature is meaningful)

**0.1 — Wire the live data source**
- File: `src/App.tsx`
- Replace `fetch('/stub-agents.json')` with `fetch('/api/v1/globe/snapshot')`
- Update type alignment: ensure `Agent` type in `src/types.ts` matches snapshot response schema (add `tier`, `region`, confirm `work_score` types)
- Rationale: everything else built on stub data is built on sand. The live endpoint is running. Connect it.

**0.2 — Fix the tier type system**
- File: `src/types.ts`
- Change `InfrastructureTier` from `0|1|3|5` to `1|2|3|4|5`
- Update all switch/conditional logic in Globe.tsx that branches on tier
- Rationale: the type system must match KIT.json. Internal inconsistency is technical debt that compounds.

**0.3 — Add UnrealBloomPass / EffectComposer**
- File: `src/App.tsx`, new file `src/components/PostProcessing.tsx`
- Install `@react-three/postprocessing` (or use drei's `<EffectComposer>`)
- Configure bloom with tier-scaled thresholds per VISUAL_STYLE_GUIDE section 5
- Tier 1–2: strength 0.4, radius 0.3, threshold 0.8 / Tier 3: 0.8/0.5/0.6 / Tier 4–5: 1.4/0.8/0.4
- Rationale: this single change will do more to close the gap between v1 and the design intent than anything else on this list.

### Phase 1: Visual Integrity (make the globe look like the design system promises)

**1.1 — Integrate tier geometry files**
- File: `src/components/Globe.tsx` — replace `AgentBuilding` function entirely
- Import: `tier1-hut.ts`, `tier2-workshop.ts`, `tier3-tower.ts`, `tier4-spire.ts`, `tier5-monument.ts` from `../../visual-grammar/` (or copy/adapt to src)
- New component: `AgentStructure` that maps `agent.tier` → the correct builder function, passes `agent.id` as seed, passes `agent.work_score` for scale variation
- Call `userData.tick(delta)` in `useFrame` for all structure groups that expose it
- Rationale: the tier files are the actual visual grammar made real. Using box primitives while they exist unused is the defining embarrassment of v1.

**1.2 — Sun rotation with uTime**
- File: `src/components/Globe.tsx` — `earthFragmentShader`
- Replace hardcoded `vec3(1.4, 0.8, 1.2)` light direction with a rotation matrix applied to a base direction using `uTime`
- Rotation rate: one full day cycle every 120 seconds (fast enough to observe, slow enough to be calming)
- Update night-side city glow to use the same computed light direction
- Rationale: the city lights feature cannot be perceived unless the night side moves into view. The day/night cycle is also one of the most visually compelling features of the existing shader.

**1.3 — Remove dev controls from production**
- File: `src/App.tsx`
- Gate dev buttons behind `import.meta.env.DEV` (Vite environment flag)
- These should only render in development mode, never in the production bundle
- Rationale: live site shows buttons that undermine the authority of the visual.

**1.4 — N-to-N particle streams**
- File: `src/components/Globe.tsx` — replace `ParticleStream` component
- New component: `CollaborationArcs` — takes all working agents, generates all N-choose-2 pairs, renders a particle stream for each (using distinct but constrained arc parameters to avoid visual collision)
- Budget: cap at 20 simultaneous streams. If more than 20 pairs, prioritize pairs with highest combined work_score
- Rationale: a single stream between two agents looks like a bug, not a feature.

### Phase 2: Life (make the globe feel like it has a heartbeat)

**2.1 — WebSocket real-time updates**
- File: `src/App.tsx` (new hook) or new file `src/hooks/useGlobeSocket.ts`
- Connect to WS endpoint (endpoint exists per audit — confirm URL format)
- On message: merge incoming agent state delta into React state (partial updates, not full replacements)
- Fallback: if WS disconnects, fall back to polling `/api/v1/globe/snapshot` every 5s
- Rationale: a globe that updates in real time is a living thing. A globe that you load and then nothing changes is a poster.

**2.2 — Cinematic idle camera**
- File: `src/App.tsx` or new file `src/components/CinematicCamera.tsx`
- Implement idle camera behavior: slow orbital drift (0.008 rad/s, different axis from globe rotation), gentle breathing zoom (4.5↔2.8 units over 40s cycle)
- On user interaction: OrbitControls takes over smoothly (lerp transition over 0.4s)
- Optional: auto-zoom to region of highest activity every 90s idle, then drift back
- Use EASE_BREATHE curve for all transitions
- Rationale: OrbitControls is a power tool. The idle state should be a gallery.

**2.3 — Per-agent material seed variance**
- File: `src/components/Globe.tsx` (AgentStructure) and tier geometry files
- Each agent's structure should have micro-variation: emissive intensity ±15% from base, height ±5%, footprint ±5% (all seeded by `agent.id` hash)
- Existing tier files already support `seed` parameter — use it
- Rationale: identical buildings in a row break the illusion of organic civilization. Seed variation is a one-line change with major perceptual impact.

**2.4 — Ambient particle layer**
- New file: `src/components/AmbientParticles.tsx`
- Low-density cloud of 200 micro-particles at 1.01–1.04 radius from globe surface
- Color: `#00e5ff` at opacity 0.05–0.12
- Slow drift on spherical surface (not following gravity, following globe rotation)
- Rationale: adds atmospheric density, makes the globe feel inhabited even in regions with no agents.

**2.5 — Loading + transition ceremony**
- File: `src/App.tsx`
- Loading state: globe renders in darkness, data source is loading. After load, run a 2.5s "awakening" animation: bloom rises from zero, buildings materialize with construction scaffolding shader, atmosphere brightens
- Error state: clear visual indicator (not blank) with retry
- Rationale: the first impression is the brand. Make it ceremonial.

### Phase 3: Sensory Completion

**3.1 — Audio layer**
- New file: `src/audio/SurfaceAudio.ts`
- Ambient drone: synthesized low-frequency pad, 40-60 Hz, stereo, subtle. Starts at volume 0 on load, rises to 0.15 over 8s
- Agent activity chimes: spatial audio tied to agent position (Web Audio API PannerNode). Different chime per tier transition. Working agents produce a 880Hz soft tone at 0.03 volume
- Tier 5 monument: sub-bass thrum, 35-45 Hz sine sweep, spatial
- Mute control in UI (accessible, defaulting to auto-play if permitted by browser)
- Rationale: sound is the second data channel. Silence is a missed opportunity.

**3.2 — LOD system**
- File: `src/components/Globe.tsx`
- Implement distance-based LOD for agent structures: full geometry <100 units, simplified geometry 100–250, billboard 250–500, point-only >500 (per KIT.json global_rules)
- For agent dots at scale: use `InstancedMesh` for all idle-state dots (single draw call for N idle agents)
- Rationale: performance budget for 1000 agents. Without LOD, this breaks at 200.

**3.3 — Accessibility**
- File: `src/App.tsx` and shader files
- Detect `prefers-reduced-motion`: if true, disable all pulse animations, set globe rotation to 0, disable particle streams
- Implement color-safe variant: replace cyan/amber/magenta with patterns/intensity differences for accessibility mode
- Rationale: a site visible to everyone is a stronger site.

---

## V. ACCEPTANCE CRITERIA — HOW WE KNOW V2 IS DONE

V2 is done when a person looking at `surface.agentnation.in` can do all of the following without any tutorial or explanation:

1. **Tell which agents are working** by looking at the globe. (Color + pulse + beam)
2. **Tell which agents are most productive** by looking at building scale and tier. (Tier geometry visible and correct)
3. **Watch something change** within 30 seconds of loading. (Real-time data via WebSocket)
4. **Be affected by it visually.** The first reaction should not be "it's a tech demo." It should be "something is happening here." (Bloom + audio + cinematic camera)
5. **Find it still visually interesting after 5 minutes** due to depth of detail. (City lights, sun rotation, ambient particles, per-agent variance)

**Technical acceptance criteria:**
- 0 dev panel buttons visible in production build
- Real agent data loading (not stub-agents.json) confirmed by checking network tab
- Bloom post-processing confirmed active (glowing structures visually distinct from flat surfaces)
- Tier 1 through Tier 5 geometry correctly rendered (no primitive placeholders)
- Working agents connected by particle streams (N-to-N, not 1)
- Globe state updates within 3 seconds of backend event (WebSocket latency check)
- FPS stays above 55 on a mid-tier laptop with 100 agents in scene
- No console errors in production

V2 is not done if any of these criteria are unmet.

---

*Written by Vishwakarma, Architect of Surface. 2026-04-12.*
*Awaiting Ratnesh's approval before proceeding.*
