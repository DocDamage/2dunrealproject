#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "VestigeTentacleVisualAdapter.generated.h"

class AGrappleAnchor;
class AActor;
class UAnimationAsset;
class UMaterialInterface;
class USceneComponent;
class USkeletalMesh;
class USkeletalMeshComponent;
class UStaticMesh;
class UStaticMeshComponent;

UCLASS(Blueprintable, ClassGroup = (Nocturne), meta = (BlueprintSpawnableComponent))
class NOCTURNESIGNAL_API UVestigeTentacleVisualAdapter : public UActorComponent
{
    GENERATED_BODY()

public:
    UVestigeTentacleVisualAdapter();

    virtual void BeginPlay() override;

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Vestige Visuals")
    void RebuildTentacleVisual();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Vestige Visuals")
    void SetTentacleVisualActive(bool bActive);

    UFUNCTION(BlueprintPure, Category = "Nocturne|Vestige Visuals")
    USceneComponent* GetTentacleVisualRoot() const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Vestige Visuals")
    USkeletalMeshComponent* GetTentacleSkeletalMeshComponent() const;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Vestige Visuals")
    UStaticMeshComponent* GetTentacleStaticMeshComponent() const;

    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Nocturne|Vestige Visuals")
    void OnGrappleSearchStarted();

    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Nocturne|Vestige Visuals")
    void OnGrappleAnchorSelected(AGrappleAnchor* Anchor);

    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Nocturne|Vestige Visuals")
    void OnGrappleExtendStarted(AGrappleAnchor* Anchor);

    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Nocturne|Vestige Visuals")
    void OnGrapplePullStarted(AGrappleAnchor* Anchor);

    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Nocturne|Vestige Visuals")
    void OnGrappleReleased();

    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Nocturne|Vestige Visuals")
    void OnGrappleCancelled();

    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Nocturne|Vestige Visuals")
    void UpdateLimbTarget(FVector WorldStart, FVector WorldEnd, float DeltaSeconds);

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals")
    bool bUsePluginDrivenVisuals = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals")
    bool bDrawFallbackDebugLine = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals")
    bool bUseFallbackBeam = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals", meta = (ClampMin = "0.5"))
    float FallbackBeamRadius = 4.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Tentacles VFX")
    bool bUseTentaclesVfxPackage = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Tentacles VFX")
    TObjectPtr<UStaticMesh> TentaclesVfxBeamMesh;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Tentacles VFX")
    TObjectPtr<UMaterialInterface> TentaclesVfxBeamMaterial;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Tentacles VFX")
    TSubclassOf<AActor> TentaclesVfxGooActorClass;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Tentacles VFX")
    bool bSpawnTentaclesVfxGooActor = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Tentacles VFX")
    TObjectPtr<UStaticMesh> TentaclesVfxImpactMesh;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Tentacles VFX")
    TObjectPtr<UMaterialInterface> TentaclesVfxImpactMaterial;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Tentacles VFX", meta = (ClampMin = "0.01"))
    float TentaclesVfxImpactScale = 0.22f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Mesh")
    bool bAutoCreateTentacleMesh = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Mesh")
    bool bAimVisualAtGrappleTarget = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Mesh")
    bool bHideVisualWhenIdle = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Mesh")
    FName AttachSocketName = NAME_None;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Mesh")
    FTransform RelativeAttachmentTransform;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Mesh")
    TObjectPtr<USkeletalMesh> TentacleSkeletalMesh;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Mesh")
    TObjectPtr<UStaticMesh> TentacleStaticMesh;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Animation")
    TObjectPtr<UAnimationAsset> IdleAnimation;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Animation")
    TObjectPtr<UAnimationAsset> ExtendAnimation;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Animation")
    TObjectPtr<UAnimationAsset> PullAnimation;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Vestige Visuals|Animation")
    TObjectPtr<UAnimationAsset> ReleaseAnimation;

private:
    USceneComponent* ResolveAttachParent() const;
    void LoadTentaclesVfxPackageDefaults();
    void PlayVisualAnimation(UAnimationAsset* AnimationAsset, bool bLoop);
    void SetFallbackBeamVisible(bool bVisible);
    void UpdateFallbackBeam(const FVector& WorldStart, const FVector& WorldEnd);
    void UpdateTentaclesVfxActor(const FVector& WorldEnd);
    void DestroyTentaclesVfxActor();

    UPROPERTY(Transient)
    TObjectPtr<USceneComponent> TentacleVisualRoot;

    UPROPERTY(Transient)
    TObjectPtr<USkeletalMeshComponent> TentacleSkeletalMeshComponent;

    UPROPERTY(Transient)
    TObjectPtr<UStaticMeshComponent> TentacleStaticMeshComponent;

    UPROPERTY(Transient)
    TObjectPtr<UStaticMeshComponent> TentacleFallbackBeamComponent;

    UPROPERTY(Transient)
    TObjectPtr<UStaticMeshComponent> TentacleImpactComponent;

    UPROPERTY(Transient)
    TObjectPtr<AActor> ActiveTentaclesVfxActor;

    bool bTentacleVisualActive = false;
};
