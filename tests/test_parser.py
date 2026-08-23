from albumatic.parser import parse_legacy_path_and_query, serialize_to_url, parse_batch_notation, serialize_batch_notation
from albumatic.models import PageConfig, Unit


def test_parse_legacy_url():
    path = "/pdf/USA/Definitives/2009/1/ABBA-hh-BBB"
    query = {
        "unit": "mm",
        "t_1_1": "blue",
        "l_1_1": "10c",
        "size_X": "120,60",
    }
    config = parse_legacy_path_and_query(path, query)

    assert config.country == "USA"
    assert config.area == "Definitives"
    assert config.year == "2009"
    assert config.no == "1"
    assert config.template == "ABBA-hh-BBB"
    assert config.texts["1_1"] == "blue"
    assert config.labels["1_1"] == "10c"
    assert config.custom_sizes["X"] == (120.0, 60.0)


def test_serialize_to_url():
    path = "/pdf/Nepal/Knives/1881/1/XXX"
    query = {"t_1_1": "red"}
    config = parse_legacy_path_and_query(path, query)
    serialized = serialize_to_url(config)

    assert "/pdf/Nepal/Knives/1881/1/XXX" in serialized
    assert "t_1_1=red" in serialized


def test_parse_batch_notation_multiline():
    batch_text = """
    AA-BB-CC
    cc-ddd-a
    XXXX-XXXX-XX
    """
    pages = parse_batch_notation(batch_text)
    assert len(pages) == 3
    assert pages[0].template == "AA-BB-CC"
    assert pages[0].no == "1"
    assert pages[1].template == "cc-ddd-a"
    assert pages[1].no == "2"
    assert pages[2].template == "XXXX-XXXX-XX"
    assert pages[2].no == "3"


def test_parse_batch_notation_slash_separated():
    slash_text = "AA-BB/cc-ddd-a/XXXX"
    pages = parse_batch_notation(slash_text)
    assert len(pages) == 3
    assert pages[0].template == "AA-BB"
    assert pages[1].template == "cc-ddd-a"
    assert pages[2].template == "XXXX"


def test_parse_batch_notation_enriched():
    enriched_text = """
    1881 | 1 | European Paper | XXX-X-XXX-X | t:1_1=blue,1_2=red | l:1_1=1A,1_2=2A
    1881 | 2 | Good Paper     | XXX-XXX     | t:1_1=green
    1907 | 1 | Shiva          | dd-dd
    """
    pages = parse_batch_notation(enriched_text)
    assert len(pages) == 3
    assert pages[0].year == "1881"
    assert pages[0].no == "1"
    assert pages[0].area == "European Paper"
    assert pages[0].template == "XXX-X-XXX-X"
    assert pages[0].texts["1_1"] == "blue"
    assert pages[0].texts["1_2"] == "red"
    assert pages[0].labels["1_1"] == "1A"

    # Test serialization
    serialized = serialize_batch_notation(pages)
    assert "European Paper" in serialized
    assert "t:1_1=blue" in serialized
