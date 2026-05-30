#include "GrappleAnchor.h"

AGrappleAnchor::AGrappleAnchor()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AGrappleAnchor::BeginPlay()
{
    Super::BeginPlay();
}

bool AGrappleAnchor::IsAvailableForStage(int32 VestigeStage, float CurrentCorruption) const
{
    if (!bIsActive)
    {
        return false;
    }

    if (VestigeStage < RequiredStage)
    {
        return false;
    }

    return CurrentCorruption >= RequiredCorruption;
}

FVector AGrappleAnchor::GetAnchorLocation() const
{
    return GetActorLocation();
}
