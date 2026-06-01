#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "TimerManager.h"
#include "VestigeLimbComponent.h"
#include "NocturnePlayerCharacter.generated.h"

class UAnimMontage;
class UAnimationAsset;
class UCameraComponent;
class AController;
class UInputAction;
class UInputMappingContext;
class UPaperFlipbookComponent;
class USpringArmComponent;
class UVestigeTentacleVisualAdapter;
struct FInputActionValue;

UENUM(BlueprintType)
enum class ENocturneJacobAbilityAnimation : uint8
{
    None UMETA(DisplayName = "None"),
    Jump UMETA(DisplayName = "Jump"),
    DoubleJump UMETA(DisplayName = "Double Jump"),
    Slide UMETA(DisplayName = "Slide"),
    TentacleAttack UMETA(DisplayName = "Tentacle Attack"),
    TentacleGrapple UMETA(DisplayName = "Tentacle Grapple"),
    TentacleConsume UMETA(DisplayName = "Tentacle Consume"),
    RecoveredCombat UMETA(DisplayName = "Recovered Combat")
};

UENUM(BlueprintType)
enum class ENocturneJacobRecoveredCombatMontage : uint8
{
    FireTrailAction01 UMETA(DisplayName = "FireTrail Action 01"),
    FireTrailAction08 UMETA(DisplayName = "FireTrail Action 08"),
    FireTrailAction16 UMETA(DisplayName = "FireTrail Action 16"),
    FightingCrossPunch UMETA(DisplayName = "Fighting Cross Punch"),
    FightingHookPunch UMETA(DisplayName = "Fighting Hook Punch"),
    FightingElbowPunch UMETA(DisplayName = "Fighting Elbow Punch"),
    FightingImpact UMETA(DisplayName = "Fighting Impact"),
    FightingDeath UMETA(DisplayName = "Fighting Death")
};

UCLASS(Blueprintable)
class NOCTURNESIGNAL_API ANocturnePlayerCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    ANocturnePlayerCharacter();

    virtual void Tick(float DeltaSeconds) override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Movement")
    void MoveHorizontal(float AxisValue);

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Movement")
    void StartJump();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Movement")
    void StopJump();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Movement")
    bool StartSlide();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Movement")
    void StopSlide();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Vestige")
    bool TryVestigeGrapple();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Vestige")
    bool TriggerTentacleGrapple();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Combat")
    bool TriggerTentacleAttack();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Combat")
    bool TriggerTentacleConsume(bool bUseAlternateConsume = false);

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Combat")
    bool TriggerRecoveredCombatMontage(ENocturneJacobRecoveredCombatMontage MontageId);

    UFUNCTION(BlueprintPure, Category = "Nocturne|Combat")
    UAnimMontage* GetRecoveredCombatMontage(ENocturneJacobRecoveredCombatMontage MontageId) const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Vestige")
    UVestigeLimbComponent* GetVestigeLimbComponent() const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Animation")
    bool IsSliding() const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Animation")
    bool IsDoubleJumping() const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Animation")
    bool IsTentacleActionActive() const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Animation")
    bool IsJacobMontagePlaying() const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Animation")
    bool IsTentacleVisualVisible() const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Animation")
    ENocturneJacobAbilityAnimation GetCurrentAbilityAnimation() const;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nocturne|Components")
    TObjectPtr<UVestigeLimbComponent> VestigeLimbComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nocturne|Components")
    TObjectPtr<UVestigeTentacleVisualAdapter> VestigeTentacleVisualAdapter;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nocturne|Components")
    TObjectPtr<USpringArmComponent> CameraBoom;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nocturne|Components")
    TObjectPtr<UCameraComponent> SideViewCamera;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Movement", meta = (ClampMin = "0.0"))
    float GroundAcceleration = 2600.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Movement", meta = (ClampMin = "0.0"))
    float GroundFriction = 8.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Movement", meta = (ClampMin = "0.0"))
    float MaxWalkSpeed2D = 420.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Movement", meta = (ClampMin = "0.0"))
    float JumpZVelocity2D = 900.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Movement", meta = (ClampMin = "0.0"))
    float SlideSpeed2D = 680.0f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Traversal")
    TObjectPtr<UAnimMontage> JumpStartMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Traversal")
    TObjectPtr<UAnimMontage> JumpLandMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Traversal")
    TObjectPtr<UAnimMontage> DoubleJumpStartMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Traversal")
    TObjectPtr<UAnimMontage> DoubleJumpLandMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Traversal")
    TObjectPtr<UAnimMontage> SlideStartMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Traversal")
    TObjectPtr<UAnimMontage> SlideExitMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Tentacles")
    TObjectPtr<UAnimMontage> TentacleAttackMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Tentacles")
    TObjectPtr<UAnimMontage> TentacleGrappleStartMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Tentacles")
    TObjectPtr<UAnimMontage> TentacleGrappleLoopMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Tentacles")
    TObjectPtr<UAnimMontage> TentacleGrappleEndMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Tentacles")
    TObjectPtr<UAnimMontage> TentacleConsumeMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Tentacles")
    TObjectPtr<UAnimMontage> TentacleConsumeAlternateMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Recovered Combat")
    TObjectPtr<UAnimMontage> FireTrailAction01Montage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Recovered Combat")
    TObjectPtr<UAnimMontage> FireTrailAction08Montage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Recovered Combat")
    TObjectPtr<UAnimMontage> FireTrailAction16Montage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Recovered Combat")
    TObjectPtr<UAnimMontage> FightingCrossPunchMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Recovered Combat")
    TObjectPtr<UAnimMontage> FightingHookPunchMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Recovered Combat")
    TObjectPtr<UAnimMontage> FightingElbowPunchMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Recovered Combat")
    TObjectPtr<UAnimMontage> FightingImpactMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Recovered Combat")
    TObjectPtr<UAnimMontage> FightingDeathMontage;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Locomotion")
    TObjectPtr<UAnimationAsset> IdleAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Locomotion")
    TObjectPtr<UAnimationAsset> WalkAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Locomotion")
    TObjectPtr<UAnimationAsset> RunAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Traversal")
    TObjectPtr<UAnimationAsset> JumpStartFallbackAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Locomotion")
    TObjectPtr<UAnimationAsset> JumpLoopAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Locomotion")
    TObjectPtr<UAnimationAsset> JumpLandAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Traversal")
    TObjectPtr<UAnimationAsset> DoubleJumpStartFallbackAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Traversal")
    TObjectPtr<UAnimationAsset> DoubleJumpLoopAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Traversal")
    TObjectPtr<UAnimationAsset> DoubleJumpLandFallbackAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Locomotion")
    TObjectPtr<UAnimationAsset> FallLoopAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Traversal")
    TObjectPtr<UAnimationAsset> SlideStartFallbackAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Locomotion")
    TObjectPtr<UAnimationAsset> SlideLoopAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Traversal")
    TObjectPtr<UAnimationAsset> SlideExitFallbackAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Tentacles")
    TObjectPtr<UAnimationAsset> TentacleAttackFallbackAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Tentacles")
    TObjectPtr<UAnimationAsset> TentacleGrappleStartFallbackAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Tentacles")
    TObjectPtr<UAnimationAsset> TentacleGrappleFallbackAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Tentacles")
    TObjectPtr<UAnimationAsset> TentacleGrappleReleaseFallbackAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Tentacles")
    TObjectPtr<UAnimationAsset> TentacleConsumeFallbackAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Tentacles")
    TObjectPtr<UAnimationAsset> TentacleAlternateConsumeFallbackAnimation;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Tentacles", meta = (ClampMin = "0.01"))
    float TentacleActionFallbackDuration = 0.45f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Animation|Locomotion")
    bool bForceNativeAnimationFallback = true;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Camera")
    bool bClampSliceCameraVerticalFrame = true;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Camera")
    float SliceCameraBaseOffsetZ = 320.0f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Camera")
    float SliceCameraMinWorldZ = 360.0f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Camera")
    float SliceCameraMaxWorldZ = 430.0f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Input")
    TObjectPtr<UInputMappingContext> SliceInputMappingContext;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Input")
    TObjectPtr<UInputAction> MoveHorizontalAction;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Input")
    TObjectPtr<UInputAction> MoveLeftAction;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Input")
    TObjectPtr<UInputAction> MoveRightAction;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Input")
    TObjectPtr<UInputAction> JumpAction;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Input")
    TObjectPtr<UInputAction> SlideAction;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Input")
    TObjectPtr<UInputAction> TentacleGrappleAction;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Input")
    TObjectPtr<UInputAction> TentacleAttackAction;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Input")
    TObjectPtr<UInputAction> TentacleConsumeAction;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Nocturne|Input")
    TObjectPtr<UInputAction> TentacleAlternateConsumeAction;

protected:
    virtual void BeginPlay() override;
    virtual void PossessedBy(AController* NewController) override;
    virtual void OnRep_Controller() override;
    virtual void Landed(const FHitResult& Hit) override;

private:
    void ApplyMovementTuning();
    void AddSliceInputMappingContext() const;
    void RefreshSliceCameraViewTarget();
    void UpdateSliceCameraFrame();
    void ShowTentacleActionVisualCue(float ReachDistance);
    float PlayJacobMontage(UAnimMontage* Montage, FName StartSection = NAME_None);
    float PlayJacobMontageOrFallback(
        UAnimMontage* Montage,
        UAnimationAsset* FallbackAnimation,
        bool bLoopFallback,
        FName StartSection = NAME_None,
        float FallbackDuration = 0.0f);
    void InitializeJacobAnimationFallback();
    void UpdateJacobAnimationFallback();
    void PlayJacobAnimationFallback(UAnimationAsset* Animation, bool bLoop);
    void HoldTraversalFallbackAnimation(float DurationSeconds);
    void SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation NewAbilityAnimation);
    FName GetRecoveredCombatStartSection(ENocturneJacobRecoveredCombatMontage MontageId) const;
    void StartSlideInput();
    void TriggerTentacleAttackInput();
    void TriggerTentacleGrappleInput();
    void TriggerTentacleConsumeInput();
    void TriggerTentacleAlternateConsumeInput();
    void MoveHorizontalEnhancedInput(const FInputActionValue& Value);
    void MoveLeftEnhancedInput(const FInputActionValue& Value);
    void MoveRightEnhancedInput(const FInputActionValue& Value);
    void StartJumpEnhancedInput(const FInputActionValue& Value);
    void StopJumpEnhancedInput(const FInputActionValue& Value);
    void StartSlideEnhancedInput(const FInputActionValue& Value);
    void StopSlideEnhancedInput(const FInputActionValue& Value);
    void TriggerTentacleAttackEnhancedInput(const FInputActionValue& Value);
    void TriggerTentacleGrappleEnhancedInput(const FInputActionValue& Value);
    void TriggerTentacleConsumeEnhancedInput(const FInputActionValue& Value);
    void TriggerTentacleAlternateConsumeEnhancedInput(const FInputActionValue& Value);

    UFUNCTION()
    void HandleGrappleStateChanged(EVestigeGrappleState NewState);

    void ScheduleTentacleActionClear(float DelaySeconds);
    void ScheduleRecoveredCombatActionClear(float DelaySeconds);

    UFUNCTION()
    void ClearTentacleActionState();

    UFUNCTION()
    void ClearRecoveredCombatActionState();

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Animation", meta = (AllowPrivateAccess = "true"))
    bool bIsSliding = false;

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Animation", meta = (AllowPrivateAccess = "true"))
    bool bIsDoubleJumping = false;

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Animation", meta = (AllowPrivateAccess = "true"))
    bool bIsTentacleActionActive = false;

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Animation", meta = (AllowPrivateAccess = "true"))
    ENocturneJacobAbilityAnimation CurrentAbilityAnimation = ENocturneJacobAbilityAnimation::None;

    FTimerHandle TentacleActionTimerHandle;
    FTimerHandle RecoveredCombatActionTimerHandle;

    UPROPERTY(Transient)
    TObjectPtr<UAnimationAsset> CurrentFallbackAnimation;

    bool bUsingSingleNodeAnimationFallback = false;

    float CachedPreSlideMaxWalkSpeed = 0.0f;
    float TraversalFallbackLockRemainingSeconds = 0.0f;
};
