#pragma once

#include "Kismet/BlueprintFunctionLibrary.h"
#include "NocturneMontageEditorLibrary.generated.h"

class UAnimMontage;

UCLASS()
class NOCTURNESIGNALEDITOR_API UNocturneMontageEditorLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "Nocturne|Animation")
    static bool SetMontageSections(UAnimMontage* Montage, const TArray<FName>& SectionNames, const TArray<float>& SectionTimes);

    UFUNCTION(BlueprintPure, Category = "Nocturne|Animation")
    static TArray<FName> GetMontageSectionNames(const UAnimMontage* Montage);

    UFUNCTION(BlueprintPure, Category = "Nocturne|Animation")
    static TArray<float> GetMontageSectionTimes(const UAnimMontage* Montage);
};
