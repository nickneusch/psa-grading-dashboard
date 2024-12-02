# psa-grading-dashboard

I developed an interactive dashboard to optimize sports card submissions to PSA by using analytics to assess grading potential and maximize value while minimizing costs. Analytics were focused on the "Gem Rate" (percentage of cards that graded as a "gem", which is a 10/10) because these are the most profitable cards.

Currently only configured for my friend, but may restructure for other users in the future.

<img src="https://github.com/user-attachments/assets/bae9965d-ddf1-421a-8230-8cf000d5bd24" alt="PSA Grading Analytics Dashboard" width="1000">

## Motivation

My friend, Taylor, owns a sports cards business. Within his business, he submits cards for grading to PSA (Professional Sports Authenticator). Each card is graded on a scale from 1-10, depending on the quality of four main categories: centering, corners, edges, and surface condition. A higher numerical grade indicates a more prestine card. Thus, cards that receive higher grades are worth exponentially more than their raw (ungraded) value, however, cards that receive a low grade can decrease the value of the card. Additionally, there is a ~$20 fee to grade each card. Therefore, it is important to be selective when deciding which cards to submit. I created this dashboard to help Taylor use analytics to help guide his decision-making.

## Workflow
1. Download the data for each submission from PSA. A submission is a group of cards submitted in the same order.
2. Clean the data with a python script. Taylor allows other people to submit their cards in his orders. Therefore, the data was only used from his cards.
3. Process the data with a python script. The data downloaded from PSA lists the card description, but does not distinguish its qualities seperately (ex. 2020 PANINI SELECT 61 JUSTIN JEFFERSON DIE-CUT PURPLE PRIZM). The description was parsed to extract the year, brand, card number, variation/parallel, and player name.
4. Import the data into Tableau to create an interactive dashboard. Data was analyzed by gem rate vs. order number, brands, parallels, sports, and players. Filters were added to introduce new perspectives of the data. Filters include order number, brand, year, parallel, and player name.

##

### View on Tableau Public

View the dashboard on Tableau Public (For Desktop-view only):
https://public.tableau.com/app/profile/nicholas.neuschwander/viz/Tay_CollectsPSADashboard/Dashboard3

##

Created in July 2024
