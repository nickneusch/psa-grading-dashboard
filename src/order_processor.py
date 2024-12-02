import pandas as pd
import re

def process_df(df, df_results, order_num, ranges, num_drops, cert_drops):
    # drop unneccesary columns
    df = df.drop(columns=['SPEC #', 'LN#'])
    # swap description and sport
    cols = list(df.columns)
    sport_index, desc_index = cols.index('SPORT'), cols.index('DESCRIPTION')
    cols[sport_index], cols[desc_index] = cols[desc_index], cols[sport_index]
    df = df[cols]

    # removing rows that are not taylor's
    for (l, r) in ranges:
        pre_range_df = df.iloc[:l].copy()
        df = df.iloc[l:r]


    # add rows based on quantity 
    # 
    # first find the amount of extra rows in those before the range
    sum_extra_before = 0
    for index, row in pre_range_df.iterrows():
        qty = row['QTY']
        if qty > 1:
            sum_extra_before += (qty-1)
    # 
    # now find the amount of extra rows in the range
    expanded_rows = pd.DataFrame(columns=df.columns)
    sum_extra_after = 0
    sum_dropped_after = 0
    # iterate through the df and duplicate rows based on quantity
    for index, row in df.iterrows():
        qty = row['QTY']
        if qty > 1:
            # Duplicate the row `qty` times
            if (index+1) in num_drops:
                sum_dropped_after += (qty-1)
            sum_extra_after += (qty-1)
            repeated_rows = pd.DataFrame([row] * qty, columns=df.columns)
            expanded_rows = pd.concat([expanded_rows, repeated_rows], ignore_index=True)
        else:
            expanded_rows = pd.concat([expanded_rows, pd.DataFrame([row], columns=df.columns)], ignore_index=True)
    # set expanded_rows equal to df
    df = expanded_rows
    # remove quantity column now that it has the correct amount of rows
    df = df.drop(columns=['QTY'])

    sum_extra = sum_extra_before + sum_extra_after

    correct_range_results = df_results.iloc[l + sum_extra_before:r + sum_extra].reset_index(drop=True)
    df['CERTS'] = correct_range_results['Cert #']


    for cert in cert_drops:
        df = df[df['CERTS'] != cert]
    df.reset_index(drop=True, inplace=True) 

    # get correct rows in results
    for (l, r) in ranges:
        df_results = df_results.iloc[l+sum_extra_before:r+sum_extra]
    for cert in cert_drops:
        df_results = df_results[df_results['Cert #'] != cert]
    # Reset index with drop=True
    df_results.reset_index(drop=True, inplace=True)

    # make dup df to keep original descriptions
    df['DESCRIPTION'] = df_results['Description']
    og_df = df.copy()


    # fix sports
    sport_pattern = r'^(.*)\sCards$'
    matches = df['SPORT'].str.extract(sport_pattern)
    # ppdate 'SPORT' column with the extracted part
    df.loc[matches[0].notna(), 'SPORT'] = matches[0]

    # add column for year
    df['YEAR'] = df['DESCRIPTION'].str.slice(0, 4)
    df['DESCRIPTION'] = df['DESCRIPTION'].str.split().apply(lambda x: ' '.join(x[1:]))

    # add column for brand (lambda appends 2nd word with ' ' in between)
    df['BRAND'] = df['DESCRIPTION'].str.split().apply(lambda x: ' '.join(x[0:2]))
    # delete some of description
    df['DESCRIPTION'] = df['DESCRIPTION'].str.split().apply(lambda x: ' '.join(x[2:]))

    # MJ Flair
    df.loc[df['BRAND'].str.contains("FLAIR 235"), ['DESCRIPTION', 'BRAND']] = ["235 MICHAEL JORDAN", "FLAIR"]
    df.loc[df['BRAND'].str.contains("TOPPS 347"), ['DESCRIPTION', 'BRAND']] = ["347 SEAN TAYLOR", "TOPPS"]
    df.loc[df['BRAND'].str.contains("TOPPS 360"), ['DESCRIPTION', 'BRAND']] = ["360 LARRY FITZGERALD", "TOPPS"]

    # fix brand patterns
    monopoly_pattern = (r'^(MONOPOLY)', 'MONOPOLY')
    update_pattern = (r'^(UPDATE)', 'UPDATE')
    box_chrome_pattern = (r'^(BOX CHROME)', 'BOX CHROME')
    optic_pattern = (r'^(OPTIC)', 'OPTIC')
    clearly_pattern = (r'^(DONRUSS)', 'DONRUSS')
    turbo_pattern = (r'^(TURBOCHARGED)', 'TURBOCHARGED')
    dp_pattern = (r'^(DRAFT PICKS)', 'DRAFT PICKS')
    prospects_pattern = (r'^(PROSPECTS)', 'PROSPECTS')
    pb_pattern = (r'^(PRIZM BLACK)', 'PRIZM BLACK')
    p_auto_pattern = (r'^(PROSPECT AUTOGRAPHS)', 'PROSPECT AUTOGRAPHS')
    brand_patterns = [monopoly_pattern, update_pattern, box_chrome_pattern, optic_pattern, clearly_pattern, turbo_pattern, dp_pattern, prospects_pattern, pb_pattern, p_auto_pattern]
    for pattern, string in brand_patterns:
        matches = df['DESCRIPTION'].str.extract(pattern)
        df['BRAND'] = df.apply(lambda row: (f"{row['BRAND']} " + string) if pd.notna(matches.loc[row.name, 0]) else row['BRAND'], axis=1)
        df['DESCRIPTION'] = df['DESCRIPTION'].str.replace(pattern, '', regex=True).str.strip()

    # create empty variation/parallel col
    df['VARIATION/PARALLEL'] = ''
    # fix variation patterns
    nfl_debut_pattern = (r'^(NFL DEBUT)', '')
    razz_pattern = (r'^(RAZZLE DAZZLE)', '')
    pbreak_pattern = (r'^(PRIZM BREAK)', '')
    topps_83_pattern = (r'^(1983 TOPPS BASEBALL)', '')
    t_minus_pattern = (r'^(T-MINUS 3...2...1...)', '')
    my_house_pattern = (r'^(MY HOUSE)', '')
    light_pattern = (r'^(LIGHT IT UP)', '')
    tr_pattern = (r'^(THE ROOKIES)', '')
    auto_pattern = (r'^(AUTOGRAPH)', '')
    mys_pattern = (r'^(MYSTIQUE)', '')
    variation_patterns = [nfl_debut_pattern, razz_pattern, pbreak_pattern, topps_83_pattern, t_minus_pattern, my_house_pattern, light_pattern, tr_pattern, auto_pattern, mys_pattern]
    for pattern, string in variation_patterns:
        matches = df['DESCRIPTION'].str.extract(pattern)
        df['VARIATION/PARALLEL'] = df.apply(lambda row: (f"{row['VARIATION/PARALLEL']}" + string) if pd.notna(matches.loc[row.name, 0]) else row['VARIATION/PARALLEL'], axis=1)
        df['DESCRIPTION'] = df['DESCRIPTION'].str.replace(pattern, '', regex=True).str.strip()

    # add column for card number
    df['CARD#'] = df['DESCRIPTION'].str.split().apply(lambda x: ' '.join(x[:1]))
    # remove card# from the description
    df['DESCRIPTION'] = df['DESCRIPTION'].str.split().apply(lambda x: ' '.join(x[1:]))
    # name
    name_pattern = r'(^[a-zA-Z\-\']+ [a-zA-Z\-\']+( II+| JR\.)?)'
    df['NAME'] = df['DESCRIPTION'].str.extract(name_pattern, expand=False)[0]
    # remove names from desc
    df['DESCRIPTION'] = df['DESCRIPTION'].str.replace(name_pattern, '', regex=True).str.strip()
    
    # sauce bug
    df.loc[df['DESCRIPTION'].str.contains("GARDNER HOLO"), ['DESCRIPTION', 'NAME']] = ["HOLO", "AHMAD SAUCE GARDNER"]
    # fixes Optic Bug
    df.loc[df['DESCRIPTION'].str.contains(r'^OPTIC', regex=True), 'BRAND'] = 'PANINI DONRUSS OPTIC'
    # remove Optic from desc
    df['DESCRIPTION'] = df['DESCRIPTION'].str.extract(r'^(OPTIC\s)(.*)$', expand=True)[1].fillna(df['DESCRIPTION'])

    # parallels
    def update_parallel(description, parallel, brand):
        words = description.split()
        word_count = len(words)

        if word_count == 1:
            new_parallel = words[-1]
        elif word_count == 2:
            new_parallel = ' '.join(words[-2:])
        elif word_count == 3:
            new_parallel = ' '.join(words[-3:])
        elif word_count == 4:
            new_parallel = ' '.join(words[-4:])
        elif description == '':
            new_parallel = f"{brand} BASE"
        else:
            new_parallel = ''
        
        # Append the new value to the existing parallel value
        return f"{parallel} {new_parallel}".strip()

    # Apply the function to update 'VARIATION/PARALLEL' column
    df['VARIATION/PARALLEL'] = df.apply(
    lambda row: update_parallel(row['DESCRIPTION'], row['VARIATION/PARALLEL'], row['BRAND']), axis=1)



    # fix parallels that have extra words
    # 
    # variation, preview
    extra_pattern = r'^(VARIATION|PREVIEW)\-(.*)$'
    matches = df['VARIATION/PARALLEL'].str.extract(extra_pattern)
    # replace the matched parts with the desired values
    df.loc[matches[0].notna(), 'VARIATION/PARALLEL'] = matches[1].str.strip()
    # 
    # chrome
    chrome_mask = df['VARIATION/PARALLEL'].str.contains(r'CHROME', regex=True)
    # move chrome to brand from parallel
    df.loc[chrome_mask, 'VARIATION/PARALLEL'] = df.loc[chrome_mask, 'VARIATION/PARALLEL'].str.replace(r'CHROME-', '', regex=True).str.strip()
    df.loc[chrome_mask, 'BRAND'] = df.loc[chrome_mask, 'BRAND'] + ' CHROME'

    # drop desc for original
    df['DESCRIPTION'] = og_df['DESCRIPTION']

    # capitalize the sport column
    df['SPORT'] = df['SPORT'].str.upper()

    # add order number
    df['ORDER NUMBER'] = order_num

    # rearrange cols
    cols = list(df.columns.values)
    desc_i, sport_i, val_i = cols.index('DESCRIPTION'), cols.index('SPORT'), cols.index('DECLARED VALUE TOTAL')
    yr_i, brand_i, parallel_i = cols.index('YEAR'), cols.index('BRAND'), cols.index('VARIATION/PARALLEL')
    card_i, name_i, order_i = cols.index('CARD#'), cols.index('NAME'), cols.index('ORDER NUMBER')
    df = df[[cols[order_i]] + [cols[desc_i]] + [cols[yr_i]] + [cols[brand_i]] + [cols[card_i]] + [cols[parallel_i]] + [cols[name_i]] + [cols[sport_i]] + [cols[val_i]]]

    # add results column (only taylor's)
    df['GRADE'] = df_results['Grade']
    # remove extra words
    df.loc[df['GRADE'].str.contains(r'^[a-z\-A-Z]+ [0-9]+', regex=True), ['GRADE']] = df['GRADE'].str.replace(r'^[a-z\-A-Z]+ ', "", regex=True).str.strip()
    df.loc[df['GRADE'].str.contains(r'^[a-z\-A-Z]+ [a-z\-A-Z]+ [0-9]+', regex=True), ['GRADE']] = df['GRADE'].str.replace(r'^[a-z\-A-Z]+ [a-z\-A-Z]+ ', "", regex=True).str.strip()
    # change grade to int value
    df['GRADE'] = df['GRADE'].astype(int)

    return df
