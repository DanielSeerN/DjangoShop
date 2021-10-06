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
    },
    'tv': {
        'Диагональ': 'diagonal',
        'Разрешение': 'resolution',
        'Яркость': 'brightness'
    },
    'washingmachine': {
        'Версия': 'version',
        'Тип': 'type_of_machine',
        'Вес': 'weight'
    },
    'conditioner': {
        'Версия': 'version',
        'Тип': 'type_of_conditioner',
        'Вес': 'weight',
        'Фильтры': 'filters'
    },
    'videogameconsole': {
        'Поддержка 4к': 'four_k_support',
        'Объём SSD': 'SSD',
        'Гарантия': 'warranty'
    },
    'lawnmover': {
        'Режущая система': 'cutting_system',
        'Момент вращения': 'rotational_moment',
        'Мощность двигателя': 'engine_capacity'
    },
    'smartphone': {
        'Операционная система': 'os',
        'Диагональ': 'diagonal',
        'Процессор': 'processor',
        'Оперативная память': 'ram'
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
    return mark_safe(TABLE_HEAD + get_content(product, model_name) + TABLE_END)
