# modules/change_control.py

class ChangeControl:
    def __init__(self):
        self.changes = []

    def request_change(self, service_id, change_details):
        change = {
            'service_id': service_id,
            'details': change_details,
            'status': 'Pending Approval'
        }
        self.changes.append(change)
        print("Solicitud de cambio registrada.")
        

    def approve_change(self, index): 
        if index < len(self.changes):
            self.changes[index] ['status'] = 'Approved'
            print("Cambio aprobado.")
        
        else:
            print("Indice de cambio no válido.")