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
easy_install requests
```

upload a file
==============
```
magik upload_files --name s3 --AWS_ACCESS_KEY YOUR_ACCESS_KEY --AWS_SECRET_KEY YOUR_SECRET_KEY --source ~/cat-photo.jpg --destination /your-bucket-name/cat-photo.jpg
```

download a file
==============
```
magik download_files --name s3 --AWS_ACCESS_KEY YOUR_ACCESS_KEY --AWS_SECRET_KEY YOUR_SECRET_KEY --source /your-bucket-name/cat-photo.jpg --destination ~/cat-photo2.jpg
```

using the REST API
==============
```
magik-server
curl -d 'blah blah file contents blah' -X PUT "http://127.0.0.1:8080/appscale/mykey?name=s3&AWS_ACCESS_KEY=$EC2_ACCESS_KEY&AWS_SECRET_KEY=$EC2_SECRET_KEY"
curl -X GET "http://127.0.0.1:8080/appscale/mykey?name=s3&AWS_ACCESS_KEY=$EC2_ACCESS_KEY&AWS_SECRET_KEY=$EC2_SECRET_KEY"
curl -X DELETE "http://127.0.0.1:8080/appscale/mykey?name=s3&AWS_ACCESS_KEY=$EC2_ACCESS_KEY&AWS_SECRET_KEY=$EC2_SECRET_KEY"
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

miscellaneous
==============
to use Google Cloud Storage, you'll need an access key and secret key. get them at https://code.google.com/apis/console#:storage:legacy
