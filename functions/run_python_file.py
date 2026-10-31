import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

  try:
    working_directory_abs_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_abs_path, file_path))

    valid_target_dir = (
      os.path.commonpath([working_directory_abs_path, target_dir])
      == working_directory_abs_path
      )
    if not valid_target_dir:
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_dir):
      return f'"{file_path}" does not exist or is not a regular file'
    
    if file_path.endswith(".py") == False:
      return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_dir]
    
    if args:
      command.extend(args)
      
    result = subprocess.run(
            command,
            cwd=working_directory_abs_path,
            capture_output=True,
            text=True,
            timeout=30,
        )
    
    output_parts = []
    
    if result.returncode != 0:
      output_parts.append(f"Process exited with code {result.returncode}")
    if not result.stdout and not result.stderr:
      output_parts.append("No output produced")
    if result.stdout:
      output_parts.append(f"STDOUT:\n{result.stdout}")
    if result.stderr:
      output_parts.append(f"STDERR:\n{result.stderr}")
      
    return "\n".join(output_parts)

  except Exception as e:
    return f"Error: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file relative to the working directory with optional command-line arguments, returning its stdout, stderr and exit code",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}
