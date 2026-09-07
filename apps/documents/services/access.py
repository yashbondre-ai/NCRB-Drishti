from apps.cases.services import CaseService


def user_can_access_case(user, case_id):
    if not user or not user.is_authenticated:
        return False
    return CaseService.get_user_cases(user).filter(pk=case_id).exists()
