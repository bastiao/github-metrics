from github_metrics.metrics.hotfixes_count import count_hotfixes
from github_metrics.metrics.merge_rate import call_merge_rate_statistics
from github_metrics.metrics.open_to_merge import (
    calulate_prs_open_to_merge_time_statistics,
)
from github_metrics.metrics.pr_size import call_pr_size_statistics
from github_metrics.metrics.time_to_merge import call_mean_time_to_merge_statistics
from github_metrics.metrics.time_to_open import call_time_to_open_statistics
from github_metrics.metrics.time_to_review import calulate_prs_review_time_statistics


def call_all_metrics(
    pr_list, include_hotfixes, exclude_authors, filter_authors, exclude_weekends
):
    # data collection
    data = {}
    data["mean_time_to_merge"] = call_mean_time_to_merge_statistics(
        pr_list=pr_list,
        include_hotfixes=include_hotfixes,
        exclude_authors=exclude_authors,
        filter_authors=filter_authors,
        exclude_weekends=exclude_weekends,
    )
    data["review_time"] = calulate_prs_review_time_statistics(
        pr_list=pr_list,
        include_hotfixes=include_hotfixes,
        exclude_authors=exclude_authors,
        filter_authors=filter_authors,
        exclude_weekends=exclude_weekends,
    )
    data["time_to_open"] = call_time_to_open_statistics(
        pr_list=pr_list,
        include_hotfixes=include_hotfixes,
        exclude_authors=exclude_authors,
        filter_authors=filter_authors,
        exclude_weekends=exclude_weekends,
    )
    data["open_to_merge_time"] = calulate_prs_open_to_merge_time_statistics(
        pr_list=pr_list,
        include_hotfixes=include_hotfixes,
        exclude_authors=exclude_authors,
        filter_authors=filter_authors,
        exclude_weekends=exclude_weekends,
    )
    data["merge_rate"] = call_merge_rate_statistics(
        pr_list=pr_list,
        include_hotfixes=include_hotfixes,
        exclude_authors=exclude_authors,
        filter_authors=filter_authors,
    )
    data["pr_size"] = call_pr_size_statistics(
        pr_list=pr_list,
        include_hotfixes=include_hotfixes,
        exclude_authors=exclude_authors,
        filter_authors=filter_authors,
    )
    data["hotfixes_count"] = count_hotfixes(
        pr_list=pr_list, exclude_authors=exclude_authors, filter_authors=filter_authors
    )
    return data