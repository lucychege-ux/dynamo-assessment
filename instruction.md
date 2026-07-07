I need you to take a look at the Apache-style access log located at `/app/access.log`. Please analyze the traffic and put together a quick JSON summary report for me. 

To complete this, make sure you hit these criteria:
1. Save the final output exactly at `/app/report.json` as a valid JSON file.
2. Calculate the total number of requests in the log and save it under the key "total_requests".
3. Count the total number of unique client IP addresses and save it under the key "unique_ips".
4. Identify the single most frequently accessed path and save it under the key "top_path".
