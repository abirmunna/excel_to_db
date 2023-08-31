# imports
import subprocess
from typing import Optional, List
import re

# Define the command to run
COMMAND: List[str] = ["lsnrctl", "status"]


def get_service_name(cmd: Optional[List[str]] = None) -> str:
    """Get the default service name from the output of lsnrctl status command."""
    try:
        output = subprocess.check_output(cmd or COMMAND, text=True)
        match = re.search(r"Default Service .*?(\w+)", output)

        if match:
            default_service = match.group(1)
            return f"{default_service}"
        else:
            return "Default Service not found in the output."
    except subprocess.CalledProcessError as error:
        return f"Error: {error}"
