import os
import kernel.registry as Registry
import kernel.procmgr as procmgr
from kernel.ipcmemory import IPCMemory
from data.commands.atlas.main import Atlas

def offline() -> int:
    # Check if model path is not empty
    modelLib: str = Registry.read("SOFTWARE.Helium.Program.Atlas.ModelLibrary")
    modelSel: str = Registry.read("SOFTWARE.Helium.Program.Atlas.ModelSelected")
    modelDef: str = Registry.read("SOFTWARE.Helium.Program.Atlas.DefaultModel")
    if modelLib == None or len(modelLib) < 1:
        print(Atlas.error(4))
        return 4
    elif modelSel == None or len(modelSel) < 1:
        print(Atlas.error(5))
        return 5
    elif modelDef == None or len(modelDef) < 1:
        print(Atlas.error(6))
        return 6
    
    # Check if models exists
    modelSel = modelLib + os.sep + modelSel
    modelDef = modelLib + os.sep + modelDef
    if not os.path.isfile(modelDef) and Registry.read("SOFTWARE.Helium.Program.Atlas.RequireDefaultModel") == "1":
        print(Atlas.error(8))
        return 8
    elif not os.path.isfile(modelSel):
        if Registry.read("SOFTWARE.Helium.Program.Atlas.AllowDefaultModelFallback") == "0":
            print(Atlas.error(7))
            return 7
        else:
            print(Atlas.error(9))
            if not os.path.isfile(modelDef):
                print(Atlas.error(8))
                return 8
    
        
    
    # If expected to load model, check if it is on State memory.
    if Registry.read("SOFTWARE.Helium.Program.Atlas.CheckModelLoadedOnLaunch") != "0":
        modelLoaded: bool = IPCMemory.getObj("Program.Atlas.ModelLoaded")
        model = IPCMemory.getObj("Program.Atlas.Model")
        if not modelLoaded or model == None:
            print(Atlas.error(2))
            return 2
        
        return 0
        
    # Otherwise, load model.
    else:
        procmgr.launch("atlas-model", ["load", modelSel])
        return 0
    
def online() -> int:
    OpenAIKey = Registry.read("SOFTWARE.Helium.Program.Atlas.OpenAIAPI")
    if OpenAIKey == None or len(OpenAIKey) < 10:
        print(Atlas.error(3))
        return 3
    # TODO Add more verification steps
    return 0