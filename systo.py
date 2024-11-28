import json
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import TypeVar


class Category(Enum):
    shared = 'shared'
    beer = 'beer'
    martini = 'martini'
    strong = 'strong'


@dataclass(kw_only=True)
class ModelBase:
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass(kw_only=True)
class Participant(ModelBase):
    name: str
    alcohol: bool
    beer: bool
    martini: bool
    strong: bool

    def __hash__(self):
        return hash(self.name)


@dataclass
class Item(ModelBase):
    price: float
    name: str
    is_alcohol: bool
    category: Category


@dataclass
class ItemEntry(ModelBase):
    item: Item
    quantity: float

    @property
    def sum(self) -> float:
        return self.item.price * self.quantity


ItemsList = TypeVar(name='ItemsList', bound=list[ItemEntry])
ParticipantsList = TypeVar(name='ParticipantsList', bound=list[Participant])


@dataclass
class Receipt(ModelBase):
    items: ItemsList

    @property
    def sum(self) -> float:
        return sum(x.sum for x in self.items)


@dataclass(kw_only=True)
class ParticipantStatistics:
    by_category: dict[Category, float]


@dataclass(kw_only=True)
class AnalysisInfo:
    info: dict[Participant, ParticipantStatistics]
    categories: dict[Category,]

    @property
    def participants(self) -> ParticipantsList:
        return list(self.info.keys())


@dataclass
class Accounter:
    output_path: str
    participants: ParticipantsList

    items: ItemsList = None

    def read_receipt(self, receipt_path: str):
        with open(receipt_path, 'rt') as input_file:
            data: list[dict] = json.loads(input_file.read())

        receipt = self._parse_receipt_from_json(data)
        self.items.append(receipt.items)

    def _parse_receipt_from_json(self, data: list[dict]) -> Receipt:
        # TODO: parse json to object
        ...

    def read_participants(self, participants_path: str):
        with open(participants_path, 'rt') as input_file:
            data: list[dict] = json.loads(input_file.read())

        participants = self._parse_participants_from_json(data)
        self.participants = participants

    def _parse_participants_from_json(self, data: list[dict]) -> Receipt:
        # TODO: parse json to object
        ...

    def count_distribution(self) -> AnalysisInfo:
        info = {}

        distribution: dict[Category, dict[Participant, float]] = {key: {} for key in list(Category)}

        alcohols = [p for p in self.participants if p.alcohol]
        beers = [p for p in self.participants if p.beer]
        martini = [p for p in self.participants if p.martini]
        strong = [p for p in self.participants if p.strong]

        for item in self.items:  # type: ItemEntry
            match item.item.category:
                case Category.shared:
                    per_person = item.sum / len(alcohols)
                case Category.beer:
                    per_person = item.sum / len(beers)
                case Category.martini:
                    per_person = item.sum / len(martini)
                case Category.strong:
                    per_person = item.sum / len(strong)
                case _:
                    per_person = 0
            for participant in alcohols:
                if participant not in distribution[item.item.category]:
                    distribution[item.item.category][participant] = 0
                distribution[item.item.category][participant] += per_person

        info = ...  # TODO: make info from distribution

        return AnalysisInfo(
            info=info,
        )


def main():
    acc = Accounter(
        output_path='result.csv'
    )
