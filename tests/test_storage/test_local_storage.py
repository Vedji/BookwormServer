import pytest, logging
from io import BytesIO
from fastapi import UploadFile, HTTPException
from tests.test_storage import local_storage


class TestS3Storage:

    exception_no_file = "Файл не найден"

    test_file_key_1 = "test_file.txt"
    test_file_content_1 = b"Test S3 uploading file"
    test_file_content_2 = b"Test 2 S3 uploading file 2"

    @pytest.mark.asyncio
    async def test_upload_file(self, local_storage):
        new_file = UploadFile(filename=self.test_file_key_1, file=BytesIO(self.test_file_content_1))
        response = await local_storage.upload_file(file_key=self.test_file_key_1, file=new_file)
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_reading_file(self, local_storage):
        response = await local_storage.read_file(file_key=self.test_file_key_1)
        assert response.body == self.test_file_content_1
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_replace_file(self, local_storage):
        new_file = UploadFile(filename=self.test_file_key_1, file=BytesIO(self.test_file_content_2))
        response = await local_storage.upload_file(file_key=self.test_file_key_1, file=new_file)
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_reading_file_after_replace(self, local_storage):
        response = await local_storage.read_file(file_key=self.test_file_key_1)
        assert response.body == self.test_file_content_2
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_file(self, local_storage):
        response = await local_storage.delete_file(self.test_file_key_1)
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_reading_not_exists_file(self, local_storage):
        with pytest.raises(HTTPException) as http_exception:
            await local_storage.read_file(file_key=self.test_file_key_1)
        assert http_exception.value.status_code == 404
        assert http_exception.value.detail == self.exception_no_file

