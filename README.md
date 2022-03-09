1. Created URL after extracting asin and country from the xlsx file.
2. Filter out webpages with status code 200 and skip the ones with status code 404.
3. Beautiful Soup is applied on working webpages and relevant data(title,price,imageUrl,details) is extracted.
4. Extracted data is then stored in a Dictionary named {data}.
5. Finally wrote the data to a JSON file name sample.json.
6. Bonus : database of name "amazon_database" is created with columns {title, image, price, details}.
