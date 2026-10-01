# Riverwood SWAT

**Lucan Valerius has asked about his Golden Claw for the last time.**

A Skyrim Special Edition mod that brings Ready or Not's battering ram to Riverwood. Equip the Breaching Ram, power-attack the Riverwood Trader's front door, and it slams open and puts you inside. Do it at night and Whiterun Hold puts a bounty on you, because a no-knock warrant still needs paperwork.

## What's here

| Path | What it is |
| --- | --- |
| `Source/Scripts/RoNRamBreachAlias.psc` | The breach: hit the door with a power attack → slam, camera shake, unlock, you're in. Optional Lucan reaction and night-time bounty. |
| `Source/Scripts/RoNRamBreachTarget.psc` | Fallback for when the door won't register melee hits: an invisible target over the doorway. |
| `tools/make_textures.py` | Packs and converts the exported Ready or Not textures into Skyrim's `ram.dds` and `ram_n.dds`. |
| `docs/GUIDE.md` | The full build: extracting the ram, Blender, NIF, Creation Kit, quest setup, testing. |

## What's not here

No Ready or Not assets. The ram's mesh, textures and sound belong to VOID Interactive, so this repo holds the code and instructions, and you port the ram from your own copy of the game. The same goes for anything from Skyrim.

Built `meshes/`, `textures/` and `sound/` folders are ignored by git so they don't end up here by accident.

## Quick start

1. Follow [docs/GUIDE.md](docs/GUIDE.md) steps 1–4 to get `breachingram.nif` and its textures.
2. Copy `Source/Scripts/*.psc` into your Skyrim `Data\Source\Scripts` folder.
3. Follow steps 5–6 in Creation Kit to make the weapon, the sound and the quest.
4. In game: `coc Riverwood`, `set gamehour to 22`, and knock.

## Status

Scripts written, not yet tested in game. The ram hasn't been ported yet.

## Credits

- Battering ram from *Ready or Not* by VOID Interactive.
- *The Elder Scrolls V: Skyrim* by Bethesda Game Studios.
- Not affiliated with either. Sorry, Lucan.
