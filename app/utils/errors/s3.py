from fastapi import HTTPException
from botocore.exceptions import NoCredentialsError, ClientError



def handle_s3_errors(func):
    """Декоратор для обработки ошибок S3-хранилища."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoCredentialsError:
            raise HTTPException(status_code=403, detail="AWS credentials not found")
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            raise HTTPException(status_code=400, detail=f"S3 Error ({error_code}): {error_message}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return wrapper