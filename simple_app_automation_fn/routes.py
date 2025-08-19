from enum import Enum
from database import *

# Routes
class Routes(str, Enum):

    HOME = "/"
    BUCKET_UPLOAD = "/bucket-upload"
    DO_BUCKET_UPLAOD = "/do-bucket-upload"
    GENERATE_OTP = "/generate-otp"

