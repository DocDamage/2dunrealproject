#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "NocturneGameMode.generated.h"

class APlayerController;

UCLASS()
class NOCTURNESIGNAL_API ANocturneGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    ANocturneGameMode();

protected:
    virtual void HandleStartingNewPlayer_Implementation(APlayerController* NewPlayer) override;
};
