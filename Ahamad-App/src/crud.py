import base64
import hashlib
import os
import re
import logging
from datetime import datetime
from tinydb import TinyDB, Query
from cryptography.fernet import Fernet
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='app.log')
logger = logging.getLogger(__name__)

# Paths
DATA_PATH = 'data/'
THUMBNAIL_PATH = os.path.join(DATA_PATH, 'thumbnails')

# Initialize TinyDB databases
lyrics_db = TinyDB(os.path.join(DATA_PATH, 'lyrics.json'))

# Encryption key (in a real application, store this securely)
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

def validate_input(input_str):
    """
    Validate input to prevent security issues.

    Args:
        input_str (str): The input string to validate.

    Returns:
        str: The validated input string.

    Raises:
        ValueError: If the input is invalid.
    """
    if not re.match(r"^[A-Za-z0-9 _]*[A-Za-z0-9][A-Za-z0-9 _]*$", input_str):
        logger.error("Invalid input detected")
        raise ValueError("Invalid input")
    return input_str

def calculate_checksum(data):
    """
    Calculate SHA-256 checksum of the given data.

    Args:
        data (str or bytes): The data to calculate the checksum for.

    Returns:
        str: The calculated checksum.
    """
    checksum = hashlib.sha256(data.encode('utf-8') if isinstance(data, str) else data).hexdigest()
    logger.info("Calculated checksum: %s", checksum)
    return checksum

def encrypt(data):
    """
    Encrypt the data with the given key.

    Args:
        data (str): The data to encrypt.

    Returns:
        str: The encrypted data.
    """
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

def decrypt(data):
    """
    Decrypt the data with the given key.

    Args:
        data (str): The encrypted data to decrypt.

    Returns:
        str: The decrypted data.
    """
    encrypted_data = base64.urlsafe_b64decode(data.encode('utf-8'))
    return cipher_suite.decrypt(encrypted_data).decode('utf-8')

def create_artefact(db, artefact, user):
    """
    Create a new artefact in the database.

    Args:
        db (TinyDB): The database to insert the artefact into.
        artefact (dict): The artefact data.
        user (str): The user creating the artefact.

    Returns:
        int: The ID of the created artefact.
    """
    try:
        artefact['title'] = validate_input(artefact['title'])
        artefact['content'] = validate_input(artefact['content'])
        artefact['content'] = encrypt(artefact['content'])
        artefact_id = len(db) + 1
        artefact['id'] = artefact_id
        artefact['created_at'] = datetime.now().isoformat()
        artefact['created_by'] = user
        artefact['checksum'] = calculate_checksum(artefact['content'])
        db.insert(artefact)
        logger.info("Artefact created with ID: %d by user: %s", artefact_id, user)
        return artefact_id
    except ValueError as e:
        logger.error("Failed to create artefact: %s", str(e))
        raise ValueError("Failed to create artefact: %s" % str(e)) from e

def read_artefacts(db):
    """
    Read all artefacts from the database.

    Args:
        db (TinyDB): The database to read from.

    Returns:
        list: A list of artefacts.
    """
    try:
        artefacts = db.all()
        for artefact in artefacts:
            artefact['content'] = decrypt(artefact['content'])
        logger.info("Read %d artefacts", len(artefacts))
        return artefacts
    except Exception as e:
        logger.error("Failed to read artefacts: %s", str(e))
        raise Exception("Failed to read artefacts: %s" % str(e)) from e

def update_artefact(db, artefact_id, updated_artefact, user):
    """
    Update an artefact in the database.

    Args:
        db (TinyDB): The database to update.
        artefact_id (int): The ID of the artefact to update.
        updated_artefact (dict): The updated artefact data.
        user (str): The user updating the artefact.

    Raises:
        PermissionError: If the user is not authorized to update the artefact.
    """
    try:
        artefact = db.get(Query().id == artefact_id)
        if artefact['created_by'] != user:
            logger.error("User %s is not authorized to update artefact %d", user, artefact_id)
            raise PermissionError("User not authorized to update this artefact")

        updated_artefact['title'] = validate_input(updated_artefact['title'])
        updated_artefact['content'] = validate_input(updated_artefact['content'])
        updated_artefact['content'] = encrypt(updated_artefact['content'])
        updated_artefact['modified_at'] = datetime.now().isoformat()
        updated_artefact['checksum'] = calculate_checksum(updated_artefact['content'])
        db.update(updated_artefact, Query().id == artefact_id)
        logger.info("Artefact with ID %d updated by user: %s", artefact_id, user)
    except ValueError as e:
        logger.error("Failed to update artefact: %s", str(e))
        raise ValueError("Failed to update artefact: %s" % str(e)) from e

def delete_artefact(db, artefact_id, user):
    """
    Delete an artefact from the database.

    Args:
        db (TinyDB): The database to delete from.
        artefact_id (int): The ID of the artefact to delete.
        user (str): The user deleting the artefact.

    Raises:
        PermissionError: If the user is not authorized to delete the artefact.
    """
    try:
        artefact = db.get(Query().id == artefact_id)
        if artefact['created_by'] != user and user != 'admin':
            logger.error("User %s is not authorized to delete artefact %d", user, artefact_id)
            raise PermissionError("User not authorized to delete this artefact")

        db.remove(Query().id == artefact_id)
        logger.info("Artefact with ID %d deleted by user: %s", artefact_id, user)
    except Exception as e:
        logger.error("Failed to delete artefact: %s", str(e))
        raise Exception("Failed to delete artefact: %s" % str(e)) from e

def save_thumbnail(image_path, category, artefact_id):
    """
    Save a thumbnail for the artefact.

    Args:
        image_path (str): The path to the image file.
        category (str): The category of the artefact.
        artefact_id (int): The ID of the artefact.

    Raises:
        Exception: If there is an error saving the thumbnail.
    """
    try:
        thumbnail_dir = os.path.join(THUMBNAIL_PATH, category)
        os.makedirs(thumbnail_dir, exist_ok=True)

        image = Image.open(image_path)
        image.thumbnail((128, 128))
        thumbnail_path = os.path.join(thumbnail_dir, f'{artefact_id}.png')
        image.save(thumbnail_path)
        logger.info("Thumbnail saved for artefact ID %d", artefact_id)
    except Exception as e:
        logger.error("Failed to save thumbnail: %s", str(e))
        raise Exception("Failed to save thumbnail: %s" % str(e)) from e

def create_artefact_with_thumbnail(db, artefact, image_path, category, user):
    """
    Create an artefact with an associated thumbnail.

    Args:
        db (TinyDB): The database to insert the artefact into.
        artefact (dict): The artefact data.
        image_path (str): The path to the image file.
        category (str): The category of the artefact.
        user (str): The user creating the artefact.

    Returns:
        int: The ID of the created artefact.
    """
    try:
        artefact_id = create_artefact(db, artefact, user)
        if artefact_id is not None:
            save_thumbnail(image_path, category, artefact_id)
            logger.info("Artefact with ID %d created with thumbnail by user: %s", artefact_id, user)
            return artefact_id
        else:
            logger.error("Failed to create artefact, artefact_id is None")
            raise Exception("Failed to create artefact, artefact_id is None")
    except Exception as e:
        logger.error("Failed to create artefact with thumbnail: %s", str(e))
        raise Exception("Failed to create artefact with thumbnail: %s" % str(e)) from e

def verify_checksum(data, checksum):
    """
    Verify the checksum of the given data.

    Args:
        data (str): The data to verify.
        checksum (str): The expected checksum.

    Returns:
        bool: True if the checksum is valid, False otherwise.
    """
    calculated_checksum = calculate_checksum(data)
    if calculated_checksum == checksum:
        logger.info("Checksum verification succeeded")
        return True
    else:
        logger.error("Checksum verification failed")
        return False
