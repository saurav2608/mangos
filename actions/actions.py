# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import rasa_sdk.events as ev
import pandas as pd


class ActionGetTypes(Action):

    def name(self) -> Text:
        return "action_get_types"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        stock = pd.read_csv('actions/mangos.tsv', delimiter=',')
        available_varieties = stock['variety'].to_list()
        return [ev.SlotSet("mango_variety", ", ".join(available_varieties))]


class ActionGetPrice(Action):

    def name(self) -> Text:
        return "action_get_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        rupee_symbol = u"\u20B9"
        mango_type = tracker.get_slot('mango_type')
        stock = pd.read_csv('actions/mangos.tsv', delimiter=',')
        price = stock[stock['variety'] == mango_type]['price'].values[0]

        return [ev.SlotSet('mango_price', f'{rupee_symbol}{price}')]
