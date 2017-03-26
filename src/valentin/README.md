# Valentin README

## Filtered arrays:
Filter suppliers & currencies arrays.
Suppliers threshold: 2
Currencies threshold: 20
All items with occurances less than the threshold are considered in 'Others class'

## Filtered arrays results:
Currency: 0.933 
Supplier: 0.63

## token_pattern='.*' Results
Results fell down: 
0.8866666666666667 for currencies
0.574 for suppliers

## Total amounts experiments

### Part 1 (tests on train + test set)
Features:
Has dot -> indicates wether the line of the price contains dot
Has comma -> indicates wether the line of the price contains comma
Has total word -> indicates wether the line of the price contains 'total'
Digits count -> the number of all the digits on the line
Order of occurance -> normalised (0-1) order of occurance compared to all prices in the receipt

TOP 1 Accuracy: 0.45
TOP 2 Accuracy: 0.56

### Part 2 (tests on train + test set)
Remove features: Has dot, Has comma
Only consider prices with dot/comma

TOP 1 Accuracy: 0.47
TOP 2 Accuracy: 0.57

### Part 3 (tests on train + test set)
Add Can be sum feature: indicates wether a price can be sum of other prices
TOP 1 Accuracy: 0.54
TOP 2 Accuracy: 0.6

### Part 4 (tests on train + test set)
RandomForest: n_estimators=50
TOP 1 Accuracy: 0.54
TOP 2 Accuracy: 0.6

### Part 5 (TESTS ONLY ON TEST SET!)
Add tf idf feature
TOP 1 Accuracy: 0.531
TOP 2 Accuracy: 0.604
TOP 3 Accuracy: 0.623
