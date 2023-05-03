import typesense
import os


client = typesense.Client({
    'api_key': os.environ.get('TYPESENSE_API_KEY'),
    'nodes': [{
        'host': os.environ.get('TYPESENSE_HOST'),
        'port': os.environ.get('TYPESENSE_PORT'),
        'protocol': os.environ.get('TYPESENSE_PROTOCOL')
    }],
    'connection_timeout_seconds': 2
})


result = client.collections['emt'].documents.search({
    'q': 'jetzt',
    'query_by': 'full_text',
})
data = []
for x in result["hits"]:
    item = {
        "id": x["document"]["id"],
        "match": x["highlight"]["full_text"]["snippet"]
    }
    data.append(item)

print(data)
