from modules.change_control import ChangeControl
from modules.delivery_certification import DeliveryCertification
from modules.incident_resolution import IncidentResolution
from modules.relationship_manager import RelationshipManager
from modules.service_provision import ServiceProvision
from utils.helpers import display_records, select_record


def main():
    services = ServiceProvision()
    incidents = IncidentResolution()
    changes = ChangeControl()
    certifications = DeliveryCertification()
    relationships = RelationshipManager()

    while True:
        print("\n=== Gestión de servicios TI ===")
        print("1. Crear servicio")
        print("2. Actualizar servicio")
        print("3. Reportar incidente")
        print("4. Resolver incidente")
        print("5. Solicitar cambio")
        print("6. Aprobar cambio")
        print("7. Realizar auditoría de servicio")
        print("8. Registrar feedback de cliente")
        print("9. Registrar queja de cliente")
        print("0. Salir")

        option = input("Selecciona una opción: ").strip()

        if option == "1":
            name = input("Nombre del servicio: ").strip()
            resources = input("Recursos del servicio: ").strip()
            sla = input("SLA del servicio: ").strip()
            services.create_service(name, resources, sla)
        elif option == "2":
            if not services.services:
                print("No hay servicios registrados; no se puede actualizar.")
                continue
            index = select_record(services.services, "servicio")
            if index is not None:
                service = services.services[index]
                resources = input("Nuevos recursos (Enter para conservar): ").strip()
                sla = input("Nuevo SLA (Enter para conservar): ").strip()
                services.update_service(
                    service["name"],
                    resources=resources or None,
                    sla=sla or None,
                )
        elif option == "3":
            description = input("Descripción del incidente: ").strip()
            incidents.report_incident(description)
        elif option == "4":
            index = select_record(incidents.incidents, "incidente")
            if index is not None:
                incidents.resolve_incident(index)
        elif option == "5":
            service_name = input("Nombre del servicio: ").strip()
            if not any(service["name"] == service_name for service in services.services):
                print(f"No existe el servicio '{service_name}'; no se registró el cambio.")
                continue
            details = input("Detalles del cambio: ").strip()
            changes.request_change(service_name, details)
        elif option == "6":
            index = select_record(changes.changes, "cambio")
            if index is not None:
                changes.approve_change(index)
        elif option == "7":
            service_name = input("Nombre del servicio que se auditará: ").strip()
            if not any(service["name"] == service_name for service in services.services):
                print(f"No existe el servicio '{service_name}'; no se realizó la auditoría.")
                continue
            certifications.perform_audit(service_name)
            display_records(certifications.audits, "Auditorías en memoria")
        elif option == "8":
            client_id = input("ID del cliente: ").strip()
            feedback = input("Feedback del cliente: ").strip()
            relationships.add_feedback(client_id, feedback)
            display_records(relationships.relationships, "Feedback y quejas en memoria")
        elif option == "9":
            client_id = input("ID del cliente: ").strip()
            complaint = input("Descripción de la queja: ").strip()
            relationships.handle_complaint(client_id, complaint)
            display_records(relationships.relationships, "Feedback y quejas en memoria")
        elif option == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()