from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class BaseFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"  # Método HTTP para enviar el formulario
        self.form_class = "form-horizontal"  # Clase CSS para diseño horizontal
        self.label_class = "col-md-3 col-form-label"  # Clase para etiquetas (3 columnas)
        self.field_class = "col-md-9"  # Clase para campos (9 columnas)
        self.render_required_fields = "True"  # Mostrar campos obligatorios