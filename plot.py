import os
import json

dir_path = "./load-test/results"
frameworks = os.listdir(dir_path)

stats_files = {}
for framework in frameworks:
    simulation_path = os.listdir(f"{dir_path}/{framework}")
    stats_files[framework] = [f"{dir_path}/{framework}/{simulation}/js/stats.json" for simulation in simulation_path]



framework_stats = {}
for framework, stats in stats_files.items():
    for stat in stats:
        with open(stat, "r") as file:
            data = file.read()
            data = json.loads(data)
            framework_stats[framework] = data['stats']




table_md = f"""
| Name | Total Requests | Successful Requests | Failed Requests |  Min Response Time (ms) | Max Response Time (ms) | Mean Response Time (ms) | Std Deviation (ms) | 50th Percentile (ms) | 75th Percentile (ms) | 95th Percentile (ms) | 99th Percentile (ms) | Mean Requests Per Second | Successful Requests Per Second | Failed Requests Per Second |
| --------------- | --------------- | ------------------- | --------------- | ----- | ---- | ----- | -------------- | ---------------- | ---------------- | ---------------- | ---------------- | ------------------------- | ------------------------------ | -------------------------- |
"""


for framework, stats in framework_stats.items():
    total = stats["numberOfRequests"]["total"]
    ok = stats["numberOfRequests"]["ok"]
    ko = stats["numberOfRequests"]["ko"]
    min_response_time = stats["minResponseTime"]["total"]
    max_response_time = stats["maxResponseTime"]["total"]
    mean_response_time = stats["meanResponseTime"]["total"]
    std_deviation = stats["standardDeviation"]["total"]
    percentiles50 = stats["percentiles1"]["total"]
    percentiles75 = stats["percentiles2"]["total"]
    percentiles95 = stats["percentiles3"]["total"]
    percentiles99 = stats["percentiles4"]["total"]
    mean_req_per_second = round(stats["meanNumberOfRequestsPerSecond"]["total"], 2)
    ok_req_per_second = round(stats["meanNumberOfRequestsPerSecond"]["ok"], 2)
    ko_req_per_second = round(stats["meanNumberOfRequestsPerSecond"]["ko"], 2)

    table_md += f"| {framework.capitalize()} | {total} | {ok} | {ko} | {min_response_time} | {max_response_time} | {mean_response_time} | {std_deviation} | {percentiles50} | {percentiles75} | {percentiles95} | {percentiles99} | {mean_req_per_second} | {ok_req_per_second} | {ko_req_per_second} |\n"




with open("README.md", "r+") as file:
    content = file.readlines()
    location = content.index("### Benchmarks Frameworks\n")
    content = content[:location + 1] + [table_md]
    file.seek(0)
    file.writelines(content)
    
    
