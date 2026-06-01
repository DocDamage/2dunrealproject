#include "VestigeLimbComponent.h"
#include "GrappleAnchor.h"
#include "VestigeTentacleVisualAdapter.h"
#include "DrawDebugHelpers.h"
#include "Engine/Engine.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/GameplayStatics.h"

namespace
{
constexpr uint64 VestigeDebugOverlayKey = 0x76535447;
}

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

    TickTimedGrappleState(DeltaTime);

    if (GrappleState == EVestigeGrappleState::PullingPlayer)
    {
        if (CurrentAnchor && (bPullingAnchorToOwner || CurrentAnchor->ShouldPullAnchorToGrappler()))
        {
            TickPullAnchorToOwner(DeltaTime);
        }
        else
        {
            TickPullToPoint(DeltaTime);
        }
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

    DrawDebugOverlay();
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
        if (LastAnchorCandidatesDirectionallyValid > 0 && LastAnchorCandidatesVisible == 0)
        {
            LastFailureReason = EVestigeGrappleFailureReason::LineBlocked;
        }
        else if (LastAnchorCandidatesEvaluated > 0 && LastAnchorCandidatesInRange == 0)
        {
            LastFailureReason = EVestigeGrappleFailureReason::OutOfRange;
        }
        else
        {
            LastFailureReason = EVestigeGrappleFailureReason::NoValidAnchor;
        }
        SetGrappleState(EVestigeGrappleState::Failed);
        SetGrappleState(EVestigeGrappleState::Idle);
        return false;
    }

    SetCurrentAnchor(Anchor);
    bPullingAnchorToOwner = Anchor->ShouldPullAnchorToGrappler();
    LastFailureReason = EVestigeGrappleFailureReason::None;
    CurrentPullVelocity = FVector::ZeroVector;

    SetTimedGrappleState(EVestigeGrappleState::Extending, GrappleExtendDuration);
    return true;
}

void UVestigeLimbComponent::CancelGrapple()
{
    LastFailureReason = EVestigeGrappleFailureReason::Interrupted;
    CurrentPullVelocity = FVector::ZeroVector;
    bPullingAnchorToOwner = false;
    TimedStateRemainingSeconds = 0.0f;

    if (VisualAdapter)
    {
        VisualAdapter->OnGrappleCancelled();
    }

    SetCurrentAnchor(nullptr);
    SetGrappleState(EVestigeGrappleState::Idle);
}

AGrappleAnchor* UVestigeLimbComponent::FindBestAnchor()
{
    if (!GetOwner() || !GetWorld())
    {
        LastAnchorCandidatesEvaluated = 0;
        LastAnchorCandidatesInRange = 0;
        LastAnchorCandidatesVisible = 0;
        LastAnchorCandidatesDirectionallyValid = 0;
        LastBestAnchorScore = 0.0f;
        LastAnchorSelectionDebug = TEXT("No owner or world.");
        return nullptr;
    }

    LastAnchorCandidatesEvaluated = 0;
    LastAnchorCandidatesInRange = 0;
    LastAnchorCandidatesVisible = 0;
    LastAnchorCandidatesDirectionallyValid = 0;
    LastBestAnchorScore = 0.0f;
    LastAnchorSelectionDebug = TEXT("No valid anchor found.");

    TArray<AActor*> FoundActors;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), AGrappleAnchor::StaticClass(), FoundActors);

    const FVector OwnerLocation = GetOwner()->GetActorLocation();
    AGrappleAnchor* BestAnchor = nullptr;
    float BestScore = TNumericLimits<float>::Max();
    const float MaxRangeSquared = MaxGrappleRange * MaxGrappleRange;
    const FVector PreferredDirection = PreferredGrappleDirection.GetSafeNormal();

    for (AActor* Actor : FoundActors)
    {
        AGrappleAnchor* Anchor = Cast<AGrappleAnchor>(Actor);
        if (!Anchor || !Anchor->IsAvailableForStage(VestigeStage, CurrentCorruption))
        {
            continue;
        }
        ++LastAnchorCandidatesEvaluated;

        const float DistanceSquared = FVector::DistSquared(OwnerLocation, Anchor->GetAnchorLocation());
        if (DistanceSquared > MaxRangeSquared)
        {
            continue;
        }
        ++LastAnchorCandidatesInRange;

        const FVector ToAnchor = (Anchor->GetAnchorLocation() - OwnerLocation).GetSafeNormal();
        const float DirectionDot = FVector::DotProduct(PreferredDirection, ToAnchor);
        if (DirectionDot < MinimumDirectionalDot)
        {
            continue;
        }
        ++LastAnchorCandidatesDirectionallyValid;

        if (!HasLineOfSightToAnchor(*Anchor))
        {
            continue;
        }
        ++LastAnchorCandidatesVisible;

        const float Distance = FMath::Sqrt(DistanceSquared);
        const float Score = Distance - (FMath::Max(0.0f, DirectionDot) * DirectionalAnchorScoreBonus);

        if (Score < BestScore)
        {
            BestScore = Score;
            BestAnchor = Anchor;
        }
    }

    if (BestAnchor)
    {
        LastBestAnchorScore = BestScore;
        LastAnchorSelectionDebug = FString::Printf(
            TEXT("Selected %s. Evaluated=%d InRange=%d Directional=%d Visible=%d Score=%.1f"),
            *BestAnchor->GetName(),
            LastAnchorCandidatesEvaluated,
            LastAnchorCandidatesInRange,
            LastAnchorCandidatesDirectionallyValid,
            LastAnchorCandidatesVisible,
            LastBestAnchorScore);
    }
    else
    {
        LastAnchorSelectionDebug = FString::Printf(
            TEXT("No valid anchor. Evaluated=%d InRange=%d Directional=%d Visible=%d"),
            LastAnchorCandidatesEvaluated,
            LastAnchorCandidatesInRange,
            LastAnchorCandidatesDirectionallyValid,
            LastAnchorCandidatesVisible);
    }

    return BestAnchor;
}

void UVestigeLimbComponent::SetPreferredGrappleDirection(FVector NewDirection)
{
    NewDirection.Z = 0.0f;
    if (!NewDirection.Normalize())
    {
        return;
    }

    PreferredGrappleDirection = NewDirection;
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

FString UVestigeLimbComponent::GetLastAnchorSelectionDebug() const
{
    return LastAnchorSelectionDebug;
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
    case EVestigeGrappleState::Failed:
        VisualAdapter->OnGrappleCancelled();
        break;
    default:
        break;
    }
}

bool UVestigeLimbComponent::HasLineOfSightToAnchor(const AGrappleAnchor& Anchor) const
{
    if (!bRequireAnchorLineOfSight || !GetOwner() || !GetWorld())
    {
        return true;
    }

    FHitResult Hit;
    FCollisionQueryParams QueryParams(SCENE_QUERY_STAT(VestigeAnchorLineOfSight), false);
    QueryParams.AddIgnoredActor(GetOwner());
    QueryParams.AddIgnoredActor(&Anchor);

    const FVector Start = GetOwner()->GetActorLocation();
    const FVector End = Anchor.GetAnchorLocation();
    const bool bHit = GetWorld()->LineTraceSingleByChannel(
        Hit,
        Start,
        End,
        AnchorLineOfSightChannel,
        QueryParams);

    return !bHit;
}

void UVestigeLimbComponent::TickTimedGrappleState(float DeltaTime)
{
    if (GrappleState != EVestigeGrappleState::Extending
        && GrappleState != EVestigeGrappleState::Releasing)
    {
        return;
    }

    TimedStateRemainingSeconds -= FMath::Max(DeltaTime, 0.0f);
    if (TimedStateRemainingSeconds > 0.0f)
    {
        return;
    }

    if (GrappleState == EVestigeGrappleState::Extending)
    {
        AdvanceFromExtendingState();
    }
    else if (GrappleState == EVestigeGrappleState::Releasing)
    {
        AdvanceFromReleasingState();
    }
}

void UVestigeLimbComponent::SetTimedGrappleState(EVestigeGrappleState NewState, float DurationSeconds)
{
    TimedStateRemainingSeconds = FMath::Max(DurationSeconds, 0.0f);
    SetGrappleState(NewState);

    if (TimedStateRemainingSeconds > 0.0f)
    {
        return;
    }

    if (NewState == EVestigeGrappleState::Extending)
    {
        AdvanceFromExtendingState();
    }
    else if (NewState == EVestigeGrappleState::Releasing)
    {
        AdvanceFromReleasingState();
    }
}

void UVestigeLimbComponent::AdvanceFromExtendingState()
{
    if (GrappleState != EVestigeGrappleState::Extending)
    {
        return;
    }

    if (!CurrentAnchor)
    {
        CancelGrapple();
        return;
    }

    TimedStateRemainingSeconds = 0.0f;
    SetGrappleState(EVestigeGrappleState::Anchored);
    SetGrappleState(EVestigeGrappleState::PullingPlayer);
}

void UVestigeLimbComponent::AdvanceFromReleasingState()
{
    if (GrappleState != EVestigeGrappleState::Releasing)
    {
        return;
    }

    TimedStateRemainingSeconds = 0.0f;
    SetGrappleState(EVestigeGrappleState::Retracting);
    SetCurrentAnchor(nullptr);
    SetGrappleState(EVestigeGrappleState::Idle);
}

void UVestigeLimbComponent::DrawDebugOverlay() const
{
    if (!bDrawDebugOverlay || !GEngine)
    {
        return;
    }

    const ACharacter* OwnerCharacter = Cast<ACharacter>(GetOwner());
    const UCharacterMovementComponent* Movement = OwnerCharacter ? OwnerCharacter->GetCharacterMovement() : nullptr;
    const float Speed = Movement ? Movement->Velocity.Size() : 0.0f;

    float DistanceToAnchor = 0.0f;
    if (OwnerCharacter && CurrentAnchor)
    {
        DistanceToAnchor = FVector::Dist(OwnerCharacter->GetActorLocation(), CurrentAnchor->GetAnchorLocation());
    }

    const FString DebugText = FString::Printf(
        TEXT("Vestige | State=%s Failure=%s Anchor=%s Dist=%.0f Speed=%.0f\nCandidates | Total=%d Range=%d Direction=%d Visible=%d Score=%.1f\n%s"),
        *StaticEnum<EVestigeGrappleState>()->GetNameStringByValue(static_cast<int64>(GrappleState)),
        *StaticEnum<EVestigeGrappleFailureReason>()->GetNameStringByValue(static_cast<int64>(LastFailureReason)),
        *GetNameSafe(CurrentAnchor),
        DistanceToAnchor,
        Speed,
        LastAnchorCandidatesEvaluated,
        LastAnchorCandidatesInRange,
        LastAnchorCandidatesDirectionallyValid,
        LastAnchorCandidatesVisible,
        LastBestAnchorScore,
        *LastAnchorSelectionDebug);

    GEngine->AddOnScreenDebugMessage(
        VestigeDebugOverlayKey,
        0.0f,
        LastFailureReason == EVestigeGrappleFailureReason::None ? FColor::Cyan : FColor::Yellow,
        DebugText);
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
        FinishGrappleRelease(true);
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

FVector UVestigeLimbComponent::GetAnchorPullTargetLocation(const AActor& OwnerActor) const
{
    FVector PullDirection = PreferredGrappleDirection;
    PullDirection.Z = 0.0f;
    if (!PullDirection.Normalize() || FMath::Abs(PullDirection.X) < KINDA_SMALL_NUMBER)
    {
        PullDirection = FVector::ForwardVector;
    }

    FVector TargetLocation = CurrentAnchor ? CurrentAnchor->GetActorLocation() : OwnerActor.GetActorLocation();
    TargetLocation.X = OwnerActor.GetActorLocation().X + PullDirection.X * 95.0f;
    TargetLocation.Y = OwnerActor.GetActorLocation().Y;
    return TargetLocation;
}

void UVestigeLimbComponent::TickPullAnchorToOwner(float DeltaTime)
{
    AActor* OwnerActor = GetOwner();
    if (!OwnerActor || !CurrentAnchor)
    {
        CancelGrapple();
        return;
    }

    const FVector TargetLocation = GetAnchorPullTargetLocation(*OwnerActor);
    const FVector AnchorLocation = CurrentAnchor->GetActorLocation();
    const float Distance = FVector::Dist(AnchorLocation, TargetLocation);
    if (Distance <= FMath::Max(ArrivalRadius, CurrentAnchor->ArrivalRadius))
    {
        CurrentAnchor->SetActorLocation(TargetLocation, true);
        FinishGrappleRelease(false);
        return;
    }

    const FVector NewLocation = FMath::VInterpConstantTo(AnchorLocation, TargetLocation, DeltaTime, PullSpeed);
    CurrentAnchor->SetActorLocation(NewLocation, true);
}

void UVestigeLimbComponent::FinishGrappleRelease(bool bApplyOwnerExitVelocity)
{
    ACharacter* OwnerCharacter = Cast<ACharacter>(GetOwner());
    if (bApplyOwnerExitVelocity && OwnerCharacter)
    {
        if (UCharacterMovementComponent* Movement = OwnerCharacter->GetCharacterMovement())
        {
            Movement->Velocity = CurrentPullVelocity * ExitVelocityScale;
        }
    }

    CurrentPullVelocity = FVector::ZeroVector;
    bPullingAnchorToOwner = false;
    SetTimedGrappleState(EVestigeGrappleState::Releasing, GrappleReleaseDuration);
}
