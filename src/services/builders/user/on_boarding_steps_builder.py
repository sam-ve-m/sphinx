class OnBoardingStepBuilder:
    def __init__(self):
        self.__on_boarding_steps: dict = {
            "current_on_boarding_step": "suitability_step",
            "suitability_step": False,
            "user_identifier_data_step": False,
            "user_self_step": False,
            "user_complementary_step": False,
            "user_quiz_step": False,
            "finished": False,
        }

    def user_suitability_step(self, user_suitability_profile):
        if user_suitability_profile is not None:
            self.__on_boarding_steps["suitability_step"] = True
            self.__on_boarding_steps[
                "current_on_boarding_step"
            ] = "user_identifier_data_step"

        return self

    def user_identifier_step(self, current_user: dict):
        user_cpf = current_user.get("cpf")
        user_cel_phone = current_user.get("cel_phone")
        if user_cpf is not None and user_cel_phone is not None:
            self.__on_boarding_steps["user_identifier_data_step"] = True
            self.__on_boarding_steps["current_on_boarding_step"] = "user_self_step"

        return self

    def user_self_step(self, user_file_exists: bool):
        if user_file_exists:
            self.__on_boarding_steps["user_self_step"] = user_file_exists
            self.__on_boarding_steps["current_on_boarding_step"] = "user_complementary_step"

        return self

    def user_complementary_step(self, current_user):
        marital = current_user.get("marital")
        is_us_person = current_user.get("is_us_person")

        if marital is not None and (is_us_person is False or is_us_person is not None):
            self.__on_boarding_steps["user_complementary_step"] = True
            self.__on_boarding_steps["current_on_boarding_step"] = "user_quiz_step"

        return self

    def user_quiz_step(self, current_user):
        has_stone_age_contract_uuid = current_user.get("is_dtvm_user_client")

        if has_stone_age_contract_uuid is not None:
            self.__on_boarding_steps["user_quiz_step"] = True
            self.__on_boarding_steps["current_on_boarding_step"] = "finished"
            self.__on_boarding_steps["finished"] = True

        return self

    def build(self) -> dict:
        on_boarding_steps = self.__on_boarding_steps
        return on_boarding_steps
