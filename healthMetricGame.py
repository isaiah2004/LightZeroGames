import random
import time
# Sample first and last names for random name generation
first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Robin", "Jamie", "Riley"]
last_names = ["Pandiyan", "Arokiyam", "Durai", "Karthikeyan", "Sendhil", "Natarajan", "Iyer", "Palaniappan"]
# Typing effect delay in seconds
typing_delay = 0.0001
# Possible outcomes for randomization
possible_outcomes = ["Healthy", "Abnormal", "Impossible"]
# Function to print with typing effect
def print_with_typing_effect(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(typing_delay)
    print()  # New line at the end
    time.sleep(0.1)

# Function to classify health metrics
def classify_metrics(bp_systolic, bp_diastolic, pulse, temperature):
    bp_status = classify_blood_pressure(bp_systolic, bp_diastolic)
    pulse_status = classify_pulse(pulse)
    temperature_status = classify_temperature(temperature)
    return bp_status, pulse_status, temperature_status

def classify_blood_pressure(bp_systolic, bp_diastolic):
    if bp_systolic < bp_diastolic or bp_systolic > 200 or bp_diastolic > 150 or bp_diastolic < 10 or bp_systolic < 50:
        return "Impossible"
    elif 90 <= bp_systolic <= 130 and 60 <= bp_diastolic <= 100:
        return "Healthy"
    else:
        return "Abnormal"

def classify_pulse(pulse):
    if pulse < 20 or pulse > 150:
        return "Impossible"
    elif 60 <= pulse <= 120:
        return "Healthy"
    else:
        return "Abnormal"

def classify_temperature(temperature):
    if temperature < 70 or temperature > 110:  # Assuming temperature is given in Fahrenheit
        return "Impossible"
    elif 95 <= temperature <= 100:
        return "Healthy"
    else:
        return "Abnormal"

def calculate_deviation_from_normal(bp_systolic, bp_diastolic, pulse, temperature):
    bp_systolic_deviation = min(abs(bp_systolic - 90), abs(bp_systolic - 130))
    bp_diastolic_deviation = min(abs(bp_diastolic - 60), abs(bp_diastolic - 100))
    pulse_deviation = min(abs(pulse - 60), abs(pulse - 120))
    temperature_deviation = min(abs(temperature - 95), abs(temperature - 100))
    return bp_systolic_deviation, bp_diastolic_deviation, pulse_deviation, temperature_deviation

def main():
    for customerNo in range(20):
        score = 0
        # Generate a random name
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        # Generate random values for health metrics
        bp_systolic = random.randint(80, 160)
        bp_diastolic = random.randint(50, 100)
        pulse = random.randint(10, 170)
        temperature = random.randint(50, 150)  # Assuming temperature is given in Fahrenheit
        # Randomly decide expected outcomes
        expected_bp_status = random.choice(possible_outcomes)
        expected_pulse_status = random.choice(possible_outcomes)
        expected_temperature_status = random.choice(possible_outcomes)
        # Classify each metric
        actual_bp_status, actual_pulse_status, actual_temperature_status = classify_metrics(bp_systolic, bp_diastolic,
                                                                                            pulse, temperature)
        # Check and score each metric
        score += 1 if actual_bp_status == expected_bp_status else 0
        score += 1 if actual_pulse_status == expected_pulse_status else 0
        score += 1 if actual_temperature_status == expected_temperature_status else 0
        # Calculate deviations from normal values
        bp_systolic_deviation, bp_diastolic_deviation, pulse_deviation, temperature_deviation = calculate_deviation_from_normal(
            bp_systolic, bp_diastolic, pulse, temperature)
        # Display the results with typing effect
        print_with_typing_effect(f"Name: {name} - No: {customerNo+1}")
        print_with_typing_effect(
            f"Expected vs Actual - Blood Pressure: {expected_bp_status} vs {actual_bp_status}  |BP:{bp_systolic}/{bp_diastolic}| |Deviation: {bp_systolic_deviation}/{bp_diastolic_deviation}|")
        print_with_typing_effect(
            f"Expected vs Actual - Pulse: {expected_pulse_status} vs {actual_pulse_status} |Pulse:{pulse}| |Deviation: {pulse_deviation}|")
        print_with_typing_effect(
            f"Expected vs Actual - Temperature: {expected_temperature_status} vs {actual_temperature_status} |Temp:{temperature}| |Deviation: {temperature_deviation}|")
        print_with_typing_effect(f"Score: {score}")
        print_with_typing_effect("---------------")

if __name__ == "__main__":
    main()