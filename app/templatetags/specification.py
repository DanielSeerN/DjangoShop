from django import template
from django.utils.safestring import mark_safe

register = template.Library()

TABLE_HEAD = '''
<table class="table">
  <tbody>
'''
TABLE_END = '''</tbody>
</table>'''
TABLE_CONTENT = ''' <tr>

                  <td>{name}</td>
                  <td>{value}</td>
    </tr>'''
PRODUCT_SPECIFICATION = {
    'photocamera': {
        'Модель': 'version',
        'Тип матрицы': 'type_of_matrix',
        'Мегапиксели': 'megapixels'

    }
}


def get_content(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPECIFICATION[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_specification(product):
    model_name = product.__class__._meta.model_name
    return (TABLE_HEAD + get_content(product, model_name) + TABLE_END)
