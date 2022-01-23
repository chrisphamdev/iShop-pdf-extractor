# New World iShop PDF Extractor

During my time at New World Stonefields (summer of 2021-2022), I have noticed the incredible, complex Excel lookup sheet my team has created, and this is my attempt at automating most of that process (since it still requires a lot of complex steps).

For context, our customers would order their groceries online and my team will be the ones picking their groceries and sending them to their homes. Most of the stuff we would just pick off the shop shelves, but for certain items, specifically butchery, deli, and seafood items, we would have to make customs orders to the respective departments at the start of the day, since they are in specific weight/quantity and sometimes customers have special requirements too.

When I started with the team, our team leader would spend half an hour every morning copying and pasting a whole pdf file into an Excel sheet that someone has (brilliantly) created. But still, the process is lengthy and time-consuming, since we still have to manually add/remove specific filters and sort the items by their IDs. My project helps shorten that process to the press of a button. The program will ask for the name of the input PDF file and will produce a single CSV file that contains all of the products that need to be ordered. You're welcome, Alex :)

This project comes as a single Python file for simplicity, as well as a converted executable file.


## Requirements

To use the Python file, install `pdfplumber` using the following command

```bash
pip install pdfplumber
```

