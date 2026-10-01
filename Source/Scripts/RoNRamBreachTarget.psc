Scriptname RoNRamBreachTarget extends ObjectReference
{Fallback for doors that don't receive OnHit from melee.
Attach to an invisible activator with collision placed in front of the door,
and point TargetDoor at the door itself.}

Weapon Property BreachingRam Auto
Sound Property RamImpact Auto
ObjectReference Property TargetDoor Auto

bool busy = false

Event OnHit(ObjectReference akAggressor, Form akSource, Projectile akProjectile, bool abPowerAttack, bool abSneakAttack, bool abBashAttack, bool abHitBlocked)
    if busy || akAggressor != Game.GetPlayer() || akSource != BreachingRam || !abPowerAttack
        return
    endif
    busy = true

    RamImpact.Play(TargetDoor)
    Game.ShakeCamera(None, 0.6, 0.4)
    Utility.Wait(0.3)
    TargetDoor.Lock(false)
    TargetDoor.Activate(akAggressor)

    busy = false
EndEvent
