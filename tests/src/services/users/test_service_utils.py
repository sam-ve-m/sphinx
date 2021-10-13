from copy import deepcopy


def get_onboarding_steps(onboarding_steps: dict):
    on_boarding_steps_copied = deepcopy(onboarding_steps)
    del on_boarding_steps_copied["current_onboarding_step"]

    return on_boarding_steps_copied


def get_current_onboarding_step(onboarding_steps: dict) -> str:
    current_onboarding_step = onboarding_steps.get("current_onboarding_step")
    return current_onboarding_step
