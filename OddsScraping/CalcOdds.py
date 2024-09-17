def calc_prob(odds):
    if odds < 0:
        bet_amount = -odds
        win_amount = 100
    else:
        bet_amount = 100
        win_amount = odds
    probwin = bet_amount/(bet_amount + win_amount)
    return probwin