import random
import string

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com"]
    return f"{generate_random_string(8)}@{random.choice(domains)}"

def generate_random_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=12))