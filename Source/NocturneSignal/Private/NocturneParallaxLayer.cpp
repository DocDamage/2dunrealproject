#include "NocturneParallaxLayer.h"

#include "Components/StaticMeshComponent.h"
#include "EngineUtils.h"
#include "GameFramework/Pawn.h"
#include "Kismet/GameplayStatics.h"

ANocturneParallaxLayer::ANocturneParallaxLayer()
{
    PrimaryActorTick.bCanEverTick = true;

    ParallaxMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ParallaxMesh"));
    SetRootComponent(ParallaxMesh);
    ParallaxMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    ParallaxMesh->SetGenerateOverlapEvents(false);
    ParallaxMesh->SetMobility(EComponentMobility::Movable);
}

void ANocturneParallaxLayer::BeginPlay()
{
    Super::BeginPlay();

    InitialLayerLocation = GetActorLocation();
    if (AActor* TargetActor = ResolveFollowTarget())
    {
        CacheReferenceFrame(*TargetActor);
        UpdateParallaxLocation();
    }
}

void ANocturneParallaxLayer::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    UpdateParallaxLocation();
}

UStaticMeshComponent* ANocturneParallaxLayer::GetParallaxMeshComponent() const
{
    return ParallaxMesh;
}

AActor* ANocturneParallaxLayer::ResolveFollowTarget() const
{
    if (!bAutoFollowPlayer)
    {
        return nullptr;
    }

    UWorld* World = GetWorld();
    if (!World)
    {
        return nullptr;
    }

    if (APawn* PlayerPawn = UGameplayStatics::GetPlayerPawn(World, 0))
    {
        return PlayerPawn;
    }

    for (TActorIterator<APawn> It(World); It; ++It)
    {
        APawn* Pawn = *It;
        if (IsValid(Pawn))
        {
            return Pawn;
        }
    }

    return nullptr;
}

void ANocturneParallaxLayer::CacheReferenceFrame(AActor& TargetActor)
{
    FollowTarget = &TargetActor;
    InitialLayerLocation = GetActorLocation();
    ReferenceTargetX = TargetActor.GetActorLocation().X;
    bHasReferenceFrame = true;
}

void ANocturneParallaxLayer::UpdateParallaxLocation()
{
    AActor* TargetActor = FollowTarget.Get();
    if (!IsValid(TargetActor))
    {
        TargetActor = ResolveFollowTarget();
        if (!TargetActor)
        {
            return;
        }
        CacheReferenceFrame(*TargetActor);
    }

    FVector NewLocation = GetActorLocation();
    const float TargetDeltaX = TargetActor->GetActorLocation().X - ReferenceTargetX;
    NewLocation.X = InitialLayerLocation.X + TargetDeltaX * HorizontalFollowFactor;
    if (bLockDepthAndHeight)
    {
        NewLocation.Y = InitialLayerLocation.Y;
        NewLocation.Z = InitialLayerLocation.Z;
    }

    SetActorLocation(NewLocation, false, nullptr, ETeleportType::TeleportPhysics);
}
