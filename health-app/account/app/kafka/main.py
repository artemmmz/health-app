from faust import StreamT, Stream

from app.kafka.app import app

token_topic = app.topic('token-topic')
account_topic = app.topic('account-topic')

valid_account_topic = app.topic('valid-account-topic')


@app.agent(token_topic)
async def process_tokens(stream: Stream | StreamT):
    async for record in stream.items():
        print(f'record: {record}')


if __name__ == '__main__':
    app.main()
