from django import template

register = template.Library()

@register.filter(name='addAttrs')
def addAttrs(value, arg):
    arg = arg.split(',')
    if len(arg) == 2:
        return value.as_widget(
             attrs={
                    'class' : arg[0],
                    'placeholder' : arg[1]
                }
            )
    elif len(arg) == 1:
        return value.as_widget(
                attrs={
                    'class' :arg[0]
                }
            )

