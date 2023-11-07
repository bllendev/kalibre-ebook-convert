import os
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from ninja.security import HttpBearer
from api.convert import convert_with_pandoc
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, HttpResponse
from ninja.errors import ValidationError

from django.conf import settings

api = NinjaAPI()

# class TokenAuth(HttpBearer):
#     def authenticate(self, request, token: str):
#         print(f"request: {request}")
#         print(f"token: {token}")
#         if not settings.DEBUG or settings.ENVIRONMENT == "PRODUCTION":
#             if token != os.environ.get("KALIBRE_PRIVADO"):
#                 raise PermissionDenied("Invalid token")
#         return token

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
            # Handle error if the file can't be opened
            return HttpResponse(f"Error serving the converted file: {e}", status=500)