from Contents.base_content import BaseContent
from db.Models.sync_models.sync_initial_model import SyncInitialModel, SyncModel


class SyncContent(BaseContent):
    data: SyncModel


class SyncInitialContent(BaseContent):
    data: SyncInitialModel
