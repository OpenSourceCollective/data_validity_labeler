import random
from datetime import datetime

import pandas as pd
import streamlit as st

import src.backend.database as db
from src.backend.schema import Record

# TODO: Create validation blocks that can be dynamically created from the app config
