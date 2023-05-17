import os
import kernel.registry as Registry
import subprocess
import sys
from tqdm import tqdm
import requests

class AtlasInstall:
    
    def __init__(self, lineArgs) -> None:
        self.args: list = lineArgs
        
    def main(self) -> int:
        # Install dependencies
        print(f"Installing packages...")
        package = []
        with open("./data/commands/atlas-install/requirements.txt", 'r') as f:
            package = f.readlines()
        args = [sys.executable, "-m", "pip", "install"]
        args.extend(package)
        print(f"Execution parameter: {args}")
        exitcode = subprocess.check_call(args)
        if exitcode != 0:
            print(f"Error while installing packages.")
            return exitcode
        print(f"Package installation complete.")
        
        # Install registry keys
        print(f"Installing registry keys...")
        regs = []
        with open("./data/commands/atlas-install/registries.txt", 'r') as f:
            regs = f.readlines()
        for line in regs:
            name = line.split("=")[0]
            value = line.split("=")[1].strip() if not line.endswith("=") else ""
        
            Registry.write(name, value)
            print(f"Updated registry: {name} -> {value}")
        print(f"Finished installing registry.")
        
        # Download offline model
        config = 0 if Registry.read("SOFTWARE.Helium.Program.Atlas.AllowModelDownload") == "0" else 1
        config = 0 if Registry.read("SOFTWARE.Helium.Program.Atlas.UseOfflineModel") == "0" else config
        config = 0 if len(Registry.read("SOFTWARE.Helium.Program.Atlas.ModelLibrary")) < 1 else config
        config = 0 if len(Registry.read("SOFTWARE.Helium.Program.Atlas.DefaultModel")) < 1 else config
        config = 0 if len(Registry.read("SOFTWARE.Helium.Program.Atlas.DefaultModelURL")) < 1 else config
        config = 0 if "--no-model-download" in self.args else config
        
        if config == 1:
            print(f"Downloading model...")
            url = Registry.read("SOFTWARE.Helium.Program.Atlas.DefaultModelURL")
            fpath = Registry.read("SOFTWARE.Helium.Program.Atlas.ModelLibrary") + os.sep + Registry.read("SOFTWARE.Helium.Program.Atlas.DefaultModel")
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
        else:
            print("Skipped model downloading.")
            
        Registry.write("SOFTWARE.Helium.Program.Atlas.SetupDone", "1")
        print("Installation complete.")
