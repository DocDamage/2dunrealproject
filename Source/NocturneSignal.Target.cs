using UnrealBuildTool;
using System.Collections.Generic;

public class NocturneSignalTarget : TargetRules
{
    public NocturneSignalTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("NocturneSignal");
    }
}
