from .repository import Repository


class FluxoHuskyRepository(Repository):

    def __init__(self, db):
        super(FluxoHuskyRepository, self).__init__(db, collection_name='fluxo_husky')