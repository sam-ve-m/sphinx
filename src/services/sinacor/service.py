# SPHINX
from src.repositories.client_register.repository import ClientRegisterRepository
from src.repositories.user.repository import UserRepository
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.services.persephone.service import PersephoneService
from src.utils.persephone_templates import get_table_response_template_with_data
from src.utils.stone_age import StoneAge
from src.utils.base_model_normalizer import normalize_enum_types


class SinacorService:
    @staticmethod
    def process_callback(
        payload: dict,
        client_register_repository=ClientRegisterRepository(),
        user_repository=UserRepository(),
        persephone_client=PersephoneService.get_client(),
    ):
        successful = payload.get("successful")
        error = payload.get("error")
        if successful is False or error is not None:
            raise BadRequestError("bureau.error.fail")
        # TODO: save this on user profile
        uuid = payload.get("uuid")

        # table_result = persephone_client.run(
        #     topic="thebes.sphinx_persephone.topic",
        #     partition=5,
        #     payload=get_user_account_template_with_data(payload=payload),
        #     schema_key="table_schema",
        # )
        # if table_result is False:
        #     raise InternalServerError("common.process_issue")

        output = payload.get("output")
        normalize_enum_types(output)
        output = StoneAge.get_only_values_from_user_data(user_data=output)

        user = user_repository.find_one({"cpf": output["identifier_document"]["document_data"]["number"]})

        # client_register_repository.s

        # return {
        #     "status_code": status.HTTP_200_OK,
        #     "message_key": "ok",
        # }

        normalized_data = StoneAge.get_only_values_from_user_data(user_data=output)
