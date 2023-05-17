# Project Atlas

An AI assistant running on [Helium Kernel](https://github.com/410-dev/Helium-core). Model powered by:`stable-vicuna-13B.q4` ([Link](https://huggingface.co/TheBloke/stable-vicuna-13B-GGML/resolve/main/stable-vicuna-13B.ggml.q4_0.bin))



## Requirements:

- Helium Kernel >= 1.1
    - Supports startup hook
    - Supports State Memory (Interprocess shared memory)
- Python 3.10 <= 
    - Helium Kernel requires Python 3.10 or higher.
- Pip
    - When Atlas installs required libraries, it uses pip.



## Libraries

These libraries are automatically installed via pip when user runs `atlas-install` command.

- llama-cp-python
- tqdm



## Instruction

1. Copy everything under `data` directory to the corresponding `data` directory of Helium Kernel.
2. Startup Helium, and you should see the following line:
    `[Atlas Hook]: Atlas is not configured yet. Please run atlas-install.`
3. Run `atlas-install`.
    1. This will automatically install python dependencies and registry keys.
4. If there's any configuration to edit, use `regedit` command to update the program settings.
    1. All of the configuration is under the following key: `SOFTWARE.Helium.Program.Atlas`
    2. If you've changed any configurations, it is recommended to restart Helium.
5. Run `atlas` to run the program.