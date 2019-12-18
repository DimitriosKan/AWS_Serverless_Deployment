from zipfile import ZipFile

zipObj = ZipFile('function_test_hello.zip', 'w')

zipObj.write('function_test_hello.py')

zipObj.close()
