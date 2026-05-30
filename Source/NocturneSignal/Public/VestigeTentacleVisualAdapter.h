#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "VestigeTentacleVisualAdapter.generated.h"

class AGrappleAnchor;

UCLASS(Abstract, Blueprintable, ClassGroup = (Nocturne), meta = (BlueprintSpawnableComponent))
class NOCTURNESIGNAL_API UVestigeTentacleVisualAdapter : public UActorComponent
{
    GENERATED_BODY()

public:
    UVestigeTentacleVisualAdapter();

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
};
