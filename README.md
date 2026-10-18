# Puerto Rico Dominoes with domino tracker

Author: Ashley Leonard

---

## Description

This project is about making a text-based way to play Puerto Rican Dominoes, a game where 4 players split into 2 teams and try to cause the end of the game to score points based on the pip-totals of the remaining dominoes. Then whichever team reaches a pre-set score (e.g. 100 or 200) after n rounds wins.

This project also includes logic for a domino tracker that figures out what dominoes players can or can't have, based on what numbers they and others have skipped on. It tracks in a table whether each player can have any of the 36 dominoes (either YES, NO or MAYBE) from a given player's perspective - therefore each player would have their own unique table as they each start by only knowing their own pieces. 

If you imagine the table where the rows are the dominoes, and the columns are the players, each row can only have yes 0 or 1 times, and each column can only have YES 0-7 times. Using this information, alongside keeping track of when players can't go (putting NO for all dominoes that include a number that was at either end of the train) the table can figure out players' pieces before they even place them.

For example, if a row for an unplayed piece contained 3 NO's and a MAYBE, that MAYBE must actually be a YES because that player is the only one that can have that piece. Taking this example further, let's say you got lucky and that YES is the last domino to figure out for that player, all other MAYBE's in the column for the player can become NO which can in turn cause a further cascade of deductions.
