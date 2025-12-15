# Measure GitHub Actions metrics
# Measure the actions (workflow runs) taken on pull requests, such as successful runs and failed runs.
from github_metrics.common import extract_datetime_or_none


def get_workflow_runs_from_pr(pr):
    """
    Extracts workflow run information from a pull request.
    
    Args:
        pr: A pull request object containing check runs or status data.
    
    Returns:
        A list of workflow run dictionaries with status information.
    """
    runs = []
    
    # Get check runs from the PR
    check_runs = pr.get("checkRuns", {}).get("nodes", [])
    for run in check_runs:
        workflow_run = {
            "type": "workflow",
            "name": run.get("name"),
            "status": run.get("status"),
            "conclusion": run.get("conclusion"),
            "created_at": extract_datetime_or_none(run.get("createdAt")),
            "completed_at": extract_datetime_or_none(run.get("completedAt")),
        }
        runs.append(workflow_run)
    
    # Alternative: Get status checks
    status_checks = pr.get("statusCheckRollup", {}).get("nodes", [])
    for check in status_checks:
        workflow_run = {
            "type": "status_check",
            "name": check.get("context"),
            "status": check.get("status"),
            "conclusion": check.get("conclusion"),
            "created_at": extract_datetime_or_none(check.get("createdAt")),
        }
        runs.append(workflow_run)
    
    return runs


def count_actions_metrics(pr_list):
    """
    Counts GitHub Actions workflow metrics from a list of pull requests.
    
    Args:
        pr_list: A list of pull request objects.
    
    Returns:
        A dictionary containing action metrics:
        - total_runs: Total number of workflow runs
        - successful_runs: Number of successful runs (conclusion: SUCCESS)
        - failed_runs: Number of failed runs (conclusion: FAILURE)
        - neutral_runs: Number of neutral runs (conclusion: NEUTRAL, SKIPPED)
        - pending_runs: Number of pending runs (status: IN_PROGRESS)
        - action_breakdown: Dictionary with counts by workflow name and status
        - success_rate: Percentage of successful runs
    """
    
    total_runs = 0
    successful_runs = 0  # Conclusion: SUCCESS
    failed_runs = 0      # Conclusion: FAILURE
    neutral_runs = 0     # Conclusion: NEUTRAL, SKIPPED
    pending_runs = 0     # Status: IN_PROGRESS
    action_breakdown = {}
    
    for pr in pr_list:
        runs = get_workflow_runs_from_pr(pr)
        total_runs += len(runs)
        
        for run in runs:
            run_name = run.get("name", "unknown")
            conclusion = run.get("conclusion", "unknown")
            status = run.get("status", "unknown")
            
            # Track action breakdown by workflow name and conclusion
            key = f"{run_name}_{conclusion}"
            action_breakdown[key] = action_breakdown.get(key, 0) + 1
            
            # Categorize runs by conclusion
            if conclusion == "SUCCESS":
                successful_runs += 1
            elif conclusion == "FAILURE":
                failed_runs += 1
            elif conclusion in ["NEUTRAL", "SKIPPED", "CANCELLED"]:
                neutral_runs += 1
            elif status == "IN_PROGRESS" or conclusion is None:
                pending_runs += 1

    
    data = {
        "total_runs": total_runs,
        "successful_runs": successful_runs,
        "failed_runs": failed_runs,
        "neutral_runs": neutral_runs,
        "pending_runs": pending_runs,
        "action_breakdown": action_breakdown,
        "success_rate": (successful_runs / total_runs * 100) if total_runs > 0 else 0,
        "failure_rate": (failed_runs / total_runs * 100) if total_runs > 0 else 0
    }
    print(f"     \033[1mGitHub Actions Metrics\033[0m\n"
          f"     ----------------------------------\n"  
            f"     Total Workflow Runs: {total_runs}\n"
            f"     Successful Runs: {successful_runs}\n"
            f"     Failed Runs: {failed_runs}\n"
            f"     Neutral Runs: {neutral_runs}\n"
            f"     Pending Runs: {pending_runs}\n"
            f"     Success Rate: {data['success_rate']:.2f}%\n"
            f"     Failure Rate: {data['failure_rate']:.2f}%\n"
    )
    return data 