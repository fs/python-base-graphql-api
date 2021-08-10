from django.utils import timezone
from server.core.auth.jwt.utils import generate_hash
from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import safe_join


def get_filename_hash(filename):
    """Generating unique hash which used as filename."""
    timestamp = timezone.now().utctimetuple()
    hash_key = f'{filename} - {timestamp}'
    return generate_hash(hash_key)


class S3DirectUploadStorage(S3Boto3Storage):
    """AWS images storage for direct upload."""

    location = 'python-avatars'
    public_location = 'python-avatars-public'

    def save(self, filename, content=None, max_length=None):  # noqa: WPS110
        """Saving image url in model field."""
        cleaned_name = self._clean_name(filename)
        self.move_file_to_private_folder(cleaned_name)
        return cleaned_name

    def move_file_to_private_folder(self, filename):
        """Moving from public folder to private. Because public folder used for direct upload from frontend."""
        public_location = safe_join(self.public_location, filename)
        private_location = safe_join(self.location, filename)
        copy_source = safe_join(self.bucket_name, public_location)

        self.bucket.Object(private_location).copy_from(CopySource=copy_source)
        self.bucket.Object(public_location).delete()

        return private_location

    def generate_presigned_post(self, filename, file_type):
        """Generate url and headers for direct upload."""
        filename_hash = get_filename_hash(filename)

        expires_in_seconds = 3600

        return self.bucket.meta.client.generate_presigned_post(
            Bucket=self.bucket_name,
            Key=f'{self.public_location}/{filename_hash}',
            Fields={'acl': 'public-read', 'Content-Type': file_type},
            Conditions=[
                {'acl': 'public-read'},
                {'Content-Type': file_type},
            ],
            ExpiresIn=expires_in_seconds,
        )
