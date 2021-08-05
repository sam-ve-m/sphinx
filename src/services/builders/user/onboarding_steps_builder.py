class OnboardingStepBuilder:
    def __init__(self):
        self.__onboarding_steps: dict = {
            "current_onboarding_step": "suitability_step",
            "suitability_step": False,
            "user_identifier_data_step": False,
            "user_selfie_step": False,
            "user_complementary_step": False,
            "user_quiz_step": False,
            "finished": False,
        }

    def user_suitability_step(self, user_suitability_profile):
        if user_suitability_profile is not None:
            self.__onboarding_steps["suitability_step"] = True
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "user_identifier_data_step"

        return self

    def user_identifier_step(self, current_user: dict):
        user_cpf = current_user.get("cpf")
        user_cel_phone = current_user.get("cel_phone")
        if user_cpf is not None and user_cel_phone is not None:
            self.__onboarding_steps["user_identifier_data_step"] = True
            self.__onboarding_steps["current_onboarding_step"] = "user_selfie_step"

        return self

    def user_selfie_step(self, user_file_exists: bool):
        if user_file_exists:
            self.__onboarding_steps["user_selfie_step"] = user_file_exists
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "user_complementary_step"

        return self

    def user_complementary_step(self, current_user):
        marital = current_user.get("marital")
        is_us_person = current_user.get("is_us_person")

        if marital is not None and (is_us_person is False or is_us_person is not None):
            self.__onboarding_steps["user_complementary_step"] = True
            self.__onboarding_steps["current_onboarding_step"] = "user_quiz_step"

        return self

    def user_quiz_step(self, current_user):
        has_stone_age_contract_uuid = current_user.get("is_dtvm_user_client")

        if has_stone_age_contract_uuid is not None:
            self.__onboarding_steps["user_quiz_step"] = True
            self.__onboarding_steps["current_onboarding_step"] = "finished"
            self.__onboarding_steps["finished"] = True

        return self

    def build(self) -> dict:
        onboarding_steps = self.__onboarding_steps
        return onboarding_steps