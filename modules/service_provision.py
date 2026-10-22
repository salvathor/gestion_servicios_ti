class ServiceProvision:
    def __init__(self):
        self.services = []

    def create_service(self,name,resources,sla):
        service = {
            'name':name,
            'resources':resources,
            'sla':sla,
            'status':'Active'
        }
        self.services.append(service)
        print(f"Servicio '{name}' creado exitosamente.")

    def update_service(self,name,resources=None,sla=None):
        for service in self.services:
            if service['name'] == name:
                if resources is not None:
                    service["resources"] = resources

                if sla is not None:
                    service["sla"] = sla

                print(f"Servicio '{name}' actualizado.")
                return
        print("Servicio no encontrado.")
