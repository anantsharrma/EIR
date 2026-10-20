class SessionNotFoundError(Exception):
    pass
class SessionAlreadyCompletedError(Exception):
    pass
class NoQuestionsConfiguredError(Exception):
    pass
class PatientHasNoSessionsErorr(Exception):
    pass