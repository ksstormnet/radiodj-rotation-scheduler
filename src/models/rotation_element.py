class RotationElement:
    def __init__(self, id, parent_id, category_id, subcategory_id, genre_id, mood, gender, language,
                 start_type, end_type, selection_type, sweeper, repeat_rule, order, data,
                 track_separation, artist_separation, title_separation, album_separation, advanced):
        self.id = id
        self.parent_id = parent_id
        self.category_id = category_id
        self.subcategory_id = subcategory_id
        self.genre_id = genre_id
        self.mood = mood
        self.gender = gender
        self.language = language
        self.start_type = start_type
        self.end_type = end_type
        self.selection_type = selection_type
        self.sweeper = sweeper
        self.repeat_rule = repeat_rule
        self.order = order
        self.data = data
        self.track_separation = track_separation
        self.artist_separation = artist_separation
        self.title_separation = title_separation
        self.album_separation = album_separation
        self.advanced = advanced
        
    def __str__(self):
        return f"RotationElement({self.id}, {self.parent_id}, {self.category_id}, {self.subcategory_id}, " \
               f"{self.genre_id}, '{self.mood}', '{self.gender}', '{self.language}', {self.start_type}, " \
               f"{self.end_type}, {self.selection_type}, {self.sweeper}, '{self.repeat_rule}', {self.order}, " \
               f"'{self.data}', {self.track_separation}, {self.artist_separation}, {self.title_separation}, " \
               f"{self.album_separation}, {self.advanced})"
    
    def __eq__(self, other):
        if isinstance(other, RotationElement):
            return (self.id == other.id and
                    self.parent_id == other.parent_id and
                    self.category_id == other.category_id and
                    self.subcategory_id == other.subcategory_id and
                    self.genre_id == other.genre_id and
                    self.mood == other.mood and
                    self.gender == other.gender and
                    self.language == other.language and
                    self.start_type == other.start_type and
                    self.end_type == other.end_type and
                    self.selection_type == other.selection_type and
                    self.sweeper == other.sweeper and
                    self.repeat_rule == other.repeat_rule and
                    self.order == other.order and
                    self.data == other.data and
                    self.track_separation == other.track_separation and
                    self.artist_separation == other.artist_separation and
                    self.title_separation == other.title_separation and
                    self.album_separation == other.album_separation and
                    self.advanced == other.advanced)
        else:
            return False