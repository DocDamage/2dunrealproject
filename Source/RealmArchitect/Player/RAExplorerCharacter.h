#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "TimerManager.h"
#include "RAExplorerCharacter.generated.h"

class USpringArmComponent;
class USkeletalMesh;
class USkeletalMeshComponent;
class UAnimSequence;
class UCameraComponent;
class UStaticMeshComponent;
class UPointLightComponent;
class UParticleSystem;
class UNiagaraSystem;
class URACameraModeComponent;
class URAGrappleComponent;

enum class EJacobAnimationState : uint8
{
    None,
    Idle,
    Walk,
    Jog,
    Jump,
    Fall,
    Action
};

UCLASS()
class REALMARCHITECT_API ARAExplorerCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    ARAExplorerCharacter();

    virtual void Tick(float DeltaSeconds) override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

    UFUNCTION(BlueprintCallable, Category="Realm Architect|Transformation")
    void SetDraconicForm(bool bNewDraconicForm);

    UFUNCTION(BlueprintPure, Category="Realm Architect|Transformation")
    bool IsInDraconicForm() const { return bIsInDraconicForm; }

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Camera")
    TObjectPtr<USpringArmComponent> CameraBoom;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Camera")
    TObjectPtr<UCameraComponent> FollowCamera;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Realm Architect")
    TObjectPtr<URACameraModeComponent> CameraModeComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Realm Architect|Traversal")
    TObjectPtr<URAGrappleComponent> GrappleComponent;

protected:
    void MoveForward(float Value);
    void MoveRight(float Value);
    void TurnAtRate(float Rate);
    void LookUpAtRate(float Rate);
    void StartSprint();
    void StopSprint();
    void StartGrapple();
    void StopGrapple();
    void ToggleDraconicForm();
    void PlayJacobActionAnimation();
    void PlayJacobIdleLoop();
    void FinishJacobActionAnimation();
    void UpdateJacobLocomotionAnimation();
    void PlayJacobAnimation(UAnimSequence* Animation, bool bLoop, EJacobAnimationState NewState, bool bForceRestart = false);
    void BeginFormTransition(bool bNewDraconicForm);
    void ApplyFormImmediate(bool bNewDraconicForm);
    void UpdateFormTransition(float DeltaSeconds);
    void ConfigureJacobAnimatedMesh();
    void SetJacobAnimatedMeshVisible(bool bVisible);
    void SpawnTransformVFX(bool bNewDraconicForm) const;
    static USkeletalMesh* LoadJacobSkeletalMesh();
    static UAnimSequence* LoadJacobIdleAnimation();
    static UAnimSequence* LoadJacobWalkAnimation();
    static UAnimSequence* LoadJacobJogAnimation();
    static UAnimSequence* LoadJacobJumpAnimation();
    static UAnimSequence* LoadJacobFallAnimation();
    static UAnimSequence* LoadJacobActionAnimation(int32 ActionIndex, int32& OutResolvedIndex);
    static UAnimSequence* LoadJacobAnimation(const TCHAR* Path);
    static UNiagaraSystem* LoadTransformNiagaraSystem(const TCHAR* Path);
    static UParticleSystem* LoadTransformParticleSystem(const TCHAR* Path);

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Realm Architect|Art")
    TObjectPtr<UStaticMeshComponent> AvatarMesh;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Realm Architect|Art")
    TObjectPtr<UStaticMeshComponent> DraconicAvatarMesh;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Realm Architect|Transformation")
    TObjectPtr<UPointLightComponent> TransformLight;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Realm Architect|Transformation")
    bool bIsInDraconicForm = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Realm Architect|Transformation")
    bool bTransformInProgress = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Realm Architect|Transformation", meta=(ClampMin="0.1"))
    float TransformDuration = 0.72f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Realm Architect|Transformation")
    float TransformSpinDegrees = 300.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Realm Architect|Transformation")
    float TransformCameraBoomPulse = 120.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Realm Architect|Transformation")
    float TransformLightPeakIntensity = 8500.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Realm Architect|Transformation")
    FLinearColor TransformLightColor = FLinearColor(0.45f, 0.62f, 1.0f, 1.0f);

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Realm Architect|Transformation")
    FVector TransformVFXOffset = FVector(0.0f, 0.0f, -72.0f);

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Realm Architect|Transformation")
    FVector NormalFormMeshOffset = FVector(0.0f, 0.0f, -88.0f);

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Realm Architect|Transformation")
    FVector DraconicFormMeshOffset = FVector(0.0f, 0.0f, -88.0f);

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Realm Architect|Transformation")
    FVector NormalFormMeshScale = FVector(0.92f);

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Realm Architect|Transformation")
    FVector DraconicFormMeshScale = FVector(0.92f);

    float TransformElapsed = 0.0f;
    float BaseCameraBoomLength = 450.0f;
    bool bPendingDraconicForm = false;
    FTimerHandle JacobIdleReturnTimerHandle;
    EJacobAnimationState CurrentJacobAnimationState = EJacobAnimationState::None;
    bool bCurrentJacobAnimationLoops = false;
    bool bJacobActionAnimationActive = false;
    int32 NextJacobActionAnimationIndex = 0;

    UPROPERTY(Transient)
    TObjectPtr<UAnimSequence> CurrentJacobAnimation;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Movement")
    float WalkSpeed = 450.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Movement")
    float SprintSpeed = 780.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Movement")
    float BaseTurnRate = 45.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Movement")
    float BaseLookUpRate = 45.0f;
};
