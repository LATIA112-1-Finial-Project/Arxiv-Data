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

3. Navigate to the corresponding folder and run the following command to execute the script, their are three folders in this repository:

   1. `BO/`: In this folder, run the command below to get the data from Computer Science and Mathematics field.

      ```bash
      $ python3 computer\ science.py
      $ python3 mathematics.py
      ```

   2. `LUNG/`: In this folder, run the command below to get the data from Quantitative Biology, Quantitative Finance, Statistics, Electrical Engineering and Systems Science, and Economics field.

      ```bash
      $ python3 TRY.py
      ```

   3. `Ryan/`: In this folder, run the command below to get the data from Physics field.
      ```bash
      $ python3 arxiv_crawler.py
      ```
