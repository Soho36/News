from django import template

register = template.Library()

BAD_WORDS = {
    'fuck': 'f**k',
    'fucking': 'f***ng',
    'shit': 's**t',
    'damn': 'd**n',
    # Add more words as needed
}

@register.filter(name='censor_bad_words')
def censor_bad_words(value):
    words = value.split()
    censored_words = [BAD_WORDS.get(word.lower(), word) for word in words]
    return ' '.join(censored_words)
