# psa-grading-dashboard

I developed a dashboard to optimize sports card submissions to PSA by using analytics to assess grading potential and maximize value while minimizing costs.

Currently only configured for my friend, but may restructure for other users in the future.

## Motivation

My friend owns a sports cards business. Within his business, he submits cards for grading to PSA (Professional Sports Authenticator). Cards are graded on a scale from 1-10, depending on the quality on four main categories: centering, corners, edges, and surface condition. A higher numerical grade indicates a more prestine card. Thus, cards that receive higher grades are worth exponentially more than their raw (ungraded) value, however, cards that receive a low grade can decrease the value of the card. Additionally, there is a ~$20 fee to grade each card. Therefore, it is important to be selective when deciding which cards to submit. I created this dashboard to help my friend use analytics to help guide his decision-making.

## Workflow

- Download the data for each submission from PSA. A submission is a group of cards submitted from grading in the same order.
- Clean the data with a python script. My friend allows other people to submit their cards in his orders. Therefore, I only focused on data my friend's cards.
- Process the data with a python script. The data downloaded from PSA lists the card description, but does not distinguish its qualities seperately (ex. 2020 PANINI SELECT 61 JUSTIN JEFFERSON DIE-CUT PURPLE PRIZM). I parsed the description to extract the year, brand, card number, variation/parallel, and player name.
- Imported the data into Tableau to create a dashboard.

## 

Created in July 2024
