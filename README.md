magik
==============

Makes it easy to upload and download files to supported cloud storage systems.

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

magik will eventually support
==============
Eucalyptus Walrus
Microsoft Azure Blob Storage

more TODOs
==============
parallelized downloads and uploads for S3 and GCS
delete_files for S3 and GCS

get help
==============
E-mail Chris Bunch (chris@appscale.com) or file an issue!
