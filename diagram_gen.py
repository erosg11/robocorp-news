"""Program to generate a diagram of robocorp news."""

from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Users
from diagrams.generic.storage import Storage
from pathlib import Path

with Diagram("Robocorp News Workflow", show=False, filename='./docs/diagram', outformat='png') as diag:
    user = Users("User")
    workitem_input = Storage("WorkItem (Input)")

    pwd = Path('.').absolute()

    with Cluster("Task 1: Data Generation"):
        data_generation = Server("Generate Data")
        news_sites = [
            Custom("AP News", str(pwd / "docs/logos/apnews.png")),
            Custom("Yahoo", str(pwd / "docs/logos/yahoo.png")),
            Custom("Reuters", str(pwd / "docs/logos/reuters.png")),
            Custom("Al Jazeera", str(pwd / "docs/logos/aljazeera.png")),
            Custom("LA Times", str(pwd / "docs/logos/latimes.png")),
            Custom("Gothamist", str(pwd / "docs/logos/gothamist.png")),
        ]

    with Cluster("Task 2: Image Download"):
        image_download = Server("Download Images")
        workitem_updated = Storage("WorkItem (Updated)")

    with Cluster("Task 3: Data Analysis and Artifact Generation"):
        workitem_images = Storage("WorkItem (Images)")
        data_analysis = Server("Analyze Data")
    artifacts = Storage("Artifacts (Images + Spreadsheet)")

    user >> workitem_input >> data_generation
    for site in news_sites:
        data_generation >> site

    data_generation >> workitem_updated >> image_download
    image_download >> workitem_images >> data_analysis >> artifacts
