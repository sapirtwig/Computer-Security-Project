# # Email configuration
# smtp_server = "smtp.gmail.com"
# smtp_port = 587
# sender_email = "projectnetworking573@gmail.com"
# sender_password = "tywf tnnf xcew xjnb"
# subject = "Your Recovery Password"

# configuration.py

import env_loader  # Loads .env once per project
from settings import EMAIL_ADDRESS, EMAIL_PASSWORD  # Use central settings

# Email server configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = EMAIL_ADDRESS
sender_password = EMAIL_PASSWORD
subject = "Your Recovery Password"

# Optional: fail early if email config is missing
if not sender_email or not sender_password:
    raise EnvironmentError("Missing EMAIL_ADDRESS or EMAIL_PASSWORD in environment variables.")
