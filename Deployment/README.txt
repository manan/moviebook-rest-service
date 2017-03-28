**** Heroku configurations
+ Create Procfile
+ Create Requirements.txt
+ Create Runtime.txt
+ Modify settings: add [
    DATABASES['default'] = dj_database_url.config()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    ALLOWED_HOSTS = ['*']
] to settings.py
+ add psycopg2-2.6.2 to requirements.txt
+ pip install whitenoise dj_database_url gunicorn
+ Create remote on heroku git
+ Push git repository to heroku git

**** S3 Bucket Configurations
+ run 'pip install django-storages boto3'
+ add 'storages' to installed apps
+ add to settings.py [
    AWS_QUERYSTRING_AUTH = False
    AWS_STORAGE_BUCKET_NAME = 'moviebook'
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.ca-central-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    MEDIA_ROOT = MEDIA_URL
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
]
+ create IAM User for s3 bucket access and create policy -
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "PublicReadForGetBucketObjects",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::BUCKET-NAME/*"
        },
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "USER_ARN"
            },
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::BUCKET-NAME",
                "arn:aws:s3:::BUCKET-NAME/*"
            ]
        }
    ]
}
+ add environment variables from heroku dashboard 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_KEY_KEY' and 'S3_USE_SIGV4'