# APIs list
APIS = [
    {
        "url": "https://www.volunteerconnector.org/api/search/",
        "params": {"limit": 50},
        "headers": {"User-Agent": "Mozilla/5.0"}
        # "Authorization": "Bearer YOUR_API_KEY"  # if needed
    },
    {
        "url": "https://api.volunteermatch.org/api/v2/opportunities",
        "params": {"location": "San Jose", "limit": 50},
        "headers": {"User-Agent": "Mozilla/5.0"}
        # "Authorization": "Bearer YOUR_API_KEY"  # if needed
    }
]
