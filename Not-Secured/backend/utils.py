import string
import random
import configparser

def generate_random_string(length: int = 12):
    """
    Generate a random string of the specified length.

    :param length: Length of the random string (default is 12).
    :return: A random string consisting of letters and digits.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def is_password_valid(password: str, policy: dict) -> bool:
    """
    Check if the given password complies with the password policy.
    :param password: The password to validate.
    :param policy: A dictionary containing the password policy.
    :return: True if the password is valid, False otherwise.
    """
    # Check length
    if len(password) < policy['PasswordLength']:
        print("Password is too short.")
        return False

    # Check complexity
    complexity = policy['Complexity']
    if 'Uppercase' in complexity and not any(c.isupper() for c in password):
        print("Password must contain an uppercase letter.")
        return False
    if 'Lowercase' in complexity and not any(c.islower() for c in password):
        print("Password must contain a lowercase letter.")
        return False
    if 'Digits' in complexity and not any(c.isdigit() for c in password):
        print("Password must contain a digit.")
        return False
    if 'SpecialCharacters' in complexity and not any(c in "!@#$%^&*()" for c in password):
        print("Password must contain a special character.")
        return False

    # Check dictionary (if enabled)
    if policy['DictionaryCheck']:
        forbidden_words = {"123456", "password", "qwerty"}  # Example of forbidden words
        if password in forbidden_words:
            print("Password is in the forbidden words list.")
            return False

    # If all checks pass
    return True


def load_password_policy(config_path='password_policy.ini'):
    """
    Load the password policy from the configuration file.
    :param config_path: Path to the configuration file.
    :return: A dictionary containing the password policy.
    """
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


def generate_recovery_code():
    """
    Generate a simple recovery code.
    :return: A recovery code consisting of 6 random digits.
    """
    return ''.join(random.choices(string.digits, k=6))
