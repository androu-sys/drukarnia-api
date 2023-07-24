# drukarnia-api


[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/androu-sys/drukarnia-api/blob/main/LICENSE)

## Overview
`drukarnia-api` is a Python library designed as a wrapper for the <a href="https://drukarnia.com.ua">***Drukarnia API***</a>, providing various functionalities for interacting with the platform. It simplifies the process of accessing and manipulating data from the web, enabling users to seamlessly work with Drukarnia. The library is actively being developed and already includes almost all of the necessary features. We are working diligently to implement the remaining features as quickly as possible.


## Simple Usage
```python
from drukarnia_api import Search


async def get_author_article_titles():
    search = Search()
    
    async with search:
        cupomanka, *_ = await search.find_author('cupomanka') 

        # Collect all data about the user
        await cupomanka.collect_data()

        # Get user articles
        articles = await cupomanka.articles

        # Print all titles
        for article in articles:
            print(await article.title)


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_author_article_titles())
```

###### Advance Examples: <a href="https://github.com/androu-sys/drukarnia-api/blob/main/usage.ipynb">usage.ipynb</a>


## Installation
You can install `drukarnia-api` using pip:

```bash
pip install drukarnia-api
```

## Contributing

Contributions to `drukarnia-api` are welcome! If you find any issues or have suggestions for improvement, please <a href="https://github.com/androu-sys/drukarnia-api/issues/new">open an issue</a> or <a href="https://t.me/U1F615">contact me</a>.