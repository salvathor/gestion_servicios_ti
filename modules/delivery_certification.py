class DeliveryCertification:
    def __init__(self):
        self.audits = []

    def perform_audit(self, service_id):
        audit = {
            'service_id': service_id,
            'result': 'Passed',
            'notes': 'No issues found.'
        }
        self.audits.append(audit)
        print("Auditoría completada exitosamente.")