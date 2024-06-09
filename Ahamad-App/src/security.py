from cryptography.fernet import Fernet

# Generate the encryption key
encryption_key = Fernet.generate_key()

# Save the encryption key to a file
with open('secret.key', 'wb') as key_file:
    key_file.write(encryption_key)

print("Encryption key generated and saved to 'secret.key'")