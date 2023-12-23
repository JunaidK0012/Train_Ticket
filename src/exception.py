import sys

def get_error_message(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()

    line_no = exc_tb.tb_lineno
    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error occured in python script {} at line number {} and error message is {}".format(
        file_name,line_no,str(error)
    )

    return error_message


class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = get_error_message(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message