# ChatGPT wrote this

# employee_availability.py
employee_hours = {
    "employee1": 40,
    "employee2": 40,
    "employee3": 40,
    "employee4": 40
}

employee_availability = {
    "employee1": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "employee2": ["Monday", "Tuesday", "Wednesday", "Thursday"],
    "employee3": ["Tuesday", "Wednesday", "Thursday", "Friday"],
    "employee4": ["Monday", "Wednesday", "Thursday", "Friday"]
}

employee_unavailability = {
    "employee1": [datetime.date(2023, 1, 17), datetime.date(2023, 1, 18)],
    "employee2": [datetime.date(2023, 1, 17)],
    "employee3": [],
    "employee4": []
}

weekday_shifts = {
    "Monday": {"long": 2, "short": 1},
    "Tuesday": {"long": 2, "short": 1},
    "Wednesday": {"long": 2, "short": 0},
    "Thursday": {"long": 2, "short": 1},
    "Friday": {"long": 2, "short": 1},
    "Saturday": {"long": 2, "short": 2},
    "Sunday": {"long": 2, "short": 0}
}


# main.py
import csv
import datetime
import employee_availability

# Define the start date and end date of the schedule
start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 1, 31)

# Create an empty list to store the schedule
schedule = []

# Loop through each date in the schedule
for i in range((end_date - start_date).days + 1):
    date = start_date + datetime.timedelta(days=i)
    weekday = date.strftime("%A")
    
    # Get the number of long and short shifts needed for the weekday
    shifts_needed = employee_availability.weekday_shifts[weekday]
    long_shifts_needed = shifts_needed["long"]
    short_shifts_needed = shifts_needed["short"]
    
    # Loop through each employee and assign shifts based on their availability
    for employee, hours_needed in employee_availability.employee_hours.items():
        if (weekday in employee_availability.employee_availability[employee]) and (date not in employee_availability.employee_unavailability[employee]):
            hours_worked = 0
            while hours_worked < hours_needed:
                if long_shifts_needed > 0:
                    schedule.append([employee, date, "long"])
                    long_shifts_needed -= 1
                    hours_worked += 8
                elif short_shifts_needed > 0:
                    schedule.append([employee, date, "short"])
                    short_shifts_needed -= 1
                    hours_worked += 4

# Write the schedule to a .csv file
with open("schedule.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Employee", "Date", "Shift Length"])
    writer.writerows(schedule)
