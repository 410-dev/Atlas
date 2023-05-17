import importlib
import kernel.registry as Registry
from kernel.states import States
import json

class Atlas:
    
    errors = [
        "Atlas installation is incomplete. Please run atlas-install command first.",
        "Model is not loaded.",
        "OpenAI key is invalid.",
        "Registry broken: SOFTWARE.Helium.Program.Atlas.ModelLibrary",
        "Registry broken: SOFTWARE.Helium.Program.Atlas.ModelSelected",
        "Registry broken: SOFTWARE.Helium.Program.Atlas.DefaultModel",
        "Selected model does not exist, and default model fallback is disabled.",
        "Default model does not exist.",
        "Warning: Selected model does not exist. Using default model fallback."
    ]
    
    def __init__(self, lineArgs) -> None:
        self.args: list = lineArgs
    
    @staticmethod
    def error(code: int) -> str:
        return f"Error {code}: {Atlas.errors[code-1]}"

    def main(self) -> int:
        
        # Check if installation was successful
        if Registry.read("SOFTWARE.Helium.Program.Atlas.SetupDone") != "1":
            print(Atlas.error(1))
            return 1
            
        # Check running mode
        # If use offline model, go to offline().
        # If use online api, go to online().
        import data.commands.atlas.validate as Validator
        offlineMode = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.UseOfflineModel")
        if offlineMode == "1":
            exitCode = Validator.offline()
        else:
            exitCode = Validator.online()
        
        # If validation failed, return exit code.
        if exitCode != 0 and not None:
            return exitCode

        if offlineMode == "1":
            import data.commands.atlas.offline as llm
        else:
            import data.commands.atlas.openai as llm
        
        llm.interactiveMode(self.args)
        
        
        
    