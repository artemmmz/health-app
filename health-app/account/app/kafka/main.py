from faust import App, Record, StreamT

from app.core.settings import settings

app = App('health-app-accounts', broker=settings.KAFKA_BROKER)

accounts_topic = app.topic('ms-accounts')


@app.agent(accounts_topic)
async def introspection_token(stream: StreamT):
    async for record in await stream.items():
        print(f'record: {record}')


if __name__ == '__main__':
    app.main()
