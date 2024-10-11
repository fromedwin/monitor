# A project or a service have a status:
#   Unknown is the default value
#   Warning is about to be offline
#   Degraded is offline but not critical
#   Offline is ... not good
STATUS = {
    'UNKNOWN': 0,
    'WARNING': 1,
    'DEGRADED': 2,
    'OFFLINE': 3,
}

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

# Lighthouse formfactor choices
LIGHTHOUSE_FORMFACTORS = {
    'DESKTOP': 0,
    'MOBILE': 1,
}

LIGHTHOUSE_FORMFACTOR_CHOICES = [
    (LIGHTHOUSE_FORMFACTORS['DESKTOP'], 'Desktop'),
    (LIGHTHOUSE_FORMFACTORS['MOBILE'], 'Mobile'),
]

# notification colors for bubble
NOTIFICATION_SEVERITY = {
    'UNKNOWN': 0,
    'WARNING': 1,
    'CRITICAL': 2,
    'RESOLVED': 3,
}

NOTIFICATION_SEVERITY_CHOICES = [
    (NOTIFICATION_SEVERITY['UNKNOWN'], 'unknown'),
    (NOTIFICATION_SEVERITY['WARNING'], 'warning'),
    (NOTIFICATION_SEVERITY['CRITICAL'], 'critical'),
    (NOTIFICATION_SEVERITY['RESOLVED'], 'resolved'),
]
