import json
import re
from pathlib import Path
from collections import Counter
import pytest

@pytest.fixture(scope="module")
def ground_truth():
    """Helper to calculate the true values directly from the log file."""
    paths, ips, total = Counter(), set(), 0
    with open("/app/access.log") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
                
    expected_top_path = paths.most_common(1)[0][0] if paths else None
    return {"total": total, "ips": len(ips), "top_path": expected_top_path}

@pytest.fixture(scope="module")
def agent_data():
    """Helper to load the agent's JSON output."""
    with open("/app/report.json") as f:
        return json.load(f)

def test_criterion_1_file_and_format():
    """1. Save the final output exactly at `/app/report.json` as a valid JSON file."""
    report_file = Path("/app/report.json")
    assert report_file.exists(), "report.json was not generated."
    try:
        with open(report_file) as f:
            json.load(f)
    except json.JSONDecodeError:
        pytest.fail("report.json is not a valid JSON file.")

def test_criterion_2_total_requests(ground_truth, agent_data):
    """2. Calculate the total number of requests in the log and save it under the key "total_requests"."""
    assert "total_requests" in agent_data, "Key 'total_requests' is missing."
    assert agent_data["total_requests"] == ground_truth["total"], f"Expected {ground_truth['total']} total requests."

def test_criterion_3_unique_ips(ground_truth, agent_data):
    """3. Count the total number of unique client IP addresses and save it under the key "unique_ips"."""
    assert "unique_ips" in agent_data, "Key 'unique_ips' is missing."
    assert agent_data["unique_ips"] == ground_truth["ips"], f"Expected {ground_truth['ips']} unique IPs."

def test_criterion_4_top_path(ground_truth, agent_data):
    """4. Identify the single most frequently accessed path and save it under the key "top_path"."""
    assert "top_path" in agent_data, "Key 'top_path' is missing."
    assert agent_data["top_path"] == ground_truth["top_path"], f"Expected top path to be {ground_truth['top_path']}."
