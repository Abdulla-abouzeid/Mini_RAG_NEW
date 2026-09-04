from enum import Enum
class ResponseSignal(Enum):
    File_type_not_allowed = "File type not allowed."
    File_size_exceeds_maximum = "File size exceeds the maximum allowed size."
    file_uploaded_successfully = "File uploaded successfully."
    file_upload_failed = "File upload failed."
    file_validation_failed = "File validation failed."