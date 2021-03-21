from typing import Dict, List
from app.cdn.repositories.base import BaseCDNRepository
from app.core.config import BUCKET, CDN_LINK_LIFESPAN

# parsers
from app.cdn.repositories.parsers import *

import logging

logger = logging.getLogger(__name__)

class PrivateYandexCDNRepository(BaseCDNRepository):

    __KEYS = None
    
    def __list_objects_raw(self, *, prefix=None, continuation_token=None) -> Dict:
        try:
            if prefix and continuation_token:
                return self.client.list_objects_v2(Bucket=BUCKET, Prefix=prefix, ContinuationToken=continuation_token)
            elif prefix:
                return self.client.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
            elif continuation_token:
                return self.client.list_objects_v2(Bucket=BUCKET, ContinuationToken=continuation_token)
            else:
                return self.client.list_objects_v2(Bucket=BUCKET)

        except Exception as e:
            logger.error("--- LIST BUCKET OBJECTS ERROR ---")
            logger.error(e)
            logger.error("--- LIST BUCKET OBJECTS ERROR ---")

    def __update_keys(self, prefix=None) -> Dict:
        self.__KEYS = []
        # list all objects
        objects = self.__list_objects_raw(prefix=prefix)
        if objects['KeyCount'] != 0:
            self.__KEYS.extend(objects['Contents'])
        else:
            return None
        # if data is truncated continue listing while we don't get all items
        while objects['IsTruncated']:
            objects = self.__list_objects_raw(continuation_token=objects['ContinuationToken'])
            self.__KEYS.extend(objects['Contents'])


    def get_object_keys(self, *, prefix=None, update=False) -> List:
        '''
        Return List od Dict with key = Key and value object key
        '''
        
        if update or not self.__KEYS:
            self.__update_keys(prefix=prefix)
            keys = self.__KEYS
        elif prefix:
            keys = filter_prefix(prefix=prefix, content_list=self.__KEYS)
        else:
            keys = self.__KEYS

        return get_specific_keys_from_content_list(content_list=keys, Key=True)


    def get_key_name_pairs(self, *, prefix=None, update=False) -> List:
        '''
        Return List of Dict with keys = object keys and value = object names
        '''

        if update or not self.__KEYS:
            self.__update_keys(prefix=prefix)
            keys = self.__KEYS
        elif prefix:
            keys = filter_prefix(prefix=prefix, content_list=self.__KEYS)
        else:
            keys = self.__KEYS

        return get_names_from_keys(content_list=keys)

    def get_key_order_pairs(self, *, prefix=None) -> List:
        '''
        Return List of Dict with keys = object keys and value = object order
        To be used with int only
        '''
        if prefix:
            keys = filter_prefix(prefix=prefix, content_list=self.__KEYS)
        else:
            keys = self.__KEYS

        (order_nums, deletion) = get_order_from_keys(content_list=keys)

        self.delete_keys(list_of_keys=deletion)

        return order_nums

    def get_sharing_links_from_keys(self, *, prefix=None) -> Dict:
        '''
        Accept List of Dict with key = Key and value = object key

        Returns Dict:
            {
                object_key_in_cdn: object_sharing_link
            }
        '''
        response = self.get_key_name_pairs(prefix=prefix)

        if prefix:
            list_of_objects = filter_prefix(prefix=prefix, content_list=self.__KEYS)
        else:
            list_of_objects = self.__KEYS

        for element in list_of_objects:
            response[element['Key']] = self.client.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': element['Key']}, ExpiresIn=CDN_LINK_LIFESPAN)

        return response

    def delete_keys(self, *, list_of_keys) -> Dict:
        '''
        Accepts List of Dict with key = Key and value = object key 
        '''

        response = self.client.delete_objects(Bucket=BUCKET, Delete={'Objects': list_of_keys})
        self.__KEYS = [key for key in self.__KEYS if key not in list_of_keys]

        return response

    def filter_object_keys(self, *, prefix, list_of_keys=None):
        '''
        Accepts List of Dict with key = Key and value = object key
        Returns filtered by prefix
        '''
        return filter_prefix(prefix=prefix, content_list=self.__KEYS if not list_of_keys else list_of_keys)