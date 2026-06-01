from __future__ import annotations

from dataclasses import dataclass

from rich.table import Table
from rich.console import Console

from .role_analysis import RoleCluster

console = Console()


@dataclass
class RoleSuggestion:
    role_name: str
    entitlements: list[str]
    rationale: str


class RoleSuggestionEngine:
    def suggest_roles(self, clusters: list[RoleCluster]) -> list[RoleSuggestion]:
        suggestions = []
        for cluster in clusters:
            suggested_name = self._name_role(cluster)
            rationale = (
                f"Group {len(cluster.members)} users under a business-aligned role because they share"
                f" {len(cluster.entitlements)} common entitlements."
            )
            suggestions.append(RoleSuggestion(suggested_name, cluster.entitlements, rationale))
        return suggestions

    def _name_role(self, cluster: RoleCluster) -> str:
        if "ent_0" in cluster.entitlements:
            return f"application_admin_{cluster.name}"
        return f"business_role_{cluster.name}"

    def print_suggestions(self, suggestions: list[RoleSuggestion]) -> None:
        table = Table(title="Role Suggestions")
        table.add_column("Role Name", style="bold green")
        table.add_column("Entitlements")
        table.add_column("Rationale")
        for suggestion in suggestions:
            table.add_row(
                suggestion.role_name,
                ", ".join(suggestion.entitlements[:6]) + ("..." if len(suggestion.entitlements) > 6 else ""),
                suggestion.rationale,
            )
        console.print(table)
