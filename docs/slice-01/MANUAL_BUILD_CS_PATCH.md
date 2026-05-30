# Manual Patch Required — `NocturneSignal.Build.cs`

The GitHub connector repeatedly blocked direct creation of `Source/NocturneSignal/NocturneSignal.Build.cs` during scaffold setup. This file is required before the Unreal C++ project can compile.

Create this file manually in the IDE or local repo:

```text
Source/NocturneSignal/NocturneSignal.Build.cs
```

Use this content:

```csharp
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
```

After creating it, regenerate project files and compile.

Expected first compile path:

1. Clone/pull repo locally.
2. Create the missing file above.
3. Right-click `NocturneSignal.uproject` and generate project files, or use Unreal's project generation flow.
4. Open the solution/IDE.
5. Build `NocturneSignalEditor`.
6. Open the project in Unreal Engine 5.7.

## Plugin Follow-Up

Before enabling Pasma Engine or Tentacles VFX in `.uproject`, capture their exact plugin identifiers from the local `.uplugin` files.

Do not guess these names.
