Scriptname RoNRamBreachAlias extends ReferenceAlias
{Attach to a quest alias filled with the Riverwood Trader's front door.
A power attack with the Breaching Ram slams the door, unlocks it and sends the player inside.}

Weapon Property BreachingRam Auto
{RoNBreachingRam}
Sound Property RamImpact Auto
{RoNRamImpactMarker}

; Optional extras. Leave unfilled to skip them.
Faction Property CrimeFactionWhiterun Auto
{Fill to add a bounty for night-time breaches.}
GlobalVariable Property GameHour Auto
Scene Property LucanReactScene Auto
{Fill with a scene where Lucan reacts. Unvoiced lines need Fuz Ro D-oh.}

Int Property NightBounty = 40 Auto

bool busy = false

Event OnHit(ObjectReference akAggressor, Form akSource, Projectile akProjectile, bool abPowerAttack, bool abSneakAttack, bool abBashAttack, bool abHitBlocked)
    if busy || akAggressor != Game.GetPlayer() || akSource != BreachingRam || !abPowerAttack
        return
    endif
    busy = true

    ObjectReference door = GetReference()
    Breach(door, akAggressor)

    busy = false
EndEvent

Function Breach(ObjectReference door, ObjectReference akBreacher)
    RamImpact.Play(door)
    Game.ShakeCamera(None, 0.6, 0.4)
    Utility.Wait(0.3)

    bool wasLocked = door.IsLocked()
    door.Lock(false)
    door.Activate(akBreacher)

    Utility.Wait(1.5)
    if LucanReactScene
        LucanReactScene.Start()
    else
        Debug.Notification("Lucan: By the Eight! What are you doing?!")
    endif

    if wasLocked && CrimeFactionWhiterun && GameHour
        float hour = GameHour.GetValue()
        if hour >= 20.0 || hour < 6.0
            CrimeFactionWhiterun.ModCrimeGold(NightBounty)
        endif
    endif
EndFunction
