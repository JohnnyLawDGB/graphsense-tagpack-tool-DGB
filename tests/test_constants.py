from tagpack.constants import (
    suggest_networks_from_currency,
    is_known_currency,
    is_known_network,
)


def test_chain_suggestiong():
    assert len(suggest_networks_from_currency("USDT")) > 0

    assert len(suggest_networks_from_currency("ETH")) == 0

    assert len(suggest_networks_from_currency("ETH", only_unknown=False)) == 1


def test_dgb_known():
    assert is_known_currency("DGB")
    assert is_known_network("DGB")
