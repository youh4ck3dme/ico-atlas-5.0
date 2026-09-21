import hashlib
import re
import unicodedata
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_

from services.database import get_db_session, GraphNode, GraphEdge

LEGAL_ENTITY_TOKENS = [
    " s.r.o", " s. r. o", " a.s", " k.s", " v.o.s", " se",
    " b.v", " gmbh", " ag", " ltd", " inc", " s.a", " sas",
    " sp. z o.o", " spółka", " spolka", " oy", " ab"
]

def _strip_diacritics(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(ch for ch in s if not unicodedata.combining(ch))

def _norm_key(s: str) -> str:
    s = _strip_diacritics(s)
    s = (s or "").lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\s\.\-\/]", "", s)  # keep basic tokens
    return s.strip()

def _looks_like_legal_entity(name: str) -> bool:
    n = _norm_key(name)
    return any(tok in n for tok in LEGAL_ENTITY_TOKENS) or (" b.v." in (name or "").lower()) or ("b.v" in n)

def _sha12(s: str) -> str:
    return hashlib.sha1((s or "").encode("utf-8")).hexdigest()[:12]

def _person_node_id(country: str, name: str, birth_date: str = "") -> str:
    key = f"{country}|{_norm_key(name)}|{_norm_key(birth_date)}"
    return f"pers_{country.lower()}_{_sha12(key)}"

def _owner_node_id(country: str, name: str) -> str:
    key = f"{country}|{_norm_key(name)}"
    return f"own_{country.lower()}_{_sha12(key)}"

class GraphService:
    def upsert_node(
        self,
        node_id: str,
        label: str,
        node_type: str,
        country: str,
        details: Dict = None
    ):
        with get_db_session() as db:
            if not db:
                return
            
            # Check if exists
            node = db.query(GraphNode).filter(GraphNode.id == node_id).first()
            if node:
                # Update logic if needed, currently just update details/timestamp
                if details:
                    # Merge details or overwrite? Overwrite for now or merge
                    current = node.details or {}
                    current.update(details or {})
                    node.details = current
                node.updated_at = datetime.utcnow()
            else:
                node = GraphNode(
                    id=node_id,
                    label=label[:500],
                    type=node_type,
                    country=country,
                    details=details or {}
                )
                db.add(node)
            try:
                db.commit()
            except Exception as e:
                print(f"Error upserting node {node_id}: {e}")
                db.rollback()

    def upsert_edge(
        self,
        source: str,
        target: str,
        edge_type: str,
        details: Dict = None,
        weight: float = 1.0
    ):
        with get_db_session() as db:
            if not db:
                return

            # Check if exists (directed edge)
            edge = db.query(GraphEdge).filter(
                GraphEdge.source == source,
                GraphEdge.target == target,
                GraphEdge.type == edge_type
            ).first()

            if edge:
                if details:
                    current = edge.details or {}
                    current.update(details)
                    edge.details = current
                edge.updated_at = datetime.utcnow()
            else:
                edge = GraphEdge(
                    source=source,
                    target=target,
                    type=edge_type,
                    details=details or {},
                    weight=weight
                )
                db.add(edge)
            try:
                db.commit()
            except Exception as e:
                print(f"Error upserting edge {source}->{target}: {e}")
                db.rollback()

    def ingest_company_relationships(
        self,
        atlas_id: str,
        country: str,
        company_label: str,
        address: dict,
        executives=None,
        owners=None,
        executive_people=None,
        shareholder_people=None,
        source: str = "V4",
    ):
        executives = executives or []
        owners = owners or []
        executive_people = executive_people or []
        shareholder_people = shareholder_people or []

        # 1) Company node (existujúce)
        company_node_id = f"{country.lower()}_{atlas_id}"
        self.upsert_node(
            node_id=company_node_id,
            label=company_label or company_node_id,
            node_type="company",
            country=country,
            details={"atlas_id": atlas_id, "source": source},
        )

        # 2) Address node (existujúce) – len príklad
        if address:
            addr_label = address.get("raw") or f'{address.get("street","")} {address.get("city","")} {address.get("postal_code","")}'.strip()
            # Basic Address Node ID - improve if needed
            addr_hash = _sha12(f"{country}|{_norm_key(addr_label)}")
            addr_node_id = f"addr_{country.lower()}_{addr_hash}"
            
            self.upsert_node(
                node_id=addr_node_id,
                label=addr_label,
                node_type="address",
                country=country,
                details={"source": source, **address},
            )
            self.upsert_edge(company_node_id, addr_node_id, "LOCATED_AT", details={"source": source})

        # 3) Executives (prefer structured)
        if executive_people:
            for p in executive_people:
                name = (p or {}).get("name") or ""
                if not name:
                    continue
                pid = _person_node_id(country, name, (p or {}).get("birth_date", ""))
                self.upsert_node(
                    node_id=pid,
                    label=name,
                    node_type="person",
                    country=country,
                    details={
                        "role": (p or {}).get("role"),
                        "since": (p or {}).get("since"),
                        "until": (p or {}).get("until"),
                        "birth_date": (p or {}).get("birth_date"),
                        "residence_address": (p or {}).get("residence_address"),
                        "source": source,
                    },
                )
                self.upsert_edge(company_node_id, pid, "MANAGED_BY", details={"role": (p or {}).get("role"), "source": source})
        else:
            for name in executives:
                if not name:
                    continue
                pid = _person_node_id(country, name, "")
                self.upsert_node(pid, name, "person", country, details={"source": source})
                self.upsert_edge(company_node_id, pid, "MANAGED_BY", details={"source": source})

        # 4) Shareholders / Owners (prefer structured)
        if shareholder_people:
            for p in shareholder_people:
                name = (p or {}).get("name") or ""
                if not name:
                    continue

                # owner can be company_ref or person
                if _looks_like_legal_entity(name):
                    oid = _owner_node_id(country, name)
                    self.upsert_node(
                        node_id=oid,
                        label=name,
                        node_type="company_ref",
                        country=country,
                        details={"source": source},
                    )
                else:
                    oid = _person_node_id(country, name, (p or {}).get("birth_date", ""))
                    self.upsert_node(
                        node_id=oid,
                        label=name,
                        node_type="person",
                        country=country,
                        details={"source": source},
                    )

                self.upsert_edge(company_node_id, oid, "OWNED_BY", details={"source": source})
        else:
            for name in owners:
                if not name:
                    continue
                if _looks_like_legal_entity(name):
                    oid = _owner_node_id(country, name)
                    self.upsert_node(oid, name, "company_ref", country, details={"source": source})
                else:
                    oid = _person_node_id(country, name, "")
                    self.upsert_node(oid, name, "person", country, details={"source": source})
                self.upsert_edge(company_node_id, oid, "OWNED_BY", details={"source": source})

    def _base_graph_for_company(self, company_node_id: str) -> Dict:
        """Helper to get direct neighbors"""
        with get_db_session() as db:
            if not db:
                 return {"nodes": [], "edges": []}
            
            # Find edges from company
            out_edges = db.query(GraphEdge).filter(GraphEdge.source == company_node_id).all()
            
            nodes = {}
            edges = []

            # Add center node
            center = db.query(GraphNode).filter(GraphNode.id == company_node_id).first()
            if center:
                nodes[center.id] = {
                    "id": center.id, "label": center.label, "type": center.type, 
                    "country": center.country, "details": center.details
                }

            for e in out_edges:
                edges.append({"source": e.source, "target": e.target, "type": e.type, "details": e.details})
                # Fetch target node
                if e.target not in nodes:
                    t = db.query(GraphNode).filter(GraphNode.id == e.target).first()
                    if t:
                        nodes[t.id] = {
                            "id": t.id, "label": t.label, "type": t.type,
                            "country": t.country, "details": t.details
                        }
            
            return {"nodes": list(nodes.values()), "edges": edges}

    def fetch_edges_from(self, source_id: str, types: List[str]) -> List[Dict]:
        with get_db_session() as db:
            if not db: return []
            edges = db.query(GraphEdge).filter(
                GraphEdge.source == source_id,
                GraphEdge.type.in_(types)
            ).all()
            return [{"source": e.source, "target": e.target, "type": e.type} for e in edges]

    def fetch_edges_to_many(self, target_ids: List[str], types: List[str], limit: int) -> List[Dict]:
        with get_db_session() as db:
            if not db: return []
            edges = db.query(GraphEdge).filter(
                GraphEdge.target.in_(target_ids),
                GraphEdge.type.in_(types)
            ).limit(limit * 5).all() # higher limit for DB query
            return [{"source": e.source, "target": e.target, "type": e.type} for e in edges]

    def merge_graph(self, g1: Dict, g2: Dict) -> Dict:
        # Simple merge logic
        nodes = {n["id"]: n for n in g1.get("nodes", [])}
        for n in g2.get("nodes", []):
            nodes[n["id"]] = n
        
        edges = {(e["source"], e["target"], e["type"]): e for e in g1.get("edges", [])}
        for e in g2.get("edges", []):
            k = (e["source"], e["target"], e["type"])
            edges[k] = e
        
        return {"nodes": list(nodes.values()), "edges": list(edges.values())}

    def build_company_graph(self, atlas_id: str, country: str, limit_related_per_anchor: int = 20):
        anchor_company_id = f"{country.lower()}_{atlas_id}"

        graph = self._base_graph_for_company(anchor_company_id)

        # --- NEW: expand via people/owners ---
        # 1) find person/owner nodes connected to anchor
        anchors = self.fetch_edges_from(anchor_company_id, types=["MANAGED_BY", "OWNED_BY"])
        related_node_ids = [e["target"] for e in anchors]

        if not related_node_ids:
            return graph

        # 2) find other companies connected to those same nodes
        # (reverse edges: COMPANY -> PERSON/OWNER)
        # Note: In GraphEdge, source=Company, target=Person. So we want edges where Target matches related_node_ids
        other_edges = self.fetch_edges_to_many(related_node_ids, types=["MANAGED_BY", "OWNED_BY"], limit=limit_related_per_anchor)

        other_company_ids = []
        for e in other_edges:
            src = e["source"]
            # Exclude self and verify it looks like a company ID for that country
            if src != anchor_company_id and src.startswith(country.lower() + "_"):
                other_company_ids.append(src)

        other_company_ids = list(dict.fromkeys(other_company_ids))[:limit_related_per_anchor]

        # 3) pull nodes+edges for those companies and merge
        for cid in other_company_ids:
            sub = self._base_graph_for_company(cid)
            graph = self.merge_graph(graph, sub)

        # 4) optional summary
        graph.setdefault("summary", {})
        graph["summary"]["same_person_or_owner_companies"] = len(other_company_ids)

        return graph

# Singleton instance
graph_service = GraphService()
