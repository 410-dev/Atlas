import os
import requests
import kernel.registry as Registry
from kernel.ipcmemory import IPCMemory
from tqdm import tqdm
from llama_cpp import Llama
from typing import List

class AtlasModel:
    
    def __init__(self, lineArgs) -> None:
        self.args: list = lineArgs
        
    def main(self) -> int:
        
        if len(self.args) == 0:
            print(f"Error: Action expected - download, set, delete, load, list")
            return 1
        
        if self.args[0] == "download":
            return self.download()
        elif self.args[0] == "set":
            return self.set()
        elif self.args[0] == "delete":
            return self.delete()
        elif self.args[0] == "load":
            return self.load()
        elif self.args[0] == "list":
            for l in self.getListOfModels(): print(l)
            return 0
        
        print(f"Error: Action expected - download, set, delete, load, list")
        return 1
            
    def getListOfModels(self) -> List[str]:
        libLoc = Registry.read("SOFTWARE.Helium.Program.Atlas.ModelLibrary")
        file_list = []
        extensions = [Registry.read("SOFTWARE.Helium.Program.Atlas.ModelFileExtension")]
        for root, dirs, files in os.walk(libLoc):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):                    
                    file_list.append(file)
        return file_list
    
    def load(self):
        models = self.getListOfModels()
        modelName = self.args[1] if len(self.args) >= 2 else Registry.read("SOFTWARE.Helium.Program.Atlas.ModelSelected")
        if modelName not in models:
            print(f"Error: No such model found - {modelName}")
            return 2
        
        print(f"Loading model: {modelName}")
        modelLoc = Registry.read("SOFTWARE.Helium.Program.Atlas.ModelLibrary") + os.sep + modelName
        
        verbose = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.Verbose") == "1"
        batch = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.Batch")
        seed = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.Seed")
        threads = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.Threads")
        tokens = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.MaxTokens")
        lasttokens = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.LastTokens")
        memoryLock = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.MemoryLock")
        tokens = int(tokens)
        lasttokens = int(lasttokens)
        seed = int(seed)
        batch = int(batch)
        threads = int(threads)
        memoryLock = memoryLock == "1"
        print(f"Verbose: {verbose}")
        print(f"Batch: {batch}")
        print(f"Seed: {seed}")
        print(f"Threads: {threads}")
        print(f"Tokens: {tokens}")
        print(f"Last Tokens: {lasttokens}")
        print(f"Memory Lock: {memoryLock}")
        try:
            llm = Llama(model_path=modelLoc, verbose=verbose, n_ctx=tokens, n_batch=batch, n_threads=threads, seed=seed, last_n_tokens_size=lasttokens, use_mlock=memoryLock)
            IPCMemory.setObj("Program.Atlas.Model", llm, persistent=True, permission="1112")
            IPCMemory.setObj("Program.Atlas.ModelLoaded", True, persistent=True, permission="1111")
            print(f"Model loaded.")
        except Exception as e:
            print(e)
            return 1
        
        return 0
        
    def set(self):
        models = self.getListOfModels()
        if len(self.args) < 2:
            print(f"Error: Expected model name.")
            return 3
        
        modelName = self.args[1]
        if modelName not in models:
            print(f"Error: No such model found - {modelName}")
            return 2
        
        Registry.write("SOFTWARE.Helium.Program.Atlas.ModelSelected", modelName)
        return 0
        
    def delete(self):
        models = self.getListOfModels();
        if len(self.args) < 2:
            print(f"Error: Expected model name.")
            return 3
        
        modelName = self.args[1]
        if modelName not in models:
            print(f"Error: No such model found - {modelName}")
            return 2
        
        os.remove(Registry.read("SOFTWARE.Helium.Program.Atlas.ModelLibrary") + os.sep + modelName)
        return 0
           
    def download(self):
        # Check registry validity
        config = 0 if Registry.read("SOFTWARE.Helium.Program.Atlas.AllowModelDownload") == "0" else 1
        config = 0 if len(Registry.read("SOFTWARE.Helium.Program.Atlas.ModelLibrary")) < 1 else config
        
        if config == 0:
            print("Error: It seems that you have invalid configurations.")
            allowDownload = Registry.read("SOFTWARE.Helium.Program.Atlas.AllowModelDownload")
            modelLib = Registry.read("SOFTWARE.Helium.Program.Atlas.ModelLibrary")
            print(f"SOFTWARE.Helium.Program.Atlas.ModelLibrary:       {modelLib}")
            print(f"SOFTWARE.Helium.Program.Atlas.AllowModelDownload: {allowDownload}")
            return 10
        
        url = Registry.read("SOFTWARE.Helium.Program.Atlas.DefaultModelURL")
        if not url.startswith("http") and not len(self.args) > 1 and not self.args[1].startswith("http"):
            print("Error: It seems you have invalid configurations or missing parameter.")
            print("URL must start with http.")
            print(f"URL parameter: {self.args[1]}")
            print(f"SOFTWARE.Helium.Program.Atlas.DefaultModelURL: {url}")
            return 11

        if len(self.args) > 1 and self.args[1].startswith("http"):
            url = self.args[1]
            
        name = url.split("/")[-1]
        print(f"Downloading model {name} from {url}")
        fpath = Registry.read("SOFTWARE.Helium.Program.Atlas.ModelLibrary") + os.sep + name
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

        with open(fpath, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()

        if total_size != 0 and progress_bar.n != total_size:
            print("Failed to download the model file.")
        else:
            print("Model file downloaded successfully.")
