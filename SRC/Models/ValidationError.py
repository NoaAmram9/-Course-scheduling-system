class ValidationError:
    def __init__(self, message, context=None, severity="error"):
        self.message = message
        self.context = context
        self.severity = severity

    def __str__(self):
        return f"{self.message}"  + (f" [Context: {self.context}]" if self.context else "")
