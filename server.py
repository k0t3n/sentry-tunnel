import json
from json import JSONDecodeError

from aiohttp import ClientSession, web

SENTRY_HOST = 'sentry.io'


async def main(request):
    data = await request.text()

    try:
        headers, *_ = data.split('\n')
        dsn = json.loads(headers)['dsn']
        project_id = int(dsn.split('/')[-1])
    except (ValueError, JSONDecodeError):
        return web.Response(text="Invalid request", status=400)

    async with ClientSession() as session:
        async with session.post(
                f'https://{SENTRY_HOST}/api/{project_id}/envelope/',
                data=data,
        ) as response:
            response_data = await response.text()

        return web.Response(text=response_data)


app = web.Application()
app.add_routes([web.post('/{param:.*}', main)])
web.run_app(app)
