import os
from zipfile import ZipFile

file_dir = os.chdir('../docs')
#fileName = 'function_test_hello.py'
list_folder = os.listdir(file_dir)
cwd = os.getcwd()

print (cwd)

zipObj = ZipFile('../function_test_hello.zip', 'w')

if 'function_test_hello.py' in list_folder:
    print ('Yas')
    zipObj.write('function_test_hello.py')
else:
    print ('ew...')

zipObj.close()
