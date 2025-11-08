"""
Calculate screen positions for Monopoly board spaces
Maps board position (0-27) to screen coordinates
28 total spaces: 4 corners + 6 properties per side
"""

class PositionCalculator:
    """Calculates screen coordinates for board positions"""
    
    def __init__(self, board_size, margin, corner_size, cell_size):
        """
        Initialize position calculator
        
        Args:
            board_size: Size of the board square
            margin: Margin from screen edge
            corner_size: Size of corner spaces
            cell_size: Size of regular property spaces
        """
        self.board_size = board_size
        self.margin = margin
        self.corner_size = corner_size
        self.cell_size = cell_size
        
    def get_position_rect(self, board_position):
        """
        Get the screen rectangle for a board position (0-27)
        
        Board layout (starting from bottom-left, going clockwise):
        - Position 0: Bottom-left corner
        - Positions 1-6: Bottom row (left to right) - 6 properties
        - Position 7: Bottom-right corner
        - Positions 8-13: Right column (bottom to top) - 6 properties
        - Position 14: Top-right corner
        - Positions 15-20: Top row (right to left) - 6 properties
        - Position 21: Top-left corner
        - Positions 22-27: Left column (top to bottom) - 6 properties
        
        Returns:
            (x, y, width, height) tuple for the property space
        """
        m = self.margin
        c = self.corner_size
        t = self.cell_size
        bs = self.board_size
        
        # Position 0: Bottom-left corner
        if board_position == 0:
            return (m, m + bs - c, c, c)
        
        # Positions 1-6: Bottom row (left to right)
        elif 1 <= board_position <= 6:
            idx = board_position - 1
            x = m + c + idx * t
            return (x, m + bs - c, t, c)
        
        # Position 7: Bottom-right corner
        elif board_position == 7:
            return (m + bs - c, m + bs - c, c, c)
        
        # Positions 8-13: Right column (bottom to top)
        elif 8 <= board_position <= 13:
            idx = board_position - 8
            y = m + bs - c - (idx + 1) * t
            return (m + bs - c, y, c, t)
        
        # Position 14: Top-right corner
        elif board_position == 14:
            return (m + bs - c, m, c, c)
        
        # Positions 15-20: Top row (right to left)
        elif 15 <= board_position <= 20:
            idx = board_position - 15
            x = m + bs - c - (idx + 1) * t
            return (x, m, t, c)
        
        # Position 21: Top-left corner
        elif board_position == 21:
            return (m, m, c, c)
        
        # Positions 22-27: Left column (top to bottom)
        elif 22 <= board_position <= 27:
            idx = board_position - 22
            y = m + c + idx * t
            return (m, y, c, t)
        
        else:
            # Invalid position
            return (0, 0, 0, 0)
    
    def get_all_positions(self):
        """Get all 28 positions for testing - returns list of (position, x, y, width, height)"""
        positions = []
        for pos in range(28):
            x, y, w, h = self.get_position_rect(pos)
            positions.append((pos, x, y, w, h))
        return positions
    
    def get_position_center(self, board_position):
        """Get the center point (x, y) of a board position"""
        x, y, w, h = self.get_position_rect(board_position)
        return (x + w // 2, y + h // 2)

