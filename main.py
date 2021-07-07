import game

# When True, the game is on:
game_on = False

while not game_on:

    start = input("Do you want to start new game? ").lower()
    if start not in ["yes", "no"]:
        print("Please type 'Yes' or 'No'")

    if start == "yes":
        game_on = True
    elif start == "no":
        print("Bye!")
        break

if game_on:
    # Create user balance:
    new_credit = game.Credit()
    # Ask user to provide value:
    new_credit.add_balance()

while game_on:

    # Game logic starts

    # which round is it
    new_round = 0

    # Put a bet:
    new_bet = new_credit.put_bet()

    #  Create a deck of cards:
    new_deck = game.Deck()
    # and shuffle it:
    new_deck.shuffle()

    # Create a new table:
    new_table = game.Table(new_deck.all_cards, new_bet)

    # Deal the cards:
    new_table.first_deal()

    # Display cards:
    new_table.print_player_cards()
    print("Dealer cards:")
    print(new_table.dealer_cards[0])
    print("X")

    new_table.sum_player_cards()
    new_table.sum_dealer_cards()

    # Variable new_move with user's choice as a value.
    # If "stand", player turn ends and the game logic proceeds to the dealer's move
    new_move = None
    # List with player's moves that need to be considered on final assessment:
    action = []

    while new_move != "stand":
        new_round += 1

        # Player's move:
        print("Commands: [hit], [stand], [insure], [d]ouble [d]own ([dd]), or [split]")
        new_move = game.take_input("Your move")

        if new_move == "hit":
            # Add new card to the player card list
            new_table.hit_player()
            new_table.print_player_cards()
            # Add new card value to overall value:
            new_table.player_sum += new_table.player_cards[-1].value
            # Check if bust:
            if new_table.player_sum > 21:
                game.bust_hand_has_ace(new_table.player_cards)
                # Reset player cards value:
                new_table.player_sum = 0
                # Count again:
                new_table.sum_player_cards()
                # If still bust:
                if new_table.player_sum > 21:
                    print("Bust!")
                    new_table.player_win = False
                    new_table.dealer_win = True
                    break
                else:
                    pass
            else:
                pass

        elif new_move == "insure":
            # Player can only make the insurance bet if the dealer's first card is Ace:
            if new_table.dealer_cards[0].rank == "Ace":
                # and if they have enough money:
                if new_credit.balance >= new_bet/2:
                    new_credit.balance -= new_table.insurance
                    action.append(new_move)  # needed for final balance
                    print(f"Insurance: {new_table.insurance}")
                    print(f"Your balance: {new_credit.balance}")
                else:
                    print("You do not have enough credit.")
            else:
                print("You cannot make insurance bet now.")

        elif new_move == 'dd':
            # Player doubles his bet, takes one (and only one card) and stands:
            if new_credit.balance >= new_bet and new_round == 1:
                new_credit.balance -= new_bet
                new_bet *= 2
                print(f"Your bet is: {new_bet}")
                print(f"Your balance is: {new_credit.balance}")
                new_table.hit_player()
                new_table.print_player_cards()
                new_table.player_sum += new_table.player_cards[-1].value
                if new_table.player_sum > 21:
                    game.bust_hand_has_ace(new_table.player_cards)
                    # Reset player cards:
                    new_table.player_sum = 0
                    # Count again:
                    new_table.sum_player_cards()
                    # If still bust:
                    if new_table.player_sum > 21:
                        print("Bust!")
                        new_table.player_win = False
                        new_table.dealer_win = True
                    else:
                        pass
                else:
                    pass
                break
            else:
                print("You can't double down now.")

        elif new_move == 'stand':
            break

        else:
            # Player can only split if the cards are equal and it is the beginning of the game:
            if new_table.player_cards[0].rank == new_table.player_cards[1].rank and new_round == 1:
                # And has enough money:
                if new_credit.balance >= new_bet:
                    new_table.hand_one_on = True
                    new_table.hand_two_on = True
                    split_round = 0
                    action.append(new_move)
                    # Table with two hands and bets:
                    new_table.split_table()
                    new_table.print_player_cards()
                    new_table.print_split_hand_two()
                    break
                else:
                    print("You do not have enough credit.")
                    new_move = None
            else:
                print("You cannot split now.")
                # if cannot split, do not go in the next loop
                new_move = None

    # Split logic:

    while new_move == 'split':

        split_round += 1

        # In round 1, count values; in later rounds they are added with every hit
        if split_round == 1:
            new_table.sum_player_cards()
            new_table.sum_split_hand_two()

        # hand one move and check:
        if new_table.hand_one_on:
            hand_one_move = game.take_input("Hand one move")
            if hand_one_move == "hit":
                new_table.hit_player()
                new_table.print_player_cards()
                new_table.player_sum += new_table.player_cards[-1].value
                if new_table.player_sum > 21:
                    game.bust_hand_has_ace(new_table.player_cards)
                    # Reset player cards value:
                    new_table.player_sum = 0
                    # Count again:
                    new_table.sum_player_cards()
                    # If still bust:
                    if new_table.player_sum > 21:
                        print("Hand one bust!")
                        new_table.hand_one_on = False
                        new_table.player_win = False
                        new_table.dealer_win = True
                    else:
                        pass
                else:
                    pass

            elif hand_one_move == "stand":
                # If hand one off, do not process it
                new_table.hand_one_on = False
            else:
                print("Please hit or stand.")
        else:
            pass

        # hand two move and check:
        if new_table.hand_two_on:
            hand_two_move = game.take_input("Hand two move")
            if hand_two_move == "hit":
                new_table.split_hit_two()
                new_table.print_split_hand_two()
                new_table.hand_two_sum += new_table.split_hand_two[-1].value
                if new_table.hand_two_sum > 21:
                    game.bust_hand_has_ace(new_table.split_hand_two)
                    # Reset hand two cards value:
                    new_table.hand_two_sum = 0
                    # Count again:
                    new_table.sum_split_hand_two()
                    # If still bust:
                    if new_table.hand_two_sum > 21:
                        print("Hand two bust!")
                        new_table.hand_two_on = False
                        new_table.hand_two_win = False
                        new_table.dealer_win_hand_two = True
            elif hand_two_move == "stand":
                new_table.hand_two_on = False
            else:
                print("Please hit or stand.")
        else:
            pass

        # If both hands are off, break
        if not new_table.hand_one_on and not new_table.hand_two_on:
            break

    # Dealer moves if the player has not busted
    while ("split" not in action and new_table.player_sum <= 21) \
            or ("split" in action and (new_table.player_sum <= 21 or new_table.hand_two_sum <= 21)):

        # Dealer hits until 17 is reached or exceeded
        if new_table.dealer_sum < 17:
            new_table.hit_dealer()
            new_table.dealer_sum += new_table.dealer_cards[-1].value
            print("Dealer hits")
            new_table.print_dealer_cards()
        else:
            new_table.print_dealer_cards()
            break

        # Check if the dealer busts
        if new_table.dealer_sum > 21:
            game.bust_hand_has_ace(new_table.dealer_cards)
            # Reset dealer cards value:
            new_table.dealer_sum = 0
            # Count again:
            new_table.sum_dealer_cards()
            # If still bust:
            if new_table.dealer_sum > 21:
                print("Dealer busts!")
                new_table.dealer_win = False
                new_table.player_win = True
                break

    # Check who wins:
    if 'split' not in action:

        # a) for regular table:

        # If both not busted:
        if new_table.player_sum <= 21 and new_table.dealer_sum <= 21:

            if 21 - new_table.player_sum < 21 - new_table.dealer_sum:
                new_table.player_win = True
                new_table.dealer_win = False
                new_table.tie = False
            elif 21 - new_table.player_sum == 21 - new_table.dealer_sum:
                new_table.player_win = False
                new_table.dealer_win = False
                new_table.tie = True
            else:
                new_table.player_win = False
                new_table.dealer_win = True
                new_table.tie = False

        # Who wins:
        if new_table.player_win:
            new_credit.balance += new_bet*2
            new_bet = 0
            print("You win!")
        elif new_table.dealer_win:
            new_bet = 0
            print("You loose!")
        if new_table.tie:
            new_credit.balance += new_bet
            new_bet = 0
            print("It's a tie!")
            # Insurance bets:
            if "insure" in action:
                if new_table.dealer_sum == 21:
                    new_credit.balance += 2 * new_table.insurance
                    new_table.insurance = 0
                    print("You win insurance bet.")
                else:
                    new_credit.balance -= new_table.insurance
                    new_table.insurance = 0
                    print("You loose insurance bet.")

        # Print final balance
        print(f"Your balance: ${new_credit.balance}")

    else:
        # b) for split table:

        # If both not busted:

        # Hand one:
        if new_table.player_sum <= 21 and new_table.dealer_sum <= 21:

            if 21 - new_table.player_sum < 21 - new_table.dealer_sum:
                new_table.player_win = True
                new_table.dealer_win = False
                new_table.tie = False
            elif 21 - new_table.player_sum == 21 - new_table.dealer_sum:
                new_table.player_win = False
                new_table.dealer_win = False
                new_table.tie = True
            else:
                new_table.player_win = False
                new_table.dealer_win = True
                new_table.tie = False

        # Hand two:
        if new_table.hand_two_sum <= 21 and new_table.dealer_sum <= 21:
            if 21 - new_table.hand_two_sum < 21 - new_table.dealer_sum:
                new_table.hand_two_win = True
                new_table.dealer_win_hand_two = False
                new_table.tie_hand_two = False
            elif 21 - new_table.player_sum == 21 - new_table.dealer_sum:
                new_table.hand_two_win = False
                new_table.dealer_win_hand_two = False
                new_table.tie_hand_two = True
            else:
                new_table.hand_two_win = False
                new_table.dealer_win_hand_two = True
                new_table.tie_hand_two = False

        # Who wins:

        # Hand one:
        if new_table.player_win:
            new_credit.balance += new_bet*2
            new_bet = 0
            print("You win hand one!")
        elif new_table.dealer_win:
            new_bet = 0
            print("You loose hand one!")
        if new_table.tie:
            new_credit.balance += new_bet
            new_bet = 0
            print("Hand one tied!")

        # Hand two:
        if new_table.hand_two_win:
            new_credit.balance += new_table.split_bet * 2
            new_table.split_bet = 0
            print("You win hand two!")
        elif new_table.dealer_win_hand_two:
            new_table.split_bet = 0
            print("You loose hand two!")
        if new_table.tie_hand_two:
            new_credit.balance += new_table.split_bet
            new_table.split_bet = 0
            print("Hand two tied!")

        # Print final balance:
        print(f"Your balance: ${new_credit.balance}")

    while True:

        replay = input("Do you want to play again? ").lower()
        if replay not in ["yes", "no"]:
            print("Please type 'Yes' or 'No'")

        if replay == "yes":
            game_on = True
            break
        elif replay == "no":
            print("Bye!")
            game_on = False
            break
