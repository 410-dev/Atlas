from kernel.states import States
import kernel.registry as Registry
import kernel.procmgr as procmgr

class atlas():
    
    def __init__(self, args):
        self.args = args
    
    def main(self) -> int:
        if Registry.read("SOFTWARE.Helium.Program.Atlas.SetupDone") == "1":
            modelName = Registry.read("SOFTWARE.Helium.Program.Atlas.ModelSelected")
            procmgr.launch("atlas-model", ["load", modelName])
        else:
            print("[Atlas Hook]: Atlas is not configured yet. Please run atlas-install.")
    