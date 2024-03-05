from aiohttp import web
import json
from datetime import datetime

# Хранилище объявлений
ads = {}

# Счетчик для ID объявлений
ads_counter = 1

async def handle_ad(request):
    global ads_counter
    if request.method == 'POST':
        # Создание объявления
        ad_data = await request.json()
        ad_id = ads_counter
        ads_counter += 1
        ads[ad_id] = {
            'title': ad_data.get('title'),
            'description': ad_data.get('description'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'owner': ad_data.get('owner')
        }
        return web.json_response({'id': ad_id}, status=201)

    elif request.method == 'GET':
        # Получение списка объявлений
        ad_id = request.query.get('id')
        if ad_id:
            ad_id = int(ad_id)
            ad = ads.get(ad_id)
            if ad:
                return web.json_response(ad, status=200)
            else:
                return web.json_response({'error': 'Ad not found'}, status=404)
        else:
            return web.json_response(list(ads.values()), status=200)

    elif request.method == 'DELETE':
        # Удаление объявления
        ad_id = request.query.get('id')
        if ad_id:
            ad_id = int(ad_id)
            if ad_id in ads:
                del ads[ad_id]
                return web.json_response({'success': 'Ad deleted'}, status=200)
            else:
                return web.json_response({'error': 'Ad not found'}, status=404)

app = web.Application()
app.add_routes([web.route('*', '/ad', handle_ad)])

if __name__ == '__main__':
    web.run_app(app, port=8080)
