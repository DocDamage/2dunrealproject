#include "NocturnePlayerCharacter.h"
#include "VestigeLimbComponent.h"
#include "GameFramework/CharacterMovementComponent.h"

ANocturnePlayerCharacter::ANocturnePlayerCharacter()
{
    PrimaryActorTick.bCanEverTick = true;

    VestigeLimbComponent = CreateDefaultSubobject<UVestigeLimbComponent>(TEXT("VestigeLimbComponent"));

    bUseControllerRotationPitch = false;
    bUseControllerRotationYaw = false;
    bUseControllerRotationRoll = false;

    ApplyMovementTuning();
}

void ANocturnePlayerCharacter::BeginPlay()
{
    Super::BeginPlay();
    ApplyMovementTuning();
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
    Jump();
}

void ANocturnePlayerCharacter::StopJump()
{
    StopJumping();
}

bool ANocturnePlayerCharacter::TryVestigeGrapple()
{
    return VestigeLimbComponent ? VestigeLimbComponent->TryStartPullToPoint() : false;
}

UVestigeLimbComponent* ANocturnePlayerCharacter::GetVestigeLimbComponent() const
{
    return VestigeLimbComponent;
}

void ANocturnePlayerCharacter::ApplyMovementTuning()
{
    UCharacterMovementComponent* Movement = GetCharacterMovement();
    if (!Movement)
    {
        return;
    }

    Movement->MaxWalkSpeed = MaxWalkSpeed2D;
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
