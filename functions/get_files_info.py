import os
import subprocess
from constant import *
from google.genai import types


def get_files_info(working_directory, directory=None):

    try: 
        full_path = os.path.join(working_directory,directory)
        output = ""

        abs_working_dir = os.path.abspath(working_directory)
        abs_target = os.path.abspath(full_path)
#       print (f"full_path:  {full_path}")
#       print (f"abs_working_dir:  {abs_working_dir}")
#       print (f"abs_target:  {abs_target}")

        if not abs_target.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        if not os.path.isdir(abs_target):
            return f'Error: "{directory}" is not a directory'
      
        content_l = os.listdir(abs_target)
        for content in content_l:
            content_path = os.path.join(abs_target,content)
        
            output += f"- {content}: file-size={os.path.getsize(content_path)} bytes, is_dir={os.path.isdir(content_path)}\n"
        return output
    
    except Exception as e:
        return f"Error: {str(e)}"
    
def get_file_content(working_directory, file_path):
    try:

        full_path = os.path.join(working_directory, file_path)

        abs_working_dir = os.path.abspath(working_directory)
        abs_target = os.path.abspath(full_path)

        if not abs_target.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_target):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_target, "r") as f:
            content = f.read(MAX_CHARS + 1)  # +1 でオーバー検出用に余分に読む

        if len(content) > MAX_CHARS:
            truncated = content[:MAX_CHARS] + '[...File "{file_path}" truncated at 8000 characters]'
            return truncated
        else:
            return content

    except Exception as e:
        return f"Error: {str(e)}"

def write_file(working_directory, file_path, content): 
    try:

        full_path = os.path.join(working_directory, file_path)

        abs_working_dir = os.path.abspath(working_directory)
        abs_target = os.path.abspath(full_path)

        if not abs_target.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        with open(abs_target, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"

def run_python_file(working_directory, file_path):
    try:
        
        full_path = os.path.join(working_directory, file_path)

        abs_working_dir = os.path.abspath(working_directory)
        abs_target = os.path.abspath(full_path)

        if not abs_target.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_target):
            return f'Error: File "{file_path}" not found.'
        
        if not abs_target[-2:] == "py":
            return f'Error: File "{file_path}" not found.'        

        result = subprocess.run(
            ["python", abs_target],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory
        )

        output_lines = []

        # 標準出力
        if result.stdout.strip():
            output_lines.append("STDOUT:\n" + result.stdout.strip())

        # 標準エラー
        if result.stderr.strip():
            output_lines.append("STDERR:\n" + result.stderr.strip())

        # 終了コードが非ゼロなら報告
        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")

        # 出力が何もない場合
        if not output_lines:
            return "No output produced."

        return "\n".join(output_lines)

    except Exception as e:
        return f"Error: {str(e)}"    



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets file content corresponding to the specified file path, limited to 8000 chars, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the target file, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python file corresponding to the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the target file, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write content to the file corresponding to the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the target file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file.",
            ),
        },
    ),
)

