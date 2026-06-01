from __future__ import annotations

import pandas as pd

def load_sample_access_data() -> pd.DataFrame:
    """Generate a synthetic dataset representing user entitlement assignments."""
    data = [
        {"user_id": f"user_{i}", "application": f"app_{i % 12}", "entitlement": f"ent_{j}", "role": None}
        for i in range(1, 81)
        for j in range((i % 5) + 1)
    ]
    return pd.DataFrame(data)


def normalize_entitlement_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize entitlement labels to a consistent business-friendly form."""
    df = df.copy()
    df["entitlement_normalized"] = (
        df["entitlement"].str.lower().str.replace(" ", "_")
    )
    return df
