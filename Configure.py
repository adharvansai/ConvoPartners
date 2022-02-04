# Configuration file

# *************************************************************************************************************

# NON NATIVE SPEAKERS

# =============================================

# File path of the processed excel sheet according to the below given instruction set. Please include .xlsx in the file path

int_filepath = "/Users/adharvan/PycharmProjects/ConvoPartners/NNS_InputFile.xlsx"

# =============================================

# Please make sure the names of the columns are correctly spelled according to the data sheets

icols = [
    'Training Timestamp',
    'Timestamp',
    'Email Address',
    'First and Last Name',
    'UIN',
    'Please select your preference for meetings with your conversation partner.',
    'What times are you available? [9 AM]',
    'What times are you available? [10 AM]',
    'What times are you available? [11 AM]',
    'What times are you available? [12 PM]',
    'What times are you available? [1 PM]',
    'What times are you available? [2 PM]',
    'What times are you available? [3 PM]',
    'What times are you available? [4 PM]',
    'What times are you available? [5 PM]',
    'What times are you available? [6 PM]',
    'What times are you available? [7 PM]',
    'What times are you available? [8 PM]'
]

# =============================================

# *************************************************************************************************************

# NON NATIVE SPEAKERS

# =============================================

# File path of the processed excel sheet according to the below given instruction set. Please include .xlsx in the file path

amc_filepath = "/Users/adharvan/PycharmProjects/ConvoPartners/NS_InputFile(1).xlsx"

# =============================================

# Please make sure the names of the columns are correctly spelled according to the data sheets

acols = [
    'Training Timestamp',
    'Timestamp',
    'Email Address',
    'First and Last Name',
    'UIN',
    'If you are interested in a Conversation Partnership, please select your preference for meeting.',
    'What times are you available? [9 AM]',
    'What times are you available? [10 AM]',
    'What times are you available? [11 AM]',
    'What times are you available? [12 PM]',
    'What times are you available? [1 PM]',
    'What times are you available? [2 PM]',
    'What times are you available? [3 PM]',
    'What times are you available? [4 PM]',
    'What times are you available? [5PM]',
    'What times are you available? [6PM]',
    'What times are you available? [7PM]',
    'What times are you available? [8PM]',
    # -- '[Conversation Partnership (10 weekly conversations; one half-hour per week)]'
]

#*******************************************************************************************************************

# Constant Configurations

week = {
    'Monday' : 1,
    'Tuesday' : 2,
    'Wednesday' : 3,
    'Thursday' : 4,
    'Friday' : 5,
    'Saturday' : 6,
    'Sunday' : 7,
    1 : 'Monday',
    2 : 'Tuesday',
    3 :'Wednesday',
    4 : 'Thursday',
    5 : 'Friday',
    6 : 'Saturday',
    7 : 'Sunday'

}

time_col_start = 6
time_col_end = 18
meeting_preference = 5

