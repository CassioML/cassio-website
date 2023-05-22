import os
from datetime import timedelta

import pandas as pd

from feast import (
    Entity,
    FeatureService,
    FeatureView,
    Field,
    FileSource,
    PushSource,
    RequestSource,
)
from feast.types import Float32, Float64, Int64

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

user = Entity(name="user", join_keys=["user_name"])

userDataSource = FileSource(
    name="user_data_source",
    path=os.path.join(CURRENT_DIR, "data/user_data.parquet"),
    timestamp_field="event_timestamp",
    # created_timestamp_column="created",
)

activeCartSource = FileSource(
    name="active_cart_source",
    path=os.path.join(CURRENT_DIR, "data/active_cart.parquet"),
    timestamp_field="event_timestamp",
    # created_timestamp_column="created",
)

userDataView = FeatureView(
    name='user_data',
    entities=[user],
    schema=[
        Field(name='age', dtype=Int64),
        Field(name='purchases', dtype=Int64),
        Field(name='visit_frequency', dtype=Float32),
    ],
    online=True,
    source=userDataSource,
)

activeCartView = FeatureView(
    name='active_cart',
    entities=[user],
    schema=[
        Field(name='active_cart', dtype=Int64),
    ],
    online=True,
    source=activeCartSource,
)

userFullView = FeatureService(
    name='user_full_view',
    features=[
        userDataView,
        activeCartView,
    ],
)
