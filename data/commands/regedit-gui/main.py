import os

class RegeditGui:

    def __init__(self, lineArgs) -> None:
        self.args: list = lineArgs

    def main(self):
        # Execute shell script
        os.system("java --enable-preview -jar data/commands/regedit-gui/Regedit.jar ./registry &")
