"""
Game state management - properties, players, ownership, and transactions
"""

class Player:
    """Represents a player in the game"""
    def __init__(self, name, token_type, starting_money=1500):
        self.name = name
        self.token_type = token_type  # e.g., 'top_hat', 'car', etc.
        self.money = starting_money
        self.position = 0  # Board position (0-39)
        self.properties = []  # List of Property objects owned
        
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
        self.position = position  # Board position (0-39)
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
        self.properties = []
        self.current_player_index = 0
        
    def add_player(self, name, token_type):
        """Add a player to the game"""
        player = Player(name, token_type)
        self.players.append(player)
        return player
    
    def add_property(self, name, position, price, base_rent, color=None, property_type='property'):
        """Add a property to the game"""
        property_obj = Property(name, position, price, base_rent, color, property_type)
        self.properties.append(property_obj)
        return property_obj
    
    def get_current_player(self):
        """Get the current player whose turn it is"""
        if not self.players:
            return None
        return self.players[self.current_player_index]
    
    def get_property_at_position(self, position):
        """Get property at a specific board position"""
        for prop in self.properties:
            if prop.position == position:
                return prop
        return None
    
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

