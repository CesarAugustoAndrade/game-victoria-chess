"""
Entity manager for handling all game entities
"""

class EntityManager:
    """Manages all entities in the game"""

    def __init__(self):
        self.entities = []
        self.units = []
        self.buildings = []
        self.next_id = 0

    def add_entity(self, entity):
        """Add an entity to the manager"""
        entity.id = self.next_id
        self.next_id += 1
        self.entities.append(entity)

        # Categorize entity
        from src.entities.unit import Unit
        if isinstance(entity, Unit):
            self.units.append(entity)
        # Add building check when buildings are implemented

    def remove_entity(self, entity):
        """Remove an entity from the manager"""
        if entity in self.entities:
            self.entities.remove(entity)

        if entity in self.units:
            self.units.remove(entity)

        if entity in self.buildings:
            self.buildings.remove(entity)

    def update(self, dt):
        """Update all entities"""
        # Update entities and remove inactive ones
        entities_to_remove = []

        for entity in self.entities:
            entity.update(dt)
            if not entity.active:
                entities_to_remove.append(entity)

        for entity in entities_to_remove:
            self.remove_entity(entity)

    def render(self, screen, camera):
        """Render all entities"""
        for entity in self.entities:
            if entity.active:
                entity.render(screen, camera)

    def get_units_at(self, position):
        """Get all units at a specific position"""
        selected = []
        for unit in self.units:
            if unit.active and unit.contains_point(position):
                selected.append(unit)
        return selected

    def get_entities_in_rect(self, rect):
        """Get all entities within a rectangle"""
        selected = []
        for entity in self.entities:
            if entity.active and rect.colliderect(entity.get_rect()):
                selected.append(entity)
        return selected

    def clear(self):
        """Remove all entities"""
        self.entities.clear()
        self.units.clear()
        self.buildings.clear()