from typing import Dict, List, Tuple, Union
from app.cdn.repositories.base import BaseCDNRepository
from app.core.config import BUCKET, CDN_LINK_LIFESPAN

# exceptions
from fastapi import HTTPException

from app.models.private import PresentationMediaCreate

from app.models.private import StructureAllModel
from app.models.private import MaterialAllModel
from app.models.private import AudioImagesAllModel

# parsers
from app.cdn.repositories.parsers import *

import logging

logger = logging.getLogger(__name__)

class PrivateYandexCDNRepository(BaseCDNRepository):

    __KEYS = None
    
    def  __list_objects_raw(self, *, prefix=None, continuation_token=None) -> Dict:
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

    def get_sharing_links_from_keys(self, *, prefix=None, list_of_objects=[], check_key=False) -> Dict:
        '''
        Accept List of Dict with key = Key and value = object key

        Returns Dict:
            {
                object_key_in_cdn: object_sharing_link
            }
        '''
        response = self.get_key_name_pairs(prefix=prefix)

        if not list_of_objects:
            if prefix:
                list_of_objects = filter_prefix(prefix=prefix, content_list=self.__KEYS)
            else:
                list_of_objects = self.__KEYS

        for element in list_of_objects:
            if check_key: 
                if check_key_exists_in_list_of_objects(element['Key'], list_of_objects=self.__KEYS):
                    response[element['Key']] = self.client.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': element['Key']}, ExpiresIn=CDN_LINK_LIFESPAN)
            else:
                response[element['Key']] = self.client.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': element['Key']}, ExpiresIn=CDN_LINK_LIFESPAN)

        return response

    def delete_keys(self, *, list_of_keys) -> Dict:
        """
        Accepts List of Dict with key = Key and value = object key 
        """

        response = self.client.delete_objects(Bucket=BUCKET, Delete={'Objects': list_of_keys})
        self.__KEYS = [key for key in self.__KEYS if key not in list_of_keys]

        return response

    def filter_object_keys(self, *, prefix, list_of_keys=None):
        '''
        Accepts List of Dict with key = Key and value = object key
        Returns filtered by prefix
        '''
        return filter_prefix(prefix=prefix, content_list=self.__KEYS if not list_of_keys else list_of_keys)

    def form_presentation_insert_data(self, *, prefix, fk, image_prefix="img", audio_prefix="mp3") -> Tuple:
        '''
        Accepts prefix, image_prefix, audio_prefix

            prefix - key to folder containing audio and image folders
            image_prefix - image folder name
            audio_prefix - audio folder name

        Returns 
            Tuple of formed data for inserting
            images = List[PresentationMediaCreate]
            audio = List[PresentationMediaCreate]
        '''
        # get all keys for a given prefix
        prefix = prefix if prefix[-1] == '/' else prefix + '/'
        self.get_object_keys(prefix=prefix)

        image_prefix = prefix + image_prefix
        audio_prefix = prefix + audio_prefix

        # in case we got two '/' 
        image_prefix = image_prefix.replace('//', '/')
        audio_prefix = audio_prefix.replace('//', '/')

        image_key_order = self.get_key_order_pairs(prefix=image_prefix)
        audio_key_order = self.get_key_order_pairs(prefix=audio_prefix)

        image = self.get_sharing_links_from_keys(prefix=image_prefix)
        audio = self.get_sharing_links_from_keys(prefix=audio_prefix)

        images = []
        for key, value in image.items():
            try:
                images.append(PresentationMediaCreate(order=image_key_order[key], url=value, fk=fk, key=key))
            except:
                pass

        audios = []
        for key, value in audio.items():
            try:
                audios.append(PresentationMediaCreate(order=audio_key_order[key], url=value, fk=fk, key=key))
            except:
                pass

        if not images:
            raise HTTPException(status_code=404, detail=f"No images found a path {prefix}. Images must be present!")

        return (images, audios)

    def form_book_insert_data(self, *, prefix) -> Tuple:
        """
        Accepts prefix at which our book is located
        """
        return self.__form_video_or_book(prefix=prefix, content_type='book')
        

    def form_video_insert_data(self, *, prefix) -> Tuple:
        """
        Accepts prefix at which our book is located
        """
        return self.__form_video_or_book(prefix=prefix, content_type='video')


    def __form_video_or_book(self, *, prefix, content_type: Union['video', 'book']) -> Tuple:
        '''
        Accepts prefix at which our book | video is located
        if multiple files choses last listed
        if files with unsuported format (suported formats listed in suported_formats) delets them
        if no valid key is found returns 404
        '''
        if content_type == 'video':
            suported_formats = ['mp4']
        elif content_type == 'book':
            suported_formats = ['pdf']

        prefix = prefix if prefix[-1] == '/' else prefix + '/'

        links = self.get_sharing_links_from_keys(prefix=prefix)

        keys_for_deletion = []

        material_key = None
        for key, value in links.items():
            keys_for_deletion.append({"Key":key})
            if key.split('/')[-1].split('.')[1] in suported_formats:
                material_key = key
                material_url = value

        if material_key:
            keys_for_deletion.remove({"Key": material_key})

        self.delete_keys(list_of_keys=keys_for_deletion)

        if not material_key:
            raise HTTPException(status_code=404, detail=f"No valid keys found for prefix {prefix}")

        return (material_key, material_url)

    def get_background_url(self, *, key, remove_extra=False) -> str:
        '''
        Accepts key to object of type (suported_formats)

        remove_extra: False | True -> If set to true, this will remove all files from a folder
        that do not equal to key parameter. NOTE: If u set remove_extra to True and you indicate wrong key
        this will remove the wanted key from folder
        '''
        suported_formats = ['jpg']
        if key.split('/')[-1].split('.')[-1] not in suported_formats:
            raise HTTPException(status_code=400, detail=f"Please specify key to file with one of the suported formats '{' ,'.join(suported_formats)}'")

        folder_prefix = key.replace(key.split('/')[-1], '')

        if remove_extra: 
            content_list = self.get_object_keys(prefix=key.split('/')[0], update=True)
            to_be_removed = list_root_directory_files(prefix=folder_prefix, content_list=content_list, exclude_files=[key])
            self.delete_keys(list_of_keys=to_be_removed)        

        link = self.get_sharing_links_from_keys(list_of_objects=[{"Key": key}], check_key=True)

        try:
            return link[key]
        except KeyError:
            raise HTTPException(status_code=404, detail="Background key error. Check your post data, and cdn! We didn't find any data in cdn for a given key")

    def delete_folder_by_inner_key(self, *, key) -> None:
        # get folder prefix from key
        prefix = get_prefix_by_inner_key(key=key)
        self.delete_folder(prefix=prefix)
    
    def delete_folder(self, *, prefix) -> None:
        # list all objects with prefix
        list_ = self.get_object_keys(prefix=prefix)
        # delete all listed objects
        self.delete_keys(list_of_keys=list_)

    def compare(self, *, db_list_of_keys, cdn_list_of_keys) -> None:
        """
        Accepts list of Dict with key = 'Key' and value = object_key
        to be compared against self.__KEYS

        Returns tuple (checked, extra_list, extra_cdn)

        checked - keys present in both list and self.__KEYS
        extra_list - keys present in list but not in self.__KEYS
        extra_cdn - keys present in self.__KEYS but not list
        """

        checked = []
        extra_list = []
        extra_cdn = []

        for key_object in cdn_list_of_keys:
            if key_object in db_list_of_keys:
                checked.append(key_object)
                db_list_of_keys.remove(key_object)
            elif key_object in checked:
                pass
            else:
                extra_cdn.append(key_object)

        extra_list = db_list_of_keys

        # filter out folders

        return (checked, extra_list, extra_cdn)

    def create_key_list_from_lists_of_objects(
        self, 
        *,
        grades: List[StructureAllModel],
        subjects: List[StructureAllModel],
        branches: List[StructureAllModel],
        lectures: List[StructureAllModel],
        theory: List[MaterialAllModel],
        practice: List[MaterialAllModel],
        theory_images: List[AudioImagesAllModel],
        theory_audio: List[AudioImagesAllModel],
        practice_images: List[AudioImagesAllModel],
        practice_audio: List[AudioImagesAllModel],
        ) -> None:

        keys = []
        keys.extend(structure_keys_from_list_of_objects(grades))
        keys.extend(structure_keys_from_list_of_objects(subjects))
        keys.extend(structure_keys_from_list_of_objects(lectures))

        keys.extend(material_keys_from_list_of_objects(theory))
        keys.extend(material_keys_from_list_of_objects(practice))

        keys.extend(audio_images_keys_from_list_of_objects(theory_images))
        keys.extend(audio_images_keys_from_list_of_objects(theory_audio))
        keys.extend(audio_images_keys_from_list_of_objects(practice_images))
        keys.extend(audio_images_keys_from_list_of_objects(practice_audio))

        return keys