#include "VestigeTentacleVisualAdapter.h"
#include "DrawDebugHelpers.h"
#include "GrappleAnchor.h"
#include "Animation/AnimationAsset.h"
#include "Components/SceneComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/Actor.h"
#include "GameFramework/Character.h"
#include "Materials/MaterialInterface.h"
#include "Math/RotationMatrix.h"

UVestigeTentacleVisualAdapter::UVestigeTentacleVisualAdapter()
{
    PrimaryComponentTick.bCanEverTick = false;
    RelativeAttachmentTransform = FTransform(FRotator(0.0f, 0.0f, 0.0f), FVector(-18.0f, 0.0f, 64.0f), FVector(0.35f));
}

void UVestigeTentacleVisualAdapter::BeginPlay()
{
    Super::BeginPlay();
    RebuildTentacleVisual();
}

void UVestigeTentacleVisualAdapter::RebuildTentacleVisual()
{
    if (!bAutoCreateTentacleMesh)
    {
        return;
    }

    LoadTentaclesVfxPackageDefaults();

    AActor* Owner = GetOwner();
    USceneComponent* AttachParent = ResolveAttachParent();
    if (!Owner || !AttachParent)
    {
        return;
    }

    if (!TentacleVisualRoot)
    {
        TentacleVisualRoot = NewObject<USceneComponent>(Owner, TEXT("VestigeTentacleVisualRoot"));
        TentacleVisualRoot->SetupAttachment(AttachParent, AttachSocketName);
        TentacleVisualRoot->RegisterComponent();
        Owner->AddInstanceComponent(TentacleVisualRoot);
    }

    TentacleVisualRoot->AttachToComponent(
        AttachParent,
        FAttachmentTransformRules::KeepRelativeTransform,
        AttachSocketName);
    TentacleVisualRoot->SetRelativeTransform(RelativeAttachmentTransform);

    if (TentacleSkeletalMesh)
    {
        if (!TentacleSkeletalMeshComponent)
        {
            TentacleSkeletalMeshComponent = NewObject<USkeletalMeshComponent>(Owner, TEXT("VestigeTentacleSkeletalMesh"));
            TentacleSkeletalMeshComponent->SetupAttachment(TentacleVisualRoot);
            TentacleSkeletalMeshComponent->RegisterComponent();
            Owner->AddInstanceComponent(TentacleSkeletalMeshComponent);
        }

        TentacleSkeletalMeshComponent->AttachToComponent(TentacleVisualRoot, FAttachmentTransformRules::KeepRelativeTransform);
        TentacleSkeletalMeshComponent->SetRelativeTransform(FTransform::Identity);
        TentacleSkeletalMeshComponent->SetSkeletalMesh(TentacleSkeletalMesh);
        TentacleSkeletalMeshComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    }

    if (TentacleStaticMesh)
    {
        if (!TentacleStaticMeshComponent)
        {
            TentacleStaticMeshComponent = NewObject<UStaticMeshComponent>(Owner, TEXT("VestigeTentacleStaticMesh"));
            TentacleStaticMeshComponent->SetupAttachment(TentacleVisualRoot);
            TentacleStaticMeshComponent->RegisterComponent();
            Owner->AddInstanceComponent(TentacleStaticMeshComponent);
        }

        TentacleStaticMeshComponent->AttachToComponent(TentacleVisualRoot, FAttachmentTransformRules::KeepRelativeTransform);
        TentacleStaticMeshComponent->SetRelativeTransform(FTransform::Identity);
        TentacleStaticMeshComponent->SetStaticMesh(TentacleStaticMesh);
        TentacleStaticMeshComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    }

    if (bUseFallbackBeam)
    {
        if (!TentacleFallbackBeamComponent)
        {
            TentacleFallbackBeamComponent = NewObject<UStaticMeshComponent>(Owner, TEXT("VestigeTentacleFallbackBeam"));
            TentacleFallbackBeamComponent->SetupAttachment(Owner->GetRootComponent());
            TentacleFallbackBeamComponent->RegisterComponent();
            Owner->AddInstanceComponent(TentacleFallbackBeamComponent);
        }

        UStaticMesh* BeamMesh = TentaclesVfxBeamMesh
            ? TentaclesVfxBeamMesh.Get()
            : LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
        if (BeamMesh)
        {
            TentacleFallbackBeamComponent->SetStaticMesh(BeamMesh);
        }
        if (TentaclesVfxBeamMaterial)
        {
            TentacleFallbackBeamComponent->SetMaterial(0, TentaclesVfxBeamMaterial.Get());
        }
        TentacleFallbackBeamComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
        TentacleFallbackBeamComponent->SetVisibility(false, true);
        TentacleFallbackBeamComponent->SetHiddenInGame(true, true);
    }

    if (bUseTentaclesVfxPackage)
    {
        if (!TentacleImpactComponent)
        {
            TentacleImpactComponent = NewObject<UStaticMeshComponent>(Owner, TEXT("VestigeTentacleImpact"));
            TentacleImpactComponent->SetupAttachment(Owner->GetRootComponent());
            TentacleImpactComponent->RegisterComponent();
            Owner->AddInstanceComponent(TentacleImpactComponent);
        }

        if (TentaclesVfxImpactMesh)
        {
            TentacleImpactComponent->SetStaticMesh(TentaclesVfxImpactMesh.Get());
        }
        if (TentaclesVfxImpactMaterial)
        {
            TentacleImpactComponent->SetMaterial(0, TentaclesVfxImpactMaterial.Get());
        }
        TentacleImpactComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
        TentacleImpactComponent->SetVisibility(false, true);
        TentacleImpactComponent->SetHiddenInGame(true, true);
    }

    SetTentacleVisualActive(!bHideVisualWhenIdle);
    PlayVisualAnimation(IdleAnimation, true);
}

void UVestigeTentacleVisualAdapter::SetTentacleVisualActive(bool bActive)
{
    bTentacleVisualActive = bActive;

    if (TentacleVisualRoot)
    {
        TentacleVisualRoot->SetVisibility(bActive, true);
        TentacleVisualRoot->SetHiddenInGame(!bActive, true);
    }

    if (!bActive)
    {
        SetFallbackBeamVisible(false);
        DestroyTentaclesVfxActor();
    }
}

USceneComponent* UVestigeTentacleVisualAdapter::GetTentacleVisualRoot() const
{
    return TentacleVisualRoot;
}

USkeletalMeshComponent* UVestigeTentacleVisualAdapter::GetTentacleSkeletalMeshComponent() const
{
    return TentacleSkeletalMeshComponent;
}

UStaticMeshComponent* UVestigeTentacleVisualAdapter::GetTentacleStaticMeshComponent() const
{
    return TentacleStaticMeshComponent;
}

void UVestigeTentacleVisualAdapter::OnGrappleSearchStarted_Implementation()
{
    SetTentacleVisualActive(true);
}

void UVestigeTentacleVisualAdapter::OnGrappleAnchorSelected_Implementation(AGrappleAnchor* Anchor)
{
}

void UVestigeTentacleVisualAdapter::OnGrappleExtendStarted_Implementation(AGrappleAnchor* Anchor)
{
    SetTentacleVisualActive(true);
    PlayVisualAnimation(ExtendAnimation ? ExtendAnimation.Get() : IdleAnimation.Get(), false);
}

void UVestigeTentacleVisualAdapter::OnGrapplePullStarted_Implementation(AGrappleAnchor* Anchor)
{
    SetTentacleVisualActive(true);
    PlayVisualAnimation(PullAnimation ? PullAnimation.Get() : IdleAnimation.Get(), true);
}

void UVestigeTentacleVisualAdapter::OnGrappleReleased_Implementation()
{
    SetTentacleVisualActive(true);
    PlayVisualAnimation(ReleaseAnimation ? ReleaseAnimation.Get() : IdleAnimation.Get(), false);
}

void UVestigeTentacleVisualAdapter::OnGrappleCancelled_Implementation()
{
    PlayVisualAnimation(ReleaseAnimation ? ReleaseAnimation.Get() : IdleAnimation.Get(), false);
    SetFallbackBeamVisible(false);
    SetTentacleVisualActive(!bHideVisualWhenIdle);
}

void UVestigeTentacleVisualAdapter::UpdateLimbTarget_Implementation(FVector WorldStart, FVector WorldEnd, float DeltaSeconds)
{
    if (TentacleVisualRoot && bAimVisualAtGrappleTarget)
    {
        const FVector VisualStart = TentacleVisualRoot->GetComponentLocation();
        const FVector ToTarget = WorldEnd - VisualStart;
        if (!ToTarget.IsNearlyZero())
        {
            TentacleVisualRoot->SetWorldRotation(ToTarget.Rotation());
        }
    }

    UpdateFallbackBeam(WorldStart, WorldEnd);
    if (bTentacleVisualActive)
    {
        UpdateTentaclesVfxActor(WorldEnd);
    }

    if (!bDrawFallbackDebugLine || !GetWorld())
    {
        return;
    }

    DrawDebugLine(GetWorld(), WorldStart, WorldEnd, FColor::Blue, false, 0.0f, 0, 3.0f);
}

USceneComponent* UVestigeTentacleVisualAdapter::ResolveAttachParent() const
{
    const AActor* Owner = GetOwner();
    if (!Owner)
    {
        return nullptr;
    }

    if (const ACharacter* CharacterOwner = Cast<ACharacter>(Owner))
    {
        if (USceneComponent* MeshComponent = CharacterOwner->GetMesh())
        {
            return MeshComponent;
        }
    }

    return Owner->GetRootComponent();
}

void UVestigeTentacleVisualAdapter::LoadTentaclesVfxPackageDefaults()
{
    if (!bUseTentaclesVfxPackage)
    {
        return;
    }

    if (!TentaclesVfxBeamMesh)
    {
        TentaclesVfxBeamMesh = LoadObject<UStaticMesh>(
            nullptr,
            TEXT("/Game/Vefects/Tentacles_VFX/VFX/Goo/SM/SM_VFX_Arm_Double_01.SM_VFX_Arm_Double_01"));
    }

    if (!TentaclesVfxBeamMaterial)
    {
        TentaclesVfxBeamMaterial = LoadObject<UMaterialInterface>(
            nullptr,
            TEXT("/Game/Vefects/Tentacles_VFX/VFX/Goo/Materials/MI_VFX_Goo_Arm_Dark_01.MI_VFX_Goo_Arm_Dark_01"));
    }

    if (!TentaclesVfxImpactMesh)
    {
        TentaclesVfxImpactMesh = LoadObject<UStaticMesh>(
            nullptr,
            TEXT("/Game/Vefects/Tentacles_VFX/VFX/Goo/SM/SM_VFX_Smooth_Sphere_01.SM_VFX_Smooth_Sphere_01"));
    }

    if (!TentaclesVfxImpactMaterial)
    {
        TentaclesVfxImpactMaterial = LoadObject<UMaterialInterface>(
            nullptr,
            TEXT("/Game/Vefects/Tentacles_VFX/VFX/Goo/Materials/MI_VFX_Goo_Dark_01.MI_VFX_Goo_Dark_01"));
    }

    if (bSpawnTentaclesVfxGooActor && !TentaclesVfxGooActorClass)
    {
        TentaclesVfxGooActorClass = LoadClass<AActor>(
            nullptr,
            TEXT("/Game/Vefects/Tentacles_VFX/VFX/Goo/BP/BP_Goo.BP_Goo_C"));
    }
}

void UVestigeTentacleVisualAdapter::PlayVisualAnimation(UAnimationAsset* AnimationAsset, bool bLoop)
{
    if (!TentacleSkeletalMeshComponent || !AnimationAsset)
    {
        return;
    }

    TentacleSkeletalMeshComponent->PlayAnimation(AnimationAsset, bLoop);
}

void UVestigeTentacleVisualAdapter::SetFallbackBeamVisible(bool bVisible)
{
    if (!TentacleFallbackBeamComponent)
    {
        return;
    }

    TentacleFallbackBeamComponent->SetVisibility(bVisible, true);
    TentacleFallbackBeamComponent->SetHiddenInGame(!bVisible, true);
}

void UVestigeTentacleVisualAdapter::UpdateFallbackBeam(const FVector& WorldStart, const FVector& WorldEnd)
{
    if (!bUseFallbackBeam || !TentacleFallbackBeamComponent)
    {
        return;
    }

    const FVector ToTarget = WorldEnd - WorldStart;
    const float Length = ToTarget.Size();
    if (Length < KINDA_SMALL_NUMBER)
    {
        SetFallbackBeamVisible(false);
        return;
    }

    const FVector Midpoint = WorldStart + ToTarget * 0.5f;
    FVector BeamScale = FVector::OneVector;
    FRotator Rotation = FRotationMatrix::MakeFromZ(ToTarget).Rotator();
    if (const UStaticMesh* BeamMesh = TentacleFallbackBeamComponent->GetStaticMesh())
    {
        const FVector Extent = BeamMesh->GetBounds().BoxExtent;
        const bool bMeshRunsAlongX = Extent.X > Extent.Y && Extent.X > Extent.Z;
        if (bMeshRunsAlongX)
        {
            Rotation = FRotationMatrix::MakeFromX(ToTarget).Rotator();
            BeamScale = FVector(
                Length / FMath::Max(Extent.X * 2.0f, 1.0f),
                FallbackBeamRadius / FMath::Max(Extent.Y, 1.0f),
                FallbackBeamRadius / FMath::Max(Extent.Z, 1.0f));
        }
        else
        {
            BeamScale = FVector(
                FallbackBeamRadius / FMath::Max(Extent.X, 1.0f),
                FallbackBeamRadius / FMath::Max(Extent.Y, 1.0f),
                Length / FMath::Max(Extent.Z * 2.0f, 1.0f));
        }
    }
    else
    {
        const float CylinderRadiusScale = FallbackBeamRadius / 50.0f;
        BeamScale = FVector(CylinderRadiusScale, CylinderRadiusScale, Length / 100.0f);
    }
    TentacleFallbackBeamComponent->SetWorldLocationAndRotation(Midpoint, Rotation);
    TentacleFallbackBeamComponent->SetWorldScale3D(BeamScale);
    SetFallbackBeamVisible(true);
}

void UVestigeTentacleVisualAdapter::UpdateTentaclesVfxActor(const FVector& WorldEnd)
{
    if (!bUseTentaclesVfxPackage || !GetWorld())
    {
        return;
    }

    LoadTentaclesVfxPackageDefaults();
    if (TentacleImpactComponent)
    {
        TentacleImpactComponent->SetWorldLocation(WorldEnd);
        TentacleImpactComponent->SetWorldScale3D(FVector(FMath::Max(TentaclesVfxImpactScale, 0.01f)));
        TentacleImpactComponent->SetVisibility(true, true);
        TentacleImpactComponent->SetHiddenInGame(false, true);
    }

    if (!bSpawnTentaclesVfxGooActor || !TentaclesVfxGooActorClass)
    {
        return;
    }

    if (!IsValid(ActiveTentaclesVfxActor))
    {
        FActorSpawnParameters SpawnParameters;
        SpawnParameters.Owner = GetOwner();
        SpawnParameters.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
        ActiveTentaclesVfxActor = GetWorld()->SpawnActor<AActor>(
            TentaclesVfxGooActorClass,
            WorldEnd,
            FRotator::ZeroRotator,
            SpawnParameters);
    }

    if (!ActiveTentaclesVfxActor)
    {
        return;
    }

    ActiveTentaclesVfxActor->SetActorLocation(WorldEnd);
    ActiveTentaclesVfxActor->SetActorHiddenInGame(false);
    ActiveTentaclesVfxActor->SetActorEnableCollision(false);
    ActiveTentaclesVfxActor->SetActorTickEnabled(true);
}

void UVestigeTentacleVisualAdapter::DestroyTentaclesVfxActor()
{
    if (TentacleImpactComponent)
    {
        TentacleImpactComponent->SetVisibility(false, true);
        TentacleImpactComponent->SetHiddenInGame(true, true);
    }

    if (IsValid(ActiveTentaclesVfxActor))
    {
        ActiveTentaclesVfxActor->Destroy();
    }
    ActiveTentaclesVfxActor = nullptr;
}
