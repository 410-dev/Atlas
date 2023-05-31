import copy
import kernel.registry as Registry
import json
import os
from llama_cpp import Llama

from kernel.ipcmemory import IPCMemory

def command(command):
    return

def main(args: list):

    if Registry.read("SOFTWARE.Helium.Program.Atlas.Local.NoModelOnIPC") == "1":
        modelLoc = Registry.read("SOFTWARE.Helium.Program.Atlas.ModelLibrary") + os.sep + Registry.read("SOFTWARE.Helium.Program.Atlas.ModelSelected")
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
        llm = Llama(model_path=modelLoc, verbose=verbose, n_ctx=tokens, n_batch=batch, n_threads=threads, seed=seed, last_n_tokens_size=lasttokens, use_mlock=memoryLock)
    else: 
        llm = IPCMemory.getObj("Program.Atlas.Model")
    
    if len(args) > 0:
        prompt = " ".join(args)
    else:
        prompt = input("atlas >>> ")
    
    while prompt != "" and prompt != "exit":
        prePrompt  = Registry.read("SOFTWARE.Helium.Program.Atlas.Preprompt")
        max_tokens = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.MaxTokensPerMessage")
        stop       = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.Stop")
        streamMode = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.Stream")
        echo       = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.Echo")
        postPrompt = Registry.read("SOFTWARE.Helium.Program.Atlas.Postprompt")
        role       = Registry.read("SOFTWARE.Helium.Program.Atlas.AssistantRole")
        rolePrompt = Registry.read("SOFTWARE.Helium.Program.Atlas.RoleDescriptionPrompt")
        name       = Registry.read("SOFTWARE.Helium.Program.Atlas.Name")
        
        echo       = echo == "1"
        streamMode = streamMode == "1"
        stop       = json.loads(stop)
        stop       = stop["data"]
        max_tokens = int(max_tokens)
        
        if echo == streamMode:
            print("Warning! Echo mode and stream mode are in same state.")
            print("This will conflict the code, so code will automatically switched to stream mode.")
            streamMode = True
            echo = False
        
        # if len(args) > 0 and not echo:
        #     print("Warning! Non-interactive mode is active.")
        #     print("Forcing echo mode.")
        #     streamMode = False
        #     echo = True
            
        if prompt.startswith(Registry.read("SOFTWARE.Helium.Program.Atlas.Local.CommandSymbol")):
            command(prompt)
            continue
        
        promptFormat = Registry.read("SOFTWARE.Helium.Program.Atlas.PromptFormat")
        prompt = promptFormat.replace("%preprompt%", prePrompt).replace("%postprompt%", postPrompt).replace("%roleprompt%", rolePrompt.replace("%role%", role).replace("%name%", name)).replace("%userprompt%", prompt)

        if Registry.read("SOFTWARE.Helium.Program.Atlas.Local.SoftVerbose") == "1":
            print("\nSettings: ")
            print(f"prompt: {prompt}")
            print(f"max_tokens: {max_tokens}")
            print(f"stop: {stop}")
            print(f"stream: {streamMode}")
            print(f"echo: {echo}")
        
        stream = llm(
            prompt=prompt,
            max_tokens=128,
            stop=stop,
            stream=streamMode,
            echo=echo
        )
        
        print("\n\n")
        print("AI:================")
        returnValue = []
        if streamMode:
            for out in stream:
                completionFragment = copy.deepcopy(out)
                print(completionFragment["choices"][0]["text"], end="", flush=True)
                returnValue.append(completionFragment["choices"][0]["text"])
        else:
            print(stream["choices"][0]["text"])
            returnValue.append(stream["choices"][0]["text"])
        
        returnValue = "".join(returnValue)
        ending = "" if returnValue.endswith("\n") else "\n"
        print(f"{ending}========End========")
        print("")
        print("")
        if len(args) > 0:
            return returnValue
        else:
            prompt = input("atlas >>> ")
    return 0        
        