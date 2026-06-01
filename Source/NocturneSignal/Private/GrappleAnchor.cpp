#include "GrappleAnchor.h"
#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"

AGrappleAnchor::AGrappleAnchor()
{
    PrimaryActorTick.bCanEverTick = false;

    AnchorRoot = CreateDefaultSubobject<USceneComponent>(TEXT("AnchorRoot"));
    SetRootComponent(AnchorRoot);

    AnchorDisplayMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("AnchorDisplayMesh"));
    AnchorDisplayMesh->SetupAttachment(AnchorRoot);
    AnchorDisplayMesh->SetCollisionProfileName(TEXT("BlockAll"));
    AnchorDisplayMesh->SetGenerateOverlapEvents(false);
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

bool AGrappleAnchor::ShouldPullAnchorToGrappler() const
{
    return bPullAnchorToGrappler;
}
