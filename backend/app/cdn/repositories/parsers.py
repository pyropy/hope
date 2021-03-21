from typing import List, Tuple

def get_specific_keys_from_content_list(content_list, **kwargs) -> List:
        '''
            Accept raw list of content
            Return list with only speficic keys
            
            Available keys:
                'Key'
                'LastModified'
                'ETag'
                'Size'
                'StorageClass'
        '''

        object_data = {}
        parsed = []
        for content in content_list:
            for key, value in kwargs.items():
                if value == True:
                    object_data[key] = content[key]
            parsed.append(object_data)
            object_data = {}
    
        return parsed


def get_names_from_keys(content_list) -> List:
    '''
        Accepts
            List of Dicts:
                [{
                    Key: "some/key/here/image.jpg"
                }]

        Returns:
            Dict:
                {
                    "some/key/here/image.jpg" : "image.jpg"
                }
    '''

    parsed = {}
    for content in content_list:
        name = content['Key'].split('/')[-1]
        if '.' in name:
            parsed[content['Key']] = name

    return parsed

def get_order_from_keys(content_list) -> Tuple:
    '''
        Accepts
            List of Dicts:
                [{
                    Key: "some/key/here/0001.jpg"
                }]

        Returns:
            Tuple(
                Dict:
                    {
                        "some/key/here/0001.jpg" : 1
                    }
                List:
                    Dict: 
                        {
                            'Key': "some/key/here/image.jpg"
                        }
            )
    '''

    parsed = {}
    delete = {}
    for_deletion = []
    for content in content_list:
        name = content['Key'].split('/')[-1]
        if '.' in name:
            try:
                parsed[content['Key']] = int(name.split('.')[0])
            except:
                delete['Key'] = content['Key'] 
                for_deletion.append(delete)
                delete = {}

    return (parsed, for_deletion)

def filter_prefix(prefix, content_list, exclude_root=True) -> List:
    '''
    Filters list of elements by prefix

        :params:
            prefix - prefix to filter by
            content_list - list to filter
            exclude_root: True - exclude root directory
    '''
    filtered = []
    prefix = prefix if prefix[-1] == '/' else prefix + '/'
    for content in content_list:
        if prefix in content['Key']:
            if not exclude_root:
                filtered.append(content)
            elif prefix != content['Key']:
                filtered.append(content)

    return filtered
