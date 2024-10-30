from typing import List, Optional, Dict

from kenar.widgets.widget_type import WidgetTypesUnion


class CreatePostAddonRequest:
    token: str

    widgets: List[WidgetTypesUnion]
    notes: str

    semantic: Optional[Dict[str, str]] = dict
    semantic_sensitives: Optional[List[str]] = list

    def __init__(self, token: str, widgets: List[WidgetTypesUnion], notes: str = ""):
        self.token = token
        self.widgets = widgets
        self.notes = notes
        self.semantic = {}
        self.semantic_sensitives = []

    def add_semantic(self, key: str, value: str, sensitive: bool = False):
        if key in self.semantic:
            raise ValueError(f"Key {key} already exists in semantic.")

        self.semantic[key] = value
        if sensitive:
            self.semantic_sensitives.append(key)

    def to_dict(self):
        return {
            "token": self.token,
            "notes": self.notes,
            "widgets": {
                "widget_list": [w.serialize_model() for w in self.widgets],
            },
            "semantic": self.semantic,
            "semantic_sensitives": self.semantic_sensitives,
        }


class App:
    slug: str
    display: str
    avatar: str
    status: str
    service_type: str

    def __init__(self, slug: str, display: str = "", avatar: str = "", status: str = "", service_type: str = "", **_):
        self.slug = slug
        self.display = display
        self.avatar = avatar
        self.status = status
        self.service_type = service_type


class AddonMetaData:
    id: str
    app: App

    created_at: str
    last_modified: str

    def __init__(self, id: str, app: Dict, created_at: str, last_modified: str, **_):
        self.id = id
        self.app = App(**app)
        self.created_at = created_at
        self.last_modified = last_modified


class PostAddon:
    meta_data: AddonMetaData
    token: str
    widgets: List[WidgetTypesUnion]
    semantic: Dict[str, str]

    def __init__(
            self,
            meta_data: Dict,
            token: str,
            widgets: List[WidgetTypesUnion],
            semantic: Dict[str, str],
            **_,
    ):
        self.meta_data = AddonMetaData(**meta_data)
        self.token = token
        self.widgets = widgets
        self.semantic = semantic


class CreateUserAddonRequest:
    widgets: List[WidgetTypesUnion]

    semantic: Dict[str, str]
    semantic_sensitives: List[str]
    notes: str
    phone: str
    management_permalink: str
    removal_permalink: str
    categories: List[str]
    ticket_uuid: Optional[str]
    verification_cost: Optional[int]

    def __init__(
            self,
            phone: str,
            widgets: List[WidgetTypesUnion],
            notes: str = "",
            categories: List[str] = None,
            ticket_uuid: Optional[str] = "",
            verification_cost: Optional[int] = 0,
    ):
        self.phone = phone
        self.widgets = widgets
        self.notes = notes
        self.categories = categories or []
        self.semantic = {}
        self.semantic_sensitives = []
        self.ticket_uuid = ticket_uuid
        self.verification_cost = verification_cost

    def add_semantic(self, key: str, value: str, sensitive: bool = False):
        if key in self.semantic:
            raise ValueError(f"Key {key} already exists in semantic.")

        self.semantic[key] = value
        if sensitive:
            self.semantic_sensitives.append(key)

    def to_dict(self):
        return {
            "widget_list": [w.serialize_model() for w in self.widgets],
            "semantic": self.semantic,
            "semantic_sensitives": self.semantic_sensitives,
            "notes": self.notes,
            "phone": self.phone,
            "management_permalink": self.management_permalink,
            "removal_permalink": self.removal_permalink,
            "categories": self.categories,
            "ticket_uuid": self.ticket_uuid,
            "verification_cost": self.verification_cost,
        }


class UserAddon:
    meta_data: AddonMetaData
    phone: str
    widgets: List[WidgetTypesUnion] = None

    semantic: Dict[str, str] = {}

    def __init__(self, meta_data: Dict, phone: str, widgets: List[WidgetTypesUnion], semantic: Dict[str, str], **_):
        self.meta_data = AddonMetaData(**meta_data)
        self.phone = phone
        self.widgets = widgets
        self.semantic = semantic
