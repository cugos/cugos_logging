# custom_filters.py
# Some custom filters for dictionary lookup.
from django.template.defaultfilters import register

@register.filter(name='hashlookup')
def hashlookup(dict, index):
    if index in dict:
        return dict[index]
    return ''

@register.filter(name='nestedhashlookup')
def nestedhashlookup(dict, args):
    if args is None:
        return ''
    arg_list = [arg.strip() for arg in args.split(',')]
    if len(arg_list) == 2:
        if arg_list[0] in dict:
            return dict[arg_list[0]][arg_list[1]]
    return ''


@register.filter(name='hashdelete')
def hashdelete(dict, index):
    if index in dict:
        del dict[index]
    return ''

