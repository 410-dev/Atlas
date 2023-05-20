from kernel.ipcmemory import IPCMemory
import json

class Ipcinspect:
    
    def __init__(self, lineArgs) -> None:
        self.args: list = lineArgs

    def main(self) -> int:
        print(json.dumps(IPCMemory.objects, indent=4))

        return 0