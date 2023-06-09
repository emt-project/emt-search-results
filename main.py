import typesense
import pandas as pd
import os

os.makedirs("out", exist_ok=True)


client = typesense.Client(
    {
        "api_key": os.environ.get("TYPESENSE_API_KEY"),
        "nodes": [
            {
                "host": os.environ.get("TYPESENSE_HOST"),
                "port": os.environ.get("TYPESENSE_PORT"),
                "protocol": os.environ.get("TYPESENSE_PROTOCOL"),
            }
        ],
        "connection_timeout_seconds": 2,
    }
)

with open("search_terms.txt") as f:
    search_terms = [line.rstrip() for line in f if not line.startswith("#")]
print(search_terms)

for search_term in search_terms:
    print(f"searching for {search_term}")
    page = 1
    per_page = 250
    data = []
    more = True
    while more:
        result = client.collections["emt"].documents.search(
            {
                "q": search_term,
                "query_by": "full_text",
                "per_page": per_page,
                "page": page,
            }
        )
        print(f"found {result['found']} documents for >>{search_term}<<")
        if (result["found"] / (per_page * page)) > 1:
            more = True
            page += 1
        else:
            more = False
        for x in result["hits"]:
            item = {
                "id": x["document"]["id"],
                "match": x["highlight"]["full_text"]["snippet"],
            }
            data.append(item)

        out_file = os.path.join("out", f"{search_term}.csv")
        df = pd.DataFrame(data)
        df.to_csv(out_file, index=False)
print("done")
