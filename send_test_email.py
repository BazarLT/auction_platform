import os
import django
from django.core.mail import send_mail

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction_platform.settings')
django.setup()

def send_test_email():
    try:
        send_mail(
            'Test Subject',
            'This is a test email from Django.',
            'your-email@gmail.com',
            ['recipient-email@example.com'],
            fail_silently=False,
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_test_email()
