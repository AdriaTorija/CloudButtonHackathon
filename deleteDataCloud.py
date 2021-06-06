from lithops import Storage
bucket='cloudbuttonhackathon'
storage=Storage()

list=storage.list_keys(bucket)
for i in list:
    if i != "keys.txt" and i != "tweets.csv" != "web.csv":
        storage.delete_object(bucket,i)
#storage.delete_objects('cloudbuttonhackathon',list)