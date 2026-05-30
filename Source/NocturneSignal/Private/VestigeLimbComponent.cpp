#include "VestigeLimbComponent.h"
#include "GrappleAnchor.h"
#include "VestigeTentacleVisualAdapter.h"
#include "DrawDebugHelpers.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/GameplayStatics.h"

UVestigeLimbComponent::UVestigeLimbComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UVestigeLimbComponent::BeginPlay()
{
    Super::BeginPlay();

    if (!VisualAdapter && GetOwner())
    {
        VisualAdapter = GetOwner()->FindComponentByClass<UVestigeTentacleVisualAdapter>();
    }
}

void UVestigeLimbComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    if (GrappleState == EVestigeGrappleState::PullingPlayer)
    {
        TickPullToPoint(DeltaTime);
    }

    if (CurrentAnchor && VisualAdapter)
    {
        const FVector OwnerLocation = GetOwner() ? GetOwner()->GetActorLocation() : FVector::ZeroVector;
        VisualAdapter->UpdateLimbTarget(OwnerLocation, CurrentAnchor->GetAnchorLocation(), DeltaTime);
    }

    if (bDrawDebugGrapple && CurrentAnchor)
    {
        const FVector OwnerLocation = GetOwner() ? GetOwner()->GetActorLocation() : FVector::ZeroVector;
        DrawDebugLine(GetWorld(), OwnerLocation, CurrentAnchor->GetAnchorLocation(), FColor::Cyan, false, 0.0f, 0, 2.0f);
        DrawDebugSphere(GetWorld(), CurrentAnchor->GetAnchorLocation(), ArrivalRadius, 16, FColor::White, false, 0.0f);
    }
}

bool UVestigeLimbComponent::TryStartPullToPoint()
{
    if (!GetOwner() || GrappleState != EVestigeGrappleState::Idle)
    {
        LastFailureReason = EVestigeGrappleFailureReason::Interrupted;
        return false;
    }

    SetGrappleState(EVestigeGrappleState::SearchingForAnchor);

    AGrappleAnchor* Anchor = FindBestAnchor();
    if (!Anchor)
    {
        LastFailureReason = EVestigeGrappleFailureReason::NoValidAnchor;
        SetGrappleState(EVestigeGrappleState::Failed);
        SetGrappleState(EVestigeGrappleState::Idle);
        return false;
    }

    SetCurrentAnchor(Anchor);
    LastFailureReason = EVestigeGrappleFailureReason::None;
    CurrentPullVelocity = FVector::ZeroVector;

    SetGrappleState(EVestigeGrappleState::Extending);
    SetGrappleState(EVestigeGrappleState::Anchored);
    SetGrappleState(EVestigeGrappleState::PullingPlayer);
    return true;
}

void UVestigeLimbComponent::CancelGrapple()
{
    LastFailureReason = EVestigeGrappleFailureReason::Interrupted;
    CurrentPullVelocity = FVector::ZeroVector;

    if (VisualAdapter)
    {
        VisualAdapter->OnGrappleCancelled();
    }

    SetCurrentAnchor(nullptr);
    SetGrappleState(EVestigeGrappleState::Idle);
}

AGrappleAnchor* UVestigeLimbComponent::FindBestAnchor() const
{
    if (!GetOwner() || !GetWorld())
    {
        return nullptr;
    }

    TArray<AActor*> FoundActors;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), AGrappleAnchor::StaticClass(), FoundActors);

    const FVector OwnerLocation = GetOwner()->GetActorLocation();
    AGrappleAnchor* BestAnchor = nullptr;
    float BestDistanceSquared = TNumericLimits<float>::Max();
    const float MaxRangeSquared = MaxGrappleRange * MaxGrappleRange;

    for (AActor* Actor : FoundActors)
    {
        AGrappleAnchor* Anchor = Cast<AGrappleAnchor>(Actor);
        if (!Anchor || !Anchor->IsAvailableForStage(VestigeStage, CurrentCorruption))
        {
            continue;
        }

        const float DistanceSquared = FVector::DistSquared(OwnerLocation, Anchor->GetAnchorLocation());
        if (DistanceSquared > MaxRangeSquared)
        {
            continue;
        }

        if (DistanceSquared < BestDistanceSquared)
        {
            BestDistanceSquared = DistanceSquared;
            BestAnchor = Anchor;
        }
    }

    return BestAnchor;
}

void UVestigeLimbComponent::SetVisualAdapter(UVestigeTentacleVisualAdapter* NewVisualAdapter)
{
    VisualAdapter = NewVisualAdapter;
}

EVestigeGrappleState UVestigeLimbComponent::GetGrappleState() const
{
    return GrappleState;
}

AGrappleAnchor* UVestigeLimbComponent::GetCurrentAnchor() const
{
    return CurrentAnchor;
}

EVestigeGrappleFailureReason UVestigeLimbComponent::GetLastFailureReason() const
{
    return LastFailureReason;
}

void UVestigeLimbComponent::SetGrappleState(EVestigeGrappleState NewState)
{
    if (GrappleState == NewState)
    {
        return;
    }

    GrappleState = NewState;
    OnGrappleStateChanged.Broadcast(GrappleState);
    NotifyVisualAdapterForState(GrappleState);
}

void UVestigeLimbComponent::SetCurrentAnchor(AGrappleAnchor* NewAnchor)
{
    if (CurrentAnchor == NewAnchor)
    {
        return;
    }

    CurrentAnchor = NewAnchor;
    OnAnchorChanged.Broadcast(CurrentAnchor);

    if (VisualAdapter && CurrentAnchor)
    {
        VisualAdapter->OnGrappleAnchorSelected(CurrentAnchor);
    }
}

void UVestigeLimbComponent::NotifyVisualAdapterForState(EVestigeGrappleState NewState)
{
    if (!VisualAdapter)
    {
        return;
    }

    switch (NewState)
    {
    case EVestigeGrappleState::SearchingForAnchor:
        VisualAdapter->OnGrappleSearchStarted();
        break;
    case EVestigeGrappleState::Extending:
        VisualAdapter->OnGrappleExtendStarted(CurrentAnchor);
        break;
    case EVestigeGrappleState::PullingPlayer:
        VisualAdapter->OnGrapplePullStarted(CurrentAnchor);
        break;
    case EVestigeGrappleState::Releasing:
        VisualAdapter->OnGrappleReleased();
        break;
    default:
        break;
    }
}

void UVestigeLimbComponent::TickPullToPoint(float DeltaTime)
{
    ACharacter* OwnerCharacter = Cast<ACharacter>(GetOwner());
    if (!OwnerCharacter || !CurrentAnchor)
    {
        CancelGrapple();
        return;
    }

    const FVector OwnerLocation = OwnerCharacter->GetActorLocation();
    const FVector AnchorLocation = CurrentAnchor->GetAnchorLocation();
    const FVector ToAnchor = AnchorLocation - OwnerLocation;
    const float Distance = ToAnchor.Size();

    if (Distance <= FMath::Max(ArrivalRadius, CurrentAnchor->ArrivalRadius))
    {
        FinishGrappleRelease();
        return;
    }

    const FVector Direction = ToAnchor.GetSafeNormal();
    const FVector DesiredVelocity = Direction * PullSpeed;
    CurrentPullVelocity = FMath::VInterpConstantTo(CurrentPullVelocity, DesiredVelocity, DeltaTime, PullAcceleration);

    if (UCharacterMovementComponent* Movement = OwnerCharacter->GetCharacterMovement())
    {
        Movement->Velocity = CurrentPullVelocity;
    }
}

void UVestigeLimbComponent::FinishGrappleRelease()
{
    ACharacter* OwnerCharacter = Cast<ACharacter>(GetOwner());
    if (OwnerCharacter)
    {
        if (UCharacterMovementComponent* Movement = OwnerCharacter->GetCharacterMovement())
        {
            Movement->Velocity = CurrentPullVelocity * ExitVelocityScale;
        }
    }

    SetGrappleState(EVestigeGrappleState::Releasing);
    SetGrappleState(EVestigeGrappleState::Retracting);
    SetCurrentAnchor(nullptr);
    CurrentPullVelocity = FVector::ZeroVector;
    SetGrappleState(EVestigeGrappleState::Idle);
}
