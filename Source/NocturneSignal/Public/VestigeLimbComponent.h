#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "VestigeLimbComponent.generated.h"

class AGrappleAnchor;
class UVestigeTentacleVisualAdapter;

UENUM(BlueprintType)
enum class EVestigeGrappleState : uint8
{
    Idle UMETA(DisplayName = "Idle"),
    SearchingForAnchor UMETA(DisplayName = "Searching For Anchor"),
    Extending UMETA(DisplayName = "Extending"),
    Anchored UMETA(DisplayName = "Anchored"),
    PullingPlayer UMETA(DisplayName = "Pulling Player"),
    Releasing UMETA(DisplayName = "Releasing"),
    Retracting UMETA(DisplayName = "Retracting"),
    Failed UMETA(DisplayName = "Failed")
};

UENUM(BlueprintType)
enum class EVestigeGrappleFailureReason : uint8
{
    None UMETA(DisplayName = "None"),
    NoValidAnchor UMETA(DisplayName = "No Valid Anchor"),
    OutOfRange UMETA(DisplayName = "Out Of Range"),
    LineBlocked UMETA(DisplayName = "Line Blocked"),
    Interrupted UMETA(DisplayName = "Interrupted")
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FVestigeGrappleStateChanged, EVestigeGrappleState, NewState);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FVestigeAnchorChanged, AGrappleAnchor*, NewAnchor);

UCLASS(ClassGroup = (Nocturne), meta = (BlueprintSpawnableComponent))
class NOCTURNESIGNAL_API UVestigeLimbComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UVestigeLimbComponent();

    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Vestige Limb")
    bool TryStartPullToPoint();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Vestige Limb")
    void CancelGrapple();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Vestige Limb")
    AGrappleAnchor* FindBestAnchor();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Vestige Limb")
    void SetPreferredGrappleDirection(FVector NewDirection);

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Vestige Limb|Visuals")
    void SetVisualAdapter(UVestigeTentacleVisualAdapter* NewVisualAdapter);

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Vestige Limb")
    EVestigeGrappleState GetGrappleState() const;

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Vestige Limb")
    AGrappleAnchor* GetCurrentAnchor() const;

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Vestige Limb")
    EVestigeGrappleFailureReason GetLastFailureReason() const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Vestige Limb|Debug")
    FString GetLastAnchorSelectionDebug() const;

    UPROPERTY(BlueprintAssignable, Category = "Nocturne|Vestige Limb")
    FVestigeGrappleStateChanged OnGrappleStateChanged;

    UPROPERTY(BlueprintAssignable, Category = "Nocturne|Vestige Limb")
    FVestigeAnchorChanged OnAnchorChanged;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Tuning", meta = (ClampMin = "1"))
    int32 VestigeStage = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Tuning", meta = (ClampMin = "0.0", ClampMax = "1.0"))
    float CurrentCorruption = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Tuning", meta = (ClampMin = "1.0"))
    float MaxGrappleRange = 900.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Tuning", meta = (ClampMin = "1.0"))
    float PullSpeed = 1450.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Tuning", meta = (ClampMin = "1.0"))
    float PullAcceleration = 5200.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Tuning", meta = (ClampMin = "1.0"))
    float ArrivalRadius = 24.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Tuning", meta = (ClampMin = "0.0", ClampMax = "2.0"))
    float ExitVelocityScale = 0.65f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Tuning", meta = (ClampMin = "0.0", ClampMax = "1.0"))
    float GrappleExtendDuration = 0.12f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Tuning", meta = (ClampMin = "0.0", ClampMax = "1.0"))
    float GrappleReleaseDuration = 0.18f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Tuning", meta = (ClampMin = "0.0"))
    float DirectionalAnchorScoreBonus = 450.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Tuning", meta = (ClampMin = "-1.0", ClampMax = "1.0"))
    float MinimumDirectionalDot = -0.2f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Tuning")
    bool bRequireAnchorLineOfSight = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Tuning")
    TEnumAsByte<ECollisionChannel> AnchorLineOfSightChannel = ECC_Visibility;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Debug")
    bool bDrawDebugGrapple = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Limb|Debug")
    bool bDrawDebugOverlay = false;

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Vestige Limb|Debug", meta = (AllowPrivateAccess = "true"))
    int32 LastAnchorCandidatesEvaluated = 0;

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Vestige Limb|Debug", meta = (AllowPrivateAccess = "true"))
    int32 LastAnchorCandidatesInRange = 0;

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Vestige Limb|Debug", meta = (AllowPrivateAccess = "true"))
    int32 LastAnchorCandidatesVisible = 0;

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Vestige Limb|Debug", meta = (AllowPrivateAccess = "true"))
    int32 LastAnchorCandidatesDirectionallyValid = 0;

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Vestige Limb|Debug", meta = (AllowPrivateAccess = "true"))
    float LastBestAnchorScore = 0.0f;

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Vestige Limb|Debug", meta = (AllowPrivateAccess = "true"))
    FString LastAnchorSelectionDebug;

private:
    void SetGrappleState(EVestigeGrappleState NewState);
    void SetCurrentAnchor(AGrappleAnchor* NewAnchor);
    void NotifyVisualAdapterForState(EVestigeGrappleState NewState);
    bool HasLineOfSightToAnchor(const AGrappleAnchor& Anchor) const;
    void DrawDebugOverlay() const;
    void TickTimedGrappleState(float DeltaTime);
    void SetTimedGrappleState(EVestigeGrappleState NewState, float DurationSeconds);
    void AdvanceFromExtendingState();
    void AdvanceFromReleasingState();
    void TickPullToPoint(float DeltaTime);
    void TickPullAnchorToOwner(float DeltaTime);
    FVector GetAnchorPullTargetLocation(const AActor& OwnerActor) const;
    void FinishGrappleRelease(bool bApplyOwnerExitVelocity = true);

    UPROPERTY(Transient)
    AGrappleAnchor* CurrentAnchor = nullptr;

    UPROPERTY(Transient)
    UVestigeTentacleVisualAdapter* VisualAdapter = nullptr;

    EVestigeGrappleState GrappleState = EVestigeGrappleState::Idle;
    EVestigeGrappleFailureReason LastFailureReason = EVestigeGrappleFailureReason::None;
    FVector CurrentPullVelocity = FVector::ZeroVector;
    FVector PreferredGrappleDirection = FVector::RightVector;
    bool bPullingAnchorToOwner = false;
    float TimedStateRemainingSeconds = 0.0f;
};
