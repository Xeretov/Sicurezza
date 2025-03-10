import pandas as pd
from collections import Counter
import json
import re
from datetime import datetime, timedelta
import numpy as np

def make_serializable(obj):
    """Recursively converts non-serializable types in a dictionary or list to serializable ones."""
    if isinstance(obj, (pd.Timestamp, pd.Timedelta)):  # Handle pandas specific types
        return str(obj)  # Convert to string
    elif isinstance(obj, (pd.Series, pd.DataFrame)): #Convert to list or dict
        return obj.to_dict()
    elif isinstance(obj, dict):
        return {key: make_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(item) for item in obj]
    elif isinstance(obj, (int, float, str, bool, type(None))): #Base cases
        return obj
    elif isinstance(obj, (np.int64, np.int32, np.float64)): #numpy types
        return obj.item()
    else:
        try:
            return str(obj) #Try converting to string as last resort
        except:
            return "Unserializable Object"

def analyze_web_logs(log_file):
    """Analyzes web logs for cyber security insights.

    Args:
        log_file: Path to the web log file.

    Returns:
        A dictionary containing cyber security insights.
    """

    try:
        # Improved log parsing to handle variations and potential errors
        log_data = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    # Example log format:  host - - [timestamp] "request" status_code bytes
                    parts = line.split()
                    if len(parts) >= 7: # Ensure enough parts exist
                        host = parts[0]
                        timestamp = " ".join(parts[3:5]).strip("[]") # Extract timestamp
                        request = " ".join(parts[5:-2]).strip('"') # Extract request
                        status_code = int(parts[-2])
                        bytes_sent = int(parts[-1]) if parts[-1].isdigit() else 0 # Handle missing bytes
                        method = request.split()[0] if request else "UNKNOWN" # Extract method
                        resource = request.split()[1] if len(request.split()) > 1 else "UNKNOWN" # Extract resource
                        log_data.append([host, timestamp, request, status_code, bytes_sent, method, resource])
                except (ValueError, IndexError) as e:
                    print(f"Skipping invalid log line: {line.strip()} - Error: {e}")  # Handle parsing errors
                    continue  # Skip to the next line

        df = pd.DataFrame(log_data, columns=['host', 'timestamp', 'request', 'status_code', 'bytes_sent', 'method', 'resource'])

    except FileNotFoundError:
        return {"error": "Log file not found."}
    except Exception as e:  # Catch other potential errors
        return {"error": f"An error occurred: {e}"}

    insights = {}

    insights['total_requests'] = len(df['host'])
    insights['request_counts_per_ip'] = df['host'].value_counts().head(20).to_dict()
    insights['frequent_request'] = df['request'].value_counts().head(20).to_dict()
    insights['requests_per_hour'] = df['timestamp'].str.split(' ').str[0].str.split(':').str[1].value_counts().to_dict()

    insights['requests_by_method'] = {}
    method_counts = df['method'].value_counts()
    for method, count in method_counts.items():
        method_df = df[df['method'] == method]
        if method not in ['GET', 'POST', 'HEAD']:
            insights['requests_by_method'][method] = {
                'count': count,
                'requests': method_df[['host', 'timestamp', 'request', 'status_code', 'bytes_sent']].to_dict(orient='records')
            }
        else:
            insights['requests_by_method'][method] = count

    insights['requests_by_status_code'] = {}
    status_counts = df['status_code'].value_counts()
    for status, count in status_counts.items():
        status_df = df[df['status_code']==status]
        if status in [200,304,404]:
            insights['requests_by_status_code'][status] = count
        elif status in [401, 403, 500]:
            insights['requests_by_status_code'][status] = {
                'count': count,
                'requests': status_df[['host','timestamp','request','method','bytes_sent']].to_dict(orient='records')[:10]
            }
            
    insights['high_error_hosts'] = {}
    error_codes = range(400, 600)

    # More efficient calculation of high error hosts
    total_requests_per_host = df['host'].value_counts()

    # Use a boolean mask for filtering
    high_traffic_mask = total_requests_per_host > 50
    high_traffic_hosts = total_requests_per_host[high_traffic_mask].index
    high_error_data = []

    if not high_traffic_hosts.empty: #Check if there are any high traffic hosts
        host_groups = df[df['host'].isin(high_traffic_hosts)].groupby('host')

        for host, host_df in host_groups:
            total_requests = len(host_df)
            error_requests = host_df['status_code'].isin(error_codes).sum()  # More efficient error count
            error_percentage = (error_requests / total_requests) * 100 if total_requests > 0 else 0

            if error_percentage >= 20:
                host_data = {
                    'host': host,
                    'total_requests': total_requests,
                    'error_percentage': error_percentage,
                    'error_requests': error_requests,
                    'requests': host_df[host_df['status_code'].isin(error_codes)][['timestamp', 'request', 'status_code']].to_dict(orient='records')[:10]
                }
                high_error_data.append(host_data)  # Add data to the list

    sorted_high_error_data = sorted(high_error_data, key=lambda x: (x['error_percentage'], x['total_requests']), reverse=True)

    insights['high_error_hosts'] = {item['host']: item for item in sorted_high_error_data[:10]}

    insights['hourly_traffic_per_day'] = {}

    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z', errors='coerce')
        df['day'] = df['timestamp'].dt.day
        df['hour'] = df['timestamp'].dt.hour
        daily_traffic = df.groupby(['hour', 'day'])['host'].count().unstack(fill_value=0)
        for date, hourly_counts in daily_traffic.items():
            insights['hourly_traffic_per_day'][date] = {
                "total_requests": hourly_counts.sum(),
                "hourly_traffic": hourly_counts.to_dict()
            }

    except Exception as e:
        print(f"Error calculating daily traffic: {e}")
        insights['hourly_traffic_per_day'] = f"Error calculating daily traffic: {e}"


    return insights



def save_report_json(insights, output_file="cyber_report.json"):
    """Saves the report to a JSON file."""
    serializable_insights = make_serializable(insights)
    try:
        with open(output_file, 'w') as f:
            json.dump(serializable_insights, f, indent=4)
        print(f"Report saved to {output_file}")
    except Exception as e:
        print(f"Error saving report to JSON: {e}")



# Example usage:
log_file_path = 'NASA_access_log_Aug95'  # Replace with your log file path
analysis_results = analyze_web_logs(log_file_path)

if "error" in analysis_results:
    print(analysis_results["error"])
else:
    time = str(datetime.datetime.now())
    report_file = "report_"+time+".log"
    save_report_json(analysis_results, report_file)  # Save to JSON file
