#include "VestigeTentacleVisualAdapter.h"
#include "DrawDebugHelpers.h"
#include "GrappleAnchor.h"
#include "Animation/AnimationAsset.h"
#include "Components/SceneComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/Actor.h"
#include "GameFramework/Character.h"

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

    SetTentacleVisualActive(!bHideVisualWhenIdle);
    PlayVisualAnimation(IdleAnimation, true);
}

void UVestigeTentacleVisualAdapter::SetTentacleVisualActive(bool bActive)
{
    if (TentacleVisualRoot)
    {
        TentacleVisualRoot->SetVisibility(bActive, true);
        TentacleVisualRoot->SetHiddenInGame(!bActive, true);
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
    PlayVisualAnimation(ReleaseAnimation ? ReleaseAnimation.Get() : IdleAnimation.Get(), false);
    SetTentacleVisualActive(!bHideVisualWhenIdle);
}

void UVestigeTentacleVisualAdapter::OnGrappleCancelled_Implementation()
{
    PlayVisualAnimation(ReleaseAnimation ? ReleaseAnimation.Get() : IdleAnimation.Get(), false);
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

void UVestigeTentacleVisualAdapter::PlayVisualAnimation(UAnimationAsset* AnimationAsset, bool bLoop)
{
    if (!TentacleSkeletalMeshComponent || !AnimationAsset)
    {
        return;
    }

    TentacleSkeletalMeshComponent->PlayAnimation(AnimationAsset, bLoop);
}
