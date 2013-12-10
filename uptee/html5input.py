from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Input


class Html5EmailInput(Input):
    input_type = 'email'


class Html5NumberInput(Input):
    input_type = 'number'


class Html5SelectDateWidget(SelectDateWidget):

    def create_select(self, name, field, value, val, choices):
        select_html = super(Html5SelectDateWidget, self).create_select(name, field, value, val, choices)
        return '<div class="styled-select {0}">{1}</div>'.format(field % name, select_html)
