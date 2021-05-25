from lithops import Storage
bucket='cloudbuttonhackathon'
storage=Storage()

list=storage.list_keys(bucket)
storage.delete_objects('cloudbuttonhackathon',list)