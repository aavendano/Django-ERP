from django import forms, template
from django.template.loader import render_to_string

register = template.Library()

WIDE_FIELD_HINTS = (
    'description',
    'notes',
    'address',
    'comment',
    'comments',
    'purpose',
    'terms',
    'message',
    'summary',
    'reason',
    'details',
    'content',
    'body',
    'observation',
    'observations',
)


def apply_bootstrap_widget_classes(field):
    """Ensure widgets carry Bootstrap 5 classes without wiping custom ones."""
    widget = field.field.widget
    existing = widget.attrs.get('class', '')
    classes = existing.split()

    if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
        css = 'form-check-input'
    elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
        css = 'form-select'
    elif isinstance(widget, forms.FileInput):
        css = 'form-control'
    else:
        css = 'form-control'

    if css not in classes:
        classes.append(css)
        widget.attrs['class'] = ' '.join(classes).strip()

    return field


def field_column_class(field):
    widget = field.field.widget
    name = field.name.lower()

    if isinstance(widget, forms.Textarea) or any(hint in name for hint in WIDE_FIELD_HINTS):
        return 'col-12'
    if isinstance(widget, forms.CheckboxInput):
        return 'col-md-6'
    return 'col-md-6'


@register.simple_tag
def render_form(form, cancel_url='', submit_label='Save', cancel_label='Cancel'):
    """
    Render a Django form as a Bootstrap grid with shared actions.

    Usage:
        {% load form_tags %}
        {% render_form form cancel_url=cancel_url %}
    """
    fields = []
    for field in form.visible_fields():
        apply_bootstrap_widget_classes(field)
        fields.append({
            'field': field,
            'column_class': field_column_class(field),
            'is_checkbox': isinstance(field.field.widget, forms.CheckboxInput),
        })

    return render_to_string(
        'includes/form_grid.html',
        {
            'form': form,
            'fields': fields,
            'cancel_url': cancel_url,
            'submit_label': submit_label,
            'cancel_label': cancel_label,
        },
    )
