from rich import print
import requests
import json
import fire
from os.path import getsize
import http

# Primary app class
class Monitor(object):
    def __init__(self):
        # Tries to read the sites dot JSON which stores the users added URLs
        try:
            with open("sites.json", "r") as f:
                if getsize("sites.json") > 0:
                    self.sites = json.load(f)
                else:
                    self.sites = []
        # If the file does not exist just create a new file and initalize an empty array
        except:
            with open("sites.json", "x") as f:
                pass
            self.sites = []
    
    def status(self):
        """Returns the status of all websites in the sites array"""
        if len(self.sites) == 0:
            print("[yellow]:warning: No sites have been added. Use [cyan]'monitor add SITE METHOD'[/cyan] to add one[/yellow]")

        for site in self.sites:
            response = requests.request(site[1], site[0])
            # Check the response code of the response and print a resulta ccordingly with the status code, url, http method and elapsed time
            if response.status_code <= 100:
                print(f":information_source: [white]{response.status_code}[/white]", response.url, f"[cyan]{response.request.method}[/cyan]", f"({response.elapsed.total_seconds() * 1000} [cyan]ms[/cyan])")
            elif response.status_code >= 200 and response.status_code < 300:
                print(f":white_check_mark: [green]{response.status_code}[/green]", response.url, f"[cyan]{response.request.method}[/cyan]", f"({response.elapsed.total_seconds() * 1000} [cyan]ms[/cyan])")
            elif response.status_code >= 300 and response.status_code < 400:
                print(f":warning: [yellow]{response.status_code}[/yellow]", response.url, f"[cyan]{response.request.method}[/cyan]", f"({response.elapsed.total_seconds() * 1000} [cyan]ms[/cyan])")
            elif response.status_code >= 400 and response.status_code < 500:
                print(f":x: [red]{response.status_code}[/red]", response.url, f"[cyan]{response.request.method}[/cyan]", f"({response.elapsed.total_seconds() * 1000} [cyan]ms[/cyan])")
            elif response.status_code >= 500:
                print(f":x: [red bold]{response.status_code}[/red bold]", response.url, f"[cyan]{response.request.method}[/cyan]", f"({response.elapsed.total_seconds() * 1000} [cyan]ms[/cyan])")
    
    def add(self, site:str, method:http.HTTPMethod):
        """Adds a site to the sites array"""
        self.sites.append((site, method))
        with open("sites.json", "w") as f:
            json.dump(self.sites, f)
    
    def remove(self, site:str):
        """Removes a site from the sites array"""
        for obj in self.sites:
            if obj[0] == site:
                self.sites.remove(obj)
        with open("sites.json", "w") as f:
            json.dump(self.sites, f)


if __name__ == "__main__":
    fire.Fire(Monitor)