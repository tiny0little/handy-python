#!/usr/local/bin/python3

weight=int(input("What is your weight in kg "))
height=int(input("What is your height in cm "))

bmi_result=round(weight/((height/100)*(height/100)),2)
if bmi_result > 35:
  bmi_info = "clinically obese"
elif bmi_result > 30:
  bmi_info = "obese"
elif bmi_result > 25:
  bmi_info = "slightly overweight"
elif bmi_result > 18.5:
  bmi_info = "normal weight"
else:
  bmi_info = "underweight"

print(f"Your BMI is {bmi_result} ({bmi_info})")

