import requests


class Mappings:
    def __init__(self):
        self.AWSDevAccountId = "478514063279"

        self.mappings = {
            "VPCResourcesMap":
                {
                    "dev": {
                        "Route53PublicZone": "Z2J9FAP6G28MU4", # Hosted Zone ID
                    },
                }
        }

        # The IP ranges below are used for Cloudflare's access to ELB resources. These ranges may change periodically
        try:
            self.cloudflare_ipv4_ranges = requests.get("https://www.cloudflare.com/ips-v4").text.split()
            self.cloudflare_ipv6_ranges = requests.get("https://www.cloudflare.com/ips-v6").text.split()
        except Exception as e:
            raise e
