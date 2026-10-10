def generate_comparison(deterministic_ladder: dict, ai_ladder: dict) -> dict:
    comparison_buckets = []
    
    # Iterate through both lists of buckets simultaneously
    for det_bucket, ai_bucket in zip(deterministic_ladder["buckets"], ai_ladder["buckets"]):
        difference = ai_bucket["net_gap"] - det_bucket["net_gap"]
        
        comparison_buckets.append({
            "bucket": det_bucket["bucket"],
            "deterministic_net_gap": det_bucket["net_gap"],
            "ai_net_gap": ai_bucket["net_gap"],
            "difference": difference
        })
        
    return {
        "run_id": deterministic_ladder["run_id"],
        "calc_date": deterministic_ladder["calc_date"],
        "currency": deterministic_ladder["currency"],
        "location": deterministic_ladder["location"],
        "approach": "comparison",
        "buckets": comparison_buckets
    }