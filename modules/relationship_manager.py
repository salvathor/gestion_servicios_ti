# modules/relationship_manager.py

class RelationshipManager:
  def __init__(self):
    self.relationships = []
  
  def add_feedback(self, client_id, feedback):
    self.relationships.append({
        'client_id': client_id,
        'feedback': feedback,
        'status': 'Reviewed'
    })
    
    print(f"Feedback del cliente {client_id} registrado.")
    
  def handle_complaint(self, client_id, complaint):
    self.relationships.append({
      'client_id': client_id,
      'complaint': complaint,
      'status': 'Resolved'
    })
    
    print(f"Queja del cliente {client_id} resuelta.")







