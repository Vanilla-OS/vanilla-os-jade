import os
import subprocess

class CommandUtils:

    @staticmethod
    def run_command(command: list, output: bool = False, decode: bool = True):
        if "FAKE" in os.environ:
            print(" ".join(command))
            return
            
        if output:
            res = subprocess.check_output(command)
            if decode:
                res = res.decode("utf-8").strip()
            return res

        return subprocess.Popen(command, stdout=subprocess.PIPE)

    @staticmethod
    def check_output(command: list, decode: bool = True):
        """Just a wrapper for convenience"""
        return CommandUtils.run_command(command, output=True, decode=decode)
