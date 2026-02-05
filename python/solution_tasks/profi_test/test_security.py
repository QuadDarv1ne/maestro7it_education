from app import create_app
from app.enhanced_security import enhanced_security

app = create_app()

with app.app_context():
    print('Argon2 hash:', enhanced_security.hash_password('test123'))
    print('2FA secret:', enhanced_security.generate_totp_secret())
    print('Security config:', enhanced_security.get_security_config())