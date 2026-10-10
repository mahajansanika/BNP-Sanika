from datetime import date
from decimal import Decimal

# Importing shared interfaces
from app.ml.predict import predict 
from app.gap.bucketing import bucket_of 
from app.behavioural.adjusted_maturity import calculate_adjusted_maturity

def generate_ai_ladder(transactions: list, calc_date: date, currency: str, location: str, run_id: str) -> dict:
    
    buckets = {
        label: {"bucket": label, "assets": Decimal(0), "liabilities": Decimal(0), "transaction_count": 0}
        for label in ["0-1M", "1-3M", "3-12M", "1-5Y", ">5Y"]
    }
    
    matured_count = 0
    
    for txn in transactions:
        # 1. Get early exit probability
        prob = predict(txn)
        
        # 2. Get the adjusted date
        adjusted_date = calculate_adjusted_maturity(
            calc_date=calc_date, 
            contractual_date=txn.maturity_date, 
            early_exit_prob=prob
        )
        
        # 3. Handle already matured contracts
        if adjusted_date < calc_date:
            matured_count += 1
            continue
            
        # 4. Group into bucket and sum cashflows
        bucket_label = bucket_of(calc_date, adjusted_date)
        buckets[bucket_label]["transaction_count"] += 1
        
        if txn.type.lower() == "asset":
            buckets[bucket_label]["assets"] += txn.cashflow
        else:
            buckets[bucket_label]["liabilities"] += txn.cashflow

    # 5. Calculate net gap
    result_buckets = []
    for label, data in buckets.items():
        data["net_gap"] = data["assets"] - data["liabilities"]
        result_buckets.append(data)
        
    return {
        "run_id": run_id,
        "calc_date": str(calc_date),
        "currency": currency,
        "location": location,
        "approach": "ai",
        "matured_count": matured_count,
        "buckets": result_buckets
    }