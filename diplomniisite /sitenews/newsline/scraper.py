import vk_api
from .models import Articles
from datetime import datetime

def fetch_articles_from_vk():
    vk_session = vk_api.VkApi(token='vk1.a.nPPCykdbQkeOGx92LoMCW4fR48b31mSc_FA2C7rmwLzu3JvI6dXGKNH5NZYBqaAykJsbCcmIPmuPdwkQPEzAK1B1ZSriFtDl3bkUypJySWBsDSMYVgYXK8og-P9JGo1uqJdNyhwLeRjWUQ5-8lpc2RtZS05r60u2m9GYpiHjRPVJtcosWS8dLFP2KmMGgblxXgUpSeTHHVMsGaA_72IKjg')

    vk_session.auth()

    api = session.get_api()
    # Выполнение запросов к VK API с использованием токена доступа
    response = vk.users.get()

    response = api.wall.get(owner_id='kei_ulstu', count=1)  # Получение одной записи со стены группы
    if response['items']:
        post = response['items'][0]
        text = post['text']
        date = datetime.fromtimestamp(post['date'])

        # Создание экземпляра Articles и сохранение текста статьи
        article = Articles(
            title=post['title'],
            anons=post['anons'],
            text_in_box=text,
            date=date,
            category=None  # Замените на соответствующую категорию статьи
        )
        article.save()
