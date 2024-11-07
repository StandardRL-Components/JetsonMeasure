import re
import subprocess
import csv
import time
import signal
import sys

# Initialize a list to store the parsed data
data_records = []
start_time = time.time() * 1000  # Starting time in milliseconds
    
def parse_line(line):
    # Define the regex pattern
    pattern = r"^RAM\ ([0-9]+)\/[^\[]*\[([0-9]+)\%@[0-9]+,([0-9]+)\%@[0-9]+,([0-9of]+)\%?@?[0-9]*,([0-9of]+)\%?@?[0-9]*\]\ [a-zA-Z0-9_%@]+\ [a-zA-Z0-9_%@]+\ [a-zA-Z0-9_%@]+\ [a-zA-Z0-9_%@]+\ [a-zA-Z0-9_%@]+\ [a-zA-Z0-9_%@\.]+\ [a-zA-Z0-9_%@\.]+\ CPU@([0-9\.]+)C\ [a-zA-Z0-9_%@\.]+\ GPU@([0-9\.]+)C\ [a-zA-Z0-9_%@\.]+\ [a-zA-Z0-9_%@\.]+\ POM_5V_IN\ ([0-9]+)\/[0-9]+ POM_5V_GPU\ ([0-9]+)\/[0-9]+\ POM_5V_CPU\ ([0-9]+)\/[0-9]+$"
    
    # Perform regex matching
    match = re.match(pattern, line)
    if match:
        # Extract the matched groups into the dictionary
        return {
            "RAM": int(match.group(1)),
            "CPU1": match.group(2),
            "CPU2": match.group(3),
            "CPU3": match.group(4),
            "CPU4": match.group(5),
            "CPUTEMP": float(match.group(6)),
            "GPUTEMP": float(match.group(7)),
            "PWR_TOTAL": float(match.group(8)),
            "PWR_GPU": float(match.group(9)),
            "PWR_CPU": float(match.group(10))
        }
    else:
        raise ValueError("Line format is incorrect or does not match expected tegrastats output")

def record_data(parsed_line):
    """
    Record the parsed data with a timestamp.
    """
    timestamp = int(time.time() * 1000 - start_time)  # Time in ms since script started
    parsed_line['timestamp'] = timestamp
    data_records.append(parsed_line)

# Define a handler for keyboard interrupt to save data and clean up
def signal_handler(sig, frame):
    print("Keyboard interrupt received. Saving data to CSV...")
    save_to_csv(data_records)
    sys.exit(0)

def save_to_csv(data_records):
    """
    Save the data_records list to a CSV file.
    """
    if data_records:
        keys = data_records[0].keys()
        with open('results.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data_records)
        print("Data saved to results.csv")

def main():
    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Run the tegrastats command
    process = subprocess.Popen(
        ["sudo", "tegrastats"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1  # Line buffering
    )

    try:
        # Read each line of output from tegrastats
        for line in process.stdout:
            parsed = parse_line(line)
            record_data(parsed)
    except KeyboardInterrupt:
        # Handle KeyboardInterrupt in case the signal handler doesn't catch it
        signal_handler(None, None)

if __name__ == "__main__":
    main()
