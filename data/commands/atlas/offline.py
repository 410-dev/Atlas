import copy
import kernel.registry as Registry
import json

from kernel.ipcmemory import IPCMemory

def command(command):
    return

def main(args: list):
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
                print(completionFragment["choices"][0]["text"], end="")
                returnValue.append(completionFragment["choices"][0]["text"])
        else:
            print(stream["choices"][0]["text"])
            returnValue.append(stream["choices"][0]["text"])
        
        returnValue = "".join(returnValue)
        print("========End========")
        print("")
        print("")
        if len(args) > 0:
            return returnValue
        else:
            prompt = input("atlas >>> ")
    return 0        
        