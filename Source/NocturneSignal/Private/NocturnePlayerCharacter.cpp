#include "NocturnePlayerCharacter.h"
#include "VestigeLimbComponent.h"
#include "VestigeTentacleVisualAdapter.h"
#include "Animation/AnimMontage.h"
#include "Animation/AnimationAsset.h"
#include "Animation/AnimInstance.h"
#include "Camera/CameraComponent.h"
#include "Components/InputComponent.h"
#include "Components/SceneComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/LocalPlayer.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/SpringArmComponent.h"
#include "InputAction.h"
#include "InputActionValue.h"
#include "InputMappingContext.h"
#include "TimerManager.h"
#include "UObject/ConstructorHelpers.h"

namespace
{
constexpr float TraversalStartFallbackDuration = 0.34f;
constexpr float TraversalExitFallbackDuration = 0.34f;
constexpr float TraversalLandFallbackDuration = 0.34f;

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
    CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
    SideViewCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("SideViewCamera"));

    CameraBoom->SetupAttachment(RootComponent);
    CameraBoom->SetRelativeLocation(FVector(0.0f, 0.0f, 320.0f));
    CameraBoom->TargetArmLength = 900.0f;
    CameraBoom->SetRelativeRotation(FRotator(0.0f, -90.0f, 0.0f));
    CameraBoom->bDoCollisionTest = false;
    CameraBoom->bUsePawnControlRotation = false;

    SideViewCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName);
    SideViewCamera->bUsePawnControlRotation = false;

    bUseControllerRotationPitch = false;
    bUseControllerRotationYaw = false;
    bUseControllerRotationRoll = false;

    JumpMaxCount = 2;

    if (USkeletalMesh* PlayerMesh = FindNocturneAsset<USkeletalMesh>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/SK_FemaleCyberStalker.SK_FemaleCyberStalker")))
    {
        GetMesh()->SetSkeletalMesh(PlayerMesh);
        GetMesh()->SetRelativeLocation(FVector(0.0f, 0.0f, -88.0f));
        GetMesh()->SetRelativeRotation(FRotator(0.0f, -90.0f, 0.0f));
        GetMesh()->SetRelativeScale3D(FVector(1.0f));
    }
    GetMesh()->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones;
    GetMesh()->bPauseAnims = false;
    GetMesh()->GlobalAnimRateScale = 1.0f;
    GetMesh()->SetAnimationMode(EAnimationMode::AnimationSingleNode);

    JumpStartMontage = nullptr;
    JumpLandMontage = nullptr;
    DoubleJumpStartMontage = nullptr;
    DoubleJumpLandMontage = nullptr;
    SlideStartMontage = nullptr;
    SlideExitMontage = nullptr;
    TentacleAttackMontage = nullptr;
    TentacleGrappleStartMontage = nullptr;
    TentacleGrappleLoopMontage = nullptr;
    TentacleGrappleEndMontage = nullptr;
    TentacleConsumeMontage = nullptr;
    TentacleConsumeAlternateMontage = nullptr;
    FireTrailAction01Montage = nullptr;
    FireTrailAction08Montage = nullptr;
    FireTrailAction16Montage = nullptr;
    FightingCrossPunchMontage = nullptr;
    FightingHookPunchMontage = nullptr;
    FightingElbowPunchMontage = nullptr;
    FightingImpactMontage = nullptr;
    FightingDeathMontage = nullptr;

    IdleAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RogueCharacter/FCS_MM_Idle.FCS_MM_Idle"));
    WalkAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/Animations/FCS_Walk.FCS_Walk"));
    RunAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/Animations/FCS_Run.FCS_Run"));
    JumpStartFallbackAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary1/FCS_SK_UAL1_MannequinArmature_Jump_Start.FCS_SK_UAL1_MannequinArmature_Jump_Start"));
    JumpLoopAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary1/FCS_SK_UAL1_MannequinArmature_Jump_Loop.FCS_SK_UAL1_MannequinArmature_Jump_Loop"));
    JumpLandAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary1/FCS_SK_UAL1_MannequinArmature_Jump_Land.FCS_SK_UAL1_MannequinArmature_Jump_Land"));
    DoubleJumpStartFallbackAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary2/FCS_SK_UAL2_MannequinArmature_NinjaJump_Start.FCS_SK_UAL2_MannequinArmature_NinjaJump_Start"));
    DoubleJumpLoopAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary2/FCS_SK_UAL2_MannequinArmature_NinjaJump_Idle_Loop.FCS_SK_UAL2_MannequinArmature_NinjaJump_Idle_Loop"));
    DoubleJumpLandFallbackAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary2/FCS_SK_UAL2_MannequinArmature_NinjaJump_Land.FCS_SK_UAL2_MannequinArmature_NinjaJump_Land"));
    FallLoopAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RogueCharacter/FCS_MM_Fall_Loop.FCS_MM_Fall_Loop"));
    SlideStartFallbackAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary2/FCS_SK_UAL2_MannequinArmature_Slide_Start.FCS_SK_UAL2_MannequinArmature_Slide_Start"));
    SlideLoopAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary2/FCS_SK_UAL2_MannequinArmature_Slide_Loop.FCS_SK_UAL2_MannequinArmature_Slide_Loop"));
    SlideExitFallbackAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary2/FCS_SK_UAL2_MannequinArmature_Slide_Exit.FCS_SK_UAL2_MannequinArmature_Slide_Exit"));
    TentacleAttackFallbackAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RamsterZ/FCS_Paired_ForceChoke_Att.FCS_Paired_ForceChoke_Att"));
    TentacleGrappleStartFallbackAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RamsterZ/FCS_Paired_ForceChoke_Start_Att.FCS_Paired_ForceChoke_Start_Att"));
    TentacleGrappleFallbackAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RamsterZ/FCS_Paired_ForceChoke_Loop_Att.FCS_Paired_ForceChoke_Loop_Att"));
    TentacleGrappleReleaseFallbackAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RamsterZ/FCS_Paired_ForceChoke_End_Att.FCS_Paired_ForceChoke_End_Att"));
    TentacleConsumeFallbackAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RamsterZ/FCS_Paired_SneakNeckBreak_Att.FCS_Paired_SneakNeckBreak_Att"));
    TentacleAlternateConsumeFallbackAnimation = FindNocturneAsset<UAnimationAsset>(
        TEXT("/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RamsterZ/FCS_Paired_Knife_Stealth_KidneyAndNeck_Att.FCS_Paired_Knife_Stealth_KidneyAndNeck_Att"));
    JumpStartFallbackAnimation = JumpStartFallbackAnimation ? JumpStartFallbackAnimation.Get() : JumpLoopAnimation.Get();
    JumpLoopAnimation = JumpLoopAnimation ? JumpLoopAnimation.Get() : FallLoopAnimation.Get();
    JumpLandAnimation = JumpLandAnimation ? JumpLandAnimation.Get() : IdleAnimation.Get();
    DoubleJumpStartFallbackAnimation = DoubleJumpStartFallbackAnimation
        ? DoubleJumpStartFallbackAnimation.Get()
        : JumpStartFallbackAnimation.Get();
    DoubleJumpLoopAnimation = DoubleJumpLoopAnimation ? DoubleJumpLoopAnimation.Get() : JumpLoopAnimation.Get();
    DoubleJumpLandFallbackAnimation = DoubleJumpLandFallbackAnimation
        ? DoubleJumpLandFallbackAnimation.Get()
        : JumpLandAnimation.Get();
    SlideStartFallbackAnimation = SlideStartFallbackAnimation ? SlideStartFallbackAnimation.Get() : SlideLoopAnimation.Get();
    SlideLoopAnimation = SlideLoopAnimation ? SlideLoopAnimation.Get() : RunAnimation.Get();
    SlideExitFallbackAnimation = SlideExitFallbackAnimation ? SlideExitFallbackAnimation.Get() : IdleAnimation.Get();
    TentacleAttackFallbackAnimation = TentacleAttackFallbackAnimation ? TentacleAttackFallbackAnimation.Get() : JumpLoopAnimation.Get();
    TentacleGrappleStartFallbackAnimation = TentacleGrappleStartFallbackAnimation
        ? TentacleGrappleStartFallbackAnimation.Get()
        : TentacleAttackFallbackAnimation.Get();
    TentacleGrappleFallbackAnimation = TentacleGrappleFallbackAnimation ? TentacleGrappleFallbackAnimation.Get() : FallLoopAnimation.Get();
    TentacleGrappleReleaseFallbackAnimation = TentacleGrappleReleaseFallbackAnimation
        ? TentacleGrappleReleaseFallbackAnimation.Get()
        : (JumpLandAnimation ? JumpLandAnimation.Get() : IdleAnimation.Get());
    TentacleConsumeFallbackAnimation = TentacleConsumeFallbackAnimation ? TentacleConsumeFallbackAnimation.Get() : JumpLandAnimation.Get();
    TentacleAlternateConsumeFallbackAnimation = TentacleAlternateConsumeFallbackAnimation
        ? TentacleAlternateConsumeFallbackAnimation.Get()
        : TentacleConsumeFallbackAnimation.Get();

    SliceInputMappingContext = FindNocturneAsset<UInputMappingContext>(
        TEXT("/Game/NocturneSignal/Input/IMC_Slice01.IMC_Slice01"));
    MoveHorizontalAction = FindNocturneAsset<UInputAction>(
        TEXT("/Game/NocturneSignal/Input/IA_MoveHorizontal.IA_MoveHorizontal"));
    MoveLeftAction = FindNocturneAsset<UInputAction>(
        TEXT("/Game/NocturneSignal/Input/IA_MoveLeft.IA_MoveLeft"));
    MoveRightAction = FindNocturneAsset<UInputAction>(
        TEXT("/Game/NocturneSignal/Input/IA_MoveRight.IA_MoveRight"));
    JumpAction = FindNocturneAsset<UInputAction>(
        TEXT("/Game/NocturneSignal/Input/IA_Jump.IA_Jump"));
    SlideAction = FindNocturneAsset<UInputAction>(
        TEXT("/Game/NocturneSignal/Input/IA_Slide.IA_Slide"));
    TentacleGrappleAction = FindNocturneAsset<UInputAction>(
        TEXT("/Game/NocturneSignal/Input/IA_TentacleGrapple.IA_TentacleGrapple"));
    TentacleAttackAction = FindNocturneAsset<UInputAction>(
        TEXT("/Game/NocturneSignal/Input/IA_TentacleAttack.IA_TentacleAttack"));
    TentacleConsumeAction = FindNocturneAsset<UInputAction>(
        TEXT("/Game/NocturneSignal/Input/IA_TentacleConsume.IA_TentacleConsume"));
    TentacleAlternateConsumeAction = FindNocturneAsset<UInputAction>(
        TEXT("/Game/NocturneSignal/Input/IA_TentacleAlternateConsume.IA_TentacleAlternateConsume"));

    if (VestigeTentacleVisualAdapter)
    {
        VestigeTentacleVisualAdapter->TentacleSkeletalMesh = nullptr;
        VestigeTentacleVisualAdapter->bHideVisualWhenIdle = true;
        VestigeTentacleVisualAdapter->bDrawFallbackDebugLine = false;
    }

    ApplyMovementTuning();
}

void ANocturnePlayerCharacter::BeginPlay()
{
    Super::BeginPlay();
    ApplyMovementTuning();
    InitializeJacobAnimationFallback();
    AddSliceInputMappingContext();
    RefreshSliceCameraViewTarget();

    if (VestigeLimbComponent)
    {
        VestigeLimbComponent->SetVisualAdapter(VestigeTentacleVisualAdapter);
        VestigeLimbComponent->OnGrappleStateChanged.AddUniqueDynamic(
            this,
            &ANocturnePlayerCharacter::HandleGrappleStateChanged);
    }
}

void ANocturnePlayerCharacter::PossessedBy(AController* NewController)
{
    Super::PossessedBy(NewController);
    AddSliceInputMappingContext();
    RefreshSliceCameraViewTarget();
}

void ANocturnePlayerCharacter::OnRep_Controller()
{
    Super::OnRep_Controller();
    AddSliceInputMappingContext();
    RefreshSliceCameraViewTarget();
}

void ANocturnePlayerCharacter::RefreshSliceCameraViewTarget()
{
    if (SideViewCamera)
    {
        SideViewCamera->SetActive(true);
    }

    APlayerController* PlayerController = Cast<APlayerController>(GetController());
    if (!PlayerController)
    {
        return;
    }

    PlayerController->SetViewTarget(this);
}

void ANocturnePlayerCharacter::UpdateSliceCameraFrame()
{
    if (!bClampSliceCameraVerticalFrame || !CameraBoom)
    {
        return;
    }

    const float DesiredWorldZ = GetActorLocation().Z + SliceCameraBaseOffsetZ;
    const float ClampedWorldZ = FMath::Clamp(DesiredWorldZ, SliceCameraMinWorldZ, SliceCameraMaxWorldZ);
    FVector RelativeLocation = CameraBoom->GetRelativeLocation();
    RelativeLocation.Z = ClampedWorldZ - GetActorLocation().Z;
    CameraBoom->SetRelativeLocation(RelativeLocation);
}

void ANocturnePlayerCharacter::ShowTentacleActionVisualCue(float ReachDistance)
{
    if (!VestigeTentacleVisualAdapter)
    {
        return;
    }

    const FVector Direction = FVector::ForwardVector;
    const FVector WorldStart = GetActorLocation() + FVector(0.0f, 0.0f, 46.0f);
    const FVector WorldEnd = WorldStart + Direction * FMath::Max(ReachDistance, 1.0f);
    VestigeTentacleVisualAdapter->UpdateLimbTarget(WorldStart, WorldEnd, 0.0f);
}

void ANocturnePlayerCharacter::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    UpdateSliceCameraFrame();
    UpdateJacobAnimationFallback();
    if (TraversalFallbackLockRemainingSeconds > 0.0f)
    {
        TraversalFallbackLockRemainingSeconds = FMath::Max(0.0f, TraversalFallbackLockRemainingSeconds - DeltaSeconds);
    }
}

void ANocturnePlayerCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    if (!PlayerInputComponent)
    {
        return;
    }

    if (UEnhancedInputComponent* EnhancedInputComponent = Cast<UEnhancedInputComponent>(PlayerInputComponent))
    {
        if (MoveHorizontalAction)
        {
            EnhancedInputComponent->BindAction(
                MoveHorizontalAction,
                ETriggerEvent::Triggered,
                this,
                &ANocturnePlayerCharacter::MoveHorizontalEnhancedInput);
        }

        if (MoveLeftAction)
        {
            EnhancedInputComponent->BindAction(MoveLeftAction, ETriggerEvent::Triggered, this, &ANocturnePlayerCharacter::MoveLeftEnhancedInput);
        }

        if (MoveRightAction)
        {
            EnhancedInputComponent->BindAction(MoveRightAction, ETriggerEvent::Triggered, this, &ANocturnePlayerCharacter::MoveRightEnhancedInput);
        }

        if (JumpAction)
        {
            EnhancedInputComponent->BindAction(JumpAction, ETriggerEvent::Started, this, &ANocturnePlayerCharacter::StartJumpEnhancedInput);
            EnhancedInputComponent->BindAction(JumpAction, ETriggerEvent::Completed, this, &ANocturnePlayerCharacter::StopJumpEnhancedInput);
            EnhancedInputComponent->BindAction(JumpAction, ETriggerEvent::Canceled, this, &ANocturnePlayerCharacter::StopJumpEnhancedInput);
        }

        if (SlideAction)
        {
            EnhancedInputComponent->BindAction(SlideAction, ETriggerEvent::Started, this, &ANocturnePlayerCharacter::StartSlideEnhancedInput);
            EnhancedInputComponent->BindAction(SlideAction, ETriggerEvent::Completed, this, &ANocturnePlayerCharacter::StopSlideEnhancedInput);
            EnhancedInputComponent->BindAction(SlideAction, ETriggerEvent::Canceled, this, &ANocturnePlayerCharacter::StopSlideEnhancedInput);
        }

        if (TentacleGrappleAction)
        {
            EnhancedInputComponent->BindAction(TentacleGrappleAction, ETriggerEvent::Started, this, &ANocturnePlayerCharacter::TriggerTentacleGrappleEnhancedInput);
        }

        if (TentacleAttackAction)
        {
            EnhancedInputComponent->BindAction(TentacleAttackAction, ETriggerEvent::Started, this, &ANocturnePlayerCharacter::TriggerTentacleAttackEnhancedInput);
        }

        if (TentacleConsumeAction)
        {
            EnhancedInputComponent->BindAction(TentacleConsumeAction, ETriggerEvent::Started, this, &ANocturnePlayerCharacter::TriggerTentacleConsumeEnhancedInput);
        }

        if (TentacleAlternateConsumeAction)
        {
            EnhancedInputComponent->BindAction(TentacleAlternateConsumeAction, ETriggerEvent::Started, this, &ANocturnePlayerCharacter::TriggerTentacleAlternateConsumeEnhancedInput);
        }

        return;
    }

    PlayerInputComponent->BindAxis(TEXT("MoveHorizontal"), this, &ANocturnePlayerCharacter::MoveHorizontal);
    PlayerInputComponent->BindAction(TEXT("Jump"), IE_Pressed, this, &ANocturnePlayerCharacter::StartJump);
    PlayerInputComponent->BindAction(TEXT("Jump"), IE_Released, this, &ANocturnePlayerCharacter::StopJump);
    PlayerInputComponent->BindAction(TEXT("Slide"), IE_Pressed, this, &ANocturnePlayerCharacter::StartSlideInput);
    PlayerInputComponent->BindAction(TEXT("Slide"), IE_Released, this, &ANocturnePlayerCharacter::StopSlide);
    PlayerInputComponent->BindAction(TEXT("TentacleGrapple"), IE_Pressed, this, &ANocturnePlayerCharacter::TriggerTentacleGrappleInput);
    PlayerInputComponent->BindAction(TEXT("TentacleAttack"), IE_Pressed, this, &ANocturnePlayerCharacter::TriggerTentacleAttackInput);
    PlayerInputComponent->BindAction(TEXT("TentacleConsume"), IE_Pressed, this, &ANocturnePlayerCharacter::TriggerTentacleConsumeInput);
    PlayerInputComponent->BindAction(TEXT("TentacleAlternateConsume"), IE_Pressed, this, &ANocturnePlayerCharacter::TriggerTentacleAlternateConsumeInput);
}

void ANocturnePlayerCharacter::MoveHorizontal(float AxisValue)
{
    if (FMath::IsNearlyZero(AxisValue))
    {
        return;
    }

    if (VestigeLimbComponent)
    {
        VestigeLimbComponent->SetPreferredGrappleDirection(FVector::ForwardVector * FMath::Sign(AxisValue));
    }

    AddMovementInput(FVector::ForwardVector, AxisValue);
}

void ANocturnePlayerCharacter::StartJump()
{
    const UCharacterMovementComponent* Movement = GetCharacterMovement();
    const bool bWantsDoubleJump = Movement && Movement->IsFalling() && JumpCurrentCount > 0;

    Jump();

    bIsDoubleJumping = bWantsDoubleJump;
    SetCurrentAbilityAnimation(
        bIsDoubleJumping ? ENocturneJacobAbilityAnimation::DoubleJump : ENocturneJacobAbilityAnimation::Jump);
    PlayJacobMontageOrFallback(
        bIsDoubleJumping ? DoubleJumpStartMontage : JumpStartMontage,
        bIsDoubleJumping ? DoubleJumpStartFallbackAnimation.Get() : JumpStartFallbackAnimation.Get(),
        false,
        NAME_None,
        TraversalStartFallbackDuration);
    HoldTraversalFallbackAnimation(TraversalStartFallbackDuration);
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
    PlayJacobMontageOrFallback(
        SlideStartMontage,
        SlideStartFallbackAnimation.Get(),
        false,
        NAME_None,
        TraversalStartFallbackDuration);
    HoldTraversalFallbackAnimation(TraversalStartFallbackDuration);
    return true;
}

void ANocturnePlayerCharacter::StartSlideInput()
{
    StartSlide();
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
    PlayJacobMontageOrFallback(
        SlideExitMontage,
        SlideExitFallbackAnimation.Get(),
        false,
        NAME_None,
        TraversalExitFallbackDuration);
    SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::None);
    HoldTraversalFallbackAnimation(TraversalExitFallbackDuration);
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
        ShowTentacleActionVisualCue(420.0f);
    }

    const float MontageDuration = PlayJacobMontageOrFallback(
        TentacleAttackMontage,
        TentacleAttackFallbackAnimation,
        false,
        TEXT("CastStart"),
        TentacleActionFallbackDuration);
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
        ShowTentacleActionVisualCue(360.0f);
    }

    UAnimMontage* Montage = bUseAlternateConsume ? TentacleConsumeAlternateMontage : TentacleConsumeMontage;
    UAnimationAsset* FallbackAnimation =
        bUseAlternateConsume ? TentacleAlternateConsumeFallbackAnimation.Get() : TentacleConsumeFallbackAnimation.Get();
    const float MontageDuration = PlayJacobMontageOrFallback(
        Montage,
        FallbackAnimation,
        false,
        TEXT("ConsumeStart"),
        TentacleActionFallbackDuration);
    if (MontageDuration <= 0.0f)
    {
        ClearTentacleActionState();
        return false;
    }

    ScheduleTentacleActionClear(MontageDuration);
    return true;
}

bool ANocturnePlayerCharacter::TriggerRecoveredCombatMontage(ENocturneJacobRecoveredCombatMontage MontageId)
{
    UAnimMontage* Montage = GetRecoveredCombatMontage(MontageId);
    if (!Montage)
    {
        return false;
    }

    SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::RecoveredCombat);
    const float MontageDuration = PlayJacobMontage(Montage, GetRecoveredCombatStartSection(MontageId));
    if (MontageDuration <= 0.0f)
    {
        ClearRecoveredCombatActionState();
        return false;
    }

    ScheduleRecoveredCombatActionClear(MontageDuration);
    return true;
}

UAnimMontage* ANocturnePlayerCharacter::GetRecoveredCombatMontage(ENocturneJacobRecoveredCombatMontage MontageId) const
{
    switch (MontageId)
    {
    case ENocturneJacobRecoveredCombatMontage::FireTrailAction01:
        return FireTrailAction01Montage;
    case ENocturneJacobRecoveredCombatMontage::FireTrailAction08:
        return FireTrailAction08Montage;
    case ENocturneJacobRecoveredCombatMontage::FireTrailAction16:
        return FireTrailAction16Montage;
    case ENocturneJacobRecoveredCombatMontage::FightingCrossPunch:
        return FightingCrossPunchMontage;
    case ENocturneJacobRecoveredCombatMontage::FightingHookPunch:
        return FightingHookPunchMontage;
    case ENocturneJacobRecoveredCombatMontage::FightingElbowPunch:
        return FightingElbowPunchMontage;
    case ENocturneJacobRecoveredCombatMontage::FightingImpact:
        return FightingImpactMontage;
    case ENocturneJacobRecoveredCombatMontage::FightingDeath:
        return FightingDeathMontage;
    default:
        return nullptr;
    }
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

bool ANocturnePlayerCharacter::IsJacobMontagePlaying() const
{
    const UAnimInstance* AnimInstance = GetMesh() ? GetMesh()->GetAnimInstance() : nullptr;
    return AnimInstance && AnimInstance->IsAnyMontagePlaying();
}

bool ANocturnePlayerCharacter::IsTentacleVisualVisible() const
{
    const USceneComponent* TentacleRoot = VestigeTentacleVisualAdapter
        ? VestigeTentacleVisualAdapter->GetTentacleVisualRoot()
        : nullptr;
    return TentacleRoot && TentacleRoot->IsVisible() && !TentacleRoot->bHiddenInGame;
}

ENocturneJacobAbilityAnimation ANocturnePlayerCharacter::GetCurrentAbilityAnimation() const
{
    return CurrentAbilityAnimation;
}

void ANocturnePlayerCharacter::Landed(const FHitResult& Hit)
{
    Super::Landed(Hit);

    PlayJacobMontageOrFallback(
        bIsDoubleJumping ? DoubleJumpLandMontage : JumpLandMontage,
        bIsDoubleJumping ? DoubleJumpLandFallbackAnimation.Get() : JumpLandAnimation.Get(),
        false,
        NAME_None,
        TraversalLandFallbackDuration);
    HoldTraversalFallbackAnimation(TraversalLandFallbackDuration);
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

    // Lock the prototype to the X/Z side-view plane used by the Sakura gameplay test map.
    Movement->bConstrainToPlane = true;
    Movement->SetPlaneConstraintNormal(FVector::RightVector);
}

void ANocturnePlayerCharacter::AddSliceInputMappingContext() const
{
    const APlayerController* PlayerController = Cast<APlayerController>(GetController());
    if (!PlayerController || !SliceInputMappingContext)
    {
        return;
    }

    ULocalPlayer* LocalPlayer = PlayerController->GetLocalPlayer();
    if (!LocalPlayer)
    {
        return;
    }

    if (UEnhancedInputLocalPlayerSubsystem* InputSubsystem =
        LocalPlayer->GetSubsystem<UEnhancedInputLocalPlayerSubsystem>())
    {
        InputSubsystem->AddMappingContext(SliceInputMappingContext, 0);
    }
}

float ANocturnePlayerCharacter::PlayJacobMontage(UAnimMontage* Montage, FName StartSection)
{
    if (!Montage)
    {
        return 0.0f;
    }

    // Some imported montage assets contain duplicate DefaultSlot tracks. Playing them
    // through AnimInstance montage APIs can fail; single-node playback keeps the slice moving.
    (void)StartSection;
    PlayJacobAnimationFallback(Montage, false);
    return Montage->GetPlayLength();
}

float ANocturnePlayerCharacter::PlayJacobMontageOrFallback(
    UAnimMontage* Montage,
    UAnimationAsset* FallbackAnimation,
    bool bLoopFallback,
    FName StartSection,
    float FallbackDuration)
{
    if ((bForceNativeAnimationFallback || bUsingSingleNodeAnimationFallback) && FallbackAnimation)
    {
        PlayJacobAnimationFallback(FallbackAnimation, bLoopFallback);
        if (FallbackDuration > 0.0f)
        {
            return FallbackDuration;
        }

        return bLoopFallback ? 0.0f : FallbackAnimation->GetPlayLength();
    }

    const float MontageDuration = PlayJacobMontage(Montage, StartSection);
    if (MontageDuration > 0.0f)
    {
        return MontageDuration;
    }

    if (!FallbackAnimation)
    {
        return 0.0f;
    }

    PlayJacobAnimationFallback(FallbackAnimation, bLoopFallback);
    if (FallbackDuration > 0.0f)
    {
        return FallbackDuration;
    }

    return bLoopFallback ? 0.0f : 0.2f;
}

void ANocturnePlayerCharacter::InitializeJacobAnimationFallback()
{
    USkeletalMeshComponent* MeshComponent = GetMesh();
    if (!MeshComponent || bUsingSingleNodeAnimationFallback)
    {
        return;
    }

    if (!bForceNativeAnimationFallback && MeshComponent->GetAnimInstance())
    {
        return;
    }

    if (!IdleAnimation)
    {
        return;
    }

    MeshComponent->SetAnimationMode(EAnimationMode::AnimationSingleNode);
    bUsingSingleNodeAnimationFallback = true;
    PlayJacobAnimationFallback(IdleAnimation, true);
}

void ANocturnePlayerCharacter::UpdateJacobAnimationFallback()
{
    const bool bIsTimedTentacleFallback =
        bIsTentacleActionActive
        && (CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::TentacleAttack
            || CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::TentacleConsume);
    const bool bIsGrappleActionActive =
        bIsTentacleActionActive
        && CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::TentacleGrapple;
    const bool bIsRecoveredCombatActionActive =
        CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::RecoveredCombat;

    if (!bUsingSingleNodeAnimationFallback
        || TraversalFallbackLockRemainingSeconds > 0.0f
        || bIsTimedTentacleFallback
        || bIsGrappleActionActive
        || bIsRecoveredCombatActionActive)
    {
        return;
    }

    const UCharacterMovementComponent* Movement = GetCharacterMovement();
    UAnimationAsset* DesiredAnimation = IdleAnimation;
    if (bIsSliding)
    {
        DesiredAnimation = SlideLoopAnimation ? SlideLoopAnimation.Get() : RunAnimation.Get();
    }
    else if (Movement && Movement->IsFalling())
    {
        if (CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::DoubleJump)
        {
            DesiredAnimation = DoubleJumpLoopAnimation ? DoubleJumpLoopAnimation.Get() : JumpLoopAnimation.Get();
        }
        else if (CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::Jump)
        {
            DesiredAnimation = JumpLoopAnimation ? JumpLoopAnimation.Get() : FallLoopAnimation.Get();
        }
        else
        {
            DesiredAnimation = FallLoopAnimation
                ? FallLoopAnimation.Get()
                : (JumpLoopAnimation ? JumpLoopAnimation.Get() : IdleAnimation.Get());
        }
    }
    else if (Movement)
    {
        const float HorizontalSpeed = FMath::Abs(GetVelocity().X);
        if (HorizontalSpeed > MaxWalkSpeed2D * 0.7f && RunAnimation)
        {
            DesiredAnimation = RunAnimation;
        }
        else if (HorizontalSpeed > 10.0f && WalkAnimation)
        {
            DesiredAnimation = WalkAnimation;
        }
    }

    PlayJacobAnimationFallback(DesiredAnimation, true);
}

void ANocturnePlayerCharacter::PlayJacobAnimationFallback(UAnimationAsset* Animation, bool bLoop)
{
    USkeletalMeshComponent* MeshComponent = GetMesh();
    if (!MeshComponent || !Animation)
    {
        return;
    }

    const bool bIsAlreadyPlayingAnimation =
        CurrentFallbackAnimation == Animation
        && MeshComponent->GetAnimationMode() == EAnimationMode::AnimationSingleNode
        && MeshComponent->IsPlaying()
        && !MeshComponent->bPauseAnims;
    if (bIsAlreadyPlayingAnimation)
    {
        return;
    }

    MeshComponent->SetAnimationMode(EAnimationMode::AnimationSingleNode);
    MeshComponent->SetPlayRate(1.0f);
    MeshComponent->PlayAnimation(Animation, bLoop);
    MeshComponent->bPauseAnims = false;
    MeshComponent->GlobalAnimRateScale = 1.0f;
    MeshComponent->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones;
    MeshComponent->RefreshBoneTransforms();
    bUsingSingleNodeAnimationFallback = true;
    CurrentFallbackAnimation = Animation;
}

void ANocturnePlayerCharacter::HoldTraversalFallbackAnimation(float DurationSeconds)
{
    TraversalFallbackLockRemainingSeconds = FMath::Max(TraversalFallbackLockRemainingSeconds, DurationSeconds);
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

    if (NewAbilityAnimation != ENocturneJacobAbilityAnimation::RecoveredCombat)
    {
        if (UWorld* World = GetWorld())
        {
            World->GetTimerManager().ClearTimer(RecoveredCombatActionTimerHandle);
        }
    }
}

FName ANocturnePlayerCharacter::GetRecoveredCombatStartSection(ENocturneJacobRecoveredCombatMontage MontageId) const
{
    switch (MontageId)
    {
    case ENocturneJacobRecoveredCombatMontage::FireTrailAction01:
    case ENocturneJacobRecoveredCombatMontage::FireTrailAction08:
    case ENocturneJacobRecoveredCombatMontage::FireTrailAction16:
        return TEXT("AttackStart");
    case ENocturneJacobRecoveredCombatMontage::FightingCrossPunch:
    case ENocturneJacobRecoveredCombatMontage::FightingHookPunch:
    case ENocturneJacobRecoveredCombatMontage::FightingElbowPunch:
        return TEXT("StrikeStart");
    case ENocturneJacobRecoveredCombatMontage::FightingImpact:
        return TEXT("ReactStart");
    case ENocturneJacobRecoveredCombatMontage::FightingDeath:
        return TEXT("DeathStart");
    default:
        return NAME_None;
    }
}

void ANocturnePlayerCharacter::TriggerTentacleAttackInput()
{
    TriggerTentacleAttack();
}

void ANocturnePlayerCharacter::TriggerTentacleGrappleInput()
{
    TriggerTentacleGrapple();
}

void ANocturnePlayerCharacter::TriggerTentacleConsumeInput()
{
    TriggerTentacleConsume(false);
}

void ANocturnePlayerCharacter::TriggerTentacleAlternateConsumeInput()
{
    TriggerTentacleConsume(true);
}

void ANocturnePlayerCharacter::MoveHorizontalEnhancedInput(const FInputActionValue& Value)
{
    MoveHorizontal(Value.Get<float>());
}

void ANocturnePlayerCharacter::MoveLeftEnhancedInput(const FInputActionValue& Value)
{
    if (Value.Get<bool>())
    {
        MoveHorizontal(-1.0f);
    }
}

void ANocturnePlayerCharacter::MoveRightEnhancedInput(const FInputActionValue& Value)
{
    if (Value.Get<bool>())
    {
        MoveHorizontal(1.0f);
    }
}

void ANocturnePlayerCharacter::StartJumpEnhancedInput(const FInputActionValue& Value)
{
    if (Value.Get<bool>())
    {
        StartJump();
    }
}

void ANocturnePlayerCharacter::StopJumpEnhancedInput(const FInputActionValue& Value)
{
    StopJump();
}

void ANocturnePlayerCharacter::StartSlideEnhancedInput(const FInputActionValue& Value)
{
    if (Value.Get<bool>())
    {
        StartSlide();
    }
}

void ANocturnePlayerCharacter::StopSlideEnhancedInput(const FInputActionValue& Value)
{
    StopSlide();
}

void ANocturnePlayerCharacter::TriggerTentacleAttackEnhancedInput(const FInputActionValue& Value)
{
    if (Value.Get<bool>())
    {
        TriggerTentacleAttack();
    }
}

void ANocturnePlayerCharacter::TriggerTentacleGrappleEnhancedInput(const FInputActionValue& Value)
{
    if (Value.Get<bool>())
    {
        TriggerTentacleGrapple();
    }
}

void ANocturnePlayerCharacter::TriggerTentacleConsumeEnhancedInput(const FInputActionValue& Value)
{
    if (Value.Get<bool>())
    {
        TriggerTentacleConsume(false);
    }
}

void ANocturnePlayerCharacter::TriggerTentacleAlternateConsumeEnhancedInput(const FInputActionValue& Value)
{
    if (Value.Get<bool>())
    {
        TriggerTentacleConsume(true);
    }
}

void ANocturnePlayerCharacter::HandleGrappleStateChanged(EVestigeGrappleState NewState)
{
    switch (NewState)
    {
    case EVestigeGrappleState::Extending:
        bIsTentacleActionActive = true;
        SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::TentacleGrapple);
        PlayJacobMontageOrFallback(
            TentacleGrappleStartMontage,
            TentacleGrappleStartFallbackAnimation,
            false,
            TEXT("GrappleStart"));
        break;

    case EVestigeGrappleState::PullingPlayer:
        bIsTentacleActionActive = true;
        SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::TentacleGrapple);
        PlayJacobMontageOrFallback(
            TentacleGrappleLoopMontage,
            TentacleGrappleFallbackAnimation,
            true,
            TEXT("GrappleLoop"));
        break;

    case EVestigeGrappleState::Releasing:
    case EVestigeGrappleState::Retracting:
        PlayJacobMontageOrFallback(
            TentacleGrappleEndMontage,
            TentacleGrappleReleaseFallbackAnimation,
            false,
            TEXT("GrappleRelease"),
            0.2f);
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

void ANocturnePlayerCharacter::ScheduleRecoveredCombatActionClear(float DelaySeconds)
{
    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    World->GetTimerManager().SetTimer(
        RecoveredCombatActionTimerHandle,
        this,
        &ANocturnePlayerCharacter::ClearRecoveredCombatActionState,
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

void ANocturnePlayerCharacter::ClearRecoveredCombatActionState()
{
    if (CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::RecoveredCombat)
    {
        SetCurrentAbilityAnimation(ENocturneJacobAbilityAnimation::None);
    }
}
