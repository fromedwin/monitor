# Incidents from alertmanager can have an unknown status, be firing, or be resolved.
INCIDENT_STATUS = {
    'UNKNOWN': 0,
    'RESOLVED': 1,
    'FIRING': 2,
}

INCIDENT_STATUS_CHOICES = [
    (INCIDENT_STATUS['UNKNOWN'], 'unknown'),
    (INCIDENT_STATUS['RESOLVED'], 'resolved'),
    (INCIDENT_STATUS['FIRING'], 'firing'),
]

# Incidents from alertmanager can have an unknown, a warning, or a critical severity.
INCIDENT_SEVERITY = {
    'UNKNOWN': 0,
    'WARNING': 1,
    'CRITICAL': 2,
}

INCIDENT_SEVERITY_CHOICES = [
    (INCIDENT_SEVERITY['UNKNOWN'], 'unknown'),
    (INCIDENT_SEVERITY['WARNING'], 'warning'),
    (INCIDENT_SEVERITY['CRITICAL'], 'critical'),
]
