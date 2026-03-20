# RSS feed definitions organized by category and region

CATEGORY_FEEDS = {
    "World": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://www.theguardian.com/world/rss",
    ],
    "Politics": [
        "https://feeds.bbci.co.uk/news/politics/rss.xml",
        "https://www.theguardian.com/politics/rss",
        "https://rss.politico.com/politics-news.xml",
    ],
    "Tech": [
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "https://www.theguardian.com/technology/rss",
        "https://feeds.wired.com/wired/index",
        "https://techcrunch.com/feed/",
    ],
    "Science": [
        "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
        "https://www.theguardian.com/science/rss",
        "https://www.sciencedaily.com/rss/top/science.xml",
    ],
    "Sports": [
        "https://feeds.bbci.co.uk/sport/rss.xml",
        "https://www.theguardian.com/sport/rss",
        "https://www.espn.com/espn/rss/news",
    ],
    "Business": [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "https://www.theguardian.com/business/rss",
    ],
}

# Google News RSS by city/region — covers main cities from each continent
REGION_FEEDS = {
    # North America
    "New York": "https://news.google.com/rss/search?q=New+York&hl=en-US&gl=US&ceid=US:en",
    "Los Angeles": "https://news.google.com/rss/search?q=Los+Angeles&hl=en-US&gl=US&ceid=US:en",
    "Chicago": "https://news.google.com/rss/search?q=Chicago&hl=en-US&gl=US&ceid=US:en",
    "Toronto": "https://news.google.com/rss/search?q=Toronto&hl=en-CA&gl=CA&ceid=CA:en",
    "Mexico City": "https://news.google.com/rss/search?q=Mexico+City&hl=en-MX&gl=MX&ceid=MX:en",
    # Europe
    "London": "https://news.google.com/rss/search?q=London&hl=en-GB&gl=GB&ceid=GB:en",
    "Paris": "https://news.google.com/rss/search?q=Paris&hl=en-FR&gl=FR&ceid=FR:en",
    "Berlin": "https://news.google.com/rss/search?q=Berlin&hl=en-DE&gl=DE&ceid=DE:en",
    "Madrid": "https://news.google.com/rss/search?q=Madrid&hl=en-ES&gl=ES&ceid=ES:en",
    "Rome": "https://news.google.com/rss/search?q=Rome&hl=en-IT&gl=IT&ceid=IT:en",
    "Amsterdam": "https://news.google.com/rss/search?q=Amsterdam&hl=en-NL&gl=NL&ceid=NL:en",
    "Brussels": "https://news.google.com/rss/search?q=Brussels&hl=en-BE&gl=BE&ceid=BE:en",
    # Asia
    "Tokyo": "https://news.google.com/rss/search?q=Tokyo&hl=en-JP&gl=JP&ceid=JP:en",
    "Beijing": "https://news.google.com/rss/search?q=Beijing&hl=en-CN&gl=CN&ceid=CN:en",
    "Seoul": "https://news.google.com/rss/search?q=Seoul&hl=en-KR&gl=KR&ceid=KR:en",
    "Singapore": "https://news.google.com/rss/search?q=Singapore&hl=en-SG&gl=SG&ceid=SG:en",
    "Mumbai": "https://news.google.com/rss/search?q=Mumbai&hl=en-IN&gl=IN&ceid=IN:en",
    "Bangkok": "https://news.google.com/rss/search?q=Bangkok&hl=en-TH&gl=TH&ceid=TH:en",
    "Jakarta": "https://news.google.com/rss/search?q=Jakarta&hl=en-ID&gl=ID&ceid=ID:en",
    # Africa
    "Cairo": "https://news.google.com/rss/search?q=Cairo&hl=en-EG&gl=EG&ceid=EG:en",
    "Lagos": "https://news.google.com/rss/search?q=Lagos&hl=en-NG&gl=NG&ceid=NG:en",
    "Nairobi": "https://news.google.com/rss/search?q=Nairobi&hl=en-KE&gl=KE&ceid=KE:en",
    "Johannesburg": "https://news.google.com/rss/search?q=Johannesburg&hl=en-ZA&gl=ZA&ceid=ZA:en",
    "Casablanca": "https://news.google.com/rss/search?q=Casablanca&hl=en-MA&gl=MA&ceid=MA:en",
    # Latin America
    "Sao Paulo": "https://news.google.com/rss/search?q=Sao+Paulo&hl=en-BR&gl=BR&ceid=BR:en",
    "Buenos Aires": "https://news.google.com/rss/search?q=Buenos+Aires&hl=en-AR&gl=AR&ceid=AR:en",
    "Bogota": "https://news.google.com/rss/search?q=Bogota&hl=en-CO&gl=CO&ceid=CO:en",
    "Lima": "https://news.google.com/rss/search?q=Lima&hl=en-PE&gl=PE&ceid=PE:en",
    "Santiago": "https://news.google.com/rss/search?q=Santiago&hl=en-CL&gl=CL&ceid=CL:en",
    # Middle East
    "Dubai": "https://news.google.com/rss/search?q=Dubai&hl=en-AE&gl=AE&ceid=AE:en",
    "Tel Aviv": "https://news.google.com/rss/search?q=Tel+Aviv&hl=en-IL&gl=IL&ceid=IL:en",
    "Istanbul": "https://news.google.com/rss/search?q=Istanbul&hl=en-TR&gl=TR&ceid=TR:en",
    "Riyadh": "https://news.google.com/rss/search?q=Riyadh&hl=en-SA&gl=SA&ceid=SA:en",
    # Oceania
    "Sydney": "https://news.google.com/rss/search?q=Sydney&hl=en-AU&gl=AU&ceid=AU:en",
    "Melbourne": "https://news.google.com/rss/search?q=Melbourne&hl=en-AU&gl=AU&ceid=AU:en",
    "Auckland": "https://news.google.com/rss/search?q=Auckland&hl=en-NZ&gl=NZ&ceid=NZ:en",
}
