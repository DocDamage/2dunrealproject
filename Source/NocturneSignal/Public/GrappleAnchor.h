#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GrappleAnchor.generated.h"

UENUM(BlueprintType)
enum class EGrappleAnchorType : uint8
{
    Architecture UMETA(DisplayName = "Architecture"),
    Organic UMETA(DisplayName = "Organic"),
    Signal UMETA(DisplayName = "Signal"),
    Enemy UMETA(DisplayName = "Enemy"),
    Penitent UMETA(DisplayName = "Penitent")
};

UCLASS(Blueprintable)
class NOCTURNESIGNAL_API AGrappleAnchor : public AActor
{
    GENERATED_BODY()

public:
    AGrappleAnchor();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Grapple")
    bool IsAvailableForStage(int32 VestigeStage, float CurrentCorruption) const;

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Grapple")
    FVector GetAnchorLocation() const;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Nocturne|Grapple")
    EGrappleAnchorType AnchorType = EGrappleAnchorType::Architecture;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Nocturne|Grapple", meta = (ClampMin = "1", ClampMax = "5"))
    int32 RequiredStage = 1;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Nocturne|Grapple", meta = (ClampMin = "0.0", ClampMax = "1.0"))
    float RequiredCorruption = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Grapple")
    bool bIsActive = true;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Nocturne|Grapple", meta = (ClampMin = "0.0"))
    float GrappleRadius = 96.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Nocturne|Grapple", meta = (ClampMin = "1.0"))
    float ArrivalRadius = 18.0f;

protected:
    virtual void BeginPlay() override;
};
