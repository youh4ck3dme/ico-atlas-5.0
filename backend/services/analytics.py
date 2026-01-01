"""
Analytics service pre ILUMINATI SYSTEM
Zbieranie a agregácia metrík pre business intelligence
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import func, and_, extract
from sqlalchemy.orm import Session

from services.database import (
    get_db_session,
    SearchHistory,
    Analytics,
    CompanyCache,
)
from services.auth import User


def get_search_trends(
    days: int = 30,
    group_by: str = "day",  # day, week, month
    user_id: Optional[int] = None,
) -> Dict:
    """
    Vráti trendy vyhľadávaní za posledných N dní.
    
    Args:
        days: Počet dní späť
        group_by: Agregácia (day, week, month)
        user_id: Filtrovať podľa používateľa (ak None, všetci)
    
    Returns:
        {
            "period": "day" | "week" | "month",
            "data": [
                {"date": "2024-12-01", "count": 10, "countries": {"SK": 5, "CZ": 5}},
                ...
            ],
            "total": 150,
            "peak_hour": 14,
            "peak_day": "Monday"
        }
    """
    with get_db_session() as session:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = session.query(SearchHistory).filter(
            SearchHistory.search_timestamp >= start_date
        )
        
        if user_id:
            # Ak máme user_id v SearchHistory, filtrujeme
            # Pre teraz používame všetky záznamy
            pass
        
        # Agregácia podľa dátumu
        if group_by == "day":
            date_expr = func.date(SearchHistory.search_timestamp)
        elif group_by == "week":
            date_expr = func.date_trunc("week", SearchHistory.search_timestamp)
        elif group_by == "month":
            date_expr = func.date_trunc("month", SearchHistory.search_timestamp)
        else:
            date_expr = func.date(SearchHistory.search_timestamp)
        
        # Získať počet vyhľadávaní podľa dátumu a krajiny
        results = (
            session.query(
                date_expr.label("date"),
                SearchHistory.country,
                func.count(SearchHistory.id).label("count"),
            )
            .filter(SearchHistory.search_timestamp >= start_date)
            .group_by(date_expr, SearchHistory.country)
            .order_by(date_expr)
            .all()
        )
        
        # Agregovať do formátu
        data_dict = {}
        for date, country, count in results:
            date_str = date.isoformat() if isinstance(date, datetime) else str(date)
            if date_str not in data_dict:
                data_dict[date_str] = {"date": date_str, "count": 0, "countries": {}}
            data_dict[date_str]["count"] += count
            if country:
                data_dict[date_str]["countries"][country] = (
                    data_dict[date_str]["countries"].get(country, 0) + count
                )
        
        data = list(data_dict.values())
        total = sum(item["count"] for item in data)
        
        # Peak hour
        hour_counts = (
            session.query(
                extract("hour", SearchHistory.search_timestamp).label("hour"),
                func.count(SearchHistory.id).label("count"),
            )
            .filter(SearchHistory.search_timestamp >= start_date)
            .group_by(extract("hour", SearchHistory.search_timestamp))
            .all()
        )
        peak_hour = max(hour_counts, key=lambda x: x[1])[0] if hour_counts else None
        
        # Peak day
        day_counts = (
            session.query(
                extract("dow", SearchHistory.search_timestamp).label("day"),
                func.count(SearchHistory.id).label("count"),
            )
            .filter(SearchHistory.search_timestamp >= start_date)
            .group_by(extract("dow", SearchHistory.search_timestamp))
            .all()
        )
        peak_day_num = max(day_counts, key=lambda x: x[1])[0] if day_counts else None
        day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        peak_day = day_names[int(peak_day_num)] if peak_day_num is not None else None
        
        return {
            "period": group_by,
            "data": data,
            "total": total,
            "peak_hour": int(peak_hour) if peak_hour is not None else None,
            "peak_day": peak_day,
        }


def get_risk_distribution(
    days: int = 30,
    user_id: Optional[int] = None,
) -> Dict:
    """
    Vráti distribúciu risk skóre.
    
    Returns:
        {
            "distribution": [
                {"score": 0, "count": 10, "percentage": 5.0},
                {"score": 1, "count": 20, "percentage": 10.0},
                ...
            ],
            "high_risk_count": 15,  # score >= 7
            "medium_risk_count": 30,  # score 4-6
            "low_risk_count": 50,  # score 0-3
            "average_score": 3.5
        }
    """
    with get_db_session() as session:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = session.query(SearchHistory).filter(
            and_(
                SearchHistory.search_timestamp >= start_date,
                SearchHistory.risk_score.isnot(None),
            )
        )
        
        results = query.all()
        
        # Distribúcia podľa skóre
        distribution = {}
        total = 0
        high_risk = 0
        medium_risk = 0
        low_risk = 0
        score_sum = 0
        
        for result in results:
            score = int(result.risk_score) if result.risk_score else 0
            distribution[score] = distribution.get(score, 0) + 1
            total += 1
            score_sum += score
            
            if score >= 7:
                high_risk += 1
            elif score >= 4:
                medium_risk += 1
            else:
                low_risk += 1
        
        # Formátovať distribúciu
        dist_data = []
        for score in range(11):  # 0-10
            count = distribution.get(score, 0)
            percentage = (count / total * 100) if total > 0 else 0
            dist_data.append({
                "score": score,
                "count": count,
                "percentage": round(percentage, 2),
            })
        
        average_score = (score_sum / total) if total > 0 else 0
        
        return {
            "distribution": dist_data,
            "high_risk_count": high_risk,
            "medium_risk_count": medium_risk,
            "low_risk_count": low_risk,
            "average_score": round(average_score, 2),
            "total": total,
        }


def get_user_activity(
    days: int = 30,
) -> Dict:
    """
    Vráti aktivitu používateľov.
    
    Returns:
        {
            "active_users": 50,
            "new_users": 10,
            "retention_rate": 75.5,  # %
            "tier_distribution": {
                "free": 40,
                "pro": 8,
                "enterprise": 2
            },
            "feature_usage": {
                "search": 1000,
                "export": 50,
                "api": 200
            }
        }
    """
    with get_db_session() as session:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Aktívni používatelia (mali aspoň 1 search)
        active_users = (
            session.query(func.count(func.distinct(SearchHistory.user_ip)))
            .filter(SearchHistory.search_timestamp >= start_date)
            .scalar()
        ) or 0
        
        # Noví používatelia (registrovaní v období)
        new_users = (
            session.query(func.count(User.id))
            .filter(User.created_at >= start_date)
            .scalar()
        ) or 0
        
        # Tier distribúcia
        tier_dist = (
            session.query(User.tier, func.count(User.id))
            .group_by(User.tier)
            .all()
        )
        tier_distribution = {tier or "free": count for tier, count in tier_dist}
        
        # Feature usage z Analytics
        feature_usage = (
            session.query(
                Analytics.event_type,
                func.count(Analytics.id).label("count"),
            )
            .filter(Analytics.timestamp >= start_date)
            .group_by(Analytics.event_type)
            .all()
        )
        feature_usage_dict = {event: count for event, count in feature_usage}
        
        # Retention rate (zjednodušené - používatelia s viac ako 1 search)
        users_with_multiple_searches = (
            session.query(SearchHistory.user_ip)
            .filter(SearchHistory.search_timestamp >= start_date)
            .group_by(SearchHistory.user_ip)
            .having(func.count(SearchHistory.id) > 1)
            .count()
        )
        retention_rate = (
            (users_with_multiple_searches / active_users * 100)
            if active_users > 0
            else 0
        )
        
        return {
            "active_users": active_users,
            "new_users": new_users,
            "retention_rate": round(retention_rate, 2),
            "tier_distribution": tier_distribution,
            "feature_usage": feature_usage_dict,
        }


def get_api_usage(
    days: int = 30,
    api_key_id: Optional[int] = None,
) -> Dict:
    """
    Vráti štatistiky API použitia.
    
    Returns:
        {
            "total_calls": 1000,
            "calls_per_day": 33.3,
            "most_used_endpoints": [
                {"endpoint": "/api/search", "count": 800},
                {"endpoint": "/api/company", "count": 200}
            ],
            "error_rate": 2.5,  # %
            "average_response_time": 250,  # ms
            "usage_by_key": [
                {"key_id": 1, "key_name": "Production", "calls": 500},
                ...
            ]
        }
    """
    with get_db_session() as session:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Z Analytics tabuľky získame API volania
        api_events = (
            session.query(Analytics)
            .filter(
                and_(
                    Analytics.timestamp >= start_date,
                    Analytics.event_type.in_(["api_call", "search"]),
                )
            )
            .all()
        )
        
        total_calls = len(api_events)
        calls_per_day = total_calls / days if days > 0 else 0
        
        # Endpoint usage (z event_data)
        endpoint_counts = {}
        error_count = 0
        
        for event in api_events:
            if event.event_data:
                endpoint = event.event_data.get("endpoint", "unknown")
                endpoint_counts[endpoint] = endpoint_counts.get(endpoint, 0) + 1
                
                if event.event_data.get("status_code", 200) >= 400:
                    error_count += 1
        
        most_used = sorted(
            [
                {"endpoint": endpoint, "count": count}
                for endpoint, count in endpoint_counts.items()
            ],
            key=lambda x: x["count"],
            reverse=True,
        )[:10]
        
        error_rate = (error_count / total_calls * 100) if total_calls > 0 else 0
        
        # Usage by API key (ak máme API keys tracking)
        # Pre teraz vrátime prázdny zoznam
        usage_by_key = []
        
        return {
            "total_calls": total_calls,
            "calls_per_day": round(calls_per_day, 2),
            "most_used_endpoints": most_used,
            "error_rate": round(error_rate, 2),
            "average_response_time": None,  # Potrebuje tracking response time
            "usage_by_key": usage_by_key,
        }


def get_dashboard_summary() -> Dict:
    """
    Vráti súhrn pre analytics dashboard.
    
    Returns:
        {
            "search_trends": {...},
            "risk_distribution": {...},
            "user_activity": {...},
            "api_usage": {...}
        }
    """
    return {
        "search_trends": get_search_trends(days=30, group_by="day"),
        "risk_distribution": get_risk_distribution(days=30),
        "user_activity": get_user_activity(days=30),
        "api_usage": get_api_usage(days=30),
    }

