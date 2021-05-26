from src.repositories.view.repository import ViewRepository
from src.repositories.feature.repository import FeatureRepository
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.utils.genarate_id import generate_id, generate_list
from fastapi import status


class ViewService:

    @staticmethod
    def create(payload: dict, view_repository=ViewRepository()):
        payload = generate_id('name', payload)
        payload = generate_list('features', payload)
        _id = payload.get('_id')
        display_name = payload.get('display_name')
        if (
                (len(_id) < 1 or _id is None) or
                (len(display_name) < 1 or display_name is None)
        ):
            raise BadRequestError('common.invalid_params')
        if view_repository.find_one(payload) is not None:
            raise BadRequestError('common.register_exists')
        if view_repository.insert(payload):
            return {
                'status_code': status.HTTP_201_CREATED,
                'message_key': 'requests.created'
            }
        else:
            raise InternalServerError('common.process_issue')

    @staticmethod
    def update(payload: dict, view_repository=ViewRepository()):
        view_id = payload.get('view_id')
        payload_data = payload.get('model')
        display_name = payload_data.get('display_name')
        if (
                (len(view_id) < 1 or view_id is None) or
                (len(display_name) < 1 or display_name is None)
        ):
            raise BadRequestError('common.invalid_params')
        old = view_repository.find_one({'_id': view_id})
        if old is None:
            raise BadRequestError('common.register_not_exists')
        new = dict(old)
        new['display_name'] = display_name
        if view_repository.update_one(old=old, new=new):
            return {
                'status_code': status.HTTP_200_OK,
                'message_key': 'requests.updated'
            }
        else:
            raise InternalServerError('common.process_issue')

    @staticmethod
    def delete(payload: dict, view_repository=ViewRepository()):
        view_id = payload.get('view_id')
        if len(view_id) < 1 or view_id is None:
            raise BadRequestError('common.invalid_params')
        old = view_repository.find_one({'_id': view_id})
        if old is None:
            raise BadRequestError('common.register_not_exists')
        if view_repository.delete_one({'_id': view_id}):
            return {
                'status_code': status.HTTP_200_OK,
                'message_key': 'requests.deleted'
            }
        else:
            raise InternalServerError('common.process_issue')

    @staticmethod
    def link_feature(payload: dict, view_repository=ViewRepository(), feature_repository=FeatureRepository()):
        view_id = payload.get('view_id')
        feature_id = payload.get('feature_id')
        if (
                len(view_id) < 1 or
                view_id is None or
                len(feature_id) < 1 or
                feature_id is None
        ):
            raise BadRequestError('common.invalid_params')
        old = view_repository.find_one({"_id": view_id})
        if old is None:
            raise BadRequestError('common.register_not_exists')
        if feature_repository.find_one({'_id': feature_id}) is None:
            raise BadRequestError('view.feature_not_exists')
        if feature_id not in old.get('features'):
            new = dict(old)
            new.get('features').append(feature_id)
            if view_repository.update_one(old=old, new=new) is False:
                raise InternalServerError('common.process_issue')
        return {
            'status_code': status.HTTP_200_OK,
            'message_key': 'requests.updated'
        }

    @staticmethod
    def get_view(payload: dict, view_repository=ViewRepository()):
        view_id = payload.get('view_id')
        if len(view_id) < 1 or view_id is None:
            raise BadRequestError('common.invalid_params')
        view = view_repository.find_one({'_id': view_id})
        if view_repository.find_one({'_id': view_id}) is None:
            raise BadRequestError('common.register_not_exists')
        return {
            'status_code': status.HTTP_200_OK,
            'payload': view
        }
