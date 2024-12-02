import pandas as pd
from order_processor import process_df

# Load the CSV files
df1 = pd.read_csv('Submission CSVs/11501721 -> 23414090.csv')
df1_results = pd.read_csv('Graded CSVs/psa-order-23414090.csv')
df2 = pd.read_csv('Submission CSVs/11639066 -> 23574072.csv')
df2_results = pd.read_csv('Graded CSVs/psa-order-23574072.csv')
df3 = pd.read_csv('Submission CSVs/11703773 -> 23614589.csv')
df3_results = pd.read_csv('Graded CSVs/psa-order-23614589.csv')
df4 = pd.read_csv('Submission CSVs/11892655 -> 23838313.csv')
df4_results = pd.read_csv('Graded CSVs/psa-order-23838313.csv')
df5 = pd.read_csv('Submission CSVs/12089275 -> 24040117.csv')
df5_results = pd.read_csv('Graded CSVs/psa-order-24040117.csv')
df6 = pd.read_csv('Submission CSVs/12128446 -> 24083941.csv')
df6_results = pd.read_csv('Graded CSVs/psa-order-24083941.csv')
df7 = pd.read_csv('Submission CSVs/12201380 -> 24186268.csv')
df7_results = pd.read_csv('Graded CSVs/psa-order-24186268.csv')
df8 = pd.read_csv('Submission CSVs/12231542 -> 24211002.csv')
df8_results = pd.read_csv('Graded CSVs/psa-order-24211002.csv')
df9 = pd.read_csv('Submission CSVs/12304040 -> 24245643.csv')
df9_results = pd.read_csv('Graded CSVs/psa-order-24245643.csv')

# Clean and Process the data
df1 = process_df(df1, df1_results, 23414090, [(0, 17)], [], [])
df2_i = process_df(df2, df2_results, 23574072, [(0, 13)], [2, 3, 4, 5, 6, 7, 9, 11, 12], [82441107, 82441108, 82441109, 82441110, 82441111, 82441112, 82441113, 82441114, 82441115, 82441116, 82441117, 82441118, 82441121, 82441123, 82441124])
df2_ii = process_df(df2, df2_results, 23574072, [(16, 36)], [29, 31, 32, 34], [82441142, 82441144, 82441145, 82441147])
df2 = pd.concat([df2_i, df2_ii], ignore_index=True)
df3 = process_df(df3, df3_results, 23614589, [(0, 13)], [], [])
df4 = process_df(df4, df4_results, 23838313, [(0, 16)], [], [])
df5_i = process_df(df5, df5_results, 24040117, [(13, 30)], [], [])
df5_ii = process_df(df5, df5_results, 24040117, [(81, 96)], [84, 85, 90, 91, 92, 94, 95], [91486691, 91486692, 91486697, 91486698, 91486699, 91486701, 91486702])
df5 = pd.concat([df5_i, df5_ii], ignore_index=True)
df6 = process_df(df6, df6_results, 24083941,[(58, 79)], [65], [92779530])
df7 = process_df(df7, df7_results, 24186268, [(68, 93)], [], [])
df8 = process_df(df8, df8_results, 24211002, [(30, 53)], [36, 41, 43, 48], [94641733, 94641738, 94641740, 94641745])
df9 = process_df(df9, df9_results, 24245643, [(18, 31)], [19, 24], [95270532, 95270537])

# # Combine into one DF
total = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9], ignore_index=True)

# Save the processed data
df1.to_csv('analyzed1.csv', index=False)
df2.to_csv('analyzed2.csv', index=False)
df3.to_csv('analyzed3.csv', index=False)
df4.to_csv('analyzed4.csv', index=False)
df5.to_csv('analyzed5.csv', index=False)
df6.to_csv('analyzed6.csv', index=False)
df7.to_csv('analyzed7.csv', index=False)
df8.to_csv('analyzed8.csv', index=False)
df9.to_csv('analyzed9.csv', index=False)
total.to_csv('total_orders.csv', index=False)
