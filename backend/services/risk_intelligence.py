"""
Risk Intelligence služba
Detekcia bielych koní, karuselových štruktúr a vylepšený risk scoring
"""

from typing import Dict, List, Set
from collections import defaultdict, Counter


def detect_white_horse(nodes: List[Dict], edges: List[Dict]) -> Dict[str, int]:
    """
    Detekuje "bielych koní" - osoby, ktoré sú konateľmi v príliš veľkom počte firiem.
    
    Returns:
        Dict s person_id -> počet firiem
    """
    # Zistiť, koľko firiem má každá osoba
    person_companies = defaultdict(set)
    
    for edge in edges:
        if edge.get("type") == "MANAGED_BY":
            source = edge.get("source")
            target = edge.get("target")
            
            # Nájsť typy uzlov
            source_node = next((n for n in nodes if n.get("id") == source), None)
            target_node = next((n for n in nodes if n.get("id") == target), None)
            
            if source_node and target_node:
                if source_node.get("type") == "company" and target_node.get("type") == "person":
                    person_companies[target].add(source)
    
    # Filtrovať osoby s viac ako 5 firmami
    white_horses = {
        person_id: len(companies)
        for person_id, companies in person_companies.items()
        if len(companies) >= 5
    }
    
    return white_horses


def detect_circular_structures(nodes: List[Dict], edges: List[Dict]) -> List[List[str]]:
    """
    Detekuje karuselové štruktúry - kruhové vlastníctvo medzi firmami.
    
    Returns:
        List kruhových štruktúr (každá je list node IDs)
    """
    # Vytvoriť graf vlastníctva
    ownership_graph = defaultdict(set)
    
    for edge in edges:
        if edge.get("type") == "OWNED_BY":
            source = edge.get("source")
            target = edge.get("target")
            
            source_node = next((n for n in nodes if n.get("id") == source), None)
            target_node = next((n for n in nodes if n.get("id") == target), None)
            
            if source_node and target_node:
                if source_node.get("type") == "company" and target_node.get("type") == "company":
                    ownership_graph[source].add(target)
    
    # Hľadať cykly v grafe (jednoduchá BFS verzia)
    circular_structures = []
    visited = set()
    
    def find_cycle(start: str, path: List[str]) -> List[str]:
        if start in path:
            # Našli sme cyklus
            cycle_start = path.index(start)
            return path[cycle_start:]
        
        if start in visited:
            return []
        
        visited.add(start)
        path.append(start)
        
        for neighbor in ownership_graph.get(start, []):
            cycle = find_cycle(neighbor, path.copy())
            if cycle:
                return cycle
        
        return []
    
    for node_id in ownership_graph:
        if node_id not in visited:
            cycle = find_cycle(node_id, [])
            if cycle and len(cycle) >= 3:  # Minimálne 3 uzly pre karusel
                circular_structures.append(cycle)
    
    return circular_structures


def detect_virtual_seats(nodes: List[Dict], edges: List[Dict]) -> Dict[str, int]:
    """
    Detekuje virtuálne sídla - adresy s viacerými firmami.
    
    Returns:
        Dict s address_id -> počet firiem
    """
    address_companies = defaultdict(set)
    
    for edge in edges:
        if edge.get("type") == "LOCATED_AT":
            source = edge.get("source")
            target = edge.get("target")
            
            source_node = next((n for n in nodes if n.get("id") == source), None)
            target_node = next((n for n in nodes if n.get("id") == target), None)
            
            if source_node and target_node:
                if source_node.get("type") == "company" and target_node.get("type") == "address":
                    address_companies[target].add(source)
    
    # Filtrovať adresy s viac ako 3 firmami
    virtual_seats = {
        address_id: len(companies)
        for address_id, companies in address_companies.items()
        if len(companies) >= 3
    }
    
    return virtual_seats


def calculate_enhanced_risk_score(
    node: Dict,
    nodes: List[Dict],
    edges: List[Dict],
    white_horses: Dict[str, int] = None,
    circular_structures: List[List[str]] = None,
    virtual_seats: Dict[str, int] = None
) -> int:
    """
    Vylepšený risk score algoritmus s použitím risk intelligence.
    
    Args:
        node: Uzol pre ktorý počítame risk score
        nodes: Všetky uzly
        edges: Všetky hrany
        white_horses: Dict bielych koní (ak už vypočítané)
        circular_structures: List karuselových štruktúr (ak už vypočítané)
        virtual_seats: Dict virtuálnych sídel (ak už vypočítané)
    """
    if white_horses is None:
        white_horses = detect_white_horse(nodes, edges)
    if circular_structures is None:
        circular_structures = detect_circular_structures(nodes, edges)
    if virtual_seats is None:
        virtual_seats = detect_virtual_seats(nodes, edges)
    
    score = node.get("risk_score", 0)
    node_id = node.get("id")
    
    # Biely kôň bonus
    if node.get("type") == "person" and node_id in white_horses:
        company_count = white_horses[node_id]
        if company_count >= 10:
            score += 5
        elif company_count >= 5:
            score += 3
    
    # Karuselová štruktúra bonus
    if node.get("type") == "company":
        for cycle in circular_structures:
            if node_id in cycle:
                score += 4
                break
    
    # Virtual seat bonus
    if node.get("type") == "address" and node_id in virtual_seats:
        company_count = virtual_seats[node_id]
        if company_count >= 20:
            score += 4
        elif company_count >= 10:
            score += 2
    
    # Dlh bonus
    if node.get("type") == "debt":
        score = max(score, 8)  # Dlh je vždy vysoké riziko
    
    return min(score, 10)  # Max 10


def generate_risk_report(nodes: List[Dict], edges: List[Dict]) -> Dict:
    """
    Generuje kompletný risk report pre graf.
    
    Returns:
        Dict s risk analýzou
    """
    white_horses = detect_white_horse(nodes, edges)
    circular_structures = detect_circular_structures(nodes, edges)
    virtual_seats = detect_virtual_seats(nodes, edges)
    
    # Vypočítať vylepšené risk scores
    enhanced_nodes = []
    for node in nodes:
        enhanced_node = node.copy()
        enhanced_node["risk_score"] = calculate_enhanced_risk_score(
            node, nodes, edges, white_horses, circular_structures, virtual_seats
        )
        enhanced_nodes.append(enhanced_node)
    
    return {
        "white_horses": white_horses,
        "circular_structures": circular_structures,
        "virtual_seats": virtual_seats,
        "enhanced_nodes": enhanced_nodes,
        "summary": {
            "white_horse_count": len(white_horses),
            "circular_structure_count": len(circular_structures),
            "virtual_seat_count": len(virtual_seats),
            "high_risk_companies": len([n for n in enhanced_nodes if n.get("type") == "company" and n.get("risk_score", 0) >= 7])
        }
    }

