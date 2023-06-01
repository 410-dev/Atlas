import json
import inspect
import kernel.procmgr as procmgr
import kernel.registry as Registry

from kernel.ipcmemory import IPCMemory

# Atlas Low Level Machine Control Stage
class AtlasMemoryAgent:
    
    def __init__(self, lineArgs) -> None:
        self.args: list = lineArgs
        
    def main(self) -> int:
        
        # Check if called script is data/commands/atlas/offline.py or data/commands/atlas/openai.py
        caller = procmgr.getParentScript()
        calledByAtlas = caller == "data/commands/atlas/offline.py" or caller == "data/commands/atlas/openai.py"

        # If action is append and is not called by atlas, return error.
        if self.args[0] == "append" and not calledByAtlas:
            print("Error: Append action can only be called by Atlas.")
            return 1

        # Redirect to corresponding function.
        if self.args[0] == "append":
            return self.append()
        elif self.args[0] == "read":
            return self.read()
        elif self.args[0] == "forget":
            return self.forget()
        else:
            print("Error: Invalid action.")
            return 1

    def append(self) -> int:
        return 0

    def read(self) -> int:
        return 0

    def forget(self) -> int:
        return 0

        
