import os

upload_dir = os.path.dirname(os.path.abspath(__file__)) + '/docs/'
print (upload_dir)

docfiles = [f for f in os.listdir(upload_dir) if os.path.isfile(os.path.join(upload_dir, f))]
print (docfiles)

for file_name in docfiles:
    print (file_name)

'''
for uploads in os.walk(upload_dir):
    #print (str(uploads) + 'uploads')
    for filename in uploads:
        print (str(filename) + 'filename')
        for obj in filename:
            file_name = obj

            print (file_name)
'''
