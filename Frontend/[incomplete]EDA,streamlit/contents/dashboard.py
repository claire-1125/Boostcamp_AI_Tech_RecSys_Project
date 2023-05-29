import os
import streamlit as st
from hydralit import HydraHeadApp


class DashboardTab(HydraHeadApp):
    def __init__(self, title = 'keyword', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        # head
        st.experimental_set_query_params(contents=self.title)

        # body
        
