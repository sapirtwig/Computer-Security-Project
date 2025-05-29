# import hmac
# import hashlib
# import string
# import random
# import configparser

# salt = b'None'  # TODO add from configuration afterwards


# def encrypt_password(password: str):
#     """
#     This function encrypts the password using hmac.
#     :param password: the password to encrypt
#     :return: encrypted password
#     """
#     return hmac.new(salt, password.encode(), hashlib.sha1).hexdigest()


# def generate_random_string(length: int = 12):
#     """
#     Generate a random string of the specified length.

#     :param length: Length of the random string (default is 12).
#     :return: A random string consisting of letters and digits.
#     """
#     characters = string.ascii_letters + string.digits
#     return ''.join(random.choices(characters, k=length))


# def encrypt_with_sha1():
#     """
#     Encrypt a string using SHA-1.
#     :return: The SHA-1 hash of the string in hexadecimal format.
#     """
#     encrypted_string = hashlib.sha1(generate_random_string().encode())
#     return encrypted_string.hexdigest()


# # login with policy password
# def is_password_valid(password: str, policy: dict) -> bool:
#     """
#     Check if the given password complies with the password policy.
#     """
#     # Check length
#     if len(password) < policy['PasswordLength']:
#         print("Password is too short.")
#         return False

#     # Check complexity
#     complexity = policy['Complexity']
#     if 'Uppercase' in complexity and not any(c.isupper() for c in password):
#         print("Password must contain an uppercase letter.")
#         return False
#     if 'Lowercase' in complexity and not any(c.islower() for c in password):
#         print("Password must contain a lowercase letter.")
#         return False
#     if 'Digits' in complexity and not any(c.isdigit() for c in password):
#         print("Password must contain a digit.")
#         return False
#     if 'SpecialCharacters' in complexity and not any(c in "!@#$%^&*()" for c in password):
#         print("Password must contain a special character.")
#         return False

#     # Check dictionary (if enabled)
#     if policy['DictionaryCheck']:
#         forbidden_words = {"123456", "password", "qwerty"}  # Example of forbidden words
#         if password in forbidden_words:
#             print("Password is in the forbidden words list.")
#             return False

#     # If all checks pass
#     return True


# def load_password_policy(config_path='password_policy.ini'):
#     """
#     Load the password policy from the configuration file.
#     """
#     config = configparser.ConfigParser()
#     config.read(config_path)

#     policy = {
#         'PasswordLength': int(config['PasswordPolicy']['PasswordLength']),
#         'Complexity': config['PasswordPolicy']['Complexity'].split(', '),
#         'HistoryLimit': int(config['PasswordPolicy']['HistoryLimit']),
#         'DictionaryCheck': config['PasswordPolicy']['DictionaryCheck'] == 'Enabled',
#         'LoginAttempts': int(config['PasswordPolicy']['LoginAttempts']),
#     }
#     return policy
# utils.py

import hmac
import hashlib
import string
import random
import configparser
import logging
from settings import SALT  # Load salt securely from environment variables

# Configure logging level
logging.basicConfig(level=logging.INFO)

# Securely hash password using SHA-256 and external salt (not hardcoded)
def encrypt_password(password: str) -> str:
    return hmac.new(SALT.encode(), password.encode(), hashlib.sha256).hexdigest()

# Generate a random alphanumeric string (e.g. for recovery codes)
def generate_random_string(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# Validate a password against the loaded policy rules
def is_password_valid(password: str, policy: dict) -> bool:
    if len(password) < policy['PasswordLength']:
        logging.warning("Password too short.")
        return False

    complexity = policy['Complexity']
    if 'Uppercase' in complexity and not any(c.isupper() for c in password):
        logging.warning("Password missing uppercase letter.")
        return False
    if 'Lowercase' in complexity and not any(c.islower() for c in password):
        logging.warning("Password missing lowercase letter.")
        return False
    if 'Digits' in complexity and not any(c.isdigit() for c in password):
        logging.warning("Password missing digit.")
        return False
    if 'SpecialCharacters' in complexity and not any(c in "!@#$%^&*()" for c in password):
        logging.warning("Password missing special character.")
        return False

    if policy['DictionaryCheck']:
        try:
            with open("dictionary.txt", "r") as f:
                forbidden_words = {line.strip().lower() for line in f}
        except FileNotFoundError:
            forbidden_words = {"123456", "password", "qwerty"}  # fallback

        if password.lower() in forbidden_words:
            logging.warning("Password found in dictionary blacklist.")
            return False

    return True

# Load password policy settings from configuration file (INI format)
def load_password_policy(config_path='password_policy.ini') -> dict:
    config = configparser.ConfigParser()
    config.read(config_path)

    policy = {
        'PasswordLength': int(config['PasswordPolicy']['PasswordLength']),
        'Complexity': config['PasswordPolicy']['Complexity'].split(', '),
        'HistoryLimit': int(config['PasswordPolicy']['HistoryLimit']),
        'DictionaryCheck': config['PasswordPolicy']['DictionaryCheck'] == 'Enabled',
        'LoginAttempts': int(config['PasswordPolicy']['LoginAttempts']),
    }
    return policy

