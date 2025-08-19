import time
import logging
from flask import request, render_template, redirect
import pandas as pd
from http import HTTPMethod
from routes import Routes
from database import *
from utils import *
from schema import CSV_SCHEMA

logger = logging.getLogger(__name__)
logger.level = logging.INFO

class Handler(object):

    @staticmethod
    def home():
        nofication_messages = Utils.get_notifications()
        return render_template('base.html', messages=nofication_messages)
    
    @staticmethod
    def bucket_upload():
        
        if request.method == HTTPMethod.GET:
            # use render_template Instead
            nofication_messages = Utils.get_notifications()
            return render_template('bucket_upload.html', messages=nofication_messages)
    
    @staticmethod
    def do_bucket_upload(otp):
        
        # TODO : add logic for only 1 request per 5 minutes .

        process_flag = DBUtils.get_process_flag()
        if process_flag:
            return render_template("notification.html", messages=["- Automation in Progress ( server allows only single automation at a time)"])
        
        if request.method == HTTPMethod.POST:

            otp_value = request.form.get('otp')

            if not otp_value:
                Utils.set_notifications('/bucket-upload', 'GET', f"ERROR : Unauthenticated Request")
                return redirect(Routes.BUCKET_UPLOAD.value)
            else:
                print(f"validating otp: {otp_value}")
                if not otp.verify(otp_value):
                    Utils.set_notifications('/bucket-upload', 'GET', f"INFO : Blocked. Invalid Otp.")
                    return redirect(Routes.BUCKET_UPLOAD.value)

            if 'csv_file' not in request.files:
                Utils.set_notifications('/bucket-upload', 'GET', f"ERROR : No file part")
                return redirect(Routes.BUCKET_UPLOAD.value)
            
            file = request.files['csv_file']
            
            if file.filename == '':
                Utils.set_notifications('/bucket-upload', 'GET', f"ERROR : No selected file")
                return redirect(Routes.BUCKET_UPLOAD.value)
            
            # TODO : limit file size to 1 MB
            # TODO : read only first 5 entries of csv
            # TODO : validate csv bucket display name to only contain 25 chars

            if file and file.filename.endswith('.csv'):
                try:
                    df = pd.read_csv(file, dtype=CSV_SCHEMA)
                    DBUtils.switch_process_flag(True)
                    print("processing started")
                    time.sleep(2)
                    print("processing completed")
                    # Now 'df' is a Pandas DataFrame containing your CSV data
                    # flash(f"CSV loaded successfully! rows:\n\n{df.head().to_html()}")
                    Utils.set_notifications('/bucket-upload', 'GET', f"SUCCESS : CSV loaded successfully!")
                    # "rows:\n\n{df.head().to_html()}"
                    DBUtils.switch_process_flag(False)
                    return redirect(Routes.BUCKET_UPLOAD.value)
                except Exception as e:
                    Utils.set_notifications('/bucket-upload', 'GET', f"ERROR : Error reading CSV: {e}")
                    DBUtils.switch_process_flag(False)
                    return redirect(Routes.BUCKET_UPLOAD.value)
            else:
                Utils.set_notifications('/bucket-upload', 'GET', "ERROR : Invalid file type. Please upload a CSV.")
                DBUtils.switch_process_flag(False)
                return redirect(Routes.BUCKET_UPLOAD.value)

    def generate_otp(otp):
        # limit request to only 4 times a day
        new_otp = otp.now()
        logger.info(f"OTP: {new_otp}")
        Utils.set_notifications('/', 'GET', "INFO : OTP generated . Valid Only for 60 Seconds. Please Complete you work Quickly")
        return redirect(Routes.HOME)

