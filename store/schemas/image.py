from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image."
    }

    def _deserialize(self, value, attr, data) -> FileStorage:
        print('_deserialize called')
        if value is None:
            return None
        print('_deserialize 2')
        if not isinstance(value, FileStorage):
            self.fail("invalid")
        print('_deserialize 3')
        return value


class ImageSchema(Schema):
    image = FileStorageField(required=True)
