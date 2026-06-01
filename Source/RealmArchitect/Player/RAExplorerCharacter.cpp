#include "Player/RAExplorerCharacter.h"
#include "RAArtAssetCatalog.h"
#include "Player/RACameraModeComponent.h"
#include "Player/RAGrappleComponent.h"
#include "Animation/AnimSequence.h"
#include "Camera/CameraComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/GameplayStatics.h"
#include "NiagaraFunctionLibrary.h"
#include "NiagaraSystem.h"

namespace
{
    constexpr const TCHAR* TransformAuraPath = TEXT("/Game/Free_Spells/VFX_Niagara/NS_Free_Spells_Aura_Lightning.NS_Free_Spells_Aura_Lightning");
    constexpr const TCHAR* TransformSpellShockwavePath = TEXT("/Game/Free_Spells/VFX_Niagara/NS_Free_Spells_Shockwave.NS_Free_Spells_Shockwave");
    constexpr const TCHAR* TransformZapPath = TEXT("/Game/Vefects/Zap_VFX/VFX/Zap/Particles/NS_Zap_02_Blue.NS_Zap_02_Blue");
    constexpr const TCHAR* TransformImpactFramePath = TEXT("/Game/Vefects/Easy_Impact_Frames/VFX/Frames/Particles/Tests/NS_Impact_Frame_01.NS_Impact_Frame_01");
    constexpr const TCHAR* TransformShockwavePath = TEXT("/Game/Vefects/Easy_Shockwaves_VFX/VFX/Shockwaves/Particles/Color_Variation/VFX_Shockwave_01_Purple_Big_1s.VFX_Shockwave_01_Purple_Big_1s");
    constexpr const TCHAR* TransformWormholePath = TEXT("/Game/FreeNiagaraPack/Effects/NS_Worm-Hole.NS_Worm-Hole");
    constexpr const TCHAR* TransformFireExplosionPath = TEXT("/Game/Fire_EXP_Vol01_Free/Niagara/EXP/NS_Sub_EXP_Mid_002_02.NS_Sub_EXP_Mid_002_02");
    constexpr const TCHAR* TransformFireTrailPath = TEXT("/Game/FIRETRAILOFTHESWORD/VFX/NS_Trail_14.NS_Trail_14");
    constexpr const TCHAR* JacobSkeletalMeshPath = TEXT("/Game/RealmArchitect/Art/Jacob/Jacob_NocturneCharacterOnly.Jacob_NocturneCharacterOnly");
    constexpr const TCHAR* JacobIdleAnimationPath = TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/JacobRTG_MM_Idle.JacobRTG_MM_Idle");
    constexpr const TCHAR* JacobWalkAnimationPath = TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/JacobRTG_MF_Unarmed_Walk_Fwd.JacobRTG_MF_Unarmed_Walk_Fwd");
    constexpr const TCHAR* JacobJogAnimationPath = TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/JacobRTG_MF_Unarmed_Jog_Fwd.JacobRTG_MF_Unarmed_Jog_Fwd");
    constexpr const TCHAR* JacobJumpAnimationPath = TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/JacobRTG_MM_Jump.JacobRTG_MM_Jump");
    constexpr const TCHAR* JacobFallAnimationPath = TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/JacobRTG_MM_Fall_Loop.JacobRTG_MM_Fall_Loop");
    constexpr const TCHAR* JacobReadySwordAnimationPath = TEXT("/Game/RealmArchitect/Art/Jacob/Jacob_NocturneCharacterOnly_Anim_Armature_Jacob_ReadySword.Jacob_NocturneCharacterOnly_Anim_Armature_Jacob_ReadySword");
    constexpr const TCHAR* JacobActionAnimationPaths[] = {
        JacobReadySwordAnimationPath,
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Combat/JacobUE4_Cross_Punch_Anim.JacobUE4_Cross_Punch_Anim"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Combat/JacobUE4_Elbow_Punching.JacobUE4_Elbow_Punching"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Combat/JacobUE4_Hook_Punch.JacobUE4_Hook_Punch"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Combat/JacobUE4_Punching.JacobUE4_Punching"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Combat/JacobUE4_Punching__1_.JacobUE4_Punching__1_"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Combat/JacobUE4_Punching__2_.JacobUE4_Punching__2_"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Combat/JacobUE4_Punching__3_.JacobUE4_Punching__3_"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_01.JacobFire_A_NS_01"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_02.JacobFire_A_NS_02"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_03.JacobFire_A_NS_03"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_04.JacobFire_A_NS_04"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_05.JacobFire_A_NS_05"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_06.JacobFire_A_NS_06"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_07.JacobFire_A_NS_07"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_08.JacobFire_A_NS_08"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_09.JacobFire_A_NS_09"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_10.JacobFire_A_NS_10"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_11.JacobFire_A_NS_11"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_12.JacobFire_A_NS_12"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_13.JacobFire_A_NS_13"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_14.JacobFire_A_NS_14"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_15.JacobFire_A_NS_15"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_16.JacobFire_A_NS_16"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_17.JacobFire_A_NS_17"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_18.JacobFire_A_NS_18"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_19.JacobFire_A_NS_19"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_20.JacobFire_A_NS_20"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_21.JacobFire_A_NS_21"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_22.JacobFire_A_NS_22"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_23.JacobFire_A_NS_23"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_24.JacobFire_A_NS_24"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_25.JacobFire_A_NS_25"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword/JacobFire_A_NS_26.JacobFire_A_NS_26"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_AirDash_Vexa.JacobVexa_AirDash_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_AirStomp_Vexa.JacobVexa_AirStomp_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_Dash_Vexa.JacobVexa_Dash_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_GunShot01_Vexa.JacobVexa_GunShot01_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_GunShot02_Vexa.JacobVexa_GunShot02_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_GunShot03_Vexa.JacobVexa_GunShot03_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_GunShotComplete_Vexa.JacobVexa_GunShotComplete_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_HandsSpell_Vexa.JacobVexa_HandsSpell_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_Healing_Vexa.JacobVexa_Healing_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_MagicWand_Vexa.JacobVexa_MagicWand_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_SnappySpell_Vexa.JacobVexa_SnappySpell_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_Stomp_Vexa.JacobVexa_Stomp_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_SummonCreature_Vexa.JacobVexa_SummonCreature_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_SwordAttack_Vexa.JacobVexa_SwordAttack_Vexa"),
        TEXT("/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic/JacobVexa_SwordSlash_Vexa.JacobVexa_SwordSlash_Vexa"),
    };
    constexpr int32 JacobActionAnimationCount = static_cast<int32>(sizeof(JacobActionAnimationPaths) / sizeof(JacobActionAnimationPaths[0]));
}

ARAExplorerCharacter::ARAExplorerCharacter()
{
    PrimaryActorTick.bCanEverTick = true;

    bUseControllerRotationPitch = false;
    bUseControllerRotationYaw = false;
    bUseControllerRotationRoll = false;

    GetCharacterMovement()->bOrientRotationToMovement = true;
    GetCharacterMovement()->RotationRate = FRotator(0.0f, 540.0f, 0.0f);
    GetCharacterMovement()->JumpZVelocity = 600.0f;
    GetCharacterMovement()->AirControl = 0.2f;
    GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;

    CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
    CameraBoom->SetupAttachment(RootComponent);
    CameraBoom->TargetArmLength = BaseCameraBoomLength;
    CameraBoom->bUsePawnControlRotation = true;

    FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
    FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName);
    FollowCamera->bUsePawnControlRotation = false;

    CameraModeComponent = CreateDefaultSubobject<URACameraModeComponent>(TEXT("CameraModeComponent"));
    GrappleComponent = CreateDefaultSubobject<URAGrappleComponent>(TEXT("GrappleComponent"));

    ConfigureJacobAnimatedMesh();

    AvatarMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("AvatarMesh"));
    AvatarMesh->SetupAttachment(RootComponent);
    AvatarMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);

    DraconicAvatarMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("DraconicAvatarMesh"));
    DraconicAvatarMesh->SetupAttachment(RootComponent);
    DraconicAvatarMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    DraconicAvatarMesh->SetVisibility(false);

    TransformLight = CreateDefaultSubobject<UPointLightComponent>(TEXT("TransformLight"));
    TransformLight->SetupAttachment(RootComponent);
    TransformLight->SetRelativeLocation(FVector(0.0f, 0.0f, 72.0f));
    TransformLight->SetAttenuationRadius(620.0f);
    TransformLight->SetIntensity(0.0f);
    TransformLight->SetLightColor(TransformLightColor);

    ApplyFormImmediate(false);
}

void ARAExplorerCharacter::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    UpdateFormTransition(DeltaSeconds);
    UpdateJacobLocomotionAnimation();
}

void ARAExplorerCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    PlayerInputComponent->BindAxis(TEXT("MoveForward"), this, &ARAExplorerCharacter::MoveForward);
    PlayerInputComponent->BindAxis(TEXT("MoveRight"), this, &ARAExplorerCharacter::MoveRight);
    PlayerInputComponent->BindAxis(TEXT("Turn"), this, &APawn::AddControllerYawInput);
    PlayerInputComponent->BindAxis(TEXT("LookUp"), this, &APawn::AddControllerPitchInput);
    PlayerInputComponent->BindAxis(TEXT("TurnRate"), this, &ARAExplorerCharacter::TurnAtRate);
    PlayerInputComponent->BindAxis(TEXT("LookUpRate"), this, &ARAExplorerCharacter::LookUpAtRate);

    PlayerInputComponent->BindAction(TEXT("Jump"), IE_Pressed, this, &ACharacter::Jump);
    PlayerInputComponent->BindAction(TEXT("Jump"), IE_Released, this, &ACharacter::StopJumping);
    PlayerInputComponent->BindAction(TEXT("Sprint"), IE_Pressed, this, &ARAExplorerCharacter::StartSprint);
    PlayerInputComponent->BindAction(TEXT("Sprint"), IE_Released, this, &ARAExplorerCharacter::StopSprint);
    PlayerInputComponent->BindAction(TEXT("Grapple"), IE_Pressed, this, &ARAExplorerCharacter::StartGrapple);
    PlayerInputComponent->BindAction(TEXT("Grapple"), IE_Released, this, &ARAExplorerCharacter::StopGrapple);
    PlayerInputComponent->BindAction(TEXT("ToggleDraconicForm"), IE_Pressed, this, &ARAExplorerCharacter::ToggleDraconicForm);
    PlayerInputComponent->BindAction(TEXT("RA_Slice11_Attack"), IE_Pressed, this, &ARAExplorerCharacter::PlayJacobActionAnimation);
}

void ARAExplorerCharacter::MoveForward(float Value)
{
    if (Controller && FMath::Abs(Value) > KINDA_SMALL_NUMBER)
    {
        const FRotator Rotation = Controller->GetControlRotation();
        const FRotator YawRotation(0.0f, Rotation.Yaw, 0.0f);
        const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
        AddMovementInput(Direction, Value);
    }
}

void ARAExplorerCharacter::MoveRight(float Value)
{
    if (Controller && FMath::Abs(Value) > KINDA_SMALL_NUMBER)
    {
        const FRotator Rotation = Controller->GetControlRotation();
        const FRotator YawRotation(0.0f, Rotation.Yaw, 0.0f);
        const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y);
        AddMovementInput(Direction, Value);
    }
}

void ARAExplorerCharacter::TurnAtRate(float Rate)
{
    AddControllerYawInput(Rate * BaseTurnRate * GetWorld()->GetDeltaSeconds());
}

void ARAExplorerCharacter::LookUpAtRate(float Rate)
{
    AddControllerPitchInput(Rate * BaseLookUpRate * GetWorld()->GetDeltaSeconds());
}

void ARAExplorerCharacter::StartSprint()
{
    GetCharacterMovement()->MaxWalkSpeed = SprintSpeed;
}

void ARAExplorerCharacter::StopSprint()
{
    GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;
}

void ARAExplorerCharacter::StartGrapple()
{
    if (GrappleComponent)
    {
        GrappleComponent->StartGrapple();
    }
}

void ARAExplorerCharacter::StopGrapple()
{
    if (GrappleComponent)
    {
        GrappleComponent->StopGrapple();
    }
}

void ARAExplorerCharacter::ToggleDraconicForm()
{
    SetDraconicForm(!bIsInDraconicForm);
}

void ARAExplorerCharacter::PlayJacobActionAnimation()
{
    USkeletalMeshComponent* CharacterMesh = GetMesh();
    int32 ResolvedActionIndex = INDEX_NONE;
    UAnimSequence* ActionAnimation = LoadJacobActionAnimation(NextJacobActionAnimationIndex, ResolvedActionIndex);
    if (!CharacterMesh || !CharacterMesh->GetSkeletalMeshAsset() || !ActionAnimation || bIsInDraconicForm || bTransformInProgress)
    {
        return;
    }

    if (ResolvedActionIndex != INDEX_NONE)
    {
        NextJacobActionAnimationIndex = (ResolvedActionIndex + 1) % JacobActionAnimationCount;
    }

    CharacterMesh->SetAnimationMode(EAnimationMode::AnimationSingleNode);
    bJacobActionAnimationActive = true;
    PlayJacobAnimation(ActionAnimation, false, EJacobAnimationState::Action, true);

    GetWorldTimerManager().ClearTimer(JacobIdleReturnTimerHandle);
    GetWorldTimerManager().SetTimer(
        JacobIdleReturnTimerHandle,
        this,
        &ARAExplorerCharacter::FinishJacobActionAnimation,
        FMath::Max(ActionAnimation->GetPlayLength(), 0.1f),
        false);
}

void ARAExplorerCharacter::PlayJacobIdleLoop()
{
    USkeletalMeshComponent* CharacterMesh = GetMesh();
    UAnimSequence* IdleAnimation = LoadJacobIdleAnimation();
    if (!CharacterMesh || !CharacterMesh->GetSkeletalMeshAsset() || !IdleAnimation || bIsInDraconicForm)
    {
        return;
    }

    CharacterMesh->SetAnimationMode(EAnimationMode::AnimationSingleNode);
    bJacobActionAnimationActive = false;
    PlayJacobAnimation(IdleAnimation, true, EJacobAnimationState::Idle, true);
}

void ARAExplorerCharacter::FinishJacobActionAnimation()
{
    bJacobActionAnimationActive = false;
    CurrentJacobAnimation = nullptr;
    CurrentJacobAnimationState = EJacobAnimationState::None;
    UpdateJacobLocomotionAnimation();
}

void ARAExplorerCharacter::UpdateJacobLocomotionAnimation()
{
    USkeletalMeshComponent* CharacterMesh = GetMesh();
    if (!CharacterMesh || !CharacterMesh->GetSkeletalMeshAsset() || bIsInDraconicForm || bTransformInProgress || bJacobActionAnimationActive)
    {
        return;
    }

    UAnimSequence* DesiredAnimation = LoadJacobIdleAnimation();
    EJacobAnimationState DesiredState = EJacobAnimationState::Idle;
    bool bLoop = true;

    const UCharacterMovementComponent* Movement = GetCharacterMovement();
    if (Movement && Movement->IsFalling())
    {
        const bool bAscending = GetVelocity().Z > 75.0f;
        DesiredAnimation = bAscending ? LoadJacobJumpAnimation() : LoadJacobFallAnimation();
        DesiredState = bAscending ? EJacobAnimationState::Jump : EJacobAnimationState::Fall;
        bLoop = !bAscending;
    }
    else
    {
        const FVector HorizontalVelocity(GetVelocity().X, GetVelocity().Y, 0.0f);
        const float GroundSpeed = HorizontalVelocity.Size();
        if (GroundSpeed > 30.0f)
        {
            const bool bSprinting = Movement && Movement->MaxWalkSpeed > WalkSpeed + 1.0f;
            DesiredAnimation = bSprinting ? LoadJacobJogAnimation() : LoadJacobWalkAnimation();
            DesiredState = bSprinting ? EJacobAnimationState::Jog : EJacobAnimationState::Walk;
        }
    }

    if (!DesiredAnimation)
    {
        DesiredAnimation = LoadJacobIdleAnimation();
        DesiredState = EJacobAnimationState::Idle;
        bLoop = true;
    }

    PlayJacobAnimation(DesiredAnimation, bLoop, DesiredState);
}

void ARAExplorerCharacter::PlayJacobAnimation(UAnimSequence* Animation, bool bLoop, EJacobAnimationState NewState, bool bForceRestart)
{
    USkeletalMeshComponent* CharacterMesh = GetMesh();
    if (!CharacterMesh || !CharacterMesh->GetSkeletalMeshAsset() || !Animation)
    {
        return;
    }

    if (!bForceRestart && CurrentJacobAnimation == Animation && CurrentJacobAnimationState == NewState && bCurrentJacobAnimationLoops == bLoop)
    {
        return;
    }

    CharacterMesh->SetAnimationMode(EAnimationMode::AnimationSingleNode);
    CharacterMesh->PlayAnimation(Animation, bLoop);
    CurrentJacobAnimation = Animation;
    CurrentJacobAnimationState = NewState;
    bCurrentJacobAnimationLoops = bLoop;
}

void ARAExplorerCharacter::SetDraconicForm(bool bNewDraconicForm)
{
    if (bIsInDraconicForm == bNewDraconicForm && !bTransformInProgress)
    {
        return;
    }

    if (GetWorld() && GetWorld()->HasBegunPlay())
    {
        BeginFormTransition(bNewDraconicForm);
        return;
    }

    ApplyFormImmediate(bNewDraconicForm);
}

void ARAExplorerCharacter::BeginFormTransition(bool bNewDraconicForm)
{
    if (!AvatarMesh || !DraconicAvatarMesh)
    {
        ApplyFormImmediate(bNewDraconicForm);
        return;
    }

    if (UStaticMesh* NormalArt = URAArtAssetCatalog::ResolveRoleMesh(ERAArtAssetRole::PlayerAvatar))
    {
        AvatarMesh->SetStaticMesh(NormalArt);
    }
    if (UStaticMesh* DraconicArt = URAArtAssetCatalog::ResolveRoleMesh(ERAArtAssetRole::HeroDraconicForm))
    {
        DraconicAvatarMesh->SetStaticMesh(DraconicArt);
    }

    bPendingDraconicForm = bNewDraconicForm;
    bTransformInProgress = true;
    TransformElapsed = 0.0f;

    const bool bHasJacobMesh = GetMesh() && GetMesh()->GetSkeletalMeshAsset();
    SetJacobAnimatedMeshVisible(bHasJacobMesh);
    AvatarMesh->SetVisibility(!bHasJacobMesh);
    DraconicAvatarMesh->SetVisibility(true);

    if (Controller)
    {
        AddControllerPitchInput(-1.35f);
        AddControllerYawInput(bNewDraconicForm ? 2.0f : -2.0f);
    }

    SpawnTransformVFX(bNewDraconicForm);
}

void ARAExplorerCharacter::ApplyFormImmediate(bool bNewDraconicForm)
{
    bIsInDraconicForm = bNewDraconicForm;
    bPendingDraconicForm = bNewDraconicForm;
    bTransformInProgress = false;
    TransformElapsed = 0.0f;

    if (UStaticMesh* NormalArt = URAArtAssetCatalog::ResolveRoleMesh(ERAArtAssetRole::PlayerAvatar))
    {
        AvatarMesh->SetStaticMesh(NormalArt);
    }
    if (UStaticMesh* DraconicArt = URAArtAssetCatalog::ResolveRoleMesh(ERAArtAssetRole::HeroDraconicForm))
    {
        DraconicAvatarMesh->SetStaticMesh(DraconicArt);
    }

    AvatarMesh->SetRelativeLocation(NormalFormMeshOffset);
    AvatarMesh->SetRelativeRotation(FRotator::ZeroRotator);
    AvatarMesh->SetRelativeScale3D(NormalFormMeshScale);

    const bool bHasJacobMesh = GetMesh() && GetMesh()->GetSkeletalMeshAsset();
    SetJacobAnimatedMeshVisible(!bIsInDraconicForm && bHasJacobMesh);
    AvatarMesh->SetVisibility(!bIsInDraconicForm && !bHasJacobMesh);

    DraconicAvatarMesh->SetRelativeLocation(DraconicFormMeshOffset);
    DraconicAvatarMesh->SetRelativeRotation(FRotator::ZeroRotator);
    DraconicAvatarMesh->SetRelativeScale3D(DraconicFormMeshScale);
    DraconicAvatarMesh->SetVisibility(bIsInDraconicForm);

    if (TransformLight)
    {
        TransformLight->SetIntensity(0.0f);
    }
    if (CameraBoom)
    {
        CameraBoom->TargetArmLength = BaseCameraBoomLength;
    }
}

void ARAExplorerCharacter::ConfigureJacobAnimatedMesh()
{
    USkeletalMeshComponent* CharacterMesh = GetMesh();
    if (!CharacterMesh)
    {
        return;
    }

    CharacterMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    CharacterMesh->SetRelativeLocation(NormalFormMeshOffset);
    CharacterMesh->SetRelativeRotation(FRotator(0.0f, -90.0f, 0.0f));
    CharacterMesh->SetRelativeScale3D(FVector(1.0f));
    CharacterMesh->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones;

    if (USkeletalMesh* JacobMesh = LoadJacobSkeletalMesh())
    {
        CharacterMesh->SetSkeletalMesh(JacobMesh);
    }

    UpdateJacobLocomotionAnimation();
}

void ARAExplorerCharacter::SetJacobAnimatedMeshVisible(bool bVisible)
{
    if (USkeletalMeshComponent* CharacterMesh = GetMesh())
    {
        CharacterMesh->SetVisibility(bVisible, true);
        CharacterMesh->SetHiddenInGame(!bVisible);
        if (bVisible && CharacterMesh->GetSkeletalMeshAsset())
        {
            CurrentJacobAnimation = nullptr;
            CurrentJacobAnimationState = EJacobAnimationState::None;
            UpdateJacobLocomotionAnimation();
        }
        else
        {
            bJacobActionAnimationActive = false;
            CurrentJacobAnimation = nullptr;
            CurrentJacobAnimationState = EJacobAnimationState::None;
            GetWorldTimerManager().ClearTimer(JacobIdleReturnTimerHandle);
        }
    }
}

void ARAExplorerCharacter::UpdateFormTransition(float DeltaSeconds)
{
    if (!bTransformInProgress || !AvatarMesh || !DraconicAvatarMesh)
    {
        return;
    }

    TransformElapsed += DeltaSeconds;
    const float RawAlpha = FMath::Clamp(TransformElapsed / FMath::Max(TransformDuration, 0.1f), 0.0f, 1.0f);
    const float Alpha = FMath::InterpEaseInOut(0.0f, 1.0f, RawAlpha, 2.2f);
    const float Pulse = FMath::Sin(RawAlpha * PI);
    const float SpinYaw = TransformSpinDegrees * Alpha * (bPendingDraconicForm ? 1.0f : -1.0f);

    const float NormalPresence = bPendingDraconicForm ? (1.0f - Alpha) : Alpha;
    const float DraconicPresence = bPendingDraconicForm ? Alpha : (1.0f - Alpha);
    const FVector NormalScale = NormalFormMeshScale * FMath::Max(0.04f, NormalPresence + Pulse * 0.16f);
    const FVector DraconicScale = DraconicFormMeshScale * FMath::Max(0.04f, DraconicPresence + Pulse * 0.22f);

    AvatarMesh->SetRelativeLocation(NormalFormMeshOffset + FVector(0.0f, 0.0f, Pulse * 24.0f));
    AvatarMesh->SetRelativeRotation(FRotator(0.0f, SpinYaw, 0.0f));
    AvatarMesh->SetRelativeScale3D(NormalScale);

    DraconicAvatarMesh->SetRelativeLocation(DraconicFormMeshOffset + FVector(0.0f, 0.0f, Pulse * 36.0f));
    DraconicAvatarMesh->SetRelativeRotation(FRotator(0.0f, SpinYaw + (bPendingDraconicForm ? -28.0f : 28.0f), 0.0f));
    DraconicAvatarMesh->SetRelativeScale3D(DraconicScale);

    if (TransformLight)
    {
        TransformLight->SetIntensity(TransformLightPeakIntensity * Pulse);
        TransformLight->SetLightColor(TransformLightColor);
    }

    if (CameraBoom)
    {
        CameraBoom->TargetArmLength = BaseCameraBoomLength + TransformCameraBoomPulse * Pulse;
    }

    if (RawAlpha >= 1.0f)
    {
        ApplyFormImmediate(bPendingDraconicForm);
    }
}

void ARAExplorerCharacter::SpawnTransformVFX(bool bNewDraconicForm) const
{
    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    const FVector BaseLocation = GetActorLocation() + TransformVFXOffset;
    const FRotator BaseRotation = FRotator::ZeroRotator;
    const FVector LargeScale = bNewDraconicForm ? FVector(1.45f) : FVector(1.15f);

    if (UNiagaraSystem* Aura = LoadTransformNiagaraSystem(TransformAuraPath))
    {
        UNiagaraFunctionLibrary::SpawnSystemAtLocation(World, Aura, GetActorLocation(), BaseRotation, FVector(1.15f), true, true);
    }
    if (UNiagaraSystem* SpellShockwave = LoadTransformNiagaraSystem(TransformSpellShockwavePath))
    {
        UNiagaraFunctionLibrary::SpawnSystemAtLocation(World, SpellShockwave, BaseLocation, BaseRotation, LargeScale, true, true);
    }
    if (UNiagaraSystem* Zap = LoadTransformNiagaraSystem(TransformZapPath))
    {
        UNiagaraFunctionLibrary::SpawnSystemAtLocation(World, Zap, GetActorLocation() + FVector(0.0f, 0.0f, 80.0f), BaseRotation, FVector(1.25f), true, true);
    }
    if (UNiagaraSystem* Wormhole = LoadTransformNiagaraSystem(TransformWormholePath))
    {
        UNiagaraFunctionLibrary::SpawnSystemAtLocation(World, Wormhole, GetActorLocation() + FVector(0.0f, 0.0f, 92.0f), BaseRotation, FVector(0.95f), true, true);
    }
    if (UNiagaraSystem* FireExplosion = LoadTransformNiagaraSystem(TransformFireExplosionPath))
    {
        UNiagaraFunctionLibrary::SpawnSystemAtLocation(World, FireExplosion, BaseLocation, BaseRotation, FVector(0.82f), true, true);
    }
    if (UNiagaraSystem* FireTrail = LoadTransformNiagaraSystem(TransformFireTrailPath))
    {
        UNiagaraFunctionLibrary::SpawnSystemAtLocation(World, FireTrail, GetActorLocation() + FVector(0.0f, 0.0f, 96.0f), GetActorRotation(), FVector(1.0f), true, true);
    }
    if (UNiagaraSystem* ImpactFrame = LoadTransformNiagaraSystem(TransformImpactFramePath))
    {
        UNiagaraFunctionLibrary::SpawnSystemAtLocation(World, ImpactFrame, GetActorLocation() + FVector(0.0f, 0.0f, 72.0f), BaseRotation, FVector(1.0f), true, true);
    }
    if (UParticleSystem* Shockwave = LoadTransformParticleSystem(TransformShockwavePath))
    {
        UGameplayStatics::SpawnEmitterAtLocation(World, Shockwave, FTransform(BaseRotation, BaseLocation, LargeScale), true);
    }
}

USkeletalMesh* ARAExplorerCharacter::LoadJacobSkeletalMesh()
{
    return LoadObject<USkeletalMesh>(nullptr, JacobSkeletalMeshPath);
}

UAnimSequence* ARAExplorerCharacter::LoadJacobIdleAnimation()
{
    return LoadJacobAnimation(JacobIdleAnimationPath);
}

UAnimSequence* ARAExplorerCharacter::LoadJacobWalkAnimation()
{
    return LoadJacobAnimation(JacobWalkAnimationPath);
}

UAnimSequence* ARAExplorerCharacter::LoadJacobJogAnimation()
{
    return LoadJacobAnimation(JacobJogAnimationPath);
}

UAnimSequence* ARAExplorerCharacter::LoadJacobJumpAnimation()
{
    return LoadJacobAnimation(JacobJumpAnimationPath);
}

UAnimSequence* ARAExplorerCharacter::LoadJacobFallAnimation()
{
    return LoadJacobAnimation(JacobFallAnimationPath);
}

UAnimSequence* ARAExplorerCharacter::LoadJacobActionAnimation(int32 ActionIndex, int32& OutResolvedIndex)
{
    OutResolvedIndex = INDEX_NONE;
    if (JacobActionAnimationCount <= 0)
    {
        return nullptr;
    }

    const int32 NormalizedStartIndex = ((ActionIndex % JacobActionAnimationCount) + JacobActionAnimationCount) % JacobActionAnimationCount;
    for (int32 Offset = 0; Offset < JacobActionAnimationCount; ++Offset)
    {
        const int32 CandidateIndex = (NormalizedStartIndex + Offset) % JacobActionAnimationCount;
        if (UAnimSequence* Animation = LoadJacobAnimation(JacobActionAnimationPaths[CandidateIndex]))
        {
            OutResolvedIndex = CandidateIndex;
            return Animation;
        }
    }

    return nullptr;
}

UAnimSequence* ARAExplorerCharacter::LoadJacobAnimation(const TCHAR* Path)
{
    return LoadObject<UAnimSequence>(nullptr, Path);
}

UNiagaraSystem* ARAExplorerCharacter::LoadTransformNiagaraSystem(const TCHAR* Path)
{
    return LoadObject<UNiagaraSystem>(nullptr, Path);
}

UParticleSystem* ARAExplorerCharacter::LoadTransformParticleSystem(const TCHAR* Path)
{
    return LoadObject<UParticleSystem>(nullptr, Path);
}
