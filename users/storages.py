from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage
from django.utils.deconstruct import deconstructible
from storages.utils import safe_join


@deconstructible
class S3DirectUploadStorage(S3Boto3Storage):
    location = 'python-avatars'
    public_location = 'python-avatars-public'

    def save(self, filename, content=None, max_length=None):
        cleaned_name = self._clean_name(filename)
        self.move_file_to_private_folder(cleaned_name)
        return cleaned_name

    def move_file_to_private_folder(self, filename):
        public_location = safe_join(self.public_location, filename)
        private_location = safe_join(self.location, filename)
        copy_source = safe_join(self.bucket_name, public_location)

        self.bucket.Object(private_location).copy_from(CopySource=copy_source)
        self.bucket.Object(public_location).delete()

        return private_location

    @staticmethod
    def get_filename_hash(filename):
        from users.jwt_auth.utils import generate_hash

        hash_key = f'{filename} - {timezone.now().utctimetuple()}'
        return f'{generate_hash(hash_key)}'

    def generate_presigned_post(self, filename, file_type):
        filename_hash = self.get_filename_hash(filename)

        return self.bucket.meta.client.generate_presigned_post(
            Bucket=self.bucket_name,
            Key=f'{self.public_location}/{filename_hash}',
            Fields={"acl": "public-read", "Content-Type": file_type},
            Conditions=[
                {"acl": "public-read"},
                {"Content-Type": file_type},
            ],
            ExpiresIn=3600
        )
