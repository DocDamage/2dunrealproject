#include "NocturneMontageEditorLibrary.h"

#include "Animation/AnimMontage.h"

DEFINE_LOG_CATEGORY_STATIC(LogNocturneMontageEditor, Log, All);

bool UNocturneMontageEditorLibrary::SetMontageSections(
    UAnimMontage* Montage,
    const TArray<FName>& SectionNames,
    const TArray<float>& SectionTimes)
{
    if (!Montage)
    {
        UE_LOG(LogNocturneMontageEditor, Error, TEXT("SetMontageSections called with no montage."));
        return false;
    }

    if (SectionNames.Num() == 0 || SectionNames.Num() != SectionTimes.Num())
    {
        UE_LOG(
            LogNocturneMontageEditor,
            Error,
            TEXT("SetMontageSections needs matching non-empty names/times arrays for %s."),
            *Montage->GetName());
        return false;
    }

    for (int32 Index = 0; Index < SectionNames.Num(); ++Index)
    {
        if (SectionNames[Index].IsNone())
        {
            UE_LOG(LogNocturneMontageEditor, Error, TEXT("Section %d on %s has no name."), Index, *Montage->GetName());
            return false;
        }

        if (SectionTimes[Index] < 0.0f)
        {
            UE_LOG(LogNocturneMontageEditor, Error, TEXT("Section %s on %s has negative time."), *SectionNames[Index].ToString(), *Montage->GetName());
            return false;
        }

        if (Index > 0 && SectionTimes[Index] < SectionTimes[Index - 1])
        {
            UE_LOG(LogNocturneMontageEditor, Error, TEXT("Sections for %s must be in ascending time order."), *Montage->GetName());
            return false;
        }
    }

    Montage->Modify();

    for (int32 Index = Montage->GetNumSections() - 1; Index >= 0; --Index)
    {
        Montage->DeleteAnimCompositeSection(Index);
    }

    for (int32 Index = 0; Index < SectionNames.Num(); ++Index)
    {
        if (Montage->AddAnimCompositeSection(SectionNames[Index], SectionTimes[Index]) == INDEX_NONE)
        {
            UE_LOG(
                LogNocturneMontageEditor,
                Error,
                TEXT("Could not add section %s to %s."),
                *SectionNames[Index].ToString(),
                *Montage->GetName());
            return false;
        }
    }

    Montage->UpdateLinkableElements();
    Montage->RefreshCacheData();
    Montage->MarkPackageDirty();
    return true;
}

TArray<FName> UNocturneMontageEditorLibrary::GetMontageSectionNames(const UAnimMontage* Montage)
{
    TArray<FName> Names;
    if (!Montage)
    {
        return Names;
    }

    for (int32 Index = 0; Index < Montage->GetNumSections(); ++Index)
    {
        Names.Add(Montage->GetSectionName(Index));
    }
    return Names;
}

TArray<float> UNocturneMontageEditorLibrary::GetMontageSectionTimes(const UAnimMontage* Montage)
{
    TArray<float> Times;
    if (!Montage)
    {
        return Times;
    }

    for (int32 Index = 0; Index < Montage->GetNumSections(); ++Index)
    {
        Times.Add(Montage->GetAnimCompositeSection(Index).GetTime());
    }
    return Times;
}
