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

magik will eventually support
==============
Google Cloud Storage
Eucalyptus Walrus
Microsoft Azure Blob Storage
