import os
import uuid
import shutil
import logging
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings

# Rule 10: Observability for file operations
logger = logging.getLogger(__name__)

def save_upload_file(file: UploadFile, sub_folder: str) -> str:
    """
    Rule 11: Decoupled business logic for saving files to physical disk.
    Rule 6: Uses UUIDs to prevent file name collisions or overwrites.
    """
    # 1. Determine the target directory based on the sub_folder (images, voice, etc.)
    target_base = Path(settings.MEDIA_ROOT) / sub_folder
    
    # 2. Rule 1: Ensure directory exists (Safety check)
    target_base.mkdir(parents=True, exist_ok=True)

    # 3. Rule 6: Generate a safe, unique filename using UUID
    extension = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4()}{extension}"
    
    # 4. Create the final physical path
    file_path = target_base / unique_filename

    # 5. Rule 2: Save the actual file bytes to disk using efficient buffering
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        # Rule 1: Always close the temporary file handle
        file.file.close()

    # 6. Return web-safe path for DB storage (e.g., "media/images/uuid.png")
    return str(file_path).replace("\\", "/")

def delete_file(relative_path: str) -> bool:
    """
    Rule 11: Decoupled business logic for deleting physical files.
    Rule 14: Security - Ensures only files inside MEDIA_ROOT can be deleted.
    """
    try:
        if not relative_path:
            return False

        # 1. Security Check: Resolve paths to prevent Path Traversal attacks
        base_path = Path(settings.MEDIA_ROOT).resolve()
        target_path = Path(relative_path).resolve()

        # 2. Verify target is strictly within the media folder
        if not str(target_path).startswith(str(base_path)):
            logger.warning(f"Security Alert: Attempted deletion outside media root: {relative_path}")
            return False

        # 3. Rule 2: Physically remove file if it exists
        if target_path.exists() and target_path.is_file():
            target_path.unlink()
            logger.info(f"Physically deleted file: {relative_path}")
            return True
            
        return False
    except Exception as e:
        logger.error(f"Failed to delete file {relative_path}: {e}")
        return False

def get_file_path(sub_folder: str, filename: str) -> str:
    relative_path = Path(settings.MEDIA_ROOT) / sub_folder / filename
    web_safe_path = str(relative_path).replace("\\", "/")

    if not relative_path.exists():
        logger.warning(f"Requested file does not exist: {web_safe_path}")
        return web_safe_path