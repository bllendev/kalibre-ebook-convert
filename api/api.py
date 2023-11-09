import os
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from ninja.security import APIKeyHeader

from api.convert import convert_with_pandoc
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, HttpResponse
from ninja.errors import ValidationError

from django.conf import settings

import logging
logger = logging.getLogger(__name__)

class InvalidToken(Exception):
    pass

class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        if key == os.getenv("KALIBRE_PRIVADO"):
            return key
        logger.error(f"error: bad authenticate: {request}")
        raise InvalidToken


header_key = ApiKey()
api = NinjaAPI(auth=header_key)

# ---------------- #
# -- Exceptions -- #
# ---------------- #
@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)


@api.exception_handler(ValidationError)
def custom_validation_errors(request, exc):
    print(exc.errors)  # <--------------------- !!!!
    return api.create_response(request, {"detail": exc.errors}, status=422)

# Endpoint for conversion
@api.post("/convert/")
def convert_file(request, input_file: UploadedFile, output_format: str):
    if hasattr(input_file, 'temporary_file_path'):
        # File is stored on disk
        input_path = input_file.temporary_file_path()
    else:
        # File is in memory, let's save it to a temp file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            for chunk in input_file.chunks():
                tmp.write(chunk)
            input_path = tmp.name

    # return {"output_path": output_path, "message": message}
    output_path, message = convert_with_pandoc(input_path, output_format)

    if output_path:
        try:
            # Open the file for reading in binary mode
            f = open(output_path, 'rb')
            # Create a FileResponse sending it as attachment
            response = FileResponse(f)
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_path)}"'
            return response
        except Exception as e:
            logger.error(f"error: couldn't open file !: {output_path}")
            return HttpResponse(f"Error serving the converted file: {e}", status=500)