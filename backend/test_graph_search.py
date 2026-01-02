import requests
import json
import time

def test_graph_search():
    ico = "35763469" # Slovak Telekom
    url = f"http://localhost:8000/api/search?q={ico}&country=SK&graph=1&force_refresh=true"
    
    print(f"Testing Graph Search for {ico}...")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            nodes = data.get("nodes", [])
            edges = data.get("edges", [])
            print(f"Nodes: {len(nodes)}")
            print(f"Edges: {len(edges)}")
            
            # Check for person nodes
            person_nodes = [n for n in nodes if n.get("type") == "person"]
            print(f"Person Nodes: {len(person_nodes)}")
            for p in person_nodes[:3]:
                print(f" - {p.get('label')} ({p.get('id')})")
                
            # Check for other companies (cross-linking)
            company_nodes = [n for n in nodes if n.get("type") == "company"]
            print(f"Company Nodes: {len(company_nodes)}")
            for c in company_nodes:
                 if c.get("ico") != ico:
                     print(f"FOUND LINKED COMPANY: {c.get('label')} ({c.get('ico')})")

        else:
            print("Error:", response.text)

    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_graph_search()
