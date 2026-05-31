using UnrealBuildTool;
using System.Collections.Generic;

public class NocturneSignalTarget : TargetRules
{
    public NocturneSignalTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V6;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("NocturneSignal");
    }
}
