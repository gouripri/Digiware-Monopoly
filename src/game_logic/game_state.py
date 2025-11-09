"""
Game state management - properties, players, ownership, and transactions
"""

class Player:
    """Represents a player in the game"""
    def __init__(self, name, token_type, starting_money=1500):
        self.name = name
        self.token_type = token_type  # e.g., 'top_hat', 'car', etc.
        self.money = starting_money
        self.position = 0  # Board position (0-27)
        self.properties = []  # List of Property objects owned
        self.in_jail = False  # True if player is in jail and must skip next turn
        self.jail_turn_skipped = False  # True if player has already skipped their turn in jail
        
    def add_money(self, amount):
        """Add money to player"""
        self.money += amount
        
    def subtract_money(self, amount):
        """Subtract money from player. Returns True if successful, False if insufficient funds"""
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    
    def owns_property(self, property_obj):
        """Check if player owns a property"""
        return property_obj in self.properties


class Property:
    """Represents a property on the board"""
    def __init__(self, name, position, price, base_rent, color=None, property_type='property'):
        self.name = name
        self.position = position  # Board position (0-27)
        self.price = price
        self.base_rent = base_rent  # Rent when owned (no houses/hotels)
        self.color = color  # Property color group
        self.property_type = property_type  # 'property', 'utility', 'railroad', 'special'
        self.owner = None  # None if not owned, otherwise Player object
        
    def is_owned(self):
        """Check if property is owned"""
        return self.owner is not None
    
    def is_available_to_buy(self):
        """Check if property can be bought (not owned and is a buyable property)"""
        return self.owner is None and self.property_type in ['property', 'utility', 'railroad']
    
    def set_owner(self, player):
        """Set the owner of this property"""
        if self.owner is not None:
            # Remove from old owner's properties list
            if self in self.owner.properties:
                self.owner.properties.remove(self)
        
        self.owner = player
        if player is not None and self not in player.properties:
            player.properties.append(self)
    
    def get_rent(self):
        """Get the rent amount for this property"""
        if not self.is_owned():
            return 0
        return self.base_rent
    
    def can_collect_rent_from(self, player):
        """Check if owner can collect rent from a player (property is owned and player is not the owner)"""
        return self.is_owned() and self.owner != player


class GameState:
    """Manages the overall game state"""
    def __init__(self):
        self.players = []
        self.properties = []  # Flat list of all properties (for iteration)
        # Position-indexed list: properties_by_position[position] = Property object
        # None means no property at that position
        self.properties_by_position = [None] * 28  # 28 board positions (0-27)
        self.current_player_index = 0
        
    def add_player(self, name, token_type):
        """Add a player to the game"""
        player = Player(name, token_type)
        self.players.append(player)
        return player
    
    def add_property(self, name, position, price, base_rent, color=None, property_type='property'):
        """
        Add a property to the game.
        The property is stored at properties_by_position[position] for fast lookup.
        """
        if position < 0 or position >= 28:
            raise ValueError(f"Position must be between 0 and 27, got {position}")
        
        property_obj = Property(name, position, price, base_rent, color, property_type)
        
        # Store in position-indexed list
        self.properties_by_position[position] = property_obj
        
        # Also keep in flat list for iteration
        self.properties.append(property_obj)
        
        return property_obj
    
    def get_current_player(self):
        """Get the current player whose turn it is"""
        if not self.players:
            return None
        return self.players[self.current_player_index]
    
    def get_property_at_position(self, position):
        """
        Get property at a specific board position (0-27).
        Returns Property object or None if no property at that position.
        """
        if position < 0 or position >= 28:
            return None
        return self.properties_by_position[position]
    
    def buy_property(self, player, property_obj):
        """
        Attempt to buy a property.
        Returns: (success: bool, message: str)
        """
        # Check if property can be bought
        if not property_obj.is_available_to_buy():
            return False, "Property is not available to buy"
        
        # Check if player has enough money
        if player.money < property_obj.price:
            return False, f"Insufficient funds. Need ${property_obj.price}, have ${player.money}"
        
        # Complete the purchase
        if player.subtract_money(property_obj.price):
            property_obj.set_owner(player)
            return True, f"{player.name} bought {property_obj.name} for ${property_obj.price}"
        
        return False, "Purchase failed"
    
    def pay_rent(self, player, property_obj):
        """
        Player pays rent to property owner.
        Returns: (success: bool, message: str, amount_paid: int)
        """
        # Check if rent should be paid
        if not property_obj.can_collect_rent_from(player):
            return False, "No rent to pay", 0
        
        rent_amount = property_obj.get_rent()
        owner = property_obj.owner
        
        # Check if player has enough money
        if player.money < rent_amount:
            # Player goes bankrupt - pay what they have
            amount_paid = player.money
            player.subtract_money(amount_paid)
            owner.add_money(amount_paid)
            return True, f"{player.name} paid ${amount_paid} rent to {owner.name} (bankrupt!)", amount_paid
        
        # Normal rent payment
        if player.subtract_money(rent_amount):
            owner.add_money(rent_amount)
            return True, f"{player.name} paid ${rent_amount} rent to {owner.name}", rent_amount
        
        return False, "Rent payment failed", 0
    
    def handle_landing(self, player, position):
        """
        Handle what happens when a player lands on a property.
        Returns: (action: str, property_obj: Property, message: str)
        Action can be: 'buy', 'rent', 'special', 'nothing'
        """
        property_obj = self.get_property_at_position(position)
        
        if property_obj is None:
            return 'nothing', None, "No property at this position"
        
        # Special spaces (GO, Jail, Free Parking, etc.)
        if property_obj.property_type == 'special':
            return 'special', property_obj, f"Landed on {property_obj.name}"
        
        # Property is not owned - can buy
        if property_obj.is_available_to_buy():
            return 'buy', property_obj, f"{property_obj.name} is available to buy for ${property_obj.price}"
        
        # Property is owned by someone else - pay rent
        if property_obj.can_collect_rent_from(player):
            success, message, amount = self.pay_rent(player, property_obj)
            return 'rent', property_obj, message
        
        # Property is owned by this player - do nothing
        if property_obj.owner == player:
            return 'nothing', property_obj, f"You own {property_obj.name}"
        
        return 'nothing', None, "Unknown state"
    
    def next_turn(self):
        """Move to the next player's turn"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def should_skip_turn(self, player):
        """
        Check if a player should skip their turn (e.g., in jail)
        Returns: (should_skip: bool, reason: str)
        """
        if player.in_jail and not player.jail_turn_skipped:
            # Player is in jail and hasn't skipped their turn yet
            player.jail_turn_skipped = True
            return True, f"{player.name} is in jail and must skip this turn"
        elif player.in_jail and player.jail_turn_skipped:
            # Player has skipped their turn, release from jail
            player.in_jail = False
            player.jail_turn_skipped = False
            return False, f"{player.name} is released from jail"
        
        return False, None
    
    def roll_dice(self, sides=6, num_dice=1):
        """
        Roll dice and return the total.
        
        Args:
            sides: Number of sides on each die (default 6)
            num_dice: Number of dice to roll (default 1 - single die, 1-6)
        
        Returns:
            Total of all dice rolls (1-6 for single die)
        """
        import random
        total = 0
        for _ in range(num_dice):
            total += random.randint(1, sides)
        return total
    
    def move_player(self, player, dice_roll):
        """
        Move a player based on dice roll.
        Handles board wrapping, GO bonuses, and Go to Jail.
        
        Args:
            player: Player object to move
            dice_roll: Total dice roll (1-6 for single die)
        
        Returns:
            (new_position: int, passed_go: bool, landed_on_go: bool, went_to_jail: bool)
        """
        old_position = player.position
        new_position = (old_position + dice_roll) % 28
        
        # Check if player passed GO (wrapped around the board)
        passed_go = (old_position + dice_roll) >= 28
        
        # Check if player landed on GO
        landed_on_go = (new_position == 0)
        
        # Check if player landed on Go to Jail (position 21)
        went_to_jail = (new_position == 21)
        
        # Handle Go to Jail rule
        if went_to_jail:
            # Send player to Jail (position 7)
            new_position = 7
            # Mark player as in jail (must skip next turn)
            player.in_jail = True
            player.jail_turn_skipped = False
        
        # Update player position
        player.position = new_position
        
        # Handle GO bonuses
        if passed_go or landed_on_go:
            # Collect $200 for passing or landing on GO
            player.add_money(200)
        
        return new_position, passed_go, landed_on_go, went_to_jail
    
    def roll_and_move(self, player, dice_roll=None):
        """
        Roll dice and move player in one action.
        If dice_roll is provided, use that instead of rolling.
        
        Args:
            player: Player object to move
            dice_roll: Optional dice roll value (if None, will roll dice)
        
        Returns:
            (dice_roll: int, new_position: int, passed_go: bool, landed_on_go: bool, went_to_jail: bool)
        """
        if dice_roll is None:
            dice_roll = self.roll_dice()
        
        new_position, passed_go, landed_on_go, went_to_jail = self.move_player(player, dice_roll)
        
        return dice_roll, new_position, passed_go, landed_on_go, went_to_jail
    
    def initialize_all_properties(self):
        """
        Initialize all 28 properties on the board.
        Call this once when setting up a new game.
        Modify this to add your actual property data.
        """
        # Position 0: GO (bottom-left corner)
        self.add_property("GO", 0, 0, 0, property_type='special')
        
        # Positions 1-6: Bottom row (left to right)
        # TODO: Add your actual properties here
        self.add_property("JARVIS", 1,60,20, property_type="property")
        self.add_property("BONNER", 2,60,20, property_type="property")
        self.add_property("EDUROAM", 3,180,100, property_type="special")
        self.add_property("FURNAS", 4,100,40, property_type="property")
        self.add_property("KNOW", 5,100,40, property_type="property")
        self.add_property("KETTER", 6,120,60, property_type="property")

        # Position 7: Bottom-right corner
        self.add_property("JAIL", 7, 0, 0, property_type='visiting') #only on with this type

        # Positions 8-13: Right column (bottom to top)
        self.add_property("GOVENORS", 8, 140, 70, property_type='property')
        self.add_property("HADLY", 9, 160, 80, property_type='property')
        self.add_property("GRIENER", 10, 180, 90, property_type='property')
        self.add_property("LOST", 11, 140, 100, property_type='special')
        self.add_property("ELLICOTT", 12, 180, 95, property_type='property')
        self.add_property("FLINT", 13, 200, 100, property_type='property')

        # Position 14: Top-right corner
        self.add_property("FREE PARKING", 14, 0, 0, property_type='parking')
        # Positions 15-20: Top row (right to left)
        self.add_property("NSC", 15, 220, 105, property_type='property')
        self.add_property("DINNING RELOAD", 16, 220, 105, property_type='special')
        self.add_property("SILVERMAN", 17, 240, 110, property_type='property')
        self.add_property("LOCKWOOD", 18, 250, 125, property_type='property')
        self.add_property("SLEE", 19, 250, 130, property_type='property')
        self.add_property("ACADEMIC CENTER", 20, 280, 140, property_type='property')
        
        # Position 21: Top-left corner
        self.add_property("GO TO JAIL", 21, 0, 0, property_type='jail')
        self.add_property("CAPEN", 22, 300, 150, property_type='property')
        self.add_property("TALBERT", 23, 300, 150, property_type='property')
        self.add_property("EMON", 24, 180, 100, property_type='special')
        self.add_property("BALDY", 25, 320, 160, property_type='property')
        self.add_property("DAVIS", 26, 350, 175, property_type='property')
        self.add_property("COMMONS", 27, 400, 200, property_type='property')

        # Positions 22-27: Left column (top to bottom)
        # TODO: Add properties for positions 22-27

