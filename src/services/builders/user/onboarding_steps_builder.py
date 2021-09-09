class OnboardingStepBuilder:
    def __init__(self):
        self.__onboarding_steps: dict = {
            "current_onboarding_step": "suitability_step",
            "suitability_step": False,
            "user_identifier_data_step": False,
            "user_selfie_step": False,
            "user_complementary_step": False,
            "user_quiz_step": False,
            "user_electronic_signature": False,
            "finished": False,
        }
        self.__steps: list = [
            "suitability_step",
            "user_identifier_data_step",
            "user_selfie_step",
            "user_complementary_step",
            "user_quiz_step",
            "user_electronic_signature",
        ]

    def user_suitability_step(self, current_user):
        user_suitability_profile = current_user.get("suitability")
        terms = current_user.get("terms")
        has_signed_refusal_term = terms.get("term_refusal")
        if (
            user_suitability_profile is not None or has_signed_refusal_term is not None
        ) and self.__onboarding_steps["current_onboarding_step"] == "suitability_step":
            self.__onboarding_steps["suitability_step"] = True
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "user_identifier_data_step"

        return self

    def user_identifier_step(self, current_user: dict):
        user_cpf = current_user.get("cpf")
        user_cel_phone = current_user.get("cel_phone")
        if (
            user_cpf is not None
            and user_cel_phone is not None
            and self.__onboarding_steps["current_onboarding_step"]
            == "user_identifier_data_step"
        ):
            self.__onboarding_steps["user_identifier_data_step"] = True
            self.__onboarding_steps["current_onboarding_step"] = "user_selfie_step"

        return self

    def user_selfie_step(self, user_file_exists: bool):
        if (
            user_file_exists
            and self.__onboarding_steps["current_onboarding_step"] == "user_selfie_step"
        ):
            self.__onboarding_steps["user_selfie_step"] = user_file_exists
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "user_complementary_step"

        return self

    def user_complementary_step(self, current_user):
        marital = current_user.get("marital")
        is_us_person = current_user.get("is_us_person")

        if (
            marital is not None
            and (is_us_person is False or is_us_person is not None)
            and self.__onboarding_steps["current_onboarding_step"]
            == "user_complementary_step"
        ):
            self.__onboarding_steps["user_complementary_step"] = True
            self.__onboarding_steps["current_onboarding_step"] = "user_quiz_step"

        return self

    def user_quiz_step(self, current_user):
        register_analyses = current_user.get("register_analyses")
        if (
            register_analyses is not None
            and self.__onboarding_steps["current_onboarding_step"] == "user_quiz_step"
        ):
            self.__onboarding_steps["user_quiz_step"] = True
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "user_electronic_signature"
        return self

    def user_electronic_signature(self, current_user):
        has_electronic_signature = current_user.get("electronic_signature")
        if (
            has_electronic_signature is not None
            and self.__onboarding_steps["current_onboarding_step"]
            == "user_electronic_signature"
        ):
            self.__onboarding_steps["user_electronic_signature"] = True
        return self

    def is_finished(self):
        if all([self.__onboarding_steps[step] for step in self.__steps]):
            self.__onboarding_steps["current_onboarding_step"] = "finished"
            self.__onboarding_steps["finished"] = True

    def build(self) -> dict:
        self.is_finished()
        onboarding_steps = self.__onboarding_steps
        return onboarding_steps
