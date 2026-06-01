from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

import networkx as nx
import pandas as pd
from sklearn.cluster import AgglomerativeClustering


@dataclass
class RoleCluster:
    name: str
    members: list[str]
    entitlements: list[str]
    score: float


class RoleMiningModel:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.graph = nx.Graph()

    def build_entitlement_graph(self) -> nx.Graph:
        grouped = self.df.groupby("user_id")
        for user_id, group in grouped:
            entitlements = sorted(group["entitlement_normalized"].unique())
            for i, a in enumerate(entitlements):
                for b in entitlements[i + 1 :]:
                    self.graph.add_edge(a, b, weight=self.graph.get_edge_data(a, b, {}).get("weight", 0) + 1)
        return self.graph

    def detect_redundant_entitlements(self) -> list[str]:
        ent_counts = Counter(self.df["entitlement_normalized"])
        return [ent for ent, count in ent_counts.most_common() if count > 15]

    def cluster_roles(self, n_clusters: int = 6) -> list[RoleCluster]:
        ent_unique = sorted(self.df["entitlement_normalized"].unique())
        ent_index = {ent: idx for idx, ent in enumerate(ent_unique)}
        user_matrix = pd.crosstab(self.df["user_id"], self.df["entitlement_normalized"]).reindex(columns=ent_unique, fill_value=0)

        if len(user_matrix) < n_clusters:
            n_clusters = max(1, len(user_matrix))

        model = AgglomerativeClustering(n_clusters=n_clusters)
        labels = model.fit_predict(user_matrix)

        clusters = []
        for label in sorted(set(labels)):
            cluster_users = user_matrix.index[labels == label].tolist()
            cluster_entitlements = user_matrix.columns[(labels == label).any()].tolist()
            clusters.append(
                RoleCluster(
                    name=f"role_cluster_{label + 1}",
                    members=cluster_users,
                    entitlements=cluster_entitlements,
                    score=len(cluster_entitlements) / max(len(cluster_users), 1),
                )
            )
        return clusters
