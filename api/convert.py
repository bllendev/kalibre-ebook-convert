# convert.py
from django.conf import settings
import os
import subprocess

import logging
logger = logging.getLogger(__name__)

def convert_with_pandoc(input_path, output_format):
    """
    Convert a file using pandoc.

    Parameters:
    - input_path: The path to the input file.
    - output_format: The format to convert to.

    Returns:
    - Tuple containing:
        - output_path: The path to the converted file or None if failed.
        - message: Success or error message.
    """
    base_name = input_path.rsplit('.', 1)[0]
    output_path = os.path.join(settings.BASE_DIR, f"{base_name}.{output_format}")
    try:
        subprocess.run(['pandoc', input_path, '-o', output_path], check=True, capture_output=True)
        return (output_path, f"File converted successfully. Saved to {output_path}.")
    except subprocess.CalledProcessError as e:
        logger.error(f"convert_with_pandoc error! {e} | output_path: {output_path}")
        return (None, f"Error during conversion: {e}")
