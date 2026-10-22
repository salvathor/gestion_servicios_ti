class IncidentResolution:
  def __init__(self):
    self.incidents = []
  
  def report_incident(self, description):
    incident = {
      'description': description,
      'status': 'Open'
    }
    
    self.incidents.append(incident)
    print("Incidente reportado.")

  def resolve_incident(self, index): 
    if index < len(self.incidents):
      self.incidents[index]['status'] = 'Resolved'
      print("Incidente resuelto.")
    else:
      print("Índice de incidente no válido.")