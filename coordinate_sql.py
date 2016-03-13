from peewee import Model, SqliteDatabase, FloatField, IntegerField, BooleanField, ForeignKeyField, CharField

#PERSISTENT_DB   = 'traffic_data.db'
TESTING_DB = ':memory:'

database = SqliteDatabase(TESTING_DB)

class BaseModel(Model):
    class Meta:
        database = database

class CoordinatesSql(BaseModel):
    name = CharField()
    latitude_delta = FloatField(null=True)
    longitude_delta = FloatField(null=True)

    def __str__(self):
        return self.name

class CoordinateSql(BaseModel):
    latitude = FloatField()
    longitude = FloatField()
    minutes = IntegerField(null=True)
    exception = BooleanField(default=False)
    area_name = ForeignKeyField(CoordinatesSql, related_name='coordinates')

    def __str__(self):
        return str(self.latitude) + ', ' + str(self.longitude)

database.connect()
database.create_tables([CoordinatesSql, CoordinateSql])

def save_data():
    coords = CoordinatesSql(name='Test area')
    coords.save()
    coord = CoordinateSql(latitude=123.123, longitude=321.321, area_name=coords)
    coord.save()
    coord = CoordinateSql(latitude=666.666, longitude=666.666, area_name=coords)
    coord.save()

def read_data():
    print 'len', len(CoordinateSql.select())
    for coord in CoordinateSql.select():
        print 'coord:', coord

    for coords in CoordinatesSql.select():
        print 'coords:', coords

    coordinates = CoordinatesSql.get(CoordinatesSql.name == 'Test area').get()
    for coord in coordinates.coordinates:
        print 'COORD', coord.exception, coord.minutes

save_data()
read_data()