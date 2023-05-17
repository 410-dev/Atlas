import copy
import kernel.registry as Registry
import json

from kernel.states import States

def interactiveMode():
    llm = States.getObj("Program.Atlas.Model")
    
    print("Running test stage.")
    
    prompt = "Question: Write me a shell script that list all the files in a directory, where only files are ending with .net file. Answer: "
    
    while prompt != "" and prompt != "exit":
        prePrompt  = Registry.read("SOFTWARE.Helium.Program.Atlas.Preprompt")
        max_tokens = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.MaxTokens")
        stop       = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.Stop")
        streamMode = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.Stream")
        echo       = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.Echo")
        postPrompt = Registry.read("SOFTWARE.Helium.Program.Atlas.Postprompt")
        role       = Registry.read("SOFTWARE.Helium.Program.Atlas.AssistantRole")
        rolePrompt = Registry.read("SOFTWARE.Helium.Program.Atlas.Local.RoleDescriptionPrompt")
        name       = Registry.read("SOFTWARE.Helium.Program.Atlas.Name")
        
        echo       = echo == "1"
        streamMode = streamMode == "1"
        stop       = json.loads(stop)
        stop       = stop["data"]
        max_tokens = int(max_tokens)
        
        prompt = rolePrompt.replace("%role%", role).replace("%name%", name) + prePrompt + prompt + postPrompt
        
        if echo == streamMode:
            print("Warning! Echo mode and stream mode are in same state.")
            print("This will conflict the code, so code will automatically switched to stream mode.")
            streamMode = True
            echo = False
        
        stream = llm(
            prompt=prompt,
            max_tokens=max_tokens,
            stop=stop,
            stream=streamMode,
            echo=echo
        )
        
        for out in stream:
            completionFragment = copy.deepcopy(out)
            print(completionFragment["choices"][0]["text"], end="")
            
        print("")
        print("")
        prompt = input("atlas >>> ")
        
        