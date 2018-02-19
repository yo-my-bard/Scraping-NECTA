# Scraping-NECTA
Python modules to scrape data from the NECTA test results webpages.

This repository is of a scraping method for the Tanzanian NECTA website. The education data is rather large, however, it is in the form of HTML Tables with no means to download the full dataset. At least none that I have been able to find to date. I used Python to circumvent having to copy-paste the tables into an Excel sheet and then editing them accordingly (Full disclosure: that was indeed the best idea on hand once.)
Please note that while this code is Open Source and you are more than welcome to use it with attributions, I have added datasets that I have already compiled using the modules in the "CompleteDatasets" folder. Unless you have specific changes that you need, I don't recommend re-running the modules as they take a long time to run and are a stress on the NECTA servers.

## How To Navigate This Repository
1) Check to see if your dataset is available in the CompleteDatasets folder.
2) Clone and customize the modules for your need (year of interest, exam of interest, databases, etc.)
3) Use docstrings/comments as a guide
4) Submit pull requests for any issues, documentation clarity, or added features!
