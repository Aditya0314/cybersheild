import re
from datetime import datetime
class LogAnalyzer:
    def __init__(self):
        self.failed_attempts ={}
        self.failure_times = {}

    def record_failure(self,ip_address,timestamp):
        try:
            # Validateing the format of the IP address
            pattern =r"^\d{1,3}(\.\d{1,3}){3}$"
            if not isinstance(ip_address,str):
                raise TypeError("IP address must be a text")

            if not re.match(pattern,ip_address):
                raise ValueError("Invalid IP address format")
            # Recording the failed attempt
            
            if ip_address in self.failed_attempts:
                self.failed_attempts[ip_address]+=1

            else:
                self.failed_attempts[ip_address]=1

            if ip_address  not in self.failure_times:
                self.failure_times[ip_address] = []

            time_value = datetime.strptime(timestamp,"%H:%M:%S")
            self.failure_times[ip_address].append(time_value)

        except(TypeError,ValueError) as error:
            print(f"Error for IP address {ip_address}: {error}")

    def show_results(self):
        return self.failed_attempts

    def analyze_file(self,file_path):
        try:
            with open(file_path,"r") as file:
                for line in file:
                    ip_match = re.search(
                        r"ip=(\d{1,3}(?:\.\d{1,3}){3})",line
                        )
                    status_match = re.search(
                        r"status=(FAILED|SUCCESS)",line
                        )
                    time_match = re.search(
                        r"(\d{2}:\d{2}:\d{2})",line
                    )
                    if ip_match and status_match and time_match :
                        ip_address = ip_match.group(1)
                        timestamp = time_match.group(1)
                        status = status_match.group(1)

                        

                        if status == "FAILED":
                            self.record_failure(ip_address,timestamp)

        except FileNotFoundError:
            print(f"Error: Log file {file_path} was not found .")

    def detect_suspicious_ips(self,threshold=5):
        suspicious_ips ={}

        for ip_address, attempts in self.failed_attempts.items():
            if attempts > threshold:
                suspicious_ips[ip_address] = attempts

        return suspicious_ips

    
    def detect_time_window(self, threshold=5, window_seconds=60):
        suspicious_ips = {}

        for ip_address, times in self.failure_times.items():
            times = sorted(times)

            for i in range(len(times)):
                window_count = 0

                for j in range(i, len(times)):
                    difference = (times[j] - times[i]).total_seconds()

                    if difference <= window_seconds:
                        window_count += 1
                    else:
                        break

                if window_count >= threshold:
                    suspicious_ips[ip_address] = window_count
                    break

        return suspicious_ips
