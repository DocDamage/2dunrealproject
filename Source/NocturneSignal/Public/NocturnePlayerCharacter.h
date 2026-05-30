#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "NocturnePlayerCharacter.generated.h"

class UVestigeLimbComponent;
class UPaperFlipbookComponent;

UCLASS(Blueprintable)
class NOCTURNESIGNAL_API ANocturnePlayerCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    ANocturnePlayerCharacter();

    virtual void Tick(float DeltaSeconds) override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Movement")
    void MoveHorizontal(float AxisValue);

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Movement")
    void StartJump();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Movement")
    void StopJump();

    UFUNCTION(BlueprintCallable, Category = "Nocturne|Vestige")
    bool TryVestigeGrapple();

    UFUNCTION(BlueprintPure, Category = "Nocturne|Vestige")
    UVestigeLimbComponent* GetVestigeLimbComponent() const;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nocturne|Components")
    TObjectPtr<UVestigeLimbComponent> VestigeLimbComponent;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Movement", meta = (ClampMin = "0.0"))
    float GroundAcceleration = 2600.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Movement", meta = (ClampMin = "0.0"))
    float GroundFriction = 8.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Movement", meta = (ClampMin = "0.0"))
    float MaxWalkSpeed2D = 420.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nocturne|Movement", meta = (ClampMin = "0.0"))
    float JumpZVelocity2D = 720.0f;

protected:
    virtual void BeginPlay() override;

private:
    void ApplyMovementTuning();
};
