from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        # Define los campos que aparecerán en el formulario
        fields = ['nombre', 'apellido', 'numero_documento', 'e_mail', 'telefono', 'direccion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()  # Instancia del helper para crispy forms
        self.helper.layout = Layout(
            # Define el orden y disposición de los campos en el formulario
            Field('nombre'),
            Field('apellido'),
            Field('numero_documento'),
            Field('e_mail'),
            Field('telefono'),
            Field('direccion'),
            # Botón de envío con estilo Bootstrap
            Submit('submit', 'Guardar', css_class='btn-success mt-3')
        )