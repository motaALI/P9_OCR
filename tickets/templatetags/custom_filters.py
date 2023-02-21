from django import template

register = template.Library()

@register.filter
def truncateText(text, maxLength):
    if len(text) > maxLength:
        shortText = text[:maxLength] + "..."
        readMoreButton = "<a href='#' class='read-more'>Read More</a>"
        fullText = "<span class='full-text'>" + text + "</span>"
        return shortText + readMoreButton + fullText
    else:
        return text
