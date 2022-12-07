"""Taxonomy - A proxy for a remote taxonomy definition"""

import csv
import json
from io import StringIO

import requests


class Concept(object):
    """Concept Definition.

    This class serves as a proxy for a concept that is defined
    in some remote taxonomy. It just provides the most essential properties.

    A concept can be viewed as an idea or notion; a unit of thought.
    See: https://www.w3.org/TR/skos-reference/#concepts

    """

    def __init__(self, taxonomy, id, uri, label, level, description):
        self.taxonomy = taxonomy
        self.id = id
        self.uri = uri
        self.label = label
        self.level = level
        self.description = description

    def to_json(self):
        return json.dumps(
            {
                "taxonomy": self.taxonomy.key,
                "id": self.id,
                "uri": self.uri,
                "label": self.label,
                "level": self.level,
                "description": self.description,
            }
        )

    def __str__(self):
        s = [
            str(self.taxonomy.key),
            str(self.id),
            str(self.uri),
            str(self.label),
            str(self.level),
            str(self.description),
        ]
        return "[" + " | ".join(s) + "]"


class Taxonomy(object):
    """TagPack Taxonomy Proxy.

    This class serves as a proxy for remote taxonomies defined at
    https://interpol-innovation-centre.github.io/DW-CC-Taxonomy/.

    It can be used for loading and parsing a taxonomy from remote
    and for ingesting a taxonomy into a local Cassandra data store.
    """

    def __init__(self, key, uri):
        self.key = key
        self.uri = uri
        self.concepts = []

    def load_from_remote(self):
        response = requests.get(self.uri)
        f = StringIO(response.text)
        csv_reader = csv.DictReader(f, delimiter=",")
        for row in csv_reader:
            level = row["level"] if "level" in row else None
            concept = Concept(
                self, row["id"], row["uri"], row["label"], level, row["description"]
            )
            self.concepts.append(concept)

    def load_from_local(self):
        with open(self.uri, "r") as f:
            csv_reader = csv.DictReader(f, delimiter=",")
            uri = self.uri
            for row in csv_reader:
                ident = row["id"]
                label = row["label"] if "label" in row else None
                level = row["level"] if "level" in row else None
                desc = row["description"] if "description" in row else ""

                concept = Concept(self, ident, uri, label, level, desc)
                self.concepts.append(concept)

    @property
    def concept_ids(self):
        return [concept.id for concept in self.concepts]

    def add_concept(self, concept_id, label, level, description):
        concept_uri = self.uri + "/" + concept_id
        concept = Concept(self, concept_id, concept_uri, label, level, description)
        self.concepts.append(concept)

    def to_json(self):
        return json.dumps({"key": self.key, "uri": self.uri})

    def __str__(self):
        s = [str(self.key), str(self.uri)]
        return "[" + " | ".join(s) + "]"
