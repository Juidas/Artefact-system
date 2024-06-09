import argparse
import logging
from tinydb import TinyDB
import crud

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='app.log')
logger = logging.getLogger(__name__)

# Paths
DATA_PATH = 'data/'
lyrics_db = TinyDB(f"{DATA_PATH}lyrics.json")

def create_artefact(args):
    """
    Create a new artefact.

    Args:
        args (argparse.Namespace): Command-line arguments containing title, content, user, and role.
    """
    artefact = {
        'title': args.title,
        'content': args.content
    }
    artefact_id = crud.create_artefact(lyrics_db, artefact, args.user, args.role)
    logger.info("Created artefact with ID: %d", artefact_id)

def read_artefacts(args):
    """
    Read all artefacts.

    Args:
        args (argparse.Namespace): Command-line arguments containing user and role.
    """
    artefacts = crud.read_artefacts(lyrics_db, args.user, args.role)
    for artefact in artefacts:
        print(artefact)

def update_artefact(args):
    """
    Update an existing artefact.

    Args:
        args (argparse.Namespace): Command-line arguments containing artefact ID, title, content, user, and role.
    """
    updated_artefact = {
        'title': args.title,
        'content': args.content
    }
    crud.update_artefact(lyrics_db, args.id, updated_artefact, args.user, args.role)
    logger.info("Updated artefact with ID: %d", args.id)

def delete_artefact(args):
    """
    Delete an artefact.

    Args:
        args (argparse.Namespace): Command-line arguments containing artefact ID, user, and role.
    """
    crud.delete_artefact(lyrics_db, args.id, args.user, args.role)
    logger.info("Deleted artefact with ID: %d", args.id)

def main():
    """
    Main function to handle command-line arguments and execute corresponding functions.
    """
    parser = argparse.ArgumentParser(description="Artefact Management System")
    subparsers = parser.add_subparsers()

    # Create artefact command
    create_parser = subparsers.add_parser('create', help='Create a new artefact')
    create_parser.add_argument('--title', required=True, help='Title of the artefact')
    create_parser.add_argument('--content', required=True, help='Content of the artefact')
    create_parser.add_argument('--user', required=True, help='User creating the artefact')
    create_parser.add_argument('--role', required=True, help='Role of the user creating the artefact')
    create_parser.set_defaults(func=create_artefact)

    # Read artefacts command
    read_parser = subparsers.add_parser('read', help='Read all artefacts')
    read_parser.add_argument('--user', required=True, help='User reading the artefacts')
    read_parser.add_argument('--role', required=True, help='Role of the user reading the artefacts')
    read_parser.set_defaults(func=read_artefacts)

    # Update artefact command
    update_parser = subparsers.add_parser('update', help='Update an existing artefact')
    update_parser.add_argument('--id', type=int, required=True, help='ID of the artefact to update')
    update_parser.add_argument('--title', required=True, help='New title of the artefact')
    update_parser.add_argument('--content', required=True, help='New content of the artefact')
    update_parser.add_argument('--user', required=True, help='User updating the artefact')
    update_parser.add_argument('--role', required=True, help='Role of the user updating the artefact')
    update_parser.set_defaults(func=update_artefact)

    # Delete artefact command
    delete_parser = subparsers.add_parser('delete', help='Delete an artefact')
    delete_parser.add_argument('--id', type=int, required=True, help='ID of the artefact to delete')
    delete_parser.add_argument('--user', required=True, help='User deleting the artefact')
    delete_parser.add_argument('--role', required=True, help='Role of the user deleting the artefact')
    delete_parser.set_defaults(func=delete_artefact)

    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        parser.print_help()
    except Exception as e:
        logger.error("An unexpected error occurred: %s", str(e))

if __name__ == "__main__":
    main()
