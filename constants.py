import os

BASE_URL = os.getenv(
    "STELLAR_BURGERS_API_URL",
    "https://stellarburgers.education-services.ru"
)

LOGIN_ERROR_MESSAGE = "email or password are incorrect"
