from src.database import DB


class Event:
    def __init__(self,  name, event_start_date, event_end_date,
                 price_high_border, price_low_border):
        self.name = name
        self.event_start_date = event_start_date
        self.event_end_date = event_end_date
        self.price_high_border = price_high_border
        self.price_low_border = price_low_border
    
    def create(self):
        with DB() as db:
            values = (self.name, self.event_start_date, self.event_end_date,
                      self.price_high_border, self.price_low_border)
            db.execute('''
                INSERT INTO Event(name, event_start_date, event_end_date, price_high_border, price_low_border) VALUES(?, ?, ?, ?, ?)
                ''', values)
            
            return self
    
    def delete(self):
        with DB() as db:
            db.execute('''
                DELETE FROM Event WHERE event_id = ?
                ''', self.id)
    
    @staticmethod
    def all():
        with DB() as db:
            all = db.execute('SELECT * FROM Event').fetchall()
            return all
        
    @staticmethod
    def find_by_id(id):
        with DB() as db:
            values = db.execute('''
                SELECT id, event_end_date, name, price_low_border, price_high_border FROM Event
                WHERE event.id = ?
            ''', (id,)).fetchone()
            
            if values:
                return Event(*values)
            
            return None
