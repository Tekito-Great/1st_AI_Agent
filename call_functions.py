from constant import *
from functions.get_files_info import *

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

FUNCTION_DISPATCH_TABLE = {
    "get_file_content": get_file_content,  # ← Python関数（例）
    "write_file": write_file,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file
}


def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")


    if function_name in ["get_files_info","get_file_content","run_python_file","write_file"]:

        target_function = FUNCTION_DISPATCH_TABLE.get(function_name)
        result = target_function(**args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_name,
                response={"result": result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    