from django import template

register = template.Library()


@register.filter(expects_localtime=True)
def tdelta(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return '{:02}:{:02}'.format(hours, minutes)
