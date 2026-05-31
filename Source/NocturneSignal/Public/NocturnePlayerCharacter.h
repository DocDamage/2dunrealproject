#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "TimerManager.h"
#include "VestigeLimbComponent.h"
#include "NocturnePlayerCharacter.generated.h"

class UAnimMontage;
class UPaperFlipbookComponent;
class UVestigeTentacleVisualAdapter;

UENUM(BlueprintType)
enum class ENocturneJacobAbilityAnimation : uint8
{
    None UMETA(DisplayName = "None"),
    Jump UMETA(DisplayName = "Jump"),
    DoubleJump UMETA(DisplayName = "Double Jump"),
    Slide UMETA(DisplayName = "Slide"),
    TentacleAttack UMETA(DisplayName = "Tentacle Attack"),
    TentacleGrapple UMETA(DisplayName = "Tentacle Grapple"),
    TentacleConsume UMETA(DisplayName = "Tentacle Consume")
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

    UFUNCTION(BlueprintPure, Category = "Nocturne|Vestige")
    UVestigeLimbComponent* GetVestigeLimbComponent() const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Animation")
    bool IsSliding() const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Animation")
    bool IsDoubleJumping() const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Animation")
    bool IsTentacleActionActive() const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Animation")
    ENocturneJacobAbilityAnimation GetCurrentAbilityAnimation() const;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nocturne|Components")
    TObjectPtr<UVestigeLimbComponent> VestigeLimbComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nocturne|Components")
    TObjectPtr<UVestigeTentacleVisualAdapter> VestigeTentacleVisualAdapter;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Movement", meta = (ClampMin = "0.0"))
    float GroundAcceleration = 2600.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Movement", meta = (ClampMin = "0.0"))
    float GroundFriction = 8.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Movement", meta = (ClampMin = "0.0"))
    float MaxWalkSpeed2D = 420.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Movement", meta = (ClampMin = "0.0"))
    float JumpZVelocity2D = 720.0f;

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

protected:
    virtual void BeginPlay() override;
    virtual void Landed(const FHitResult& Hit) override;

private:
    void ApplyMovementTuning();
    float PlayJacobMontage(UAnimMontage* Montage, FName StartSection = NAME_None);
    void SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation NewAbilityAnimation);

    UFUNCTION()
    void HandleGrappleStateChanged(EVestigeGrappleState NewState);

    void ScheduleTentacleActionClear(float DelaySeconds);

    UFUNCTION()
    void ClearTentacleActionState();

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Animation", meta = (AllowPrivateAccess = "true"))
    bool bIsSliding = false;

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Animation", meta = (AllowPrivateAccess = "true"))
    bool bIsDoubleJumping = false;

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Animation", meta = (AllowPrivateAccess = "true"))
    bool bIsTentacleActionActive = false;

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Nocturne|Animation", meta = (AllowPrivateAccess = "true"))
    ENocturneJacobAbilityAnimation CurrentAbilityAnimation = ENocturneJacobAbilityAnimation::None;

    FTimerHandle TentacleActionTimerHandle;

    float CachedPreSlideMaxWalkSpeed = 0.0f;
};
