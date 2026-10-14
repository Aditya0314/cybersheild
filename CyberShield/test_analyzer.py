from analyzer import LogAnalyzer

analyzer=LogAnalyzer()
analyzer.analyze_file("CyberShield/sample_log.txt")
print("Failed login attempts :")
print(analyzer.show_results())
print("\n Susupicious IPs Address:")
print(analyzer.detect_suspicious_ips())
print("\nAnalyzer failure times:",analyzer.failure_times)
print("\nSuspicious IPs based on time window:")
print(analyzer.detect_time_window())
