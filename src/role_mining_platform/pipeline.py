from __future__ import annotations

import pandas as pd

from .data_loader import load_sample_access_data, normalize_entitlement_labels
from .role_analysis import RoleMiningModel
from .role_suggestions import RoleSuggestionEngine


class RoleMiningPipeline:
    """Encapsulates an IAM role mining pipeline for enterprise data.

    This pipeline is architected to show clear boundaries between data ingestion,
    analysis, and recommendation. It is intentionally simple to make the
    decision points visible to reviewers.
    """

    def __init__(self, source: str | None = None) -> None:
        self.source = source
        self.df: pd.DataFrame | None = None
        self.analysis_model: RoleMiningModel | None = None

    def load(self) -> pd.DataFrame:
        if self.source:
            self.df = pd.read_csv(self.source)
        else:
            self.df = load_sample_access_data()
        self.df = normalize_entitlement_labels(self.df)
        return self.df

    def analyze(self) -> dict[str, object]:
        if self.df is None:
            raise RuntimeError("Data must be loaded before analysis.")
        self.analysis_model = RoleMiningModel(self.df)
        graph = self.analysis_model.build_entitlement_graph()
        redundant = self.analysis_model.detect_redundant_entitlements()
        clusters = self.analysis_model.cluster_roles(n_clusters=5)
        return {
            "graph": graph,
            "redundant_entitlements": redundant,
            "role_clusters": clusters,
        }

    def recommend(self, clusters: list[object]) -> list[object]:
        engine = RoleSuggestionEngine()
        return engine.suggest_roles(clusters)
