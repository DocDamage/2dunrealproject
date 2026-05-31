using UnrealBuildTool;

public class NocturneSignal : ModuleRules
{
    public NocturneSignal(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine",
            "InputCore",
            "EnhancedInput",
            "Paper2D"
        });

        PrivateDependencyModuleNames.AddRange(new string[]
        {
        });
    }
}
