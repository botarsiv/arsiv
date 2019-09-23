import uuid
from aiogram.utils.callback_data import CallbackData


POSTS = {
    str(uuid.uuid4()): {
        'title': f'Grup Yönetimi\n',
        'body': '\n@Combot \n@MissRose_bot \n@baymax_en_bot',
    }
}



posts_cb = CallbackData('post','id', 'action')
