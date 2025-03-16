from IP2Location import IP2Location
from configs.configs import IP2LOCATION_FILE


class IPtoLocationParser:
    def __init__(self, logger):
        self.ip2location = IP2Location()
        self.ip2location.open(IP2LOCATION_FILE)
        self.logger = logger

    def get_location(self, ip):
        try:
            location_info = self.ip2location.get_all(ip)
            self.logger.info(f"Converted IP {ip} to location successfully.")
            return {
                "ip": ip,
                "country_short": location_info.country_short,
                "country_long": location_info.country_long,
                "region": location_info.region,
                "city": location_info.city,
            }
        except Exception as e:
            self.logger.error(f"Failed to convert IP {ip} to location: {e}")
            return self.default_location(ip)
