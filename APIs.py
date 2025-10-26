APIS = [
    {
        "url": "https://www.volunteerconnector.org/api/search/",
        "params": {"limit": 50},
        "headers": {"User-Agent": "Mozilla/5.0"}
    },
    {
        "url": "https://api.volunteermatch.org/api/v2/opportunities",
        "params": {"location": "San Jose", "limit": 50},
        "headers": {"User-Agent": "Mozilla/5.0"}
    },
    {
        "url": "https://pointapp.org/api/events",
        "params": {"location": "San Jose", "limit": 50},
        "headers": {"User-Agent": "Mozilla/5.0"}
    },
    {
        "url": "https://api.goldenvolunteer.com/v1/opportunities",
        "params": {"city": "San Jose", "limit": 50},
        "headers": {"User-Agent": "Mozilla/5.0"}
    },
    {
        "url": "https://api.every.org/v0.2/search/volunteer",
        "params": {"limit": 50},  # Optional: customize limit
        "headers": {"User-Agent": "Mozilla/5.0"},
        "notes": "Every.org nonprofit metadata API"
    }
]
