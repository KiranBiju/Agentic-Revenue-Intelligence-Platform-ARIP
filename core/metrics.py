def compute_campaign_metrics(results, duration_seconds=None):
    total = len(results)
    sent = sum(1 for r in results if r.get("status") == "sent")
    failed = sum(1 for r in results if r.get("status") == "failed")

    attempts = [r.get("attempts", 1) for r in results]
    avg_attempts = sum(attempts) / len(attempts) if attempts else 0

    validation_failures = sum(
        1
        for r in results
        if r.get("failure_reason") == "validation_failed"
    )

    return {
        "total_processed": total,
        "sent": sent,
        "failed": failed,
        "success_rate": sent / total if total else 0,
        "validation_failure_rate": validation_failures / total if total else 0,
        "avg_attempts": round(avg_attempts, 2),
        "duration_seconds": duration_seconds,
    }