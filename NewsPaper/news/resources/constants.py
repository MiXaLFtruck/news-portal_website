from pathlib import Path
from project_files.settings import BASE_DIR


article = 'AR'
news = 'NW'

OPTIONS = [
    (article, 'статья'),
    (news, 'новость')
]


p = Path(BASE_DIR, 'news', 'resources', 'censor_list.txt')

with open(p) as f:
    a = f.read()
    CENS_CORE = a.split(', ')
