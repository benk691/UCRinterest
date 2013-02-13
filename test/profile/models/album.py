class album(Document):
    creator = StringField(min_length = 3, max_length = 25, required = true)
    title = StringField(min_length = 3, max_length = 25, required = true)
    dscrp = StringField(min_length = 3, max_length = 400)
    pins = ListField()
    
