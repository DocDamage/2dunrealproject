#include "NocturnePlayerCharacter.h"
#include "VestigeLimbComponent.h"
#include "VestigeTentacleVisualAdapter.h"
#include "Animation/AnimMontage.h"
#include "Engine/SkeletalMesh.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "TimerManager.h"
#include "UObject/ConstructorHelpers.h"

namespace
{
template <typename ObjectType>
ObjectType* FindNocturneAsset(const TCHAR* AssetPath)
{
    ConstructorHelpers::FObjectFinder<ObjectType> Finder(AssetPath);
    return Finder.Succeeded() ? Finder.Object : nullptr;
}
}

ANocturnePlayerCharacter::ANocturnePlayerCharacter()
{
    PrimaryActorTick.bCanEverTick = true;

    VestigeLimbComponent = CreateDefaultSubobject<UVestigeLimbComponent>(TEXT("VestigeLimbComponent"));
    VestigeTentacleVisualAdapter = CreateDefaultSubobject<UVestigeTentacleVisualAdapter>(TEXT("VestigeTentacleVisualAdapter"));

    bUseControllerRotationPitch = false;
    bUseControllerRotationYaw = false;
    bUseControllerRotationRoll = false;

    JumpMaxCount = 2;

    JumpStartMontage = FindNocturneAsset<UAnimMontage>(
        TEXT("/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_Jump_Start.AM_Jacob_Jump_Start"));
    JumpLandMontage = FindNocturneAsset<UAnimMontage>(
        TEXT("/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_Jump_Land.AM_Jacob_Jump_Land"));
    DoubleJumpStartMontage = FindNocturneAsset<UAnimMontage>(
        TEXT("/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_DoubleJump_Start.AM_Jacob_DoubleJump_Start"));
    DoubleJumpLandMontage = FindNocturneAsset<UAnimMontage>(
        TEXT("/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_DoubleJump_Land.AM_Jacob_DoubleJump_Land"));
    SlideStartMontage = FindNocturneAsset<UAnimMontage>(
        TEXT("/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_Slide_Start.AM_Jacob_Slide_Start"));
    SlideExitMontage = FindNocturneAsset<UAnimMontage>(
        TEXT("/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_Slide_Exit.AM_Jacob_Slide_Exit"));
    TentacleAttackMontage = FindNocturneAsset<UAnimMontage>(
        TEXT("/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_TentacleAttack_ForceChoke.AM_Jacob_TentacleAttack_ForceChoke"));
    TentacleGrappleStartMontage = FindNocturneAsset<UAnimMontage>(
        TEXT("/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_TentacleGrapple_Start.AM_Jacob_TentacleGrapple_Start"));
    TentacleGrappleLoopMontage = FindNocturneAsset<UAnimMontage>(
        TEXT("/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_TentacleGrapple_Loop.AM_Jacob_TentacleGrapple_Loop"));
    TentacleGrappleEndMontage = FindNocturneAsset<UAnimMontage>(
        TEXT("/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_TentacleGrapple_End.AM_Jacob_TentacleGrapple_End"));
    TentacleConsumeMontage = FindNocturneAsset<UAnimMontage>(
        TEXT("/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_TentacleConsume_SneakNeckBreak.AM_Jacob_TentacleConsume_SneakNeckBreak"));
    TentacleConsumeAlternateMontage = FindNocturneAsset<UAnimMontage>(
        TEXT("/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_TentacleConsume_KidneyNeck.AM_Jacob_TentacleConsume_KidneyNeck"));

    if (VestigeTentacleVisualAdapter)
    {
        VestigeTentacleVisualAdapter->TentacleSkeletalMesh = FindNocturneAsset<USkeletalMesh>(
            TEXT("/Game/NocturneSignal/Characters/Jacob/Tentacles/RoboticTentacleHands/hand_18/SkeletalMeshes/Cylinder.Cylinder"));
        VestigeTentacleVisualAdapter->bHideVisualWhenIdle = true;
        VestigeTentacleVisualAdapter->bDrawFallbackDebugLine = true;
    }

    ApplyMovementTuning();
}

void ANocturnePlayerCharacter::BeginPlay()
{
    Super::BeginPlay();
    ApplyMovementTuning();

    if (VestigeLimbComponent)
    {
        VestigeLimbComponent->SetVisualAdapter(VestigeTentacleVisualAdapter);
        VestigeLimbComponent->OnGrappleStateChanged.AddUniqueDynamic(
            this,
            &ANocturnePlayerCharacter::HandleGrappleStateChanged);
    }
}

void ANocturnePlayerCharacter::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
}

void ANocturnePlayerCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    // Enhanced Input bindings should be assigned in the Blueprint subclass for Slice 1.
    // This C++ shell exposes Blueprint-callable hooks for movement, jump, and grapple.
}

void ANocturnePlayerCharacter::MoveHorizontal(float AxisValue)
{
    if (FMath::IsNearlyZero(AxisValue))
    {
        return;
    }

    AddMovementInput(FVector::RightVector, AxisValue);
}

void ANocturnePlayerCharacter::StartJump()
{
    const UCharacterMovementComponent* Movement = GetCharacterMovement();
    const bool bWantsDoubleJump = Movement && Movement->IsFalling() && JumpCurrentCount > 0;

    Jump();

    bIsDoubleJumping = bWantsDoubleJump;
    SetCurrentAbilityAnimation(
        bIsDoubleJumping ? ENocturneJacobAbilityAnimation::DoubleJump : ENocturneJacobAbilityAnimation::Jump);
    PlayJacobMontage(bIsDoubleJumping ? DoubleJumpStartMontage : JumpStartMontage);
}

void ANocturnePlayerCharacter::StopJump()
{
    StopJumping();
}

bool ANocturnePlayerCharacter::StartSlide()
{
    UCharacterMovementComponent* Movement = GetCharacterMovement();
    if (!Movement || bIsSliding || Movement->IsFalling())
    {
        return false;
    }

    CachedPreSlideMaxWalkSpeed = Movement->MaxWalkSpeed;
    Movement->MaxWalkSpeed = SlideSpeed2D;
    bIsSliding = true;
    SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::Slide);
    PlayJacobMontage(SlideStartMontage);
    return true;
}

void ANocturnePlayerCharacter::StopSlide()
{
    if (!bIsSliding)
    {
        return;
    }

    if (UCharacterMovementComponent* Movement = GetCharacterMovement())
    {
        Movement->MaxWalkSpeed = CachedPreSlideMaxWalkSpeed > 0.0f ? CachedPreSlideMaxWalkSpeed : MaxWalkSpeed2D;
    }

    bIsSliding = false;
    PlayJacobMontage(SlideExitMontage);
    SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::None);
}

bool ANocturnePlayerCharacter::TryVestigeGrapple()
{
    return VestigeLimbComponent ? VestigeLimbComponent->TryStartPullToPoint() : false;
}

bool ANocturnePlayerCharacter::TriggerTentacleGrapple()
{
    SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::TentacleGrapple);
    const bool bStartedGrapple = TryVestigeGrapple();
    if (!bStartedGrapple)
    {
        if (VestigeTentacleVisualAdapter)
        {
            VestigeTentacleVisualAdapter->SetTentacleVisualActive(false);
        }
        SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::None);
    }
    return bStartedGrapple;
}

bool ANocturnePlayerCharacter::TriggerTentacleAttack()
{
    bIsTentacleActionActive = true;
    SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::TentacleAttack);
    if (VestigeTentacleVisualAdapter)
    {
        VestigeTentacleVisualAdapter->SetTentacleVisualActive(true);
    }

    const float MontageDuration = PlayJacobMontage(TentacleAttackMontage, TEXT("CastStart"));
    if (MontageDuration <= 0.0f)
    {
        ClearTentacleActionState();
        return false;
    }

    ScheduleTentacleActionClear(MontageDuration);
    return true;
}

bool ANocturnePlayerCharacter::TriggerTentacleConsume(bool bUseAlternateConsume)
{
    bIsTentacleActionActive = true;
    SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::TentacleConsume);
    if (VestigeTentacleVisualAdapter)
    {
        VestigeTentacleVisualAdapter->SetTentacleVisualActive(true);
    }

    UAnimMontage* Montage = bUseAlternateConsume ? TentacleConsumeAlternateMontage : TentacleConsumeMontage;
    const float MontageDuration = PlayJacobMontage(Montage, TEXT("ConsumeStart"));
    if (MontageDuration <= 0.0f)
    {
        ClearTentacleActionState();
        return false;
    }

    ScheduleTentacleActionClear(MontageDuration);
    return true;
}

UVestigeLimbComponent* ANocturnePlayerCharacter::GetVestigeLimbComponent() const
{
    return VestigeLimbComponent;
}

bool ANocturnePlayerCharacter::IsSliding() const
{
    return bIsSliding;
}

bool ANocturnePlayerCharacter::IsDoubleJumping() const
{
    return bIsDoubleJumping;
}

bool ANocturnePlayerCharacter::IsTentacleActionActive() const
{
    return bIsTentacleActionActive;
}

ENocturneJacobAbilityAnimation ANocturnePlayerCharacter::GetCurrentAbilityAnimation() const
{
    return CurrentAbilityAnimation;
}

void ANocturnePlayerCharacter::Landed(const FHitResult& Hit)
{
    Super::Landed(Hit);

    PlayJacobMontage(bIsDoubleJumping ? DoubleJumpLandMontage : JumpLandMontage);
    bIsDoubleJumping = false;

    if (CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::Jump
        || CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::DoubleJump)
    {
        SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::None);
    }
}

void ANocturnePlayerCharacter::ApplyMovementTuning()
{
    UCharacterMovementComponent* Movement = GetCharacterMovement();
    if (!Movement)
    {
        return;
    }

    Movement->MaxWalkSpeed = MaxWalkSpeed2D;
    if (!bIsSliding)
    {
        CachedPreSlideMaxWalkSpeed = MaxWalkSpeed2D;
    }
    Movement->JumpZVelocity = JumpZVelocity2D;
    Movement->MaxAcceleration = GroundAcceleration;
    Movement->GroundFriction = GroundFriction;
    Movement->BrakingFrictionFactor = 1.0f;
    Movement->AirControl = 0.45f;
    Movement->GravityScale = 1.65f;
    Movement->bOrientRotationToMovement = false;

    // Lock the prototype to a 2D plane. Adjust axis/origin in-editor if the Paper2D scene uses a different plane.
    Movement->bConstrainToPlane = true;
    Movement->SetPlaneConstraintNormal(FVector::ForwardVector);
}

float ANocturnePlayerCharacter::PlayJacobMontage(UAnimMontage* Montage, FName StartSection)
{
    if (!Montage)
    {
        return 0.0f;
    }

    return PlayAnimMontage(Montage, 1.0f, StartSection);
}

void ANocturnePlayerCharacter::SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation NewAbilityAnimation)
{
    CurrentAbilityAnimation = NewAbilityAnimation;
    if (NewAbilityAnimation != ENocturneJacobAbilityAnimation::TentacleAttack
        && NewAbilityAnimation != ENocturneJacobAbilityAnimation::TentacleGrapple
        && NewAbilityAnimation != ENocturneJacobAbilityAnimation::TentacleConsume)
    {
        bIsTentacleActionActive = false;
        if (UWorld* World = GetWorld())
        {
            World->GetTimerManager().ClearTimer(TentacleActionTimerHandle);
        }
    }
}

void ANocturnePlayerCharacter::HandleGrappleStateChanged(EVestigeGrappleState NewState)
{
    switch (NewState)
    {
    case EVestigeGrappleState::Extending:
        bIsTentacleActionActive = true;
        SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::TentacleGrapple);
        PlayJacobMontage(TentacleGrappleStartMontage, TEXT("GrappleStart"));
        break;

    case EVestigeGrappleState::PullingPlayer:
        bIsTentacleActionActive = true;
        SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::TentacleGrapple);
        PlayJacobMontage(TentacleGrappleLoopMontage, TEXT("GrappleLoop"));
        break;

    case EVestigeGrappleState::Releasing:
    case EVestigeGrappleState::Retracting:
        PlayJacobMontage(TentacleGrappleEndMontage, TEXT("GrappleRelease"));
        break;

    case EVestigeGrappleState::Idle:
    case EVestigeGrappleState::Failed:
        if (VestigeTentacleVisualAdapter)
        {
            VestigeTentacleVisualAdapter->SetTentacleVisualActive(false);
        }

        if (CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::TentacleGrapple)
        {
            bIsTentacleActionActive = false;
            SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::None);
        }
        break;

    default:
        break;
    }
}

void ANocturnePlayerCharacter::ScheduleTentacleActionClear(float DelaySeconds)
{
    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    World->GetTimerManager().SetTimer(
        TentacleActionTimerHandle,
        this,
        &ANocturnePlayerCharacter::ClearTentacleActionState,
        FMath::Max(DelaySeconds, 0.01f),
        false);
}

void ANocturnePlayerCharacter::ClearTentacleActionState()
{
    if (CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::TentacleAttack
        || CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::TentacleConsume)
    {
        bIsTentacleActionActive = false;
        SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::None);
        if (VestigeTentacleVisualAdapter)
        {
            VestigeTentacleVisualAdapter->SetTentacleVisualActive(false);
        }
    }
}
