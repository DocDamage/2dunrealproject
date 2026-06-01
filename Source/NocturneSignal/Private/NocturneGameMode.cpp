#include "NocturneGameMode.h"
#include "NocturnePlayerCharacter.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerController.h"

ANocturneGameMode::ANocturneGameMode()
{
    DefaultPawnClass = ANocturnePlayerCharacter::StaticClass();
}

void ANocturneGameMode::HandleStartingNewPlayer_Implementation(APlayerController* NewPlayer)
{
    if (!NewPlayer)
    {
        Super::HandleStartingNewPlayer_Implementation(NewPlayer);
        return;
    }

    if (NewPlayer->GetPawn())
    {
        return;
    }

    UWorld* World = GetWorld();
    if (World)
    {
        for (TActorIterator<ANocturnePlayerCharacter> It(World); It; ++It)
        {
            ANocturnePlayerCharacter* PlacedPlayer = *It;
            if (IsValid(PlacedPlayer)
                && !PlacedPlayer->GetController()
                && PlacedPlayer->AutoPossessPlayer == EAutoReceiveInput::Player0)
            {
                NewPlayer->Possess(PlacedPlayer);
                return;
            }
        }
    }

    Super::HandleStartingNewPlayer_Implementation(NewPlayer);
}
