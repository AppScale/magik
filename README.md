magik
==============

Makes it easy to upload and download files to supported cloud storage systems.

dependencies
==============
```
easy_install boto
easy_install azure
```

when using magik-server:
```
easy_install WebOb
easy_install Paste
easy_install webapp2
```

upload a file
==============
```
magik upload_files --name s3 --AWS_ACCESS_KEY YOUR_ACCESS_KEY --AWS_SECRET_KEY YOUR_SECRET_KEY --source ~/cat-photo.jpg --destination /your-bucket-name/cat-photo.jpg
```

download a file
==============
```
magik upload_files --name s3 --AWS_ACCESS_KEY YOUR_ACCESS_KEY --AWS_SECRET_KEY YOUR_SECRET_KEY --source /your-bucket-name/cat-photo.jpg --destination ~/cat-photo2.jpg
```

magik supports
==============
Amazon Simple Storage Service (S3)
Google Cloud Storage
Eucalyptus Walrus
Microsoft Azure Blob Storage

more TODOs
==============
parallelized downloads and uploads
delete_files

miscellaneous
==============
to use Google Cloud Storage, you'll need an access key and secret key. get them at https://code.google.com/apis/console#:storage:legacy

get help
==============
E-mail Chris Bunch (chris@appscale.com) or file an issue!
