import tkinter as tk
from tkinter import messagebox, ttk

from modules.change_control import ChangeControl
from modules.delivery_certification import DeliveryCertification
from modules.incident_resolution import IncidentResolution
from modules.relationship_manager import RelationshipManager
from modules.service_provision import ServiceProvision


class TestingApp:
    def __init__(self):
        self.services = ServiceProvision()
        self.incidents = IncidentResolution()
        self.changes = ChangeControl()
        self.certifications = DeliveryCertification()
        self.relationships = RelationshipManager()

        self.root = tk.Tk()
        self.root.title("Pruebas de lógica - Gestión de servicios TI")
        self.root.minsize(640, 500)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._build_services_tab()
        self._build_incidents_tab()
        self._build_changes_tab()
        self._build_audits_tab()
        self._build_relationships_tab()

    def _add_entry(self, parent, label):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text=label, width=24).pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        return entry

    def _add_list(self, parent, title):
        ttk.Label(parent, text=title).pack(anchor=tk.W, padx=10, pady=(10, 2))
        items = tk.Listbox(parent, height=7, exportselection=False)
        items.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        return items

    @staticmethod
    def _show_records(widget, records, formatter):
        widget.delete(0, tk.END)
        for record in records:
            widget.insert(tk.END, formatter(record))

    @staticmethod
    def _selected_index(widget):
        selection = widget.curselection()
        return selection[0] if selection else None

    def _build_services_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Servicios")

        self.service_name = self._add_entry(tab, "Nombre del servicio")
        self.service_resources = self._add_entry(tab, "Recursos")
        self.service_sla = self._add_entry(tab, "SLA")

        buttons = ttk.Frame(tab)
        buttons.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(
            buttons, text="Crear servicio", command=self._create_service
        ).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(
            buttons,
            text="Actualizar servicio seleccionado",
            command=self._update_service,
        ).pack(side=tk.LEFT)

        self.service_list = self._add_list(tab, "Servicios registrados")
        self.service_list.bind("<<ListboxSelect>>", self._load_service)

    def _create_service(self):
        name = self.service_name.get().strip()
        if not name:
            messagebox.showerror("Dato requerido", "Ingresa el nombre del servicio.")
            return

        self.services.create_service(
            name,
            self.service_resources.get().strip(),
            self.service_sla.get().strip(),
        )
        self._refresh_services()

    def _load_service(self, _event):
        if _event.widget is not self.service_list:
            return

        index = self._selected_index(self.service_list)
        if index is None:
            return

        service = self.services.services[index]
        self.service_name.delete(0, tk.END)
        self.service_name.insert(0, service["name"])
        self.service_resources.delete(0, tk.END)
        self.service_resources.insert(0, service["resources"])
        self.service_sla.delete(0, tk.END)
        self.service_sla.insert(0, service["sla"])

    def _update_service(self):
        index = self._selected_index(self.service_list)
        if index is None:
            messagebox.showerror(
                "Servicio no seleccionado",
                "Selecciona un servicio de la lista para actualizarlo.",
            )
            return

        service = self.services.services[index]
        self.services.update_service(
            service["name"],
            resources=self.service_resources.get().strip(),
            sla=self.service_sla.get().strip(),
        )
        self._refresh_services()
        self.service_list.selection_set(index)

    def _refresh_services(self):
        self._show_records(
            self.service_list,
            self.services.services,
            lambda item: (
                f"{item['name']} | Recursos: {item['resources']} | "
                f"SLA: {item['sla']} | Estado: {item['status']}"
            ),
        )

    def _build_incidents_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Incidentes")

        self.incident_description = self._add_entry(tab, "Descripción")
        ttk.Button(
            tab, text="Reportar incidente", command=self._report_incident
        ).pack(anchor=tk.W, padx=10, pady=5)
        self.incident_list = self._add_list(tab, "Incidentes registrados")
        ttk.Button(
            tab,
            text="Resolver incidente seleccionado",
            command=self._resolve_incident,
        ).pack(anchor=tk.W, padx=10, pady=5)

    def _report_incident(self):
        description = self.incident_description.get().strip()
        if not description:
            messagebox.showerror("Dato requerido", "Ingresa la descripción del incidente.")
            return

        self.incidents.report_incident(description)
        self._show_records(
            self.incident_list,
            self.incidents.incidents,
            lambda item: f"{item['description']} | Estado: {item['status']}",
        )

    def _resolve_incident(self):
        index = self._selected_index(self.incident_list)
        if index is None:
            messagebox.showerror(
                "Incidente no seleccionado",
                "Selecciona un incidente de la lista para resolverlo.",
            )
            return

        self.incidents.resolve_incident(index)
        self._show_records(
            self.incident_list,
            self.incidents.incidents,
            lambda item: f"{item['description']} | Estado: {item['status']}",
        )
        self.incident_list.selection_set(index)

    def _build_changes_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Cambios")

        self.change_service = self._add_entry(tab, "ID o nombre del servicio")
        self.change_details = self._add_entry(tab, "Detalles del cambio")
        ttk.Button(
            tab, text="Solicitar cambio", command=self._request_change
        ).pack(anchor=tk.W, padx=10, pady=5)
        self.change_list = self._add_list(tab, "Cambios registrados")
        ttk.Button(
            tab,
            text="Aprobar cambio seleccionado",
            command=self._approve_change,
        ).pack(anchor=tk.W, padx=10, pady=5)

    def _request_change(self):
        service_id = self.change_service.get().strip()
        details = self.change_details.get().strip()
        if not service_id or not details:
            messagebox.showerror(
                "Datos requeridos",
                "Ingresa el ID o nombre del servicio y los detalles del cambio.",
            )
            return

        self.changes.request_change(service_id, details)
        self._show_records(
            self.change_list,
            self.changes.changes,
            lambda item: (
                f"{item['service_id']} | {item['details']} | Estado: {item['status']}"
            ),
        )

    def _approve_change(self):
        index = self._selected_index(self.change_list)
        if index is None:
            messagebox.showerror(
                "Cambio no seleccionado",
                "Selecciona un cambio de la lista para aprobarlo.",
            )
            return

        self.changes.approve_change(index)
        self._show_records(
            self.change_list,
            self.changes.changes,
            lambda item: (
                f"{item['service_id']} | {item['details']} | Estado: {item['status']}"
            ),
        )
        self.change_list.selection_set(index)

    def _build_audits_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Auditorías")

        self.audit_service = self._add_entry(tab, "ID o nombre del servicio")
        ttk.Button(
            tab, text="Realizar auditoría", command=self._perform_audit
        ).pack(anchor=tk.W, padx=10, pady=5)
        self.audit_list = self._add_list(tab, "Auditorías realizadas")

    def _perform_audit(self):
        service_id = self.audit_service.get().strip()
        if not service_id:
            messagebox.showerror(
                "Dato requerido", "Ingresa el ID o nombre del servicio."
            )
            return

        self.certifications.perform_audit(service_id)
        self._show_records(
            self.audit_list,
            self.certifications.audits,
            lambda item: (
                f"{item['service_id']} | Resultado: {item['result']} | {item['notes']}"
            ),
        )

    def _build_relationships_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Relación con clientes")

        self.client_id = self._add_entry(tab, "ID del cliente")
        self.feedback = self._add_entry(tab, "Feedback")
        self.complaint = self._add_entry(tab, "Queja")

        buttons = ttk.Frame(tab)
        buttons.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(
            buttons, text="Registrar feedback", command=self._add_feedback
        ).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(
            buttons, text="Registrar queja", command=self._handle_complaint
        ).pack(side=tk.LEFT)
        self.relationship_list = self._add_list(tab, "Registros de clientes")

    def _add_feedback(self):
        client_id = self.client_id.get().strip()
        feedback = self.feedback.get().strip()
        if not client_id or not feedback:
            messagebox.showerror(
                "Datos requeridos", "Ingresa el ID del cliente y el feedback."
            )
            return

        self.relationships.add_feedback(client_id, feedback)
        self._refresh_relationships()

    def _handle_complaint(self):
        client_id = self.client_id.get().strip()
        complaint = self.complaint.get().strip()
        if not client_id or not complaint:
            messagebox.showerror(
                "Datos requeridos", "Ingresa el ID del cliente y la queja."
            )
            return

        self.relationships.handle_complaint(client_id, complaint)
        self._refresh_relationships()

    def _refresh_relationships(self):
        self._show_records(
            self.relationship_list,
            self.relationships.relationships,
            lambda item: (
                f"Cliente: {item['client_id']} | "
                f"{'Feedback: ' + item['feedback'] if 'feedback' in item else 'Queja: ' + item['complaint']} "
                f"| Estado: {item['status']}"
            ),
        )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    TestingApp().run()
