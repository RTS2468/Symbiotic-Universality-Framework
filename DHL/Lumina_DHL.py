import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# This script requires the PyCryptodome library.
# If you don't have it, you can install it with:
# pip install pycryptodome

# A salt is used to make the key derivation process more secure.
# It should be a unique, randomly generated value for each password.
SALT = b'c\x83\x8f\xc8\xaf\x1cE\xb4\x13\x12Yn\x91\xf8\x0b\xa3'

def derive_keys(password: str):
    """
    Derives two keys from a single password using different hash functions.
    The outer key is derived with a stronger hash (SHA-256) for a 256-bit key.
    The inner key is derived with a less strong hash (SHA-1) for a 128-bit key.
    This demonstrates the concept of a stronger outer layer.
    """
    password_bytes = password.encode('utf-8')
    
    # Outer layer key (256-bit, 32 bytes) derived from SHA-256
    outer_key = hashlib.sha256(SALT + password_bytes).digest()
    
    # Inner layer key (128-bit, 16 bytes) derived from SHA-1
    # Note: SHA-1 is not considered collision-resistant for new applications,
    # but it serves as a good example of a "less strong" hash for this layered
    # encryption demonstration.
    inner_key = hashlib.sha1(SALT + password_bytes).digest()[:16]

    return outer_key, inner_key

def encrypt_file_cascaded(file_path: str, password: str):
    """
    Encrypts a file using a two-layer (cascading) encryption scheme.
    - Layer 1 (inner): AES-128 encryption
    - Layer 2 (outer): AES-256 encryption
    """
    try:
        # Step 1: Read the original file data
        with open(file_path, 'rb') as f:
            original_data = f.read()

        # Step 2: Derive the keys from the password
        outer_key, inner_key = derive_keys(password)
        
        print("Starting two-layer encryption...")

        # Step 3: Inner Layer Encryption (AES-128)
        # Create a cipher for the inner layer
        cipher_inner = AES.new(inner_key, AES.MODE_CBC)
        # Encrypt and pad the original data
        inner_ciphertext = cipher_inner.encrypt(pad(original_data, AES.block_size))
        
        print("Inner layer (AES-128) encryption complete.")
        
        # Step 4: Outer Layer Encryption (AES-256)
        # Create a cipher for the outer layer. We need a new IV for this.
        cipher_outer = AES.new(outer_key, AES.MODE_CBC)
        # Encrypt the inner ciphertext
        outer_ciphertext = cipher_outer.encrypt(pad(inner_ciphertext, AES.block_size))

        print("Outer layer (AES-256) encryption complete.")

        # Step 5: Combine IVs and the final ciphertext and write to a new file
        # The IV for the inner layer must be stored to allow decryption
        encrypted_file_path = f"{file_path}.enc"
        with open(encrypted_file_path, 'wb') as f:
            # We store both IVs for decryption. The order is important.
            f.write(cipher_outer.iv)
            f.write(cipher_inner.iv)
            f.write(outer_ciphertext)
        
        print(f"File successfully encrypted to: {encrypted_file_path}")

    except Exception as e:
        print(f"An error occurred during encryption: {e}")

def decrypt_file_cascaded(encrypted_file_path: str, password: str):
    """
    Decrypts a two-layer encrypted file.
    - This process must be done in reverse order: outer layer first, then inner layer.
    """
    try:
        # Step 1: Read the encrypted file data
        with open(encrypted_file_path, 'rb') as f:
            # Read the IVs first (16 bytes each)
            outer_iv = f.read(16)
            inner_iv = f.read(16)
            encrypted_data = f.read()

        # Step 2: Derive the keys from the password
        outer_key, inner_key = derive_keys(password)

        print("Starting two-layer decryption...")

        # Step 3: Outer Layer Decryption (AES-256)
        # The first key to use is the outer key (AES-256)
        cipher_outer = AES.new(outer_key, AES.MODE_CBC, outer_iv)
        # Decrypt the outermost layer and unpad
        inner_ciphertext = unpad(cipher_outer.decrypt(encrypted_data), AES.block_size)

        print("Outer layer (AES-256) decryption complete.")

        # Step 4: Inner Layer Decryption (AES-128)
        # Now use the inner key (AES-128) and the inner IV
        cipher_inner = AES.new(inner_key, AES.MODE_CBC, inner_iv)
        # Decrypt the inner ciphertext to get the original data
        original_data = unpad(cipher_inner.decrypt(inner_ciphertext), AES.block_size)

        print("Inner layer (AES-128) decryption complete.")

        # Step 5: Save the decrypted file
        original_file_path = encrypted_file_path.replace(".enc", "")
        with open(original_file_path, 'wb') as f:
            f.write(original_data)

        print(f"File successfully decrypted and saved as: {original_file_path}")
        
    except Exception as e:
        print(f"An error occurred during decryption. Check your password: {e}")

if __name__ == "__main__":
    # --- Example Usage ---
    
    # Create a dummy file to encrypt
    dummy_filename = "secret_report.txt"
    with open(dummy_filename, "w") as f:
        f.write("This is a very important and highly confidential report.\n")
        f.write("It must be protected with multiple layers of encryption.")

    user_password = "mySuperSecretPassword123"
    
    # Encrypt the file
    encrypt_file_cascaded(dummy_filename, user_password)
    
    # At this point, the 'secret_report.txt' file is still there and
    # 'secret_report.txt.enc' has been created.
    # For a real-world scenario, you would delete the original file.
    os.remove(dummy_filename)
    
    print("\nOriginal file deleted for security.")

    # Decrypt the file
    encrypted_filename = "secret_report.txt.enc"
    print("\nAttempting to decrypt the file...")
    decrypt_file_cascaded(encrypted_filename, user_password)

    # Clean up the encrypted file after decryption
    # os.remove(encrypted_filename)
