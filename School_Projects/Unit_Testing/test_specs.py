# test_specs.py
"""Python Essentials: Unit Testing.
Adam Kotter
Math 321 - 1
8/31/18
"""

import specs
import pytest


def test_add():
    assert specs.add(1, 3) == 4, "failed on positive integers"
    assert specs.add(-5, -7) == -12, "failed on negative integers"
    assert specs.add(-6, 14) == 8

def test_divide():
    assert specs.divide(4,2) == 2, "integer division"
    assert specs.divide(5,4) == 1.25, "float division"
    with pytest.raises(ZeroDivisionError) as excinfo:
        specs.divide(4, 0)
    assert excinfo.value.args[0] == "second input cannot be zero"


# Problem 1: write a unit test for specs.smallest_factor(), then correct it.
def test_smallest_factor():
    assert specs.smallest_factor(1) == 1, "failed on n=1"
    assert specs.smallest_factor(2) == 2, "failed on n=2"
    assert specs.smallest_factor(3) == 3, "failed on n=3"
    assert specs.smallest_factor(4) == 2, "failed on n=4"
    assert specs.smallest_factor(11) == 11, "failed on n=11"
    assert specs.smallest_factor(12) == 2, "failed on n=12"
    assert specs.smallest_factor(15) == 3, "failed on n=15"

# Problem 2: write a unit test for specs.month_length().
def test_month_length():
    assert specs.month_length("September") == 30, "failed on 30-day month"
    assert specs.month_length("August") == 31, "failed on 31-day month"
    assert specs.month_length("February") == 28, "failed on non-leap year Feb"
    assert specs.month_length("February", leap_year = True) == 29, "failed on leap year Feb"
    assert specs.month_length("Yeet") == None, "failed on non-month string"
    assert specs.month_length(1) == None, "failed on non-string input"

# Problem 3: write a unit test for specs.operate().
def test_operate():
    with pytest.raises(TypeError) as type_error_test:
        specs.operate(1,2,3)
    assert type_error_test.value.args[0] == "oper must be a string"
    assert specs.operate(1,2,"+") == 3, "failed on positive addition"
    assert specs.operate(1,-2,"+") == -1, "failed on positive/negative addition"
    assert specs.operate(-1,-2,"+") == -3, "failed on negative addition"
    assert specs.operate(2,1,"-") == 1, "failed on positive result positive subtraction"
    assert specs.operate(1,2,"-") == -1, "failed on negative result positive subtraction"
    assert specs.operate(1,-2,"-") == 3, "failed on positive/negative subtraction"
    assert specs.operate(-1,-2,"-") == 1, "failed on negative subtraction"
    assert specs.operate(1,2,"*") == 2, "failed on positive multiplication"
    assert specs.operate(1,-2,"*") == -2, "failed on positive/negative multiplication"
    assert specs.operate(-1,-2,"*") == 2, "failed on negative multiplication"
    assert specs.operate(1,0,"*") == 0, "failed on zero multiplication"
    assert specs.operate(1,2,"/") == 0.5, "failed on positive division"
    assert specs.operate(1,-2,"/") == -0.5, "failed on positive/negative division"
    assert specs.operate(-1,-2,"/") == 0.5, "failed on negative division"
    assert specs.operate(0,1,"/") == 0, "failed on zero division"
    with pytest.raises(ZeroDivisionError) as zero_error:
        specs.operate(1,0,"/")
    assert zero_error.value.args[0] == "division by zero is undefined"
    with pytest.raises(ValueError) as value_error:
        specs.operate(1,2,"3")
    assert value_error.value.args[0] == "oper must be one of '+', '/', '-', or '*'"
    assert type_error_test.value.args[0] == "oper must be a string"

# Problem 4: write unit tests for specs.Fraction, then correct it.
@pytest.fixture
def set_up_fractions():
    frac_1_3 = specs.Fraction(1, 3)
    frac_1_2 = specs.Fraction(1, 2)
    frac_n2_3 = specs.Fraction(-2, 3)
    return frac_1_3, frac_1_2, frac_n2_3

def test_fraction_init(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_3.numer == 1
    assert frac_1_2.denom == 2
    assert frac_n2_3.numer == -2
    frac = specs.Fraction(30, 42)
    assert frac.numer == 5
    assert frac.denom == 7
    with pytest.raises(ZeroDivisionError) as zero_error:
        frac_0 = specs.Fraction(1,0)
    assert zero_error.value.args[0] == "denominator cannot be zero"
    with pytest.raises(TypeError) as numer_type1:
        frac_1 = specs.Fraction(1.0,2)
    assert numer_type1.value.args[0] == "numerator and denominator must be integers"
    with pytest.raises(TypeError) as numer_type2:
        frac_2 = specs.Fraction(1,2.0)
    assert numer_type2.value.args[0] == "numerator and denominator must be integers"

def test_fraction_str(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert str(frac_1_3) == "1/3"
    assert str(frac_1_2) == "1/2"
    assert str(frac_n2_3) == "-2/3"
    frac = specs.Fraction(1,1)
    assert str(frac) == "1", "failed on str with denominator = 1"

def test_fraction_float(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert float(frac_1_3) == 1 / 3.
    assert float(frac_1_2) == .5
    assert float(frac_n2_3) == -2 / 3.

def test_fraction_eq(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_2 == specs.Fraction(2, 4)
    assert frac_1_3 == specs.Fraction(2, 6)
    assert frac_n2_3 == specs.Fraction(8, -12)
    assert frac_1_2 == 0.5
    frac_2_n3 = specs.Fraction(2,-3)
    assert frac_n2_3 == frac_2_n3, "failed on -2/3 = 2/-3"

def test_add_2(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_3 + frac_1_2 == specs.Fraction(5,6), "failed on positive addition"
    assert frac_1_3 + frac_n2_3 == specs.Fraction(-1,3), "failed on positive/negative addition"
    assert frac_n2_3 + frac_n2_3 == specs.Fraction(-4,3), "failed on negative addition"

def test_sub(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_2 - frac_1_3 == specs.Fraction(1,6), "failed on positive outcome positive subtraction"
    assert frac_1_3 - frac_1_2 == specs.Fraction(-1,6), "failed on negative outcome positive subtraction"
    assert frac_1_3 - frac_n2_3 == specs.Fraction(1,1), "failed on positive/negative subtraction"
    assert frac_n2_3 - frac_n2_3 == specs.Fraction(0,1), "failed on negative subtraction"

def test_mul(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_3 * frac_1_2 == specs.Fraction(1,6), "failed on positive multiplication"
    assert frac_1_3 * frac_n2_3 == specs.Fraction(-2,9), "failed on positive/negative multiplication"
    assert frac_n2_3 * frac_n2_3 == specs.Fraction(4,9), "failed on negative multiplication"

def test_truediv(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    frac0 = specs.Fraction(0,1)
    with pytest.raises(ZeroDivisionError) as zero_error:
        frac_1_3 / frac0
    assert zero_error.value.args[0] == "cannot divide by zero"
    frac_0_1 = specs.Fraction(0,1)
    assert frac_0_1 / frac_1_3 == specs.Fraction(0,1), "failed on zero division"
    frac_2_3 = specs.Fraction(2,3)
    assert frac_1_3 / frac_2_3 == specs.Fraction(1,2), "failed on positive division"
    assert frac_n2_3 / frac_1_3 == specs.Fraction(-2,1), "failed on negative/positive division"
    assert frac_1_3 / frac_n2_3 == specs.Fraction(-1,2), "failed on negative/positive division"
    assert frac_n2_3 / frac_n2_3 == specs.Fraction(1,1), "failed on negative division"

# Problem 5: Write test cases for Set.
def test_is_set():
    assert specs.is_set("1111","2222","0000"), "failed on all different"
    assert specs.is_set("1111","1222","1000"), "failed on sddd"
    assert specs.is_set("1111","2122","0100"), "failed on dsdd"
    assert specs.is_set("1111","1122","1100"), "failed on ssdd"
    assert specs.is_set("1111","2212","0010"), "failed on ddsd"
    assert specs.is_set("1111","1212","1010"), "failed on sdsd"
    assert specs.is_set("1111","2112","0110"), "failed on dssd"
    assert specs.is_set("1111","1112","1110"), "failed on sssd"
    assert specs.is_set("1111","2221","0001"), "failed on ddds"
    assert specs.is_set("1111","1221","1001"), "failed on sdds"
    assert specs.is_set("1111","2121","0101"), "failed on dsds"
    assert specs.is_set("1111","1121","1101"), "failed on ssds"
    assert specs.is_set("1111","2211","0011"), "failed on ddss"
    assert specs.is_set("1111","1211","1011"), "failed on sdss"
    assert specs.is_set("1111","2111","0111"), "failed on dsss"
    assert specs.is_set("1111","1111","1111"), "failed on ssss"
    assert not specs.is_set("1111","1211","1111"), "failed on 1 not set"
    assert not specs.is_set("1111","1221","1111"), "failed on 2 not set"
    assert not specs.is_set("1111","1222","1111"), "failed on 3 not set"
    assert not specs.is_set("1111","2222","1111"), "failed on 4 not set"

def test_count_sets():
    cards_11 = ["1212","1210","1211","1111","1112","1110","0111","2111","2222","0000","1010"]
    cards_13 = ["1212","1210","1211","1111","1112","1110","0111","2111","2222","0000","1010","0011","2211"]
    cards_not_unique = ["1111","1111","1212","0120","0120","1111","1212","1201","0120","2020","1010","1010"]
    cards_3_dig = ["111","222","000","1202","1201","1021","0111","0122","0121","2102","2012","2000"]
    cards_5_dig = ["11111","2222","00000","1202","1201","1021","0111","0122","0121","2102","2012","2000"]
    cards_not_base_3 = ["1111","2232","0000","1202","1201","1021","0111","0122","0121","2102","2012","2000"]
    cards_not_int = ["1111","22a2","0000","1202","1201","1021","0111","0122","0121","2102","2012","2000"]
    no_sets = ["1101","1212","2110","1100","1210","2111","1121","1012","0110","1120","1010","0111"]
    one_set	 = ["1101","1212","2110","1100","1210","2111","1121","1012","0110","1102","1010","0111"]
    three_sets = ["1101","1212","2110","1100","1210","2111","1110","1012","0110","1102","1010","0111"]
    six_sets = ["1022","1122","0100","2021","0010","2201","2111","0020","1102","0210","2110","1020"]
    with pytest.raises(ValueError) as ve1:
        specs.count_sets(cards_11)
    assert ve1.value.args[0] == "exactly 12 cards required"
    with pytest.raises(ValueError) as ve2:
        specs.count_sets(cards_13)
    assert ve2.value.args[0] == "exactly 12 cards required"
    with pytest.raises(ValueError) as ve3:
        specs.count_sets(cards_not_unique)
    assert ve3.value.args[0] == "cards not unique"
    with pytest.raises(ValueError) as ve4:
        specs.count_sets(cards_3_dig)
    assert ve4.value.args[0] == "cards must have exactly 4 digits"
    with pytest.raises(ValueError) as ve5:
        specs.count_sets(cards_5_dig)
    assert ve5.value.args[0] == "cards must have exactly 4 digits"
    with pytest.raises(ValueError) as ve6:
        specs.count_sets(cards_not_base_3)
    assert ve6.value.args[0] == "cards must be integers in base 3"
    with pytest.raises(ValueError) as ve7:
        specs.count_sets(cards_not_int)
    assert ve7.value.args[0] == "cards must be integers in base 3"
    assert specs.count_sets(no_sets) == 0, "failed at no sets"
    assert specs.count_sets(one_set) == 1, "failed at 1 set"
    assert specs.count_sets(three_sets) == 3, "failed at three sets"
    assert specs.count_sets(six_sets) == 6, "failed at six sets"