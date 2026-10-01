# Riverwood SWAT: the full guide

Eight steps from Ready or Not's battering ram to Lucan Valerius's living room. Budget a weekend, most of it in Blender.

## Tools

| Tool | What it's for |
| --- | --- |
| [FModel](https://github.com/4sval/FModel) | Browsing Ready or Not's `.pak` files and exporting the ram |
| Blender 4.x | Cleaning, scaling and orienting the mesh |
| PyNifly (Blender add-on) | Exporting Skyrim `.nif` models |
| NifSkope 2.0 Dev | Checking and fixing the NIF |
| texconv (DirectXTex) + Python with Pillow | Textures to `.dds` via `tools/make_textures.py` |
| Creation Kit (Special Edition) | Weapon, sound, quest, script |
| vgmstream | Only if the sound is in Wwise `.wem` files |
| xEdit (SSEEdit) | Optional: checking the `.esp` |

Assumes Skyrim Special Edition and Mod Organizer 2 or Vortex. Build everything in one mod folder named `RoNBreachingRam`.

## Step 1: Extract the ram from Ready or Not

1. Open FModel. In **Directory Selector**, point it at `...\steamapps\common\Ready Or Not\ReadyOrNot\Content\Paks`.
2. Set **UE Versions** to the game's engine version. If archives open empty or error out, the version is wrong; the Ready or Not modding community lists the current one.
3. If it asks for an AES key, leave it blank first. If that fails, the modding wiki or Discord has it.
4. In **Settings → Models**, export meshes as **glTF 2.0** (or `.psk` if you use the PSK importer) and textures as **PNG**.
5. **Packages → Search** (Ctrl+Shift+F) for `ram`, `breach` or `battering`. Look under weapon and gadget folders.
6. Double-click to preview, then right-click the mesh → **Save Model**.
7. If textures didn't come along, open the mesh's material (`M_`/`MI_`) to see which it uses (base color, normal, packed roughness/metal) and **Save Texture** on each.
8. For the sound, search `ram`, `breach` or `door_kick` in the audio folders. Convert `.wem` files to `.wav` with vgmstream.

## Step 2: Prepare the mesh in Blender

Skyrim puts a weapon's origin at the player's hand, so copy a vanilla warhammer's setup.

1. Install PyNifly (**Edit → Preferences → Add-ons → Install**) and set its Skyrim SE path.
2. Extract `meshes\weapons\steel\steelwarhammer.nif` from `Skyrim - Meshes0.bsa` with BSA Browser.
3. Import the warhammer (**File → Import → NIF**). Note its length, which way the head points, and where the grip sits on the origin.
4. Import your ram.
5. **Scale:** 1 Skyrim unit is about 1.43 cm. Make the ram about the warhammer's length, then **Ctrl+A → All Transforms**.
6. **Orientation:** point it the same way as the warhammer's head, apply rotation.
7. **Grip:** move the mesh so the rear handle sits where the warhammer's grip meets the origin. Apply.
8. **Clean up:** delete sockets, LODs and Unreal collision; join parts (Ctrl+J); triangulate; keep it under about 20,000 triangles; fix normals (Shift+N); one UV map.
9. Hide or delete the reference warhammer and save the `.blend`.

## Step 3: Convert the textures

| Skyrim file | Made from | Format |
| --- | --- | --- |
| `ram.dds` | RoN base color | BC7 |
| `ram_n.dds` | RoN normal in RGB, inverted roughness in alpha (specular) | BC7 |

The script in `tools/` does the channel packing, resizing and conversion:

```
pip install pillow
python tools/make_textures.py --base T_Ram_BC.png --normal T_Ram_N.png --rough T_Ram_ORM.png --rough-channel G --out <mod folder>\textures\RoNBreachingRam
```

Check which channel of the packed map is roughness before you run it. If the dents look inverted in game, rerun with `--flip-green`.

## Step 4: Export the NIF and fix it in NifSkope

**Export**

1. Point the material's image texture nodes at `textures\RoNBreachingRam\ram.dds` and `ram_n.dds`.
2. Select the ram, **File → Export → NIF**, game **Skyrim SE**.
3. Save as `meshes\RoNBreachingRam\breachingram.nif` in the mod folder.

**Fix**

1. Open your NIF and the vanilla `steelwarhammer.nif` side by side.
2. **BSLightingShaderProperty → BSShaderTextureSet:** slot 0 is `textures\RoNBreachingRam\ram.dds`, slot 1 is `ram_n.dds`. No absolute `C:\` paths.
3. **Collision:** in the warhammer, right-click **bhkCollisionObject → Block → Copy Branch**; in yours, right-click the root → **Block → Paste Branch**.
4. Match the root node type and flags to the warhammer (usually **BSFadeNode**).
5. **Render → Settings → Show Collision** to check the box covers the ram. Save.

## Step 5: The weapon and sound in Creation Kit

**Plugin:** launch CK through your mod manager. **File → Data**, tick `Skyrim.esm` and `Update.esm`, OK. Save as `RoNBreachingRam.esp`.

**Weapon**

1. **Items → Weapon**, open `SteelWarhammer`, change the ID to `RoNBreachingRam`, OK, **Yes** to create a new form.
2. Name: **Breaching Ram**. Model: `meshes\RoNBreachingRam\breachingram.nif`. Weight 25–35. Keep the `WeapTypeWarhammer` keyword and two-handed animation type.

**Sound** (Papyrus plays a Sound Marker → Sound Descriptor → file)

1. Save the sound as 16-bit PCM `.wav`, 44.1 kHz, at `sound\fx\RoNBreachingRam\ram_impact.wav`.
2. **Audio → Sound Descriptor → New:** ID `RoNRamImpactSD`, add the file, SFX category, mono 3D output model (copy a vanilla impact descriptor's settings).
3. **Audio → Sound Marker → New:** ID `RoNRamImpactMarker`, descriptor `RoNRamImpactSD`.
4. Save.

## Step 6: The breach script

The script sits on a quest alias pointing at the door, so no vanilla reference gets edited.

**Set up compiling:** extract `Data\Scripts.zip` so the `.psc` files land in `Data\Source\Scripts`. Copy this repo's `Source\Scripts\*.psc` there too.

1. **Character → Quest → New:** ID `RoNBreachQuest`, name "Breaching Ram". Tick **Start Game Enabled** and **Run Once**. OK, then reopen.
2. In **Cell View**, world space **Tamriel**, load Riverwood and find the Riverwood Trader's front door.
3. **Quest Aliases → New Reference Alias**, name `LucanDoor`.
4. **Fill Type:** Specific Reference → Select Forced Reference → Select Reference in Render Window, click the door. Leave Optional unticked.
5. **Scripts → Add →** `RoNRamBreachAlias` (from this repo). Compile.
6. **Properties → Auto-Fill All**. Set `BreachingRam` to `RoNBreachingRam` and `RamImpact` to `RoNRamImpactMarker` by hand if needed.
7. Save.

**If the door ignores hits:** use `RoNRamBreachTarget.psc` instead. Duplicate an invisible collision activator as `RoNBreachTarget`, place it over the doorway with collision on the weapon layer, attach the script, and point `TargetDoor` at the door. This edits the Riverwood exterior cell, so load it after other Riverwood mods.

## Step 7 (optional): Lucan's reaction

`RoNRamBreachAlias` already has the hooks; leave any of these unfilled to skip it.

- **Subtitle:** with no scene filled, it shows "Lucan: By the Eight! What are you doing?!" a moment after you break in.
- **Bounty:** fill `CrimeFactionWhiterun` and `GameHour`. Breaching a locked door between 8 p.m. and 6 a.m. adds `NightBounty` (40) to your Whiterun bounty.
- **Scene:** add a `Lucan` alias (forced to Lucan Valerius in the Riverwood Trader interior), make a one-phase scene with his line, and fill `LucanReactScene`. Install Fuz Ro D-oh so unvoiced lines show as subtitles. For cowering, add an idle from **Gameplay → Animations** (search "cower").

## Step 8: Test and troubleshoot

```
RoNBreachingRam/
├── RoNBreachingRam.esp
├── meshes/RoNBreachingRam/breachingram.nif
├── textures/RoNBreachingRam/ram.dds, ram_n.dds
├── sound/fx/RoNBreachingRam/ram_impact.wav
└── scripts/RoNRamBreachAlias.pex
```

1. Load a save, open the console (backtick).
2. `help "breaching ram" 4` for the form ID, then `player.additem <form ID> 1`, and equip it.
3. `coc Riverwood`, walk to the Riverwood Trader.
4. `set gamehour to 22` so the door is locked.
5. Power-attack the door: slam, shake, inside. A normal swing or another weapon should do nothing.

| What you see | Likely cause | Fix |
| --- | --- | --- |
| Red exclamation mark | Game can't read the NIF | Check the Model path; re-export for Skyrim SE |
| Purple ram | Texture paths wrong | Fix BSShaderTextureSet paths (Step 4) |
| Held wrong or sideways | Origin or rotation | Redo Step 2 against the warhammer |
| Falls through the floor | No collision | Paste the warhammer's collision (Step 4) |
| Nothing at the door | Quest not running or empty properties | `sqv RoNBreachQuest`; `startquest RoNBreachQuest`; check properties |
| Quest runs, door ignores hits | Door doesn't send `OnHit` | Use `RoNRamBreachTarget` (Step 6) |
| No sound | File format or missing marker | 16-bit PCM `.wav`; marker points to descriptor |
| Works on a new game, not an old save | Quest cached in the save | Use a save from before install, or `startquest` |
