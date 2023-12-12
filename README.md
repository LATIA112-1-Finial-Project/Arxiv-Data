# Arxiv-Data

This series of Python scripts aims to scrape the [arxiv.org](https://arxiv.org/) website for the annual publication counts of papers in various categories within different fields. The data is then stored in corresponding CSV files based on categories, facilitating further analysis and research in the future.

## Dependancy

- requirements.txt

  Run the following command to install all the required packages:

  ```bash
  $ pip install -r requirements.txt
  ```

## How To Use

1. Clone the repository and go to the directory

   ```bash
   $ git clone https://github.com/LATIA112-1-Finial-Project/Arxiv-Data.git
   $ cd Arxiv-Data
   ```

2. Install dependencies

   ```bash
   $ pip install -r requirements.txt
   ```

3. Run the following command to execute the script.

   ```bash
   $ python3 scripts/arxiv_crawler.py
   ```

The resulting CSV files are stored in folder named `outputs/`, and each file is named by their field and category `ex. Physics_Astrophysics.csv`.
