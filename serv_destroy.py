from sample.s3_bucket import S3_Delete
from locators.client_locator import S3Client
from locators.resource_locator import S3Resource

s3_resource = S3Resource().get_resource()

s3_res = S3_Delete(s3_resource)

# fetch the list of buckets still up
def fetch_buckets():
    return s3_res.fetch_buckets()

def empty_and_destroy_buckets():
    # if length of list is above 0 run the 'for' loop
    # iterate through list and run commands on individual instances

    proj_bucket = 'fresh-bucket-but-boto3-2020'

    print ('The buckets I could find are:')
    for bckt in fetch_buckets():
        print (bckt)
    print ('')

    if proj_bucket in fetch_buckets():
        print (f'Destroying "{proj_bucket}" bucket ...')
        s3_res.delete_files(proj_bucket)
        print (f'Bucket "{proj_bucket}" has been emptied')
        s3_res.destroy_bucket(proj_bucket)
        print (f'{proj_bucket} was destroyed.')
    # if it is not, run confirmation of no instances in list
    else:
        print ("We are on the 'else' statement ... Probably there's nothing to clean up")
        print ("Yay!")

if __name__ == "__main__":
    fetch_buckets()
    empty_and_destroy_buckets()
