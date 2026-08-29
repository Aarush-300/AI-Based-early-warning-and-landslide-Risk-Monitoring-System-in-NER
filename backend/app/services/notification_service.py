from datetime import datetime

# In-memory history for mock purposes
_notification_history = []

class NotificationProvider:
    def send(self, recipient, message, alert=None):
        raise NotImplementedError()

class MockSMSProvider(NotificationProvider):
    def send(self, recipient, message, alert=None):
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "provider": "SMS",
            "recipient": recipient,
            "message": message,
            "alert_id": alert.id if alert else None
        }
        _notification_history.append(record)
        print(f"[MockSMS] Sending to {recipient}: {message}")

class MockEmailProvider(NotificationProvider):
    def send(self, recipient, message, alert=None):
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "provider": "Email",
            "recipient": recipient,
            "message": message,
            "alert_id": alert.id if alert else None
        }
        _notification_history.append(record)
        print(f"[MockEmail] Sending to {recipient}: {message}")

class MockPushProvider(NotificationProvider):
    def send(self, recipient, message, alert=None):
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "provider": "Push",
            "recipient": recipient,
            "message": message,
            "alert_id": alert.id if alert else None
        }
        _notification_history.append(record)
        print(f"[MockPush] Sending to {recipient}: {message}")

class NotificationService:
    def __init__(self):
        self.sms_provider = MockSMSProvider()
        self.email_provider = MockEmailProvider()
        self.push_provider = MockPushProvider()
        
    def notify_alert(self, alert, recipients):
        """
        Send notifications to a list of recipients based on alert severity.
        recipients: list of User objects
        """
        msg = f"ALERT ({alert.severity}): {alert.title}"
        for user in recipients:
            # Everyone gets push notifications
            self.push_provider.send(user.username, msg, alert)
            
            # Critical alerts get SMS
            if alert.severity == "CRITICAL":
                if hasattr(user, 'phone') and user.phone:
                    self.sms_provider.send(user.phone, msg, alert)
                else:
                    self.sms_provider.send(f"unknown_phone_for_{user.username}", msg, alert)
                    
            # Officials get email for any high+ alert
            if user.role in ["admin", "officer"]:
                self.email_provider.send(f"{user.username}@bhoodrishti.ner", msg, alert)

def get_notification_history():
    return _notification_history
