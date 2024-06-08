"""Main module for the command-line application."""

import os
import logging
from tinydb import TinyDB
import crud
from logging_config import setup_logging

def main():
    """Main function to run the application."""
    setup_logging()
    logger = logging.getLogger(__name__)

    data_path = 'data/'

    try:
        # User registration example
        crud.register_user('admin', 'admin_password', 'admin')
        crud.register_user('user', 'user_password', 'user')

        # User login example
        admin = crud.login_user('admin', 'admin_password')
        if admin:
            lyrics_db = TinyDB(os.path.join(data_path, 'lyrics.json'))

            # Example usage
            crud.create_entry_with_thumbnail(lyrics_db, {
                'title': 'Sample Song',
                'content': 'Lyrics of the song'
            }, os.path.join('images', 'example.png'), 'lyrics')

            logger.info("Entry with thumbnail created successfully")

    except ValueError as e:
        logger.error("A ValueError occurred: %s", str(e))
    except FileNotFoundError as e:
        logger.error("FileNotFoundError: %s", str(e))
    except Exception as e:
        logger.error("An unexpected error occurred: %s", str(e))

if __name__ == '__main__':
    main()
