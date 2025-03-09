## Indian Cattle Breed Data

Data for 50 Indian Cattle Breeds.
This project collects and processes data for 51 Indian cattle breeds. The data is fetched from [Animal Genetic Resources of India](http://14.139.252.116:8080/appangr/openagr.htm)


### Data Fields

- **Id**
- **Breed**
- **State**
- **Places**
- **Longitude**
- **Latitude**
- **Population**
- **Synonyms**
- **Origin**
- **Major utility**
- **Comments on utility**
- **Comments on breeding tract**
- **Adaptability to environment**
- **Management system**
- **Mobility**
- **Feeding of adults**
- **Comments on Management**
- **Colour**
- **Horn shape and size**
- **Visible characteristics**
- **Height (avg. cm.)**
- **Body Length (avg. cm.)**
- **Heart girth (avg. cm.)**
- **Body weight (avg. kg.)**
- **Birth weight (avg. kg.)**
- **Litter size born**
- **Age at first parturition (months)**
- **Parturition interval (months)**
- **Milk yield per lactation (kg)**
- **Milk Fat (%)**
- **Any Peculiarity of the breed**

### Usage
Directly Download the data from this Repository. OR download it using the script - 
1. Ensure you have Python installed on your system.
2. Install the required libraries using the following command:
   ```sh
   pip install requests beautifulsoup4
   ```
3. Run the script to fetch and process the data:
    ```sh
    python script.py
    ```
4. The Data will be written to data.csv in the same directory.

Notes
- The script downloads images for each breed and saves them in the images directory.
- The script handles inconsistent data by using default values for missing fields.