from django import template

register = template.Library()

@register.filter(name='star_rating')
def star_rating(value):
    stars = ''.join([
        '<span class="rating glyphicon glyphicon-star" style="color: #ffcc00;"></span>'
        for _ in range(value)])
    return stars