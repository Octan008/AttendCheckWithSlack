import os

def consts(request):
    return {
        'domain': os.environ.get('SERVER_DOMAIN'),
        'telektlist':"https://telektlist.com"
    }