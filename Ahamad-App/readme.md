### Description

The Artefact Management System is a comprehensive solution for managing various types of artefacts, including lyrics, music scores, and musical recordings. The system provides functionalities for creating, reading, updating, and deleting artefacts and generating and verifying checksums for data integrity. It supports secure storage through encryption and thumbnail generation for visual artefacts.

### Components & Architecture 
Database Layer (TineyDB, 2023):
TinyDB is the underlying database chosen for its lightweight, document-oriented structure. This allows for easy storage and retrieval of artefact data without a complex database setup.

Security Layer (Cryptography, 2024):
The cryptography library's Fernet module encrypts artefact content, ensuring the data remains confidential and tamper-proof. This is crucial for maintaining the integrity and security of sensitive artefacts.

Processing Layer (Pillow, 2024):
Pillow (PIL) is a powerful library used for image processing, specifically for generating thumbnails. This enhances the visual representation of artefacts, making managing and displaying visual content easier.

Checksum Layer (Python, 2024):
hashlib is utilized for generating and verifying SHA-256 checksums, ensuring the integrity of the artefacts. This layer guarantees that the data has not been altered or corrupted.

Role-Based Access Control (RBAC) Layer:
 The system distinguishes between permissions for regular users and administrators in order to uphold data security and integrity.The system establishes distinct access rights for regular users and administrators to ensure the security and accuracy of the data. This helps maintain control over who can view, modify, or delete sensitive information, thereby safeguarding the integrity of the data.

Logging Layer (Python, 2024):
The logging module is configured to capture detailed logs essential for debugging and monitoring the system. This helps track the operations performed and any issues arising during execution.

### Methodology
The system follows a structured methodology, including:
Requirement Analysis: Understanding the needs for artefact management and security.
Design: Architecting the system with modular components.
Implementation: Developing the system using Python and the chosen libraries.
Testing: Creating comprehensive tests to ensure functionality and integrity.
Documentation: Providing detailed documentation for users and developers.

### Features
Create, Read, Update, Delete (CRUD): Manage artefacts with standard CRUD operations.
Checksum Generation and Verification: Ensure data integrity with SHA-256 checksums.
Encryption: Securely store artefacts with encryption using the Fernet module.
Thumbnail Generation: Automatically create thumbnails for visual artefacts.
Role-Based Access Control: Differentiate permissions between users and administrators.

### Installation
bash
git clone https://github.com/Juidas/Artefact-system.git 
cd <repository_name>
Or unzip the file uploaded to the learning platform.
Create a virtual environment:
python3 -m venv .venv
source .venv/bin/activate
Install the required libraries:
pip install  cryptography tinydb pillow datetime
create a security key
pyton3 src/security.py
Run the application:
python3 src/main.py

###Usage
          Bash
Create a Secret.key to store encryption keys
python3 src/security.py
Create an artefact with an Admin role:
python3 src/main.py create --title "Hey Jude" --content "Hey Jude" --user "admin1" --role "admin"

Read Artefacts
python3 src/main.py read --user "admin1" --role "admin"

Update Artefact with admin role / same ‘created_by’ user:
python3 src/main.py update --id 1 --title "Yesterday" --content "All My Troubles" --user "admin1" --role "admin"


Delete Artefact with admin role /same ‘created_by’ user:
python3 src/main.py delete --id 1 --user “admin” --role "admin"

Create an artefact with the user role:
python3 src/main.py create --title "Yesterday" --content "All My Trouble" --user "user1" --role "user"

read artefacts wrong role
python3 src/main.py read --user "user1" --role "user1"

Read artefacts correct role
python3 src/main.py read --user "user1" --role "user"

Update artefact with user not matching ‘created_by’ 
python3 src/main.py update --id 1 --title "Yesterday" --content "All My Troubles" --user "user2" --role "user"

Update artefact with admin role
python3 src/main.py update --id 1 --title "Tomorrow" --content "All My Troubles" --user "admin1" --role "admin"

Update artefact without passing all args
python3 src/main.py update --id 1 --title “Tomorrow”  --user “user2” --role “user”

Update with the same user equals “created_by” 
python3 src/main.py update --id 1 --title "Tomorrow" --content "All My Troubles" --user "user1" --role "user"

Delete artefact with the user not matching ‘created_by’ 
python3 src/main.py delete --id 1 --user "user2" --role "user"

Delete artefact with the user  matching ‘created_by’ 
python3 src/main.py delete --id 1 --user "user1" --role "user"

### Test Coverage
The project includes a comprehensive suite of unit tests to ensure the system's functionality. To run the tests, use the following command:
bash
PYTHONPATH=src python3 -m unittest discover tests.
The test suite covers:

CRUD Operations: Tests for creating, reading, updating, and deleting artefacts.
Thumbnail Generation: Tests for creating thumbnails for visual artefacts.
Checksum: Tests for generating and verifying checksums.
Role-Based Access Control: Tests for ensuring appropriate permissions for users and administrators.
While the current system is fully functional, several enhancements could be considered.

### For future development:
User Interface: Develop a graphical user interface (GUI) for easier interaction with the system.
Advanced Search: Implement advanced search capabilities, allowing users to search artefacts based on various criteria.
Audit Logs: Maintain a detailed audit log of all operations for better tracking and accountability.
Cloud Integration: Integrate with cloud solutions for scalable and reliable data storage.
Notification System: Implement a notification system to alert users about important events or changes.




Reference: 

Cryptography, 2024.  Welcome to pyca/cryptography. Available at: https://cryptography.io/en/latest/ [Accessed 2 June 2024]

Pillow, 2024. Pillow Available at: https://pillow.readthedocs.io/en/stable/  [Accessed 29 May 2024]

Python, 2024. hashlib — Secure hashes and message digests. Available at: https://docs.python.org/3/library/hashlib.html [Accessed 04 June 2024]

Python, 2024. logging — Logging facility for Python. Available at: https://docs.python.org/3/library/logging.html [Accessed 04 June 2024]

TinyDB, 2023. Welcome to TinyDB!. Available at:  https://tinydb.readthedocs.io/en/latest/ [Accessed 26 May, 2024]



