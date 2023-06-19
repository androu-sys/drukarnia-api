# drukarnia-api


[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/androu-sys/drukarnia-api/blob/main/LICENSE)

## Overview
`drukarnia-api` is a Python library designed as a wrapper for the ***Drukarnia API***, providing various functionalities for interacting with the Drukarnia platform. It simplifies the process of accessing and manipulating data from the Drukarnia API, enabling users to seamlessly integrate Drukarnia's features into their applications. The library is actively being developed and already includes almost all of the necessary features. We are working diligently to implement the remaining features as quickly as possible.


## Simple Usage
```python
from drukarnia_api import Search


async def get_author_article_titles():
    # Retrieve all results
    authors = await Search().find_author('cupomanka')
    # Get the first search result
    author = authors[0]

    # Collect all data about the user
    await author.collect_data()

    # Get user articles
    articles = await author.articles

    # Print all titles
    for article in articles:
        print(article.title)

    # Close the session (we are still considering the best way to make it seamless)
    await author.close_session()


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_author_article_titles())
```


## Installation
You can install `drukarnia-api` using pip:

```bash
pip install drukarnia-api
```

## Contributing

Contributions to `drukarnia-api` are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on the GitHub repository: https://github.com/androu-sys/drukarnia-api.