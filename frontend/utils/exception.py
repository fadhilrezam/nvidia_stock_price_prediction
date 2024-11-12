import sys
from utils.logger import logging
# def error_message_detail(error, error_detail:sys):
def error_message_detail(error, error_detail:sys):
    #error_detail:sys is use to get error detail more specific
    _,_,exc_tb=error_detail.exc_info() #exc_info will return 3 outputs but I will only use the output to get the error detail
    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = 'Error occured in python script [{0}], line [{1}], error message: {2}'.format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    #filename: return python file where error happened
    #exc_tb.tb_lineno: return line number where error happened
    return error_message

class CustomException(Exception):
    def __init__(self,error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail = error_detail)

    def __str__(self):
        return self.error_message

# try:
#     a = 1/0
#     print('a is output')
# except Exception as e:
#     logging.info(CustomException(e,sys))

