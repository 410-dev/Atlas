from kernel.states import States
import kernel.registry as Registry

class atlas():
    
    def __init__(self, args):
        self.args = args
    
    def main(self) -> int:
        if Registry.read("SOFTWARE.Helium.Program.Atlas.SetupDone") == "1":
            States.setObj("Program.Atlas.Model", "This should be a model variable")
            States.setObj("Program.Atlas.ModelLoaded", True)
        else:
            print("[Atlas Hook]: Atlas is not configured yet. Please run atlas-install.")
    