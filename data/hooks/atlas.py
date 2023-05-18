from kernel.states import States
import kernel.registry as Registry
import kernel.procmgr as procmgr


def main(args) -> int:
    if Registry.read("SOFTWARE.Helium.Program.Atlas.SetupDone") == "1":
        if Registry.read("SOFTWARE.Helium.Program.Atlas.Local.LoadModelOnSystemBoot") == "1":
            modelName = Registry.read("SOFTWARE.Helium.Program.Atlas.ModelSelected")
            procmgr.launch("atlas-model", ["load", modelName])
        else:
            print("Model is not loaded on system boot.")
    else:
        print("[Atlas Hook]: Atlas is not configured yet. Please run atlas-install.")
    