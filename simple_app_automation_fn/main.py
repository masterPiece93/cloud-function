import functions_framework
import logging
import pyotp
from typing import Final
from environs import Env
from routes import Routes
from handlers import Handler
from database import *

# ENV VARIABLES
env = Env()
env.read_env() # Reads .env file in the current directory

DEBUG: Final[bool] = env.bool("DEBUG")
ENV: Final[str] = env.str("ENV")
SA_FILE_PATH: Final[str] = env.str('SA_FILE_PATH')


# Logger 
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.INFO


# PyOTP
secret_key = pyotp.random_base32()
otp = pyotp.TOTP(secret_key, interval=60, digits=6)

# Flask Messages Initialization
messages_default = {
    f"{Routes.HOME.value}": {"GET": []},
    f"{Routes.BUCKET_UPLOAD.value}": {"GET": [], "POST": []},
}

# DB Initialization
initialize_db()
SeedData.seed_process_flag()
SeedData.seed_message(messages_default)

# Main :
@functions_framework.http
def hello_http(request):
    """
    Entrypoint of CloudFn
        - each time a http request is fired , this
            gets executed . 
    """
    if request.path == Routes.HOME:
        return Handler.home()
    if request.path == Routes.BUCKET_UPLOAD:
        return Handler.bucket_upload()
    if request.path == Routes.DO_BUCKET_UPLAOD:
        return Handler.do_bucket_upload(otp)
    if request.path == Routes.GENERATE_OTP:
        return Handler.generate_otp(otp)
    
    return "Method not allowed", 405
