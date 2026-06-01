#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "NocturneParallaxLayer.generated.h"

class UStaticMeshComponent;

UCLASS(Blueprintable)
class NOCTURNESIGNAL_API ANocturneParallaxLayer : public AActor
{
    GENERATED_BODY()

public:
    ANocturneParallaxLayer();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;

    UFUNCTION(BlueprintPure, Category = "Nocturne|Parallax")
    UStaticMeshComponent* GetParallaxMeshComponent() const;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nocturne|Parallax")
    TObjectPtr<UStaticMeshComponent> ParallaxMesh;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Parallax")
    bool bAutoFollowPlayer = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Parallax", meta = (ClampMin = "0.0", ClampMax = "1.0"))
    float HorizontalFollowFactor = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Parallax")
    bool bLockDepthAndHeight = true;

private:
    AActor* ResolveFollowTarget() const;
    void CacheReferenceFrame(AActor& TargetActor);
    void UpdateParallaxLocation();

    UPROPERTY(Transient)
    TObjectPtr<AActor> FollowTarget;

    FVector InitialLayerLocation = FVector::ZeroVector;
    float ReferenceTargetX = 0.0f;
    bool bHasReferenceFrame = false;
};
