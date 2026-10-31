import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs_path, directory))

        valid_target_dir = (
            os.path.commonpath([working_directory_abs_path, target_dir])
            == working_directory_abs_path
        )
        if not valid_target_dir:
            raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory')

        if not os.path.isdir(target_dir):
            raise Exception(f'"{directory}" is not a directory')

        files_list: list[str] = []
        for filename in os.listdir(target_dir):
            file_path = os.path.join(target_dir, filename)
            files_list.append(
                f"- {filename}: file_size={os.path.getsize(file_path)}, "
                f"is_dir={os.path.isdir(file_path)}"
            )

        listing = "\n".join(files_list)
        return f'Result for "{directory}" directory:\n{listing}'

    except Exception as e:
        return f'Result for "{directory}" directory:\nError: {e}'
      
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}