#include "VestigeTentacleVisualAdapter.h"
#include "DrawDebugHelpers.h"
#include "GrappleAnchor.h"

UVestigeTentacleVisualAdapter::UVestigeTentacleVisualAdapter()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UVestigeTentacleVisualAdapter::OnGrappleSearchStarted_Implementation()
{
}

void UVestigeTentacleVisualAdapter::OnGrappleAnchorSelected_Implementation(AGrappleAnchor* Anchor)
{
}

void UVestigeTentacleVisualAdapter::OnGrappleExtendStarted_Implementation(AGrappleAnchor* Anchor)
{
}

void UVestigeTentacleVisualAdapter::OnGrapplePullStarted_Implementation(AGrappleAnchor* Anchor)
{
}

void UVestigeTentacleVisualAdapter::OnGrappleReleased_Implementation()
{
}

void UVestigeTentacleVisualAdapter::OnGrappleCancelled_Implementation()
{
}

void UVestigeTentacleVisualAdapter::UpdateLimbTarget_Implementation(FVector WorldStart, FVector WorldEnd, float DeltaSeconds)
{
    if (!bDrawFallbackDebugLine || !GetWorld())
    {
        return;
    }

    DrawDebugLine(GetWorld(), WorldStart, WorldEnd, FColor::Blue, false, 0.0f, 0, 3.0f);
}
