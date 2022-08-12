import math, random

def generateOTP() : 
    # Declare a digits variable   
    # which stores all digits  
    digits = "0123456789"
    OTP = "" 
    # by changing value in range 
    for i in range(5) : 
        OTP += digits[math.floor(random.random() * 10)] 
  
    return OTP