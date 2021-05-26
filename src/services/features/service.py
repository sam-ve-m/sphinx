from src.repositories.feature.repository import FeatureRepository
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.utils.genarate_id import generate_id
from fastapi import status


class FeatureService:

    @staticmethod
    def create(payload: dict, feature_repository=FeatureRepository()):
        payload = generate_id('name', payload)
        name = payload.get('name')
        display_name = payload.get('display_name')
        if (
                (len(name) < 1 or name is None) or
                (len(display_name) < 1 or display_name is None)
        ):
            raise BadRequestError('common.invalid_params')
        if feature_repository.find_one(payload) is not None:
            raise BadRequestError('common.register_exists')
        if feature_repository.insert(payload):
            return {
                'status_code': status.HTTP_201_CREATED,
                'message_key': 'requests.created'
            }
        else:
            raise InternalServerError('common.process_issue')

    @staticmethod
    def update(payload: dict, feature_repository=FeatureRepository()):
        feature_id = payload.get('feature_id')
        payload_data = payload.get('model')
        display_name = payload_data.get('display_name')
        if (
                (len(feature_id) < 1 or feature_id is None) or
                (len(display_name) < 1 or display_name is None)
        ):
            raise BadRequestError('common.invalid_params')
        old = feature_repository.find_one({'_id': feature_id})
        if old is None:
            raise BadRequestError('common.register_not_exists')
        new = dict(old)
        new['display_name'] = display_name
        if feature_repository.update_one(old=old, new=new):
            return {
                'status_code': status.HTTP_200_OK,
                "message_key": 'requests.updated'
            }
        else:
            raise InternalServerError('common.process_issue')

    @staticmethod
    def delete(payload: dict, feature_repository=FeatureRepository()):
        feature_id = payload.get('feature_id')
        if len(feature_id) < 1 or feature_id is None:
            raise BadRequestError('common.invalid_params')
        old = feature_repository.find_one({'_id': feature_id})
        if old is None:
            raise BadRequestError('common.register_not_exists')
        if feature_repository.delete_one({'_id': feature_id}):
            return {
                'status_code': status.HTTP_200_OK,
                "message_key": 'requests.deleted'
            }
        else:
            raise InternalServerError('common.process_issue')
