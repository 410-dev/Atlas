# Atlas Registry Documentation

The registry contains settings and parameters for the Atlas. Below is an explanation of each key and its possible values:

## SOFTWARE.Helium.Program.Atlas.OpenAIAPI
- Description: Specifies the OpenAI API configuration for the Atlas. This is required if you are using OpenAI's GPT.
- Possible Values: Any valid OpenAI API configuration value.

## SOFTWARE.Helium.Program.Atlas.OpenAIModel
- Description: Specifies the model of OpenAI's GPT. This is required if you are using OpenAI's GPT.
- Possible Values: Any valid OpenAI API configuration value.

## SOFTWARE.Helium.Program.Atlas.GoogleAPI
- Description: Specifies the Google API configuration for the Atlas. This is used for searching in Google.
- Possible Values: Any valid Google Search API configuration value.

## SOFTWARE.Helium.Program.Atlas.GoogleAPICX
- Description: Specifies the Google API CX configuration for the Atlas. This is used for searching in Google.
- Possible Values: Any valid Google Search CX value.

## SOFTWARE.Helium.Program.Atlas.Name
- Description: Specifies the name of the Atlas program.
- Possible Values: Any string value.

## SOFTWARE.Helium.Program.Atlas.AssistantRole
- Description: Specifies the role of the Atlas program.
- Possible Values: Any string value representing the role.

## SOFTWARE.Helium.Program.Atlas.Preprompt
- Description: Specifies the pre-prompt text for the Atlas.
- Possible Values: Any string value.

## SOFTWARE.Helium.Program.Atlas.Postprompt
- Description: Specifies the post-prompt text for the Atlas.
- Possible Values: Any string value.

## SOFTWARE.Helium.Program.Atlas.StoreContext
- Description: Specifies whether the context should be stored by the Atlas.
- Possible Values: 0 (do not store context) or 1 (store context).

## SOFTWARE.Helium.Program.Atlas.UseOfflineModel
- Description: Specifies whether the Atlas should use an offline AI model.
- Possible Values: 0 (do not use offline model) or 1 (use offline model).

## SOFTWARE.Helium.Program.Atlas.ModelLibrary
- Description: Specifies the directory path for the AI models used by the Atlas.
- Possible Values: Any valid directory path.

## SOFTWARE.Helium.Program.Atlas.ModelSelected
- Description: Specifies the selected AI model for the Atlas.
- Possible Values: Any valid AI model identifier with file extension.

## SOFTWARE.Helium.Program.Atlas.DefaultModel
- Description: Specifies the default AI model for the Atlas.
- Possible Values: Any valid AI model identifier with file extension.

## SOFTWARE.Helium.Program.Atlas.DefaultModelURL
- Description: Specifies the URL for downloading the default AI model.
- Possible Values: Any valid URL.

## SOFTWARE.Helium.Program.Atlas.RequreDefaultModel
- Description: Specifies whether the default AI model is required by the Atlas.
- Possible Values: 0 (default model not required) or 1 (default model required).

## SOFTWARE.Helium.Program.Atlas.AllowDefaultModelFallback
- Description: Specifies whether the Atlas can fall back to the default model.
- Possible Values: 0 (fallback not allowed) or 1 (fallback allowed).

## SOFTWARE.Helium.Program.Atlas.AllowModelDownload
- Description: Specifies whether the Atlas can download additional AI models.
- Possible Values: 0 (model download not allowed) or 1 (model download allowed).

## SOFTWARE.Helium.Program.Atlas.AllowProgramUpdate
- Description: Specifies whether the Atlas can perform program updates.
- Possible Values: 0 (program update not allowed) or 1 (program update allowed).

## SOFTWARE.Helium.Program.Atlas.AllowKernelUpdate
- Description: Specifies whether the Atlas can perform kernel updates.
- Possible Values: 0 (kernel update not allowed) or 1 (kernel update allowed).

## SOFTWARE.Helium.Program.Atlas.AllowAutoUpdate
- Description: Specifies whether the Atlas can perform automatic updates.
- Possible Values: 0 (auto-update not allowed) or 1 (auto-update allowed).

## SOFTWARE.Helium.Program.Atlas.LoadModelOnSystemBoot
- Description: Specifies whether the AI model should be loaded on system boot.
- Possible Values: 0 (do not load model on boot) or 1 (load model on boot).

## SOFTWARE.Helium.Program.Atlas.ModelFileExtension
- Description: Specifies the file extension for AI model files used by the Atlas.
- Possible Values: Any valid file extension.

## SOFTWARE.Helium.Program.Atlas.AllowMicrophoneAccess
- Description: Specifies whether the Atlas can access the microphone.
- Possible Values: 0 (microphone access not allowed) or 1 (microphone access allowed).

## SOFTWARE.Helium.Program.Atlas.AllowProgramInternetAccess
- Description: Specifies whether the Atlas can access the internet.
- Possible Values: 0 (internet access not allowed) or 1 (internet access allowed).

## SOFTWARE.Helium.Program.Atlas.CheckModelLoadedOnLaunch
- Description: Specifies whether the Atlas should check if the model is loaded on launch.
- Possible Values: 0 (do not check model loaded) or 1 (check model loaded).

## SOFTWARE.Helium.Program.Atlas.GPUAcceleration
- Description: Specifies whether GPU acceleration is enabled for the Atlas.
- Possible Values: 0 (disable GPU acceleration) or 1 (enable GPU acceleration).
