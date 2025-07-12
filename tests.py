# from subdirectory.filename import function_name
from functions.get_files_info import get_files_info
from functions.get_files_info import get_file_content
from functions.get_files_info import write_file
from functions.get_files_info import run_python_file




#print (get_file_content("calculator", "lorem.txt"))
#print ("**********************************")
print (run_python_file("calculator", "main.py"))
#print ("**********************************")
print (run_python_file("calculator", "tests.py"))
#print ("**********************************")
print (run_python_file("calculator", "../main.py"))
#print ("**********************************")
print (run_python_file("calculator", "nonexistent.py"))
#print ("**********************************")
