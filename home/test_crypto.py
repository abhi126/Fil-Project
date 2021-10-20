import pytest

from .model_prediction import cryptoprediction

def test_modelPrediction():
    assert len(cryptoprediction("Ethereum"))>0

def test_modelPrediction1():
    assert cryptoprediction("Ether")!="CryptoCurrency Not present in List"
