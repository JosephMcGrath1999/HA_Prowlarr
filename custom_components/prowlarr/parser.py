import json

def parse_data(data):
    indexers = []
    parsed = {'data': {}}

    for index, item in enumerate(data):
        indexer = {}
        categories = []

        indexer['name'] = item.get('name', f'Indexer {index+1}')
        indexer['indexerUrls'] = item.get('indexerUrls', '')
        indexer['legacyUrls'] = item.get('legacyUrls', '')
        indexer['added'] = item.get('added', '')
        indexer['baseSettings'] = {}
        for field in item.get('fields', []):
            if field['name'] == 'baseUrl':
                indexer['baseUrl'] = field.get('value', '')
            elif field['name'] == 'vipExpiration':
                indexer['vipExpiration'] = field.get('value', '')
            elif field['name'] == 'baseSettings.queryLimit':
                indexer['baseSettings']['queryLimit'] = field.get('value', '')
            elif field['name'] == 'baseSettings.grabLimit':
                indexer['baseSettings']['grabLimit'] = field.get('value', '')
        capabilities = item.get('capabilities', {})
        for category in capabilities.get('categories', []):
            categories.append(category.get('name', ''))
        indexer['categories'] = categories
        indexers.append(indexer)

    parsed['data'] = indexers
    return parsed