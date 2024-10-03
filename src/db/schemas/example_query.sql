SELECT 
    r.report_id,
    r.event_id,
    r.threat_actor,
    r.malware_family,
    r.target_sector,
    r.risk_score,
    r.threat_level,
    r.incident_duration,
    r.estimated_cost,
    r.impact_assessment,
    r.executive_summary
FROM 
    intelligence_reports r
WHERE 
    r.threat_level = 'high'
    AND r.risk_score > 80
ORDER BY 
    r.incident_duration DESC;